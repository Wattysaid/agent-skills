---
name: ai-skill-factory
description: A skill for creating new AI skills for Codex, Claude, and Gemini.
version: "R2.00"
author: "Gemini"
---

# AI Skill Factory

## Purpose
- **Use when:** You need to create a new AI skill.
- **Goal:** To generate a new, agent-agnostic AI skill with all the necessary boilerplate and best practices.

## Workflow
1.  **Confirm scope:** Ask the user for the name, description, triggers, and goal of the new skill.
2.  **Gather inputs:** Prompt the user for the steps of the skill.
3.  **Execute steps:** Run the `init_ai_skill.py` script to generate the new skill.
4.  **Provide outputs:** Inform the user that the new skill has been created.
5.  **Verify:** Check that the new skill has been created in the correct directory and that it contains all the necessary files.

## Instructions
1.  Run the `init_ai_skill.py` script with the following command:
    ```bash
    python3 skills/ai-skill-factory/scripts/init_ai_skill.py --name <skill-name> --description "<description>" --triggers "<triggers>" --goal "<goal>" --step1 "<step1>" --step2 "<step2>" --step3 "<step3>"
    ```
2.  The new skill will be created in the `skills` directory.

## Safety & Guardrails
- **File modifications:** The `init_ai_skill.py` script will not overwrite existing files unless the `--force` flag is used.

## Examples
- **Command:** `create a new skill called 'my-new-skill' that does '...'.`
- **Expected output:** A new skill called `my-new-skill` will be created in the `skills` directory.