# What happens when context is missing?

## Idea

Instead of adding noise, I removed parts of the information to simulate
incomplete data.

## Approach

- Removed words from sample sentences
- Measured similarity with the original text

## Observation

Similarity dropped significantly when words were removed. Some sentences lost
most of their meaning because the remaining text no longer carried enough
specific information.

## Interpretation

Missing context is different from ordinary noise. Noise adds clutter, but
missing context removes the clues a system needs to infer what the sentence was
about in the first place.

## Why it matters

Many real systems make decisions from partial records. If key details are
absent, the output may look confident while being based on an incomplete view of
the situation.

## Real-world example

In healthcare, the sentence "The patient requires immediate treatment" changes
substantially if the words "immediate" or "treatment" disappear. The remaining
text may still look readable, but the urgency and action are weakened.

## Conclusion

Incomplete information can break understanding faster than noisy data.
