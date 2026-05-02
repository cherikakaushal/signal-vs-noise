import pandas as pd
import matplotlib.pyplot as plt
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
df = pd.read_csv("data/headlines.csv")

# Bias injection function
def add_bias(text, bias_words=["crisis", "failure", "collapse"], intensity=5):
    words = text.split()

    # Replace actual words instead of just adding
    for _ in range(intensity):
        if words:
            idx = random.randint(0, len(words)-1)
            words[idx] = random.choice(bias_words)

    return " ".join(words)

# Apply bias
df["biased"] = df["text"].apply(lambda x: add_bias(x))

# Vectorize
vectorizer = TfidfVectorizer()
combined = pd.concat([df["text"], df["biased"]])
vectorizer.fit(combined)

X = vectorizer.transform(df["text"])
X_biased = vectorizer.transform(df["biased"])

# Similarity
similarity = cosine_similarity(X, X_biased)
scores = similarity.diagonal()

# Print
print("\nOriginal vs Biased Similarity:\n")
for i, score in enumerate(scores):
    print(f"{df['text'][i][:40]}... → {score:.3f}")

# Plot
plt.figure()
plt.bar(range(len(scores)), scores)
plt.title("Meaning Similarity After Bias Injection")
plt.xlabel("Sample")
plt.ylabel("Similarity")

plt.savefig("visuals/bias_effect.png")
plt.show()