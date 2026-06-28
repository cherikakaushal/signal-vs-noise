# Methodology

## Original Sentence

The experiments use ten short English-language sentences from
`data/sentences.csv`. Each sentence is treated as an undistorted reference. The
dataset includes medical, scientific, system-status, economics, healthcare,
technology, climate, education, AI, and cybersecurity examples, providing varied
but consistently brief samples.

## Distortion Techniques

Three controlled transformations simulate information loss and manipulation:

- **Noise injection** replaces original words with the neutral token `noise`.
- **Missing context** deletes words from the sentence.
- **Bias injection** replaces words with emotionally loaded terms such as
  `crisis`, `failure`, and `collapse`.

The threshold experiment tests distortion from 0% to 100% in five-percentage-
point steps. At each level, the selected words are divided approximately evenly
among the three techniques. It runs 100 trials per sentence with a fixed random
seed, making the aggregate results reproducible while reducing sensitivity to
any single random word selection.

The information overload experiment keeps the original sentence intact and adds
irrelevant terms at increasing multiples of the original sentence length. This
tests whether excess unrelated information can obscure meaning even without
deleting or replacing the original words.

## Measurement Approach

Meaning retention is approximated using TF-IDF vectors and cosine similarity.
Every distorted sentence is compared with its original: 1.0 means identical
vector direction, while values closer to 0 indicate little shared lexical
signal. Scores are averaged across all sentences and trials at each distortion
level. For this study, **meaning collapse is operationally defined as the first
tested level where mean similarity falls below 0.50**.

This is a lexical proxy, not a complete measure of human semantic understanding.
It is transparent and consistent with the earlier experiments, but it may miss
paraphrases, negation, word order, and subtle framing changes.

## Visualization Process

The threshold chart plots mean similarity against the percentage of words
distorted. A shaded band shows one standard deviation across samples and trials.
A horizontal line marks the 0.50 collapse criterion, and the first tested point
below it is annotated as the failure threshold. The script writes the resulting
figure to `visuals/failure_threshold.png` at 200 DPI.

The overload chart plots mean similarity against the amount of irrelevant
information added, expressed as a multiple of the original word count. It uses
the same 0.50 collapse criterion and writes the figure to
`visuals/information_overload.png`.

The overall comparison chart recreates the first five experiment conditions and
plots their mean TF-IDF cosine similarity scores together. This provides a
single visual summary of how noise, missing context, bias, combined distortion,
and threshold-level distortion compare on the same measurement scale.
