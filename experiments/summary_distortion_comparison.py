"""Create one comparison chart across the first five experiments."""

from pathlib import Path
import random

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SEED = 42
THRESHOLD_TRIALS = 100
COLLAPSE_SIMILARITY = 0.50
THRESHOLD_LEVELS = np.arange(0.0, 1.01, 0.05)
BIAS_WORDS = ("crisis", "failure", "collapse")

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sentences.csv"
OUTPUT_PATH = ROOT / "visuals" / "overall_distortion_comparison.png"


def add_noise(text: str, rng: random.Random, level: float = 0.3) -> str:
    words = text.split()
    replacement_count = int(len(words) * level)
    for _ in range(replacement_count):
        words[rng.randrange(len(words))] = "noise"
    return " ".join(words)


def remove_words(text: str, rng: random.Random, level: float = 0.4) -> str:
    words = text.split()
    removal_count = int(len(words) * level)
    for _ in range(removal_count):
        if words:
            words.pop(rng.randrange(len(words)))
    return " ".join(words)


def add_bias(text: str, rng: random.Random, intensity: int = 5) -> str:
    words = text.split()
    for _ in range(intensity):
        if words:
            words[rng.randrange(len(words))] = rng.choice(BIAS_WORDS)
    return " ".join(words)


def apply_combined(text: str, rng: random.Random) -> str:
    text = add_noise(text, rng, level=0.3)
    text = remove_words(text, rng, level=0.3)
    return add_bias(text, rng, intensity=4)


def distort_for_threshold(text: str, level: float, rng: random.Random) -> str:
    words = text.split()
    altered_count = min(len(words), round(len(words) * level))

    if altered_count == 0:
        return text

    altered_indices = rng.sample(range(len(words)), altered_count)
    rng.shuffle(altered_indices)

    deleted = set()
    for position, index in enumerate(altered_indices):
        technique = position % 3
        if technique == 0:
            deleted.add(index)
        elif technique == 1:
            words[index] = "noise"
        else:
            words[index] = rng.choice(BIAS_WORDS)

    return " ".join(
        word for index, word in enumerate(words) if index not in deleted
    )


def mean_similarity(originals: list[str], variants: list[str]) -> float:
    vectorizer = TfidfVectorizer()
    vectorizer.fit(originals + variants)
    original_vectors = vectorizer.transform(originals)
    variant_vectors = vectorizer.transform(variants)
    scores = cosine_similarity(original_vectors, variant_vectors).diagonal()
    return float(np.mean(scores))


def threshold_result(texts: list[str], rng: random.Random) -> tuple[float, float]:
    records: list[tuple[int, int, str]] = []

    for level_index, level in enumerate(THRESHOLD_LEVELS):
        for _trial in range(THRESHOLD_TRIALS):
            for text_index, text in enumerate(texts):
                variant = distort_for_threshold(text, level, rng)
                records.append((level_index, text_index, variant))

    variants = [record[2] for record in records]
    vectorizer = TfidfVectorizer()
    vectorizer.fit(texts + variants)
    original_vectors = vectorizer.transform(texts)
    variant_vectors = vectorizer.transform(variants)

    scores_by_level: list[list[float]] = [
        [] for _ in range(len(THRESHOLD_LEVELS))
    ]
    for row, (level_index, text_index, _variant) in enumerate(records):
        score = cosine_similarity(
            original_vectors[text_index], variant_vectors[row]
        )[0, 0]
        scores_by_level[level_index].append(float(score))

    means = np.array([np.mean(scores) for scores in scores_by_level])
    collapsed = np.flatnonzero(means < COLLAPSE_SIMILARITY)
    if collapsed.size:
        index = int(collapsed[0])
    else:
        index = len(THRESHOLD_LEVELS) - 1
    return float(THRESHOLD_LEVELS[index]), float(means[index])


def build_results(texts: list[str]) -> tuple[list[str], list[float], float]:
    rng = random.Random(SEED)
    variants = {
        "Noise": [add_noise(text, rng) for text in texts],
        "Missing Context": [remove_words(text, rng) for text in texts],
        "Bias": [add_bias(text, rng) for text in texts],
        "Combined": [apply_combined(text, rng) for text in texts],
    }

    labels = list(variants)
    scores = [mean_similarity(texts, variants[label]) for label in labels]
    threshold_level, threshold_score = threshold_result(texts, rng)

    labels.append(f"Threshold ({threshold_level:.0%})")
    scores.append(threshold_score)
    return labels, scores, threshold_level


def plot_results(labels: list[str], scores: list[float]) -> None:
    colors = ["#4f81bd", "#c0504d", "#9bbb59", "#8064a2", "#f79646"]
    positions = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(positions, scores, color=colors)
    ax.axhline(
        COLLAPSE_SIMILARITY,
        color="#8c3030",
        linestyle="--",
        linewidth=1.6,
        label=f"Collapse criterion ({COLLAPSE_SIMILARITY:.2f})",
    )

    for bar, score in zip(bars, scores):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            score + 0.025,
            f"{score:.2f}",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ax.set(
        title="Overall Distortion Comparison",
        xlabel="Experiment",
        ylabel="Mean TF-IDF cosine similarity",
        ylim=(0, 1.08),
    )
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, rotation=18, ha="right")
    ax.grid(axis="y", alpha=0.18)
    ax.legend(frameon=False)
    fig.tight_layout()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    texts = pd.read_csv(DATA_PATH)["sentence"].dropna().astype(str).tolist()
    labels, scores, threshold_level = build_results(texts)
    plot_results(labels, scores)

    print("\nOverall distortion comparison:\n")
    for label, score in zip(labels, scores):
        print(f"{label:<22} -> {score:.3f} mean similarity")
    print(f"\nThreshold condition uses collapse at {threshold_level:.0%} distortion.")
    print(f"Visualization saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
