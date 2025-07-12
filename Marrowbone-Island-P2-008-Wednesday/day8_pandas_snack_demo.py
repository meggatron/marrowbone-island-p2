import pandas as pd
import matplotlib.pyplot as plt

# Load from CSV
df = pd.read_csv("snacks.csv")

# Group by category and compute average rating
avg_ratings = df.groupby("category")["rating"].mean().sort_values(ascending=False)

# Plot
ax = avg_ratings.plot(kind="bar", color="purple", title="Average Snack Rating by Category")
ax.set_ylabel("Average Rating")
ax.set_xlabel("Category")
plt.tight_layout()
plt.show()