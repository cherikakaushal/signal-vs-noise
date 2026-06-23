# Findings

## Noise Injection

Meaning degraded gradually as neutral noise replaced words. The remaining
original vocabulary preserved partial similarity rather than causing immediate
failure.

## Missing Context

Meaning dropped rapidly when words were removed because each deletion reduced
the evidence available to reconstruct the original sentence.

## Bias Injection

Meaning shifted without complete failure. Biased terms changed the framing,
even when enough of the original sentence remained recognizable.

## Combined Distortion

Failure was non-linear. Noise, missing context, and bias reinforced one another,
producing a sharper decline than any single distortion suggested on its own.

## Threshold Analysis

System breakdown occurred around 65% distortion. This is the first tested level
at which mean TF-IDF cosine similarity fell below the experiment's 0.50 collapse
criterion across 100 seeded trials per headline.
