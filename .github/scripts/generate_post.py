"""
generate_post.py
Calls the Anthropic API to research and write a new post for The Mothapo Doctrine.
Saves the result as a Jekyll-formatted Markdown file in _posts/.
"""

import anthropic
import os
import json
import re
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are the writer and analyst behind The Mothapo Doctrine — a personal intelligence blog written for one reader who wants to understand the true state of the world without the noise, spin, and false balance of mainstream media.

Your writing standard is as follows:

1. You begin by identifying what the dominant mainstream framing of an issue currently says.
2. You then ask: what is this framing leaving out? What is being misrepresented, omitted, or softened? Whose interests does the dominant framing serve?
3. You follow the evidence honestly. If the evidence confirms the mainstream account, say so. If it contradicts it, say so directly.
4. You write with rigour and intelligence, not for effect. You do not use dramatic language to compensate for thin arguments.
5. You are honest about genuine uncertainty. When something is unclear, say so and explain why.
6. You do not perform balance. If a government is lying, describe it as lying and show the evidence. If a company is overstating its capabilities, name it.
7. You write for a reader who is intelligent, curious, and tired of being manipulated.

Every post must be structured as follows:
- Opening: state the central claim or question plainly, in the first paragraph, without burying the lead
- Body: build the argument in sections (use ## for section headers), cross-referencing sources, exposing tensions, following the evidence
- Close: what does this mean for how the reader should understand the world right now — not a call to action, but a honest framing

Length: 900–1,400 words.

Output format — you MUST output valid Jekyll frontmatter followed by Markdown body. Use this exact structure:

---
layout: post
title: "POST TITLE HERE"
date: YYYY-MM-DD
category: "CATEGORY"
tags: [tag1, tag2, tag3]
excerpt: "One sentence that states the central argument plainly."
---

[Post body in Markdown]

Category must be one of: geopolitics, ai-technology, finance, philosophy, occult
Do not include any text outside the frontmatter + body. Output only the raw Markdown file content."""

MONDAY_PROMPT = """Today is Monday. Research and write a critical analysis post focused on GEOPOLITICS or GLOBAL POWER.

Use your web search capability to find the most significant, newsworthy geopolitical development from the past week. Prioritise stories involving:
- Shifts in global power (US, China, Russia, EU, BRICS, Africa)
- Wars and conflicts and their real drivers beyond the stated narratives
- Economic warfare, sanctions, resource competition
- What African nations — especially South Africa — need to understand about global power dynamics

Write with the full editorial standard described above. Do not cover trivial diplomatic events. Find the story that actually matters right now and explain why it matters."""

THURSDAY_PROMPT = """Today is Thursday. Research and write a critical analysis post focused on ARTIFICIAL INTELLIGENCE or TECHNOLOGY.

Use your web search capability to find the most significant AI or technology development from the past week. Prioritise stories involving:
- The actual capabilities and limitations of AI systems (cut through the hype)
- Who controls AI development, who funds it, and what their interests are
- The structural and societal implications of AI deployment
- Regulatory developments and what they actually mean vs. what they claim to mean
- What AI means for labour, power, privacy, and autonomy

Write with the full editorial standard described above. Do not cover product launches for their own sake unless the implications are significant. Find the story that actually matters and explain why."""


def determine_topic():
    """Determine the post topic based on day of week or override."""
    override = os.environ.get("TOPIC_OVERRIDE", "").strip()
    if override:
        return override

    # Monday = 0, Thursday = 3
    day = datetime.now(timezone.utc).weekday()
    if day == 0:
        return MONDAY_PROMPT
    elif day == 3:
        return THURSDAY_PROMPT
    else:
        # Fallback for manual triggers on other days — alternate
        from datetime import date
        week_num = date.today().isocalendar()[1]
        return MONDAY_PROMPT if week_num % 2 == 0 else THURSDAY_PROMPT


def generate_post(topic_prompt: str) -> str:
    """Call the Claude API with web search and return the post content."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[
            {
                "role": "user",
                "content": topic_prompt
            }
        ]
    )

    # Extract text content from response
    post_content = ""
    for block in response.content:
        if block.type == "text":
            post_content += block.text

    return post_content.strip()


def extract_frontmatter_field(content: str, field: str) -> str:
    """Extract a field value from Jekyll frontmatter."""
    pattern = rf'^{field}:\s*["\']?(.*?)["\']?\s*$'
    match = re.search(pattern, content, re.MULTILINE)
    return match.group(1).strip() if match else ""


def save_post(content: str) -> Path:
    """Save the generated post as a Jekyll Markdown file."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Extract title to build slug
    title = extract_frontmatter_field(content, "title")
    if not title:
        title = f"Post {today}"

    # Build slug from title
    slug = re.sub(r'[^a-z0-9\s-]', '', title.lower())
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)[:60]

    filename = f"{today}-{slug}.md"
    posts_dir = Path("_posts")
    posts_dir.mkdir(exist_ok=True)
    filepath = posts_dir / filename

    filepath.write_text(content, encoding="utf-8")
    print(f"Post saved: {filepath}")

    # Save metadata for Telegram notification step
    metadata = {
        "title": title,
        "filename": filename,
        "date": today,
        "excerpt": extract_frontmatter_field(content, "excerpt"),
        "slug": slug
    }
    with open(".post_metadata.json", "w") as f:
        json.dump(metadata, f)

    return filepath


def main():
    print("Determining topic...")
    topic_prompt = determine_topic()

    print("Generating post via Claude API...")
    content = generate_post(topic_prompt)

    if not content:
        raise ValueError("No content generated from API call")

    print("Saving post...")
    filepath = save_post(content)
    print(f"Done. Post at: {filepath}")


if __name__ == "__main__":
    main()
