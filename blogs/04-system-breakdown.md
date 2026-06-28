# When does a system actually break?

## Idea

Instead of testing individual distortions, I combined noise, missing data, and
bias.

## Approach

- Applied all three distortions together
- Measured similarity with the original text

## Observation

When noise, missing context, and bias were combined, similarity dropped more
sharply than the individual experiments suggested. The system did not degrade in
a neat straight line.

## Interpretation

Failures interact. Missing words reduce context, noisy terms add confusion, and
biased replacements shift framing. Together, they compound into a stronger form
of breakdown.

## Why it matters

Real-world data rarely fails in just one way. A model or decision system may be
asked to process input that is incomplete, noisy, and biased at the same time.
Testing only one failure mode can underestimate the real risk.

## Real-world example

In cybersecurity, an alert stream might contain missing fields, irrelevant log
noise, and biased priority labels. Any one issue is manageable, but together
they can cause analysts or automated systems to misread the severity of an
incident.

## Conclusion

Understanding combined effects is critical for building reliable systems.
