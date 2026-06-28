# At what point does meaning collapse?

## Idea

Instead of testing a single fixed distortion level, I increased distortion from
0% to 100% to find the point where meaning breaks down.

## Approach

- Applied noise, missing context, and bias together
- Increased the percentage of distorted words in small steps
- Ran repeated seeded trials for each distortion level
- Measured mean TF-IDF cosine similarity against the original sentences

## Observation

Meaning did not collapse immediately. Similarity declined gradually at first,
then crossed the failure criterion around 65% distortion.

## Interpretation

This suggests that breakdown has a threshold. A system may tolerate moderate
distortion, but once enough of the sentence is altered, deleted, or reframed,
the original meaning can no longer be reliably recovered.

## Why it matters

Thresholds are useful because they turn a vague idea like "too much distortion"
into something measurable. This makes it easier to compare systems, evaluate
robustness, and explain failure points.

## Real-world example

In an automated monitoring system, a report might remain useful if a few fields
are noisy or missing. But after enough fields are distorted, the system may
still produce output while no longer representing the real event.

## Conclusion

System breakdown occurred around 65% distortion in this experiment.
