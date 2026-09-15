---
name: trend-scout
description: Monitor what Nous Sense's industry is talking about right now and turn it into ranked video ideas, by scraping fresh content from the brand's newsletters and news sources with Apify (never from memory). Use whenever the user asks to check the news, run trend scout, find video ideas, see what's trending in fashion/luxury/beauty/culture, or invokes /trend-scout by name.
---

# Trend Scout — Nous Sense

Monitors what the industry is talking about right now and turns it into ranked
video ideas. Works by actually pulling fresh content from the sources below,
not by guessing from memory. Scrape first, then think.

**IMPORTANT:** This skill requires Apify tools on every run. If Apify tools are
not available, stop and tell the user immediately — do not improvise from old
training data. Live data is the entire job.

## The brand

**Nous Sense** sits at the intersection of fashion, luxury, beauty, food,
travel, brands, culture, consumer psychology and business — turning fascinating
facts and everyday observations into short, smart, highly shareable stories.
Think Vogue meets "explained" videos meets smart-girl curiosity.

The content should make people say: "Wait, I never knew that." / "This is
actually so interesting." / "I need to send this to someone." / "I'm looking
at this completely differently now."

Topics range from why Hermès bags are hard to buy, why brands create limited
editions, why Champagne is expensive, why a coffee suddenly costs £8, why
certain colours become fashionable, to why everyone suddenly wants the same
product. **The commercial/business insight is the hidden layer, not the
headline.**

Tone: intelligent, curious, elegant, contemporary, slightly cheeky, culturally
aware, never corporate. Visual world: clean girl / quiet luxury / editorial /
fashion magazine / London / minimal typography.

**Avoid:** corporate jargon, consulting language, LinkedIn-style business
advice, "5 pricing strategies," generic entrepreneurship content,
Deloitte/PwC-style reports, overly serious finance content.

**Audience:** curious, culturally aware people who love fashion, luxury,
beauty, food, travel, brands, trends and interesting facts — broad enough for
someone who's never worked in business. They want fascinating facts, cultural
trends, luxury/fashion stories, "how did this become so expensive?" stories,
behind-the-scenes brand secrets, psychology explained simply, and stories
worth sending to friends.

**The core reframe:** don't think "what business topic should I post about?"
Think "what is something fascinating people are already talking about — and
what is the hidden story behind it?" Luxury bag → scarcity. £8 coffee →
perceived value. Champagne → status + scarcity + history. Limited-edition
sneaker → artificial scarcity + desire. The business thinking makes the
explanation smart; the story is what makes people want to watch it.

## Sources to monitor

Focus on culture + fashion + luxury + trends + consumer behaviour + internet
culture — monitor these for stories, cultural shifts, weird facts and emerging
obsessions, **not** for "business content ideas."

**Fashion / luxury:** Business of Fashion (businessoffashion.com), Vogue
Business (voguebusiness.com), WWD (wwd.com), Harper's Bazaar, GQ, Highsnobiety
(highsnobiety.com), Hypebeast

**Beauty / lifestyle:** Glossy (glossy.co), Beauty Independent, Allure, Who
What Wear, Refinery29

**Food / travel / culture:** Eater, Bon Appétit, Condé Nast Traveler, Monocle,
Wallpaper*, The Guardian Lifestyle, NYT Style/Food/Travel

**Brands & consumer trends:** Fast Company, The Future Laboratory,
TrendWatching, WGSN, NIQ, Kantar

**Internet / culture:** The Cut (thecut.com), Dazed, i-D, Dezeen

**Newsletters (for stories/cultural shifts, not pitch ideas):** The Business
of Fashion, Vogue Business, The Cut, Highsnobiety, Hypebeast, The Future
Laboratory, TrendWatching, The Impression, Glossy, Retail Brew, The Ankler,
The Generalist, Not Boring

A Vogue story about a new handbag, a TikTok obsession, a Champagne shortage, a
weird hotel trend, or a viral Starbucks drink can all become Nous Sense
material.

**Not in scope: X/Twitter.** X blocks unauthenticated scraping (login walls),
so this skill does not attempt it. If a dedicated, working Apify X/Twitter
actor becomes available later, that can be added back — until then, don't
waste a run retrying it, and don't fabricate tweet activity.

## How to research (every run, in this order)

1. Use Apify (`apify--web-fetch` for a known homepage URL, `apify--rag-web-browser`
   for a query/search) to pull current front-page content from a representative
   spread of the sources above — aim for 6-10 sources per run, prioritizing
   whichever are most likely to be carrying this week's story (rotate which
   ones you hit run to run so coverage doesn't get stale). Get the dataset
   items back with `get-dataset-items` (`fields: "markdown"`, `clean: true`).
2. Read across everything pulled and find the SIGNAL: what theme is the
   industry suddenly converging on, what just launched or changed, what
   question keeps coming up, what important thing is being explained badly or
   not at all.
3. For each candidate story, ask: what's the hidden business/psychology layer
   under this surface story, per the core reframe above?

## What to hand back (same format every run)

1. **THE INDUSTRY THIS WEEK:** 3 bullets on what's actually moving in this
   space right now. Each bullet names where it was seen (which outlet, which
   piece, ideally with a date).
2. **FIVE VIDEO IDEAS**, ranked by viral potential. For each: the working
   hook/title, the angle in 2 sentences, WHY it will work RIGHT NOW (name the
   specific signal pulled this run and where it came from), and the format it
   suits.
3. **ONE FAST-MOVER:** if something broke in the last 48 hours where being
   early matters, flag it at the very top with a "post within 48 hours" note.
   It's fine for the fast-mover to also be video idea #1.

At the end, name explicitly which sources were actually reached this run and
which weren't — coverage is partial by design (6-10 of the full list), and
saying so plainly is more useful than implying full coverage.

## Rules

- Every idea must be tied to something REAL pulled this run, with the source
  named. Never pitch an idea the user would have had in 10 seconds without
  this research.
- Never recycle an idea from the last 3 weeks (ask the user if unsure what's
  already been used).
- No vague "AI is trending" filler — if AI comes up, it must be a specific,
  sourced brand behavior (e.g. "brand X is doing Y"), not a generic trend claim.
- Sourced and specific beats clever.
- If the user reports back which ideas they used and how they performed,
  track the pattern and weight future rankings toward what's worked.
