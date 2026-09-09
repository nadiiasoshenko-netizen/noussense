---
name: growth-edit-hooks
description: Write hooks, curiosity gaps, and slide-by-slide content structure for The Growth Edit's Instagram carousels — an editorial commercial-insight brand (pricing, brand strategy, consumer behaviour told through everyday examples like coffee, Zara, airlines, supermarkets). Use this skill whenever the user asks to write, brainstorm, or improve a carousel HOOK, TITLE, TOPIC, CAPTION, or CTA for The Growth Edit, or asks "what should this carousel say," "give me hooks for X," or wants the content/copy for a carousel before (or instead of) the visual build. Always use this skill before writing carousel copy for this brand — never default to generic hook-writing. For turning finished copy into on-brand visual slides, hand off to the `growth-edit-carousels` skill instead.
---

# The Growth Edit — Hook & Engagement Skill

Writes the *content* of a Growth Edit carousel — the hook, the slide-by-slide
structure, and the CTA — before any visual design happens. This is the
content-strategy layer; `growth-edit-carousels` is the visual-build layer.
Typical order: run this skill first to lock the hook and slide sequence, then
hand the copy to `growth-edit-carousels` to lay it out on-brand.

## 1. Purpose

Create carousels that attract new audiences and generate swipes, saves,
shares, comments, and profile visits — while building The Growth Edit as a
premium, intelligent editorial brand.

The goal is never generic "business tips." It's making sophisticated
commercial thinking feel obvious, relevant, and unexpectedly interesting
through everyday consumer examples.

**Never create a carousel that merely informs. Create one that creates a
reaction:** "Wait, what?" / "Is that actually true?" / "I never thought about
it like that." / "I need to know the answer." / "I should save this." /
"Someone I know needs to see this."

## 2. The core formula

**FAMILIARITY + TENSION + CURIOSITY + COMMERCIAL INSIGHT**

- **Familiarity** — start with something people already know: coffee,
  chocolate, restaurants, supermarkets, beauty, travel, fashion,
  subscriptions.
- **Tension** — introduce an unexpected question, contradiction, or
  commercial problem.
- **Curiosity** — leave one important question unresolved.
- **Commercial insight** — reveal the pricing, portfolio, promotion, brand,
  profitability, or consumer-behaviour lesson underneath it.

Recurring editorial universe — reuse and extend these pairings so the brand
feels like a recognisable universe of observations, not disconnected tips:
coffee → pricing power · Zara → scarcity · airlines → segmentation ·
restaurant menus → price anchoring · luxury hotels → willingness to pay ·
supermarkets → promotions/portfolio strategy · beauty → premiumisation ·
champagne → perceived value.

## 3. Title vs. hook

A title describes the content. A hook creates tension. Always choose the
hook.

- Weak: "5 Principles of Pricing Strategy"
- Strong: "Your customers don't know your costs. So why should your price be
  based on them?"

## 4. Hook mechanisms

Pick the mechanism that best fits the insight — don't force one every time.

| Mechanism | What it does | Example |
|---|---|---|
| **Contrarian** | Challenge a common assumption | "Discounting isn't always the best way to drive sales." |
| **I never thought about it like that** | Turn ordinary consumer behaviour into a surprising business lesson | "Your £5 coffee is actually a pricing lesson." |
| **Specific number** | Use a number for specificity and tension | "£3.80 → £5.00: what actually changed?" |
| **Question** | Ask a specific question containing commercial tension | "Why would someone pay £6 for a coffee they could get for £4?" |
| **Everyday object → big idea** | Familiar product as gateway to strategy | "What a £5 coffee can teach us about pricing power." |
| **Mistake** | Name a common commercial mistake, no manufactured controversy | "You're probably thinking about promotions backwards." |
| **Before → after** | Show a transformation, ask what caused it | "Same product. Different proposition. Very different price." |
| **Hidden mechanism** | Suggest the visible explanation isn't the real one | "The reason people pay more isn't what you think." |
| **Mini case study** | Recognisable brand or situation as entry point | "What Pret can teach us about pricing." |
| **Social/share hook** | Give the viewer a reason to send it to someone | "Every commercial team should have this conversation before the next price increase." |

See `references/hook-library.md` for a longer bank of fill-in-the-blank hook
formulas to riff from.

## 5. Curiosity gap rule

