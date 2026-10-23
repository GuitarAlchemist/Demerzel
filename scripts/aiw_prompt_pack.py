import json
import sys
from pathlib import Path

import jsonschema

_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "aiw-harness-result.schema.json"

class PromptPack:
    def __init__(self, template_path):
        with open(template_path, 'r') as f:
            self.template = f.read()

    def validate_sections(self):
        required_sections = [
            "## Role",
            "## Task",
            "## Source of truth",
            "## Context bundle",
            "## Allowed scope",
            "## Non-goals",
            "## Constraints",
            "## Required process",
            "## Required outputs",
            "## Stop conditions"
        ]

        missing = []
        for section in required_sections:
            if section not in self.template:
                missing.append(section)

        if missing:
            raise ValueError(f"Prompt template is missing required sections: {', '.join(missing)}")

        return True

def get_past_lessons():
    obs_file = Path(__file__).resolve().parents[1] / "state" / "learning" / "observations.jsonl"
    lessons = []
    if obs_file.is_file():
        try:
            with open(obs_file, "r") as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        if data.get("type") == "failure" or "lesson" in data:
                            lessons.append(data.get("lesson", data.get("message", "")))
        except Exception:
            pass
    return lessons[:5]

def generate_prompt(template_path, **kwargs):
    pack = PromptPack(template_path)
    pack.validate_sections()

    prompt = pack.template
    for key, value in kwargs.items():
        prompt = prompt.replace(f"<{key}>", str(value))

    # Validation logic specific to tests
    if "<issue-url-or-number>" in prompt:
        raise ValueError("Generated prompt must include issue number")

    if "<path>" in prompt:
        raise ValueError("Generated prompt must include allowed paths")

    # Ingest lessons from past failures (Recursive Self-Improvement)
    lessons = get_past_lessons()
    if lessons:
        lessons_block = "\n\n## Ingested Lessons from Past Failures\n"
        for i, lesson in enumerate(lessons, 1):
            lessons_block += f"{i}. {lesson}\n"
        prompt += lessons_block

    return prompt

def check_harness_execution_rules(job_spec, harness_result_path=None):
    """
    Validates rules around execution, risk, budget, retry, etc.
    Returns (True, "success") or (False, "reason for failure")
    """

    # 1. Missing test command blocks AFK patch/pr modes
    if job_spec.get('autonomy_mode') in ['patch', 'pr']:
        if not job_spec.get('test_command'):
            return False, "missing test command blocks AFK patch/pr modes"

    # 2. High/critical risk blocks autonomous implementation
    risk = job_spec.get('risk_level', 'low')
    if risk in ['high', 'critical']:
        return False, "high/critical risk blocks autonomous implementation"

    # 3. Budget cap is enforced before provider invocation
    budget = job_spec.get('budget', {})
    if budget.get('estimated_cost_usd', 0) > budget.get('max_cost_usd', 0):
        return False, "budget cap exceeded before provider invocation"

    # 4. Retry count is capped
    if job_spec.get('retry_count', 0) >= budget.get('max_retries', 0):
        if job_spec.get('retry_count', 0) > 0:
             return False, "retry count is capped"
        elif budget.get('max_retries', 0) == 0 and job_spec.get('retry_count', 0) > 0:
             return False, "retry count is capped"

    # 5. NotebookLM output cannot be treated as canonical unless exported/linked back
    if job_spec.get('source_type') == 'notebooklm' and not job_spec.get('exported_link'):
        return False, "NotebookLM output cannot be treated as canonical unless exported/linked back"

    # 6. Validate JSON schema if path provided
    if harness_result_path:
        baml_validated = False
        try:
            # Attempt to validate using compiled BAML client and Pydantic model
            sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
            from baml_client.types import HarnessResult
            with open(harness_result_path, 'r') as f:
                instance_data = json.load(f)
            
            # Coerce lowercase JSON strings to capitalized BAML class enums
            if "issue" in instance_data:
                instance_data["issue"] = str(instance_data["issue"])
            if "lane" in instance_data and isinstance(instance_data["lane"], str):
                instance_data["lane"] = instance_data["lane"].capitalize()
            if "autonomy_mode" in instance_data and isinstance(instance_data["autonomy_mode"], str):
                mode = instance_data["autonomy_mode"]
                instance_data["autonomy_mode"] = "Pr" if mode.lower() == "pr" else mode.capitalize()
            if "budget" in instance_data and isinstance(instance_data["budget"], dict):
                budget = instance_data["budget"]
                if "tier" in budget and isinstance(budget["tier"], str):
                    budget["tier"] = "".join(p.capitalize() for p in budget["tier"].split("-"))
            if "commands_run" in instance_data and isinstance(instance_data["commands_run"], list):
                for cmd in instance_data["commands_run"]:
                    if isinstance(cmd, dict) and "status" in cmd and isinstance(cmd["status"], str):
                        cmd["status"] = cmd["status"].capitalize()

            # Throws ValidationError if format is incorrect
            HarnessResult.model_validate(instance_data)
            print("[BAML Validation] Harness result successfully validated via Pydantic model.")
            baml_validated = True
        except Exception as exc:
            print(f"[BAML Validation Warning] BAML validation skipped or failed: {exc}")
            print("Running fallback jsonschema validation...")

        if not baml_validated:
            with open(_SCHEMA_PATH, 'r') as f:
                schema = json.load(f)
            with open(harness_result_path, 'r') as f:
                instance = json.load(f)
            try:
                jsonschema.validate(instance, schema)
            except jsonschema.exceptions.ValidationError as e:
                return False, f"harness output JSON fails schema validation: {e.message}"

    return True, "success"
