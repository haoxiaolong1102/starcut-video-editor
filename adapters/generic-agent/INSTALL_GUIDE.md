# Generic installation guide

For an Agent that supports Markdown instructions but not Agent Skills:

1. Create a custom Agent/workflow named StarCut.
2. Paste `MASTER_PROMPT.md` into its main instruction field.
3. Attach `WORKFLOW.md` and the StarCut reference files that the platform permits.
4. If local command execution is unavailable, use StarCut for planning/SHOTBOOK/QA and perform media operations in a separate editor.
5. Never paste API keys into prompts; configure provider secrets using the platform's secret mechanism.
6. Test with non-sensitive sample media before granting write, network, publishing, or payment permissions.

This path provides the director logic, not a fictitious one-click automation layer.
