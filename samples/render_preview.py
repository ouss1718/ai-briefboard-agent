"""Create a local layout preview without any service connection."""
from pathlib import Path
from agent.render import render_carousel

stories = [
    {"headline": "A new model arrives", "summary": "An AI lab released a new model and explained its key capabilities.",
     "why_it_matters": "A practical change for people choosing AI tools.",
     "source_url": "https://openai.com/news/example", "announcement_date": "2026-09-24"},
    {"headline": "An AI tool gets updated", "summary": "The company announced a product update with new features.",
     "why_it_matters": "Everyday tasks could become quicker.",
     "source_url": "https://blog.google/example", "announcement_date": "2026-09-24"},
]
output = Path("out/preview")
print(render_carousel(stories, "2026-09-24", output, {}))
