---
name: creating-skills
description: Generates high-quality, predictable, and efficient .agent/skills/ directories based on user requirements. Use when the user asks to create a new skill or formalize a workflow.
---

# Antigravity Skill Creator

## When to use this skill
- When the user asks to "create a skill" for a specific task.
- When the user supplies requirements for a new agent capability.
- When the user wants to save a repeatable workflow.

## Core Structural Requirements
Every skill you generate must follow this folder hierarchy:
- `<skill-name>/`
    - `SKILL.md` (Required: Main logic and instructions)
    - `scripts/` (Optional: Helper scripts)
    - `examples/` (Optional: Reference implementations)
    - `resources/` (Optional: Templates or assets)

## YAML Frontmatter Standards
The `SKILL.md` must start with YAML frontmatter following these strict rules:
- **name**: Generund form (e.g., `testing-code`, `managing-databases`). Max 64 chars. Lowercase, numbers, and hyphens only. No "claude" or "anthropic" in the name.
- **description**: Written in **third person**. Must include specific triggers/keywords. Max 1024 chars. (e.g., "Extracts text from PDFs. Use when the user mentions document processing or PDF files.")

## Writing Principles (The "Claude Way")
When writing the body of `SKILL.md`, adhere to these best practices:

* **Conciseness**: Assume the agent is smart. Do not explain what a PDF or a Git repo is. Focus only on the unique logic of the skill.
* **Progressive Disclosure**: Keep `SKILL.md` under 500 lines. If more detail is needed, link to secondary files (e.g., `[See ADVANCED.md](ADVANCED.md)`) only one level deep.
* **Forward Slashes**: Always use `/` for paths, never `\`.
* **Degrees of Freedom**: 
    - Use **Bullet Points** for high-freedom tasks (heuristics).
    - Use **Code Blocks** for medium-freedom (templates).
    - Use **Specific Bash Commands** for low-freedom (fragile operations).

## Workflow & Feedback Loops
For complex tasks, include:
1.  **Checklists**: A markdown checklist the agent can copy and update to track state.
2.  **Validation Loops**: A "Plan-Validate-Execute" pattern. (e.g., Run a script to check a config file BEFORE applying changes).
3.  **Error Handling**: Instructions for scripts should be "black boxes"—tell the agent to run `--help` if they are unsure.

## Instructions
When implementing this skill to generate a new skill for the user:
1.  Identify the **gerund-name** and **description** from the user's request.
2.  Create the directory: `.agent/skills/<skill-name>/`.
3.  Draft the `SKILL.md` content following the formatting rules above.
4.  Use `write_to_file` to create the `SKILL.md` and any supporting files (`scripts/`, `examples/`).
5.  Prioritize **utility** and **specific instructions** over generic advice.
