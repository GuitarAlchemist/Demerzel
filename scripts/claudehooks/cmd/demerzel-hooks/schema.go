package main

import (
	"encoding/json"
	"fmt"
	"math"
	"os"
	"path/filepath"
	"sort"
	"unicode/utf8"
)

// The rules a written digest must follow come from its schema file, not from this code
// (ADR-0003: the schema is the single source of structural validation), as DigestState's
// Test-SchemaObject read them through Test-Json.
var schemaFiles = map[string]string{
	"digest":    "docs/contracts/digest-schema.json",
	"rationale": "docs/contracts/pr-rationale-schema.json",
}

// validateFields checks a frontmatter field list against kind's schema under root; nil when it
// conforms.
func validateFields(root, kind string, fields []kv) error {
	path := filepath.Join(root, filepath.FromSlash(schemaFiles[kind]))
	raw, err := os.ReadFile(path)
	if err != nil {
		return fmt.Errorf("schema not found: %s", path)
	}
	var schema map[string]any
	if err := json.Unmarshal(raw, &schema); err != nil {
		return fmt.Errorf("schema %s is not a JSON object: %v", path, err)
	}
	inst := map[string]any{}
	for _, f := range fields {
		inst[f.key] = f.val
	}
	return checkSchema(schema, inst, "")
}

// checkSchema is the subset of JSON Schema 2020-12 the two digest schemas use: type, const, enum,
// minLength, minimum, required, properties, additionalProperties: false and items. Other keywords
// (format among them, an annotation by default in 2020-12) are not asserted.
func checkSchema(s map[string]any, v any, at string) error {
	where := at
	if where == "" {
		where = "/"
	}
	if t, ok := s["type"]; ok && !hasType(t, v) {
		return fmt.Errorf("%s: %s is not of type %v", where, describe(v), t)
	}
	if c, ok := s["const"]; ok && !sameJSON(c, v) {
		return fmt.Errorf("%s: %s is not the constant %v", where, describe(v), c)
	}
	if enum, ok := s["enum"].([]any); ok {
		found := false
		for _, x := range enum {
			if sameJSON(x, v) {
				found = true
				break
			}
		}
		if !found {
			return fmt.Errorf("%s: %s is not one of %v", where, describe(v), enum)
		}
	}
	if str, ok := v.(string); ok {
		if n, ok := s["minLength"].(float64); ok && float64(utf8.RuneCountInString(str)) < n {
			return fmt.Errorf("%s: %s is shorter than %v", where, describe(v), n)
		}
	}
	if x, ok := number(v); ok {
		if n, ok := s["minimum"].(float64); ok && x < n {
			return fmt.Errorf("%s: %v is less than %v", where, x, n)
		}
	}
	if obj, ok := v.(map[string]any); ok {
		if req, ok := s["required"].([]any); ok {
			for _, r := range req {
				if name, _ := r.(string); name != "" {
					if _, ok := obj[name]; !ok {
						return fmt.Errorf("%s: required property %q is missing", where, name)
					}
				}
			}
		}
		props, _ := s["properties"].(map[string]any)
		keys := make([]string, 0, len(obj))
		for k := range obj {
			keys = append(keys, k)
		}
		sort.Strings(keys)
		for _, k := range keys {
			sub, known := props[k].(map[string]any)
			if !known {
				if ap, ok := s["additionalProperties"].(bool); ok && !ap {
					return fmt.Errorf("%s: property %q is not allowed", where, k)
				}
				continue
			}
			if err := checkSchema(sub, obj[k], at+"/"+k); err != nil {
				return err
			}
		}
	}
	if arr, ok := v.([]any); ok {
		if items, ok := s["items"].(map[string]any); ok {
			for i, x := range arr {
				if err := checkSchema(items, x, fmt.Sprintf("%s/%d", at, i)); err != nil {
					return err
				}
			}
		}
	}
	return nil
}

func hasType(t, v any) bool {
	switch t := t.(type) {
	case string:
		return isType(t, v)
	case []any:
		for _, x := range t {
			if name, _ := x.(string); isType(name, v) {
				return true
			}
		}
	}
	return false
}

func isType(name string, v any) bool {
	switch name {
	case "null":
		return v == nil
	case "string":
		_, ok := v.(string)
		return ok
	case "boolean":
		_, ok := v.(bool)
		return ok
	case "object":
		_, ok := v.(map[string]any)
		return ok
	case "array":
		_, ok := v.([]any)
		return ok
	case "number":
		_, ok := number(v)
		return ok
	case "integer":
		x, ok := number(v)
		return ok && x == math.Trunc(x)
	}
	return false
}

func number(v any) (float64, bool) {
	switch x := v.(type) {
	case int:
		return float64(x), true
	case float64:
		return x, true
	}
	return 0, false
}

// sameJSON compares two JSON values, numbers by value whatever their Go type.
func sameJSON(a, b any) bool {
	if x, ok := number(a); ok {
		y, ok := number(b)
		return ok && x == y
	}
	ja, err1 := json.Marshal(a)
	jb, err2 := json.Marshal(b)
	return err1 == nil && err2 == nil && string(ja) == string(jb)
}

func describe(v any) string {
	if v == nil {
		return "null"
	}
	b, err := json.Marshal(v)
	if err != nil {
		return fmt.Sprint(v)
	}
	return string(b)
}
