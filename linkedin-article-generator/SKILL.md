---
name: linkedin-article-generator
description: |
  Generate leadership‑style LinkedIn articles from a collection of topic and conversation files.  
  Use this skill whenever a user wants to draft a reflective LinkedIn post or long‑form article based on notes, meeting transcripts or other documents.  
  The skill reads all text files within a specified folder, synthesises the key points and produces a polished LinkedIn article using a distinctive tone of voice (observational, pragmatic and operator‑credible) with second‑order thinking and practical takeaways.  
---

# LinkedIn Article Generator

This skill helps an agent draft LinkedIn posts and articles by reading a folder of source documents (e.g. meeting notes, chat logs, research) and composing a thoughtful post in a distinctive tone of voice.  The skill uses **progressive disclosure**: lightweight metadata (the `name` and `description` fields) allow Claude to discover the skill, and detailed instructions appear in this document.  Additional resources such as tone guidance and templates live in the `references/` directory and only load when needed【477748344563007†L372-L383】.

## When to use this skill

Use this skill whenever a user wants to publish a LinkedIn post or article and provides a folder containing topics and conversation transcripts.  Typical requests include:

- Drafting an experience‑led post that extracts lessons from a recent meeting or pattern.
- Writing a thought‑leadership article on an emerging market shift with second‑order consequences.
- Composing a short punchy post that shares a single operational truth with a checklist and question.
- Converting a rant into a constructive article that channels emotion into mechanism and outcomes.

If the user asks for help with general writing that is **not** intended for LinkedIn (e.g. academic papers, sales emails), do not activate this skill.

## How it works

1. **Get the input folder**: Ask the user for the path to the folder containing their topics and conversation transcripts.  Each file should be plain‑text (`.txt` or `.md`) and describe an event, meeting or concept.
2. **Read all files**: Use the provided Python script `scripts/generate_article.py` to read and concatenate the contents of the folder.  The script supports optional arguments such as `--archetype` (e.g. `experience`, `market`, `punch`, `rant`) and `--length` (`short` or `long`) to tailor the output style.
3. **Identify the archetype**: Determine which post archetype best fits the content and the user’s brief:
   - **Experience‑led**: story from the field with operational tips.
   - **Market shift**: analysis of a trend with second‑order effects.
   - **Short punch**: concise statement plus bullets.
   - **Controlled rant**: a venting line followed by constructive outcomes.
4. **Summarise key points**: Extract the narrative hook, surprising insight, and practical takeaways from the documents.  Highlight human factors such as ownership, belonging, judgment and tacit knowledge.
5. **Draft the article**: Follow the tone guidance in [`references/TONE.md`](references/TONE.md) and templates in [`references/TEMPLATES.md`](references/TEMPLATES.md) to assemble the article.  Use short paragraphs (one to three sentences) and vary sentence length.  Include a clear call‑to‑action or question at the end.
6. **Review and refine**: Ensure the post flows logically, respects word‑count guidelines (80–140 words for short posts; 220–450 words for long posts), and avoids over‑claiming numbers.  If the content feels ambiguous or the archetype is unclear, ask the user for clarification before finalising.

## Tone of voice summary

The desired voice is **observational and reflective**—start with something you saw and extract a leadership lesson.  Be a **pragmatic optimist**: call out a problem but point to mechanisms for improvement.  Show **operator credibility** by grounding your insights in real situations (e.g. retirements, café value streams, recruitment shifts), and occasionally employ **calm provocation** through a measured rant.  Use vocabulary such as *ownership*, *belonging*, *visibility*, *value streams*, *tacit knowledge*, *judgment*, *validation*, *context*, *accuracy*, *upskilling*, *mentoring*, *coaching*, *productivity*, *workflows*, *inefficiencies*, *adoption* and *scaling growth*.  For detailed guidance see [`references/TONE.md`](references/TONE.md).

## Post archetypes and structures

Choose the appropriate archetype based on the user’s aim and the complexity of the topic.  High‑level structures are summarised below, with full templates in [`references/TEMPLATES.md`](references/TEMPLATES.md):

- **Experience‑led (medium)** — begin with a scene, note a human or operational surprise, list 3–5 practical takeaways (e.g. “put the work on the wall,” “make ideas frictionless,” “give someone stewardship”), and close with a question.
- **Market shift (long)** — trigger event, common misconceptions, second‑order consequences, leader checklist, soft call‑to‑action.
- **Short punch (short)** — one strong statement, two to three lines of context, up to three bullets, and a question.
- **Controlled rant (short to medium)** — a single rant line followed by mechanisms and outcomes, ending constructively.

Rotate between two short posts, one experience post, and one market insight post every two weeks to maintain variety.  Alternate CTAs such as:

- “If you are tackling this in 2026, what is your biggest constraint right now: ownership, capability, or data?”
- “If useful, I can share the checklist I use in discovery. DM me.”
- “If this resonates, where does it show up most for you: CRM, PMO, service ops, or data governance?”

Avoid rhetorical questions back‑to‑back, over‑claiming statistics, and dichotomies like *tools vs IT*.  Focus on ownership and operating models.

## Using the Python script

The `scripts/generate_article.py` script encapsulates the mechanics of reading files and assembling a draft.  You can run it within your agent environment using Bash or Python.  It accepts the following arguments:

```
python scripts/generate_article.py --folder /path/to/topics --archetype experience --length medium
```

If no archetype is provided, the script infers one based on document length.  The script writes the output to standard output.  See the script’s docstring for details.

## Examples

- **Experience post**: A folder contains transcripts from a team retrospective about implementing a new CRM.  After running the script with `--archetype experience`, you craft a post that opens with a scene from the meeting, shares a surprising insight about tacit knowledge, offers three concrete tips (visual management, frictionless idea capture, stewardship), and ends by asking readers how they handle CRM adoption challenges.
- **Market shift post**: Documents describe recent layoffs in tech and the rise of AI assistants.  Using `--archetype market --length long`, your draft highlights the trend, explains what most people miss about second‑order effects (e.g. knowledge erosion), recommends what leaders should do (assign stewardship, mentor teams, establish metrics), and closes with a soft CTA about discovery checklists.

## Troubleshooting and edge cases

- **Missing folder or empty files**: If the provided path is invalid or contains no readable text, prompt the user to supply a different folder.  Do not attempt to guess file contents.
- **Multiple conflicting topics**: When the folder contains unrelated topics, ask the user which one to prioritise or consider splitting the content into separate posts.
- **Ambiguous desired length**: If the user doesn’t specify a length, infer based on the complexity of the material; ask the user if they prefer a short or long post.
- **Excessive verbosity**: Keep the article concise.  Move detailed analysis to footnotes or follow‑up posts when necessary.

By following these instructions and leveraging the provided references and script, the agent can consistently deliver high‑quality LinkedIn articles that resonate with readers.
