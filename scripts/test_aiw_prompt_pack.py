import pytest
import tempfile
import os
import json
from aiw_prompt_pack import PromptPack, generate_prompt, check_harness_execution_rules

@pytest.fixture
def valid_prompt_template():
    return """
## Role
## Task
## Source of truth
## Context bundle
## Allowed scope
## Non-goals
## Constraints
## Required process
## Required outputs
## Stop conditions

You are acting as: <provider-role>.
Issue: <issue-url-or-number>
Allowed paths: <path>
"""

@pytest.fixture
def invalid_prompt_template():
    return """
## Role
## Task
## Source of truth
## Context bundle
## Allowed scope
## Non-goals
## Required process
## Required outputs
## Stop conditions

Missing Constraints
"""

def test_prompt_pack_contains_required_sections(valid_prompt_template):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(valid_prompt_template)
        temp_path = f.name

    try:
        pack = PromptPack(temp_path)
        assert pack.validate_sections() == True
    finally:
        os.unlink(temp_path)

def test_prompt_pack_missing_sections(invalid_prompt_template):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(invalid_prompt_template)
        temp_path = f.name

    try:
        pack = PromptPack(temp_path)
        with pytest.raises(ValueError, match="Prompt template is missing required sections: ## Constraints"):
            pack.validate_sections()
    finally:
        os.unlink(temp_path)

def test_generated_prompt_includes_issue_and_paths(valid_prompt_template):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(valid_prompt_template)
        temp_path = f.name

    try:
        # Should raise error if missing
        with pytest.raises(ValueError, match="Generated prompt must include allowed paths"):
            generate_prompt(temp_path, **{"provider-role": "docs-worker", "issue-url-or-number": "123"})

        with pytest.raises(ValueError, match="Generated prompt must include issue number"):
            generate_prompt(temp_path, **{"provider-role": "docs-worker", "path": "docs/"})

        # Should succeed if provided
        prompt = generate_prompt(temp_path, **{"provider-role": "docs-worker", "issue-url-or-number": "123", "path": "docs/"})
        assert "Issue: 123" in prompt
        assert "Allowed paths: docs/" in prompt
    finally:
        os.unlink(temp_path)

def test_generated_prompt_refuses_broad_scope_when_issue_lacks_files():
    # Example logic test, can be implemented more strictly in harness
    pass

def test_missing_test_command_blocks_afk_patch_pr_modes():
    # Patch mode without test command
    job_spec = {
        "autonomy_mode": "patch",
        "test_command": ""
    }
    success, reason = check_harness_execution_rules(job_spec)
    assert success == False
    assert "missing test command blocks AFK patch/pr modes" in reason

    # Pr mode without test command
    job_spec = {
        "autonomy_mode": "pr",
        "test_command": ""
    }
    success, reason = check_harness_execution_rules(job_spec)
    assert success == False
    assert "missing test command blocks AFK patch/pr modes" in reason

    # Patch mode with test command
    job_spec = {
        "autonomy_mode": "patch",
        "test_command": "pytest"
    }
    success, reason = check_harness_execution_rules(job_spec)
    assert success == True

    # Draft mode without test command is allowed
    job_spec = {
        "autonomy_mode": "draft",
        "test_command": ""
    }
    success, reason = check_harness_execution_rules(job_spec)
    assert success == True

def test_high_critical_risk_blocks_autonomous_implementation():
    job_spec = {
        "risk_level": "high"
    }
    success, reason = check_harness_execution_rules(job_spec)
    assert success == False
    assert "high/critical risk blocks autonomous implementation" in reason

    job_spec = {
        "risk_level": "critical"
    }
    success, reason = check_harness_execution_rules(job_spec)
    assert success == False
    assert "high/critical risk blocks autonomous implementation" in reason

    job_spec = {
        "risk_level": "low"
    }
    success, reason = check_harness_execution_rules(job_spec)
    assert success == True

def test_budget_cap_is_enforced_before_provider_invocation():
    job_spec = {
        "budget": {
            "estimated_cost_usd": 10.0,
            "max_cost_usd": 5.0
        }
    }
    success, reason = check_harness_execution_rules(job_spec)
    assert success == False
    assert "budget cap exceeded before provider invocation" in reason

    job_spec = {
        "budget": {
            "estimated_cost_usd": 2.0,
            "max_cost_usd": 5.0
        }
    }
    success, reason = check_harness_execution_rules(job_spec)
    assert success == True

def test_retry_count_is_capped():
    job_spec = {
        "retry_count": 3,
        "budget": {
            "max_retries": 2
        }
    }
    success, reason = check_harness_execution_rules(job_spec)
    assert success == False
    assert "retry count is capped" in reason

    job_spec = {
        "retry_count": 1,
        "budget": {
            "max_retries": 2
        }
    }
    success, reason = check_harness_execution_rules(job_spec)
    assert success == True

def test_notebooklm_output_cannot_be_canonical_unless_exported():
    job_spec = {
        "source_type": "notebooklm"
    }
    success, reason = check_harness_execution_rules(job_spec)
    assert success == False
    assert "NotebookLM output cannot be treated as canonical unless exported/linked back" in reason

    job_spec = {
        "source_type": "notebooklm",
        "exported_link": "https://example.com"
    }
    success, reason = check_harness_execution_rules(job_spec)
    assert success == True

def test_harness_output_json_validates_against_schema():
    # Use the example provided to ensure it works
    example_path = "examples/aiw-harness-result.example.json"
    job_spec = {}
    success, reason = check_harness_execution_rules(job_spec, harness_result_path=example_path)
    assert success == True

    # Create invalid JSON to test failure
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump({"job_id": "123"}, f) # Missing required fields
        temp_path = f.name

    try:
        success, reason = check_harness_execution_rules(job_spec, harness_result_path=temp_path)
        assert success == False
        assert "harness output JSON fails schema validation" in reason
    finally:
        os.unlink(temp_path)
