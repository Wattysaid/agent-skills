#!/usr/bin/env python3
"""
generate_article.py
====================

This script assembles a draft LinkedIn article from a folder of text documents.
It is intended for use within the LinkedIn Article Generator skill.  The script
reads all `.txt` and `.md` files in the specified folder, performs a very
simple sentence‑based summarisation, and arranges the content into one of
several archetypal post formats.  The result is printed to standard output.

Usage examples:

    python generate_article.py --folder /path/to/topics --archetype experience --length medium
    python generate_article.py --folder ./notes --archetype market --length long

Arguments:

--folder    Required. Path to the folder containing source documents.  The script
            will read all files ending in `.txt` or `.md` within this folder.
--archetype Optional. One of `experience`, `market`, `punch`, or `rant`.  If
            omitted, the script infers the archetype based on the total number
            of words (shorter corpora default to `punch`, longer to `experience`).
--length    Optional. Desired post length (`short`, `medium`, or `long`).  This
            flag affects the number of sentences and bullets used.  If not
            specified, the script selects a reasonable length automatically.

Note: This script provides a basic implementation and may produce generic
bullets or placeholders when the source material is sparse.  Agents should
review and adjust the output to ensure it matches the user’s intent and the
tone guidance in the skill references.
"""

import argparse
import os
import re
import sys
from typing import List


def read_files(folder: str) -> str:
    """Concatenate the contents of all .txt and .md files in a folder."""
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"Folder not found: {folder}")
    texts: List[str] = []
    for fname in sorted(os.listdir(folder)):
        lower = fname.lower()
        if lower.endswith(('.txt', '.md')):
            path = os.path.join(folder, fname)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    texts.append(f.read())
            except Exception as e:
                print(f"Warning: Could not read {path}: {e}", file=sys.stderr)
    return "\n".join(texts)


def split_sentences(text: str) -> List[str]:
    """Naively split text into sentences using punctuation heuristics."""
    # Replace newlines with spaces and strip extra whitespace
    cleaned = re.sub(r"\s+", " ", text.strip())
    # Split on sentence enders followed by whitespace
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    # Remove empty strings
    return [s.strip() for s in sentences if s.strip()]


def summarise(sentences: List[str], n: int) -> List[str]:
    """Return the first n sentences from the list, or fewer if not available."""
    return sentences[: max(n, 0)]


def bulletise(sentences: List[str], max_bullets: int = 3) -> List[str]:
    """Create a list of bullet points from sentences.  Capitalise and remove trailing punctuation."""
    bullets: List[str] = []
    for sent in sentences[:max_bullets]:
        cleaned = sent.strip().strip(".!")
        # Capitalise first letter for readability
        bullets.append(cleaned[:1].upper() + cleaned[1:])
    # If not enough sentences, supply generic tips
    while len(bullets) < max_bullets:
        bullets.append(
            [
                "Put the work on the wall",
                "Make ideas frictionless",
                "Give someone stewardship",
                "Visualise value streams",
                "Enable ownership and belonging",
            ][len(bullets) % 5]
        )
    return bullets[:max_bullets]


def make_experience_post(sentences: List[str], length: str) -> str:
    """Assemble an experience‑led post."""
    # Determine counts based on desired length
    story_count = 3 if length != "short" else 1
    bullet_count = 3
    hook = sentences[0] if sentences else "Another day, another meet."
    story = summarise(sentences[1:], story_count)
    bullets = bulletise(sentences[1 + story_count :], bullet_count)
    parts: List[str] = []
    parts.append(f"{hook} made something obvious about ownership and value streams.")
    parts.extend(story)
    parts.append("")
    parts.extend([f"- {b}" for b in bullets])
    parts.append("")
    parts.append("Where are you seeing this most?")
    return "\n".join(parts)


def make_market_post(sentences: List[str], length: str) -> str:
    """Assemble a market‑shift post."""
    # Use the first two sentences for hook variables
    trend = sentences[0] if sentences else "automation"
    impact = sentences[1] if len(sentences) > 1 else "knowledge erosion"
    body_start = 2
    # Determine counts based on length
    what_most_people_think = summarise(sentences[body_start:], 2)
    what_breaks_next = summarise(sentences[body_start + 2 :], 4 if length == "long" else 2)
    bullets = bulletise(sentences[body_start + 6 :], 3)
    parts: List[str] = []
    parts.append(f"The market is moving towards {trend}, but the real impact is {impact}.")
    if what_most_people_think:
        parts.append("\nWhat most people think:")
        parts.extend(what_most_people_think)
    if what_breaks_next:
        parts.append("\nWhat breaks next:")
        parts.extend(what_breaks_next)
    parts.append("\nWhat to do now:")
    parts.extend([f"- {b}" for b in bullets])
    parts.append("")
    parts.append("Where does this show up most for you?")
    return "\n".join(parts)


def make_punch_post(sentences: List[str], length: str) -> str:
    """Assemble a short punchy post."""
    hook = sentences[0] if sentences else "If you cannot name the owner, you cannot scale."
    context = summarise(sentences[1:], 2)
    bullets = bulletise(sentences[3:], 3)
    parts: List[str] = []
    parts.append(f"{hook}")
    parts.extend(context)
    parts.append("")
    parts.extend([f"- {b}" for b in bullets])
    parts.append("")
    parts.append("Where are you seeing this most?")
    return "\n".join(parts)


def make_rant_post(sentences: List[str], length: str) -> str:
    """Assemble a controlled rant."""
    rant_line = sentences[0] if sentences else "A rant... we keep reinventing the wheel."
    mechanism = summarise(sentences[1:], 3)
    parts: List[str] = []
    parts.append(f"A rant… {rant_line}")
    parts.append("")
    parts.append("What to do about it:")
    parts.extend([f"- {b}" for b in bulletise(mechanism, 3)])
    parts.append("")
    parts.append("Until then… remain curious.")
    return "\n".join(parts)


def infer_archetype(total_words: int) -> str:
    """Infer archetype based on total word count."""
    if total_words < 80:
        return "punch"
    elif total_words < 250:
        return "experience"
    else:
        return "market"


def infer_length(total_words: int) -> str:
    """Infer post length based on total word count."""
    if total_words < 100:
        return "short"
    elif total_words < 220:
        return "medium"
    else:
        return "long"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a LinkedIn article from text files.")
    parser.add_argument("--folder", required=True, help="Folder containing source `.txt` or `.md` files")
    parser.add_argument("--archetype", choices=["experience", "market", "punch", "rant"], help="Type of post to generate")
    parser.add_argument("--length", choices=["short", "medium", "long"], help="Desired length of post")
    args = parser.parse_args()

    # Read and split sentences
    corpus = read_files(args.folder)
    if not corpus.strip():
        print("No readable text found in the provided folder.", file=sys.stderr)
        sys.exit(1)
    sentences = split_sentences(corpus)
    total_words = len(corpus.split())

    archetype = args.archetype or infer_archetype(total_words)
    length = args.length or infer_length(total_words)

    if archetype == "experience":
        article = make_experience_post(sentences, length)
    elif archetype == "market":
        article = make_market_post(sentences, length)
    elif archetype == "punch":
        article = make_punch_post(sentences, length)
    elif archetype == "rant":
        article = make_rant_post(sentences, length)
    else:
        raise ValueError(f"Unsupported archetype: {archetype}")

    print(article)


if __name__ == "__main__":
    main()
