import json
import jsonschema

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

    # Check if context files and allowed paths are provided when trying to do broad scope
    # For now we'll rely on the harness check, but can implement it here too if needed

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
        with open('schemas/aiw-harness-result.schema.json', 'r') as f:
            schema = json.load(f)
        with open(harness_result_path, 'r') as f:
            instance = json.load(f)
        try:
            jsonschema.validate(instance, schema)
        except jsonschema.exceptions.ValidationError as e:
            return False, f"harness output JSON fails schema validation: {e.message}"

    return True, "success"
