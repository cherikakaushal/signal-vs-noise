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
criterion across 100 seeded trials per sentence.

## Information Overload

Too much irrelevant information also degraded meaning. Even when the original
sentence remained intact, added unrelated terms diluted the signal and pushed
the sentence representation away from its starting point. Collapse occurred at
4.75x irrelevant information, meaning the added irrelevant words were 4.75 times
the original sentence length.

## Overall Comparison

The summary comparison places the first five experiments on one scale. It makes
the contrast easier to see: single distortions can leave partial meaning intact,
while combined distortion and threshold-level distortion move much closer to
the collapse boundary. In the summary run, mean similarity was 0.813 for noise,
0.792 for missing context, 0.460 for bias, 0.263 for combined distortion, and
0.496 at the 65% threshold condition.
