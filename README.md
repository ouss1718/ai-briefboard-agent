# The AI Briefboard: daily Instagram agent

This is an unattended daily pipeline for **@theaibriefboard**. It checks selected public Instagram pages for recent AI posts, treats them as story leads, searches for the original announcements, checks the resulting claims against the source article, designs an original image carousel, and schedules that carousel through the connected Buffer Instagram channel.

It **skips a day** when there is no recent, source-verified story. It never reposts a competitor's images. Publishing is automatic after the one-time setup below.

## One-time setup

1. Create an **Apify** account and get an API token. Test [Apify's Instagram Scraper](https://apify.com/apify/instagram-scraper) with `https://www.instagram.com/try_applyy/` and confirm it returns recent captions and post URLs. Public-page collection is less reliable than an official feed; a failed collection skips the day.
2. Create an **OpenAI API** account and API key. API usage is billed separately from a ChatGPT subscription. Set a usage budget you are comfortable with. The workflow uses `gpt-5.4-mini` with web search and a separate source check.
3. In [Buffer API settings](https://publish.buffer.com/settings/api), create an API key. Confirm **@theaibriefboard** is a connected professional Instagram channel set to automatic publishing. Obtain its Buffer **channel ID** from the API's [get channels](https://developers.buffer.com/guides/your-first-post.html) example; the schedule-page URL may contain it, but verify that the API returns the correct Instagram name before activation.
4. Create a **public GitHub repository** and add the contents of this folder. Public access is required because Buffer fetches the generated images from public image URLs. Keep API tokens only in repository **Actions secrets**, never in the repository files. Enable GitHub Actions and allow workflow write access to repository contents under **Settings → Actions → General → Workflow permissions**.
5. Create four Actions repository secrets: `APIFY_TOKEN`, `OPENAI_API_KEY`, `BUFFER_API_KEY`, and `BUFFER_CHANNEL_ID`. Use the channel ID for @theaibriefboard, not a personal account.
6. Edit `config.json` to add the exact public Instagram profile URLs you want monitored. The initial list contains only `@try_applyy`. Add several relevant pages for a useful daily roundup. The `source_domains` list defines which original publishers count as evidence; expand it for other legitimate AI vendors.
7. In **Actions → Daily AI Briefboard → Run workflow**, run it once manually and inspect the run log, the generated slides in `published/YYYY-MM-DD/`, the Buffer scheduled post, and the actual Instagram publication. A scheduled run then starts at **08:00 UTC daily**; Buffer's publish time is set about 35 minutes later. GitHub's scheduled starts can be delayed. The time can be changed in `.github/workflows/daily.yml`.

## What each run does

`prepare` calls Apify once for the configured profiles, filters posts older than 72 hours, and sends the recent captions to OpenAI as untrusted leads. Web search is restricted to the configured original-source domains. A story is rejected unless the original announcement URL appears in the search tool's actual retrieved sources, has an announcement date inside the time window, and passes a second check against the fetched announcement article. A fresh 3–5 image carousel and source-linked caption are then rendered.

The workflow commits the images before `publish` calls Buffer, verifies each image URL is public, and schedules an image-only carousel on the configured Instagram channel. It records successful source URLs and dates to avoid normal repeats. The daily action allows only one concurrent run. If a run fails after Buffer accepts a post but before the history commit, investigate the Buffer queue before manually rerunning it; that narrow failure window could create a duplicate.

The generated slides are designed for a daily multi-story carousel. Sources appear as domains on slides and as full URLs in the caption. Neither Instagram captions nor retrieved pages are allowed to instruct the agent. Posts that fail verification are skipped; there is no fallback to unsourced text.

## Local commands

Install `pip install -r requirements.txt`, then use `python -m agent.main prepare` and `python -m agent.main publish` with the respective environment variables. `publish` requires the images already committed to a **public** GitHub repository. Do not run `publish` locally merely to test rendering; it creates a real scheduled post.

The `samples/` directory provides a non-network rendering example: `python -m samples.render_preview`. This does not call Apify, OpenAI, or Buffer.

## Operational limits

- This setup requires separate Apify and OpenAI API accounts and a public GitHub repository. Buffer Free supports API access and up to ten posts queued per channel at once; the daily run keeps its queue short.
- A public scraper can fail or change output. If it fails, the workflow stops before creating a post.
- Automated fact checking reduces errors but does not guarantee editorial accuracy. Review the first week of scheduled and published posts, especially source dates and summaries. Add a human approval gate if you need stricter editorial control.
- The script uses public, text-led original graphics. It does not download or reuse other pages' copyrighted images.
