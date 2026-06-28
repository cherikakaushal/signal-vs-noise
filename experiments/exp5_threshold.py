"""Find the distortion level at which sentence meaning collapses.

The experiment progressively alters a fixed share of each sentence's words.
Altered words are evenly assigned to deletion, neutral noise, and biased
replacement. Meaning is approximated with TF-IDF cosine similarity, matching
the earlier experiments in this project.
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
COLLAPSE_SIMILARITY = 0.50
DISTORTION_LEVELS = np.arange(0.0, 1.01, 0.05)
BIAS_WORDS = ("crisis", "failure", "collapse")

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sentences.csv"
OUTPUT_PATH = ROOT / "visuals" / "failure_threshold.png"


def distort(text: str, level: float, rng: random.Random) -> str:
    """Alter ``level`` of the words using three distortion techniques."""
    words = text.split()
    altered_count = min(len(words), round(len(words) * level))

    if altered_count == 0:
        return text

    altered_indices = rng.sample(range(len(words)), altered_count)
    rng.shuffle(altered_indices)

    # Cycle through techniques so their contribution stays approximately even.
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


def run_experiment(texts: list[str]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return mean similarity and its standard deviation at every level."""
    rng = random.Random(SEED)
    records: list[tuple[int, int, int, str]] = []

    for level_index, level in enumerate(DISTORTION_LEVELS):
        for trial in range(TRIALS):
            for text_index, text in enumerate(texts):
                records.append(
                    (level_index, trial, text_index, distort(text, level, rng))
                )

    # Fit once on originals and all variants so every comparison shares the
    # same vocabulary and feature weights.
    variants = [record[3] for record in records]
    vectorizer = TfidfVectorizer()
    vectorizer.fit(texts + variants)
    original_vectors = vectorizer.transform(texts)
    variant_vectors = vectorizer.transform(variants)

    scores_by_level: list[list[float]] = [
        [] for _ in range(len(DISTORTION_LEVELS))
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
    return DISTORTION_LEVELS, means, standard_deviations


def first_collapse_level(levels: np.ndarray, means: np.ndarray) -> float | None:
    """Find the first tested level whose mean similarity is below the cutoff."""
    collapsed = np.flatnonzero(means < COLLAPSE_SIMILARITY)
    return float(levels[collapsed[0]]) if collapsed.size else None


def plot_results(
    levels: np.ndarray,
    means: np.ndarray,
    standard_deviations: np.ndarray,
    threshold: float | None,
) -> None:
    percentages = levels * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(percentages, means, color="#245b78", linewidth=2.5, marker="o")
    ax.fill_between(
        percentages,
        np.clip(means - standard_deviations, 0, 1),
        np.clip(means + standard_deviations, 0, 1),
        color="#76a9c2",
        alpha=0.22,
        label="±1 standard deviation",
    )
    ax.axhline(
        COLLAPSE_SIMILARITY,
        color="#b54a4a",
        linestyle="--",
        linewidth=1.8,
        label=f"Collapse criterion ({COLLAPSE_SIMILARITY:.2f})",
    )

    if threshold is not None:
        threshold_percent = threshold * 100
        threshold_score = means[np.where(levels == threshold)[0][0]]
        ax.axvline(threshold_percent, color="#b54a4a", linestyle=":", linewidth=1.8)
        ax.scatter(
            [threshold_percent], [threshold_score], color="#b54a4a", s=75, zorder=5
        )
        ax.annotate(
            f"Failure threshold: {threshold_percent:.0f}%",
            xy=(threshold_percent, threshold_score),
            xytext=(-120, -42),
            textcoords="offset points",
            arrowprops={"arrowstyle": "->", "color": "#b54a4a"},
            color="#8c3030",
            fontweight="bold",
        )

    ax.set(
        title="Meaning Collapse Under Increasing Distortion",
        xlabel="Words distorted (%)",
        ylabel="Mean TF-IDF cosine similarity",
        xlim=(0, 100),
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

    print("\nDistortion threshold analysis:\n")
    for level, mean in zip(levels, means):
        print(f"{level:>4.0%} distortion -> {mean:.3f} mean similarity")
    if threshold is None:
        print("\nNo collapse was observed within the tested range.")
    else:
        print(
            f"\nMeaning collapsed at {threshold:.0%} distortion "
            f"(mean similarity < {COLLAPSE_SIMILARITY:.2f})."
        )
    print(f"Visualization saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
