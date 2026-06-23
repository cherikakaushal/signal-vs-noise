# Methodology

## Original Sentence

The experiments use ten short English-language headlines from
`data/headlines.csv`. Each headline is treated as an undistorted reference. The
dataset spans economics, healthcare, technology, climate, education, security,
space, and biotechnology, providing varied but consistently brief samples.

## Distortion Techniques

Three controlled transformations simulate information loss and manipulation:

- **Noise injection** replaces original words with the neutral token `noise`.
- **Missing context** deletes words from the sentence.
- **Bias injection** replaces words with emotionally loaded terms such as
  `crisis`, `failure`, and `collapse`.

The threshold experiment tests distortion from 0% to 100% in five-percentage-
point steps. At each level, the selected words are divided approximately evenly
among the three techniques. It runs 100 trials per headline with a fixed random
seed, making the aggregate results reproducible while reducing sensitivity to
any single random word selection.

## Measurement Approach

Meaning retention is approximated using TF-IDF vectors and cosine similarity.
Every distorted sentence is compared with its original: 1.0 means identical
vector direction, while values closer to 0 indicate little shared lexical
signal. Scores are averaged across all headlines and trials at each distortion
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
