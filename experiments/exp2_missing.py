import pandas as pd
import matplotlib.pyplot as plt
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
df = pd.read_csv("data/sentences.csv")

# Function to remove words (simulate missing context)
def remove_words(text, remove_ratio=0.4):
    words = text.split()
    n = int(len(words) * remove_ratio)

    for _ in range(n):
        if words:
            idx = random.randint(0, len(words)-1)
            words.pop(idx)

    return " ".join(words)

# Apply missing context
df["missing"] = df["sentence"].apply(lambda x: remove_words(x, 0.4))

# Vectorize
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["sentence"])
X_missing = vectorizer.transform(df["missing"])

# Similarity
similarity = cosine_similarity(X, X_missing)
scores = similarity.diagonal()

# Print
print("\nOriginal vs Missing Context Similarity:\n")
for i, score in enumerate(scores):
    print(f"{df['sentence'][i][:40]}... → {score:.3f}")

# Plot
plt.figure()
plt.bar(range(len(scores)), scores)
plt.title("Meaning Similarity After Missing Context")
plt.xlabel("Sample")
plt.ylabel("Similarity")

plt.savefig("visuals/missing_context.png")
plt.show()
