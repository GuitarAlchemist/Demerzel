#!/usr/bin/env node
/**
 * IxQL Validator — minimal proof that .ixql files parse
 * NOT a full parser — just enough to validate structure and extract metadata.
 * ERGOL: runs now, proves the language works.
 */

const fs = require('fs');
const path = require('path');

// --- Tokenizer ---
const TOKEN_PATTERNS = [
  ['COMMENT',     /^--[^\n]*/],
  ['ARROW',       /^[→=]>/],
  ['BIND',        /^<-/],
  ['HANDLE',      /^@[\w-]+/],
  ['ALIAS',       /^#[\w-]+/],
  ['KEYWORD',     /^(?:pipeline|invoke|route|fan_out|when|compound|assert|distill|ambient|type|provided)\b/],
  ['GATE',        /^(?:bias_assessment|confidence_calibration|explanation_requirement|reversibility_check|data_provenance_check)\b/],
  ['CONCLUSION',  /^(?:conclude)\b/],
  ['TRUTH',       /^[TFUC]\b/],
  ['COMPARATOR',  /^(?:>=|<=|>|<|==|!=)/],
  ['NUMBER',      /^-?\d+(?:\.\d+)?/],
  ['STRING',      /^"[^"]*"/],
  ['PAREN_OPEN',  /^\(/],
  ['PAREN_CLOSE', /^\)/],
  ['BRACE_OPEN',  /^\{/],
  ['BRACE_CLOSE', /^\}/],
  ['COMMA',       /^,/],
  ['COLON',       /^:/],
  ['DOT',         /^\./],
  ['GLOB',        /^[\w-]+\*/],
  ['IDENT',       /^[\w][\w-]*/],
  ['NEWLINE',     /^\n/],
  ['WHITESPACE',  /^[ \t\r]+/],
];

function tokenize(source) {
  const tokens = [];
  let pos = 0;
  let line = 1;

  while (pos < source.length) {
    let matched = false;
    for (const [type, pattern] of TOKEN_PATTERNS) {
      const match = source.slice(pos).match(pattern);
      if (match) {
        if (type === 'NEWLINE') line++;
        if (type !== 'WHITESPACE' && type !== 'NEWLINE' && type !== 'COMMENT') {
          tokens.push({ type, value: match[0], line });
        }
        pos += match[0].length;
        matched = true;
        break;
      }
    }
    if (!matched) {
      // Skip unknown character
      pos++;
    }
  }
  return tokens;
}

// --- Validator ---
function validate(tokens, filename) {
  const issues = [];
  const metadata = {
    file: filename,
    handles: [],
    invocations: [],
    gates: [],
    routes: [],
    bindings: [],
    fan_outs: 0,
    conclusions: [],
    has_compound: false,
  };

  for (let i = 0; i < tokens.length; i++) {
    const t = tokens[i];
    const next = tokens[i + 1];

    // Collect handles
    if (t.type === 'HANDLE') {
      metadata.handles.push(t.value);
    }

    // Collect invocations
    if (t.type === 'KEYWORD' && t.value === 'invoke' && next) {
      if (next.type === 'HANDLE') {
        metadata.invocations.push({ target: next.value, line: t.line, level: 'L0' });
      } else if (next.type === 'ALIAS') {
        metadata.invocations.push({ target: next.value, line: t.line, level: 'L1' });
      } else if (next.type === 'GLOB') {
        metadata.invocations.push({ target: next.value, line: t.line, level: 'L2' });
      }
    }

    // Collect routes
    if (t.type === 'KEYWORD' && t.value === 'route' && next && next.type === 'PAREN_OPEN') {
      const intentToken = tokens[i + 2];
      if (intentToken && intentToken.type === 'STRING') {
        metadata.routes.push({ intent: intentToken.value, line: t.line, level: 'L3' });
      }
    }

    // Collect gates
    if (t.type === 'GATE') {
      metadata.gates.push({ gate: t.value, line: t.line });
    }

    // Collect bindings
    if (t.type === 'IDENT' && next && next.type === 'BIND') {
      metadata.bindings.push({ name: t.value, line: t.line });
    }

    // Count fan_outs
    if (t.type === 'KEYWORD' && t.value === 'fan_out') {
      metadata.fan_outs++;
    }

    // Check compound
    if (t.type === 'KEYWORD' && t.value === 'compound') {
      metadata.has_compound = true;
    }

    // Collect conclusions
    if (t.type === 'CONCLUSION') {
      const truthToken = tokens[i + 1];
      if (truthToken && truthToken.type === 'TRUTH') {
        metadata.conclusions.push({ value: truthToken.value, line: t.line });
      }
    }

    // Validation: when clause needs a comparator
    if (t.type === 'KEYWORD' && t.value === 'when') {
      // Look for a truth value or comparison in the next few tokens
      let foundCondition = false;
      for (let j = i + 1; j < Math.min(i + 6, tokens.length); j++) {
        if (tokens[j].type === 'TRUTH' || tokens[j].type === 'COMPARATOR' || tokens[j].type === 'COLON') {
          foundCondition = true;
          break;
        }
        if (tokens[j].type === 'ARROW') break;
      }
      if (!foundCondition) {
        issues.push({ line: t.line, severity: 'warn', message: `'when' clause at line ${t.line} may be missing a condition` });
      }
    }
  }

  // Validation rules
  if (metadata.gates.length === 0) {
    issues.push({ severity: 'info', message: 'No governance gates found — consider adding bias_assessment or confidence_calibration' });
  }

  if (!metadata.has_compound) {
    issues.push({ severity: 'info', message: 'No compound phase — learnings from this pipeline won\'t be harvested' });
  }

  return { metadata, issues };
}

// --- Main ---
function main() {
  const pipelinesDir = path.join(__dirname, '..', 'pipelines');
  const files = fs.readdirSync(pipelinesDir).filter(f => f.endsWith('.ixql'));

  console.log(`\n  IxQL Validator — ${files.length} pipeline files\n`);
  console.log('  ' + '='.repeat(60));

  let totalIssues = 0;
  const allMetadata = [];

  for (const file of files) {
    const source = fs.readFileSync(path.join(pipelinesDir, file), 'utf-8');
    const tokens = tokenize(source);
    const { metadata, issues } = validate(tokens, file);
    allMetadata.push(metadata);

    const icon = issues.filter(i => i.severity === 'error').length > 0 ? '✗' : '✓';
    console.log(`\n  ${icon} ${file}`);
    console.log(`    Tokens: ${tokens.length} | Bindings: ${metadata.bindings.length} | Gates: ${metadata.gates.length} | Fan-outs: ${metadata.fan_outs}`);
    console.log(`    Invocations: ${metadata.invocations.length} | Routes: ${metadata.routes.length} | Compound: ${metadata.has_compound}`);

    if (issues.length > 0) {
      for (const issue of issues) {
        const prefix = issue.severity === 'error' ? '  ✗' : issue.severity === 'warn' ? '  ⚠' : '  ℹ';
        console.log(`    ${prefix} ${issue.message}`);
      }
    }

    totalIssues += issues.length;
  }

  // Summary
  console.log('\n  ' + '='.repeat(60));
  console.log(`\n  Summary: ${files.length} files, ${allMetadata.reduce((s, m) => s + m.gates.length, 0)} governance gates, ${totalIssues} issues`);

  // Pipeline dependency graph
  console.log('\n  Pipeline Graph:');
  for (const m of allMetadata) {
    if (m.invocations.length > 0) {
      const deps = m.invocations.map(i => `${i.target}(${i.level})`).join(', ');
      console.log(`    ${m.file} → ${deps}`);
    }
  }

  console.log('');
}

main();
