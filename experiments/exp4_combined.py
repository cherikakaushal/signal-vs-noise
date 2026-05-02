import pandas as pd
import random
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
df = pd.read_csv("data/headlines.csv")

# Noise
def add_noise(text, level=0.3):
    words = text.split()
    n = int(len(words) * level)
    for _ in range(n):
        idx = random.randint(0, len(words)-1)
        words[idx] = "noise"
    return " ".join(words)

# Missing
def remove_words(text, level=0.3):
    words = text.split()
    n = int(len(words) * level)
    for _ in range(n):
        if words:
            idx = random.randint(0, len(words)-1)
            words.pop(idx)
    return " ".join(words)

# Bias
def add_bias(text, bias_words=["crisis", "failure", "collapse"], intensity=4):
    words = text.split()
    for _ in range(intensity):
        if words:
            idx = random.randint(0, len(words)-1)
            words[idx] = random.choice(bias_words)
    return " ".join(words)

# Apply all together
def apply_all(text):
    text = add_noise(text, 0.3)
    text = remove_words(text, 0.3)
    text = add_bias(text)
    return text

df["combined"] = df["text"].apply(apply_all)

# Vectorize properly
vectorizer = TfidfVectorizer()
combined_data = pd.concat([df["text"], df["combined"]])
vectorizer.fit(combined_data)

X = vectorizer.transform(df["text"])
X_combined = vectorizer.transform(df["combined"])

# Similarity
similarity = cosine_similarity(X, X_combined)
scores = similarity.diagonal()

# Print
print("\nOriginal vs Combined Distortion:\n")
for i, score in enumerate(scores):
    print(f"{df['text'][i][:40]}... → {score:.3f}")

# Plot
plt.figure()
plt.bar(range(len(scores)), scores)
plt.title("System Breakdown Under Combined Distortion")
plt.xlabel("Sample")
plt.ylabel("Similarity")

plt.savefig("visuals/system_breakdown.png")
plt.show()