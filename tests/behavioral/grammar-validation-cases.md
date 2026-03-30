# Grammar Validation Test Cases

**Purpose:** Detect drift between IXQL grammar spec (EBNF), documentation, and pipeline implementations.
**Frequency:** Run on every grammar or pipeline file change.
**Policy:** grammar-evolution-policy.yaml

## Test Case 1: Section Count Matches

**Given:** The EBNF grammar `grammars/sci-ml-pipelines.ebnf`
**And:** The guide `docs/ixql-guide.md`
**When:** Counting section headers in EBNF (lines matching `(* N.`)
**And:** Counting rows in the guide's Grammar Structure table
**Then:** Both counts must be equal
**Current expected:** 18 sections

## Test Case 2: Section Numbering Sequential

**Given:** The EBNF grammar `grammars/sci-ml-pipelines.ebnf`
**When:** Extracting all section numbers from headers
**Then:** Numbers must be sequential from 1 to N with no gaps or duplicates

## Test Case 3: Section Titles Match

**Given:** The EBNF section headers
**And:** The guide table section names
**When:** Comparing titles (ignoring minor formatting differences)
**Then:** Every EBNF section title must appear in the guide table

## Test Case 4: All Pipeline Tools Defined

**Given:** All `pipelines/*.ixql` files
**When:** Extracting every `ix.io.*` function call
**Then:** Every `ix.io.*` function must have a corresponding production in `grammars/sci-ml-pipelines.ebnf` Section 9

### Known tool functions:
- `ix.io.read` -- defined
- `ix.io.write` -- defined
- `ix.io.glob` -- defined
- `ix.io.move` -- defined (added 2026-03-30)
- `ix.io.append` -- defined (added 2026-03-30)
- `ix.io.gh` -- defined
- `ix.io.walk` -- defined
- `ix.io.count_artifacts` -- defined

## Test Case 5: Binding Scope Consistency

**Given:** All `pipelines/*.ixql` files
**When:** Finding all `<-` binding expressions
**Then:** Each binding must occur in a context that matches the grammar's binding production scope
**Note:** Grammar allows bindings in `mcp_step` (Section 10) and as `conclusion_binding` (Section 13). Pipeline usage outside these contexts should be flagged for grammar extension.

## Test Case 6: Governance Gates Referenced

**Given:** All `pipelines/*.ixql` files
**When:** Extracting governance gate names (bias_assessment, confidence_calibration, etc.)
**Then:** Every gate name must match a production in Section 7 (Governance Integration)

## Test Case 7: Production Count Estimate

**Given:** The EBNF grammar
**When:** Counting `::=` production definitions
**Then:** Count should be within 10% of the documented estimate in `docs/ixql-guide.md`
**Current documented:** ~400+ productions

## Test Case 8: Pipeline Files Parse Without Error

**Given:** All `pipelines/*.ixql` files
**When:** Running `scripts/ixql-validate.js` on each
**Then:** No errors reported (warnings and info acceptable)

## Test Case 9: Example Code in Guide Parses

**Given:** Code blocks in `docs/ixql-guide.md`
**When:** Extracting IXQL code blocks and validating syntax
**Then:** All examples should use valid grammar constructs

## Test Case 10: Grammar-CLAUDE.md Sync

**Given:** `CLAUDE.md` artifact counts
**When:** Comparing grammar-related counts (grammars/, pipelines/, examples/ixql/)
**Then:** Counts in CLAUDE.md must match actual file counts
