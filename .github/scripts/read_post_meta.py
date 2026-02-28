"""
read_post_meta.py
Reads the post metadata saved by generate_post.py and writes it to
GitHub Actions step outputs so the Telegram notification can use it.
"""

import json
import os
from pathlib import Path


def main():
    meta_file = Path(".post_metadata.json")
    if not meta_file.exists():
        print("No metadata file found. Skipping.")
        return

    with open(meta_file) as f:
        meta = json.load(f)

    title = meta.get("title", "New Post")
    excerpt = meta.get("excerpt", "")
    slug = meta.get("slug", "")
    date = meta.get("date", "")

    # Build the post URL
    # Format: https://shalom91.github.io/YYYY/MM/DD/slug/
    date_parts = date.split("-") if date else ["", "", ""]
    year, month, day = date_parts[0], date_parts[1], date_parts[2]
    post_url = f"https://shalom91.github.io/{year}/{month}/{day}/{slug}/"

    # Write to GitHub Actions output
    output_file = os.environ.get("GITHUB_OUTPUT", "")
    if output_file:
        with open(output_file, "a") as f:
            f.write(f"post_title={title}\n")
            f.write(f"post_url={post_url}\n")
            f.write(f"post_excerpt={excerpt}\n")
    else:
        print(f"post_title={title}")
        print(f"post_url={post_url}")
        print(f"post_excerpt={excerpt}")


if __name__ == "__main__":
    main()
