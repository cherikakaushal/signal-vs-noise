import random
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
df = pd.read_csv("data/headlines.csv")

# Add noise function
def add_noise(text, noise_level=0.3):
    words = text.split()
    n = int(len(words) * noise_level)

    for _ in range(n):
        idx = random.randint(0, len(words)-1)
        words[idx] = "noise"

    return " ".join(words)

# Apply noise
df["noisy"] = df["text"].apply(lambda x: add_noise(x, 0.3))

# Vectorize
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["text"])
X_noisy = vectorizer.transform(df["noisy"])

# Similarity
similarity = cosine_similarity(X, X_noisy)
scores = similarity.diagonal()

# Print results
print("\nOriginal vs Noisy Similarity:\n")
for i, score in enumerate(scores):
    print(f"{df['text'][i][:40]}... → {score:.3f}")

# Plot
plt.figure()
plt.bar(range(len(scores)), scores)
plt.title("Meaning Similarity After Noise")
plt.xlabel("Sample")
plt.ylabel("Similarity")

plt.savefig("visuals/noise_similarity.png")
plt.show()