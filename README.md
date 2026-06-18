# 📉 survival-of-the-firmest — will the business make it?

Kaplan–Meier-style **business survival curves by industry**, grounded in U.S. Bureau of Labor Statistics data — plus an honest test of whether you can predict an *individual* company's survival.

### ▶️ [Live demo](https://danielduongg.github.io/survival-of-the-firmest/)

Pick an industry and read its 1/3/5/10-year survival curve against the all-industry average. Then set founder/firm traits (size, funding, experience, location) and watch the 5-year survival barely budge.

## The finding: it's mostly the base rate

I simulated 8,000 establishments whose survival follows the sector curves, with small, realistic effects from firm traits, and asked a model to predict 5-year survival:

| Model | ROC-AUC |
|---|---|
| Sector **base rate** only | 0.573 |
| Founder/firm **traits** only | 0.578 |
| Base rate + traits | **0.607** |

Founder/firm attributes lift AUC barely above a coin flip. **Which industry you're in dominates; the individual outcome is mostly irreducible chance** — and the "lessons" from famous survivors are a survivorship-biased sample. This is the entrepreneurship version of the same lesson the rest of my portfolio keeps finding: confident-looking predictions often encode a base rate plus noise.

## Survival by industry (5-year, BLS-grounded)

Health care **59%** · Education 55% · Finance 52% · Manufacturing 50% · Professional svcs 48% · Retail 45% · Construction / Information 43% · Transportation 41% · **Restaurants 40%**

## Method

- `build.py` — fits a Weibull survival curve per sector to BLS (1-yr, 5-yr) survival anchors, simulates establishments, fits the logistic 5-yr predictor, reports the AUC comparison, exports `web_model.json`.
- `index.html` — survival curves + 5-yr predictor in the browser; the math reproduces `build.py`.

```bash
pip install -r requirements.txt
python build.py
python build_demo.py
```

> Survival anchors reflect BLS Business Employment Dynamics establishment-survival patterns; the establishment-level records are simulated to those curves so the repo is fully reproducible.