Slide 1 should tell the viewer enough to understand why they should care —
but not enough to remove the reason to swipe. Ask: *what does the viewer know
after Slide 1, and what do they still need to know?* Never reveal the whole
answer on Slide 1.

**One unresolved question.** Slide 1 should create exactly one clear
unresolved question. The rest of the carousel progressively answers it. Don't
pack several claims, questions, and concepts into the first slide.

## 6. The swipe ladder

Default structure — use as the backbone, adapt slide count to the content:

1. **Curiosity** — stop the scroll, create the unresolved question.
2. **Context** — establish the familiar situation.
3. **First reveal** — the first surprising piece of information.
4. **Deeper insight** — what's really happening.
5. **Payoff** — connect the observation to the commercial principle.
6. **Takeaway + action** — a memorable conclusion and one clear CTA.

Every slide must answer "why should I swipe again?" If it doesn't, remove,
rewrite, or reorder it.

## 7. Pick one engagement objective per carousel

- **Save** — frameworks, checklists, formulas, mistakes, decision questions,
  reference material.
- **Share** — surprising observations, relatable truths, industry insights,
  ideas worth sending to someone.
- **Comment** — opinion gaps, questions with two or more legitimate
  positions.
- **Follow** — distinctive recurring thinking that makes people want to see
  what The Growth Edit notices next.

**Comment hooks** should create a genuine opinion gap, not "What do you
think?" — e.g. "Would you pay £6 for this?" / "Which matters more: product
quality or brand?" / "Is this premiumisation — or simply better marketing?"

## 8. Tone

Intelligent but accessible · editorial rather than corporate · sharp but not
aggressive · curious rather than preachy · premium and understated ·
commercially credible without sounding like a consultant deck · human,
observational, slightly witty when it fits.

The brand sounds like someone who notices commercially interesting things
that other people walk past — not a consultant.

## 9. What not to do

- Generic hooks ("5 Ways to Grow Your Business")
- LinkedIn-style corporate jargon
- Fake urgency ("STOP SCROLLING!!!")
- Manufactured controversy
- Unsupported claims or exaggerated promises
- Clickbait the content can't justify
- Overloading Slide 1 with information
- Turning the carousel into a PowerPoint deck
- Optimising for likes alone

## 10. Visual hook rules (for whoever builds the slide)

The first slide must work visually before the caption is read: one strong
headline, one visual tension, large legible type, a real object/price/
receipt/brand environment where relevant, premium and uncluttered. Avoid
giant clickbait typography, excessive emojis, cartoon graphics, noisy
layouts. Hand these constraints to `growth-edit-carousels` along with the
copy — that skill owns the actual token values (colors, type scale).

## 11. Hook generation workflow

Run this whenever asked for hooks or a full carousel:

1. Identify the single commercial insight.
2. Find the most relatable everyday entry point.
3. Identify the tension, contradiction, or curiosity gap.
4. Choose the most suitable hook mechanism (§4).
5. Generate **10 genuinely different hooks** — not 10 rewrites of the same
   sentence.
6. Score each against `references/hook-library.md`'s rubric (scroll-stop,
   curiosity, specificity, shareability, follow potential, credibility,
   originality, brand fit).
7. Select the strongest combination of curiosity × credibility × relevance ×
   brand fit.
8. Build the carousel around that one unresolved question.
9. Write the slide-by-slide swipe ladder (§6).
10. Choose ONE primary engagement objective (§7).
11. Write a concise CTA matching that objective.
12. Run the final quality check below before handing off.

## 12. Final quality check

- Can Slide 1 be understood in under two seconds?
- Does Slide 1 create one clear unresolved question?
- Does the viewer have a reason to swipe?
- Does each slide have one clear job?
- Is the payoff stronger than the hook?
- Is the commercial insight genuinely useful or surprising?
- Is it understandable to someone outside FMCG?
- Does it avoid consultant jargon?
- Is the primary engagement action clear?
- Would a new follower understand what The Growth Edit is about?
- Does it feel premium, editorial, and distinctive?

## Signature principle

Don't make The Growth Edit sound like a consultant. Make it sound like
someone who notices things other people walk past. Ordinary thing →
unexpected question → commercial insight → memorable takeaway.

## Reference

`references/hook-library.md` — the full fill-in-the-blank hook formula bank
and the 9-dimension scoring rubric with target scores. Read it when
generating the 10-hook batch in step 5 above.
