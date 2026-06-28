"""Measure whether irrelevant extra information can obscure meaning.

The experiment keeps each original sentence intact, then appends increasing
amounts of unrelated information. Meaning retention is approximated with
TF-IDF cosine similarity between the original sentence and the overloaded
sentence.
"""

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
TRIALS = 100
OVERLOAD_LEVELS = np.arange(0.0, 5.01, 0.25)
COLLAPSE_SIMILARITY = 0.50
IRRELEVANT_TERMS = (
    "archive",
    "weather",
    "ceremony",
    "traffic",
    "festival",
    "inventory",
    "garden",
    "currency",
    "painting",
    "stadium",
    "recipe",
    "tourism",
    "furniture",
    "satellite",
    "concert",
    "shipment",
    "museum",
    "harbor",
    "fashion",
    "schedule",
)

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sentences.csv"
OUTPUT_PATH = ROOT / "visuals" / "information_overload.png"


def overload(text: str, level: float, rng: random.Random) -> str:
    """Append irrelevant terms equal to ``level`` times the original length."""
    words = text.split()
    extra_count = round(len(words) * level)
    extra_words = [rng.choice(IRRELEVANT_TERMS) for _ in range(extra_count)]
    return " ".join(words + extra_words)


def run_experiment(texts: list[str]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return mean similarity and standard deviation at each overload level."""
    rng = random.Random(SEED)
    records: list[tuple[int, int, int, str]] = []

    for level_index, level in enumerate(OVERLOAD_LEVELS):
        for trial in range(TRIALS):
            for text_index, text in enumerate(texts):
                overloaded = overload(text, level, rng)
                records.append((level_index, trial, text_index, overloaded))

    variants = [record[3] for record in records]
    vectorizer = TfidfVectorizer()
    vectorizer.fit(texts + variants)
    original_vectors = vectorizer.transform(texts)
    variant_vectors = vectorizer.transform(variants)

    scores_by_level: list[list[float]] = [
        [] for _ in range(len(OVERLOAD_LEVELS))
    ]
    for row, (level_index, _trial, text_index, _variant) in enumerate(records):
        score = cosine_similarity(
            original_vectors[text_index], variant_vectors[row]
        )[0, 0]
        scores_by_level[level_index].append(float(score))

    means = np.array([np.mean(scores) for scores in scores_by_level])
    standard_deviations = np.array(
        [np.std(scores) for scores in scores_by_level]
    )
    return OVERLOAD_LEVELS, means, standard_deviations


def first_collapse_level(levels: np.ndarray, means: np.ndarray) -> float | None:
    """Find the first overload multiplier below the collapse criterion."""
    collapsed = np.flatnonzero(means < COLLAPSE_SIMILARITY)
    return float(levels[collapsed[0]]) if collapsed.size else None


def plot_results(
    levels: np.ndarray,
    means: np.ndarray,
    standard_deviations: np.ndarray,
    threshold: float | None,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(levels, means, color="#5d3a7a", linewidth=2.5, marker="o")
    ax.fill_between(
        levels,
        np.clip(means - standard_deviations, 0, 1),
        np.clip(means + standard_deviations, 0, 1),
        color="#b79bd0",
        alpha=0.24,
        label="+/- 1 standard deviation",
    )
    ax.axhline(
        COLLAPSE_SIMILARITY,
        color="#b54a4a",
        linestyle="--",
        linewidth=1.8,
        label=f"Collapse criterion ({COLLAPSE_SIMILARITY:.2f})",
    )

    if threshold is not None:
        threshold_score = means[np.where(levels == threshold)[0][0]]
        ax.axvline(threshold, color="#b54a4a", linestyle=":", linewidth=1.8)
        ax.scatter([threshold], [threshold_score], color="#b54a4a", s=75, zorder=5)
        ax.annotate(
            f"Overload threshold: {threshold:.2f}x",
            xy=(threshold, threshold_score),
            xytext=(18, 30),
            textcoords="offset points",
            arrowprops={"arrowstyle": "->", "color": "#b54a4a"},
            color="#8c3030",
            fontweight="bold",
        )

    ax.set(
        title="Meaning Loss Under Information Overload",
        xlabel="Irrelevant information added (x original word count)",
        ylabel="Mean TF-IDF cosine similarity",
        xlim=(0, float(levels.max())),
        ylim=(0, 1.04),
    )
    ax.grid(alpha=0.18)
    ax.legend(frameon=False)
    fig.tight_layout()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    texts = pd.read_csv(DATA_PATH)["sentence"].dropna().astype(str).tolist()
    levels, means, standard_deviations = run_experiment(texts)
    threshold = first_collapse_level(levels, means)
    plot_results(levels, means, standard_deviations, threshold)

    print("\nInformation overload analysis:\n")
    for level, mean in zip(levels, means):
        print(f"{level:>4.2f}x irrelevant info -> {mean:.3f} mean similarity")
    if threshold is None:
        print("\nNo overload collapse was observed within the tested range.")
    else:
        print(
            f"\nMeaning collapsed at {threshold:.2f}x irrelevant information "
            f"(mean similarity < {COLLAPSE_SIMILARITY:.2f})."
        )
    print(f"Visualization saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
