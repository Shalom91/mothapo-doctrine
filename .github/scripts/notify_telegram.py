"""
notify_telegram.py
Sends a Telegram notification via Agent Adam bot when a new post is published.
"""

import os
import requests


def send_notification():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    title = os.environ.get("POST_TITLE", "New post published")
    url = os.environ.get("POST_URL", "https://shalom91.github.io")
    excerpt = os.environ.get("POST_EXCERPT", "")

    if not bot_token or not chat_id:
        print("Telegram credentials not set. Skipping notification.")
        return

    # Build message
    message = f"""📰 *The Mothapo Doctrine*

*{title}*

_{excerpt}_

[Read the full post →]({url})"""

    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }

    response = requests.post(api_url, json=payload, timeout=30)

    if response.status_code == 200:
        print("Telegram notification sent successfully.")
    else:
        print(f"Telegram notification failed: {response.status_code} — {response.text}")


if __name__ == "__main__":
    send_notification()
