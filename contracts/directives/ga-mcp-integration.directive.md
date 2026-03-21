# Directive: Connect GA Chatbot to Live MCP Server

**Directive ID:** DIR-2026-03-21-002
**Type:** feature-requirement
**From:** Demerzel (Governor)
**To:** ga
**Priority:** High
**Issued:** 2026-03-21
**Compliance Deadline:** Next sprint cycle

## Context

The GA chatbot currently uses static YAML-based answers. Issue #27 requires replacing these with live calls to the GA MCP server (50+ tools) for dynamically computed responses.

## Requirements

1. **MCP Client Integration**: GA chatbot must connect to the GA MCP server at runtime
2. **Dynamic Computation**: Music theory queries (intervals, chords, scales, progressions) must be computed live, not looked up
3. **Tool Discovery**: Chatbot should discover available MCP tools and route queries to appropriate tools
4. **Fallback**: If MCP server is unavailable, gracefully degrade to static responses
5. **Multilingual**: Per multilingual-policy.yaml, responses should adapt to user's language where possible

## Governance Requirements

- Add `@ai probe` annotations on all MCP client integration code (per ai-probes-policy.yaml)
- Minimum 30% probe coverage on new code
- Log MCP tool invocations for auditability (Article 7)

## Acceptance Criteria

- [ ] Chatbot can query MCP server for chord construction
- [ ] Chatbot can query MCP server for scale/mode information
- [ ] Chatbot can query MCP server for interval calculations
- [ ] Fallback to static responses works when MCP unavailable
- [ ] MCP tool invocations are logged

## Reference

- Issue: GuitarAlchemist/Demerzel#27
- MCP spec: GA repo MCP server documentation
- Probe policy: policies/ai-probes-policy.yaml
