# The Mothapo Doctrine

A personal intelligence blog. Critical analysis of geopolitics, AI, finance, and the forces shaping the world. Twice weekly. No noise.

Live at: **https://shalom91.github.io/mothapo-doctrine**

---

## Setup Instructions

### 1. Enable GitHub Pages

1. Go to your repo on GitHub → **Settings** → **Pages**
2. Under **Source**, select **Deploy from a branch**
3. Branch: `main`, folder: `/ (root)`
4. Click Save. Your site will be live within a few minutes.

### 2. Add Repository Secrets

Go to your repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these three secrets:

| Secret Name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key (starts with `sk-ant-...`) |
| `TELEGRAM_BOT_TOKEN` | Agent Adam's bot token from BotFather |
| `TELEGRAM_CHAT_ID` | Your personal Telegram chat ID |

### 3. Enable GitHub Actions

Go to **Actions** tab → if prompted, click **"I understand my workflows, go ahead and enable them"**

The workflow will now run automatically:
- **Every Monday at 08:00 SAST** — Geopolitics post
- **Every Thursday at 08:00 SAST** — AI & Technology post

### 4. Test a Manual Run

Go to **Actions** → **Generate Post** → **Run workflow** → **Run workflow**

This will generate a post immediately so you can verify everything works end to end.

---

## Local Development (Optional)

```bash
gem install bundler
bundle install
bundle exec jekyll serve
```

Visit `http://localhost:4000` to preview locally.

---

## How It Works

1. GitHub Actions triggers on a cron schedule
2. Python script calls the Claude API with web search enabled
3. Claude researches current events and writes a critical analysis post
4. The post is saved as a Markdown file and committed to `_posts/`
5. GitHub Pages rebuilds the site automatically
6. A Telegram message is sent to your phone via Agent Adam

---

*Written with rigour. Read with intent.*
