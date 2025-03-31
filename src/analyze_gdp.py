import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 🟢 Load GDP Data
df = pd.read_csv("gdp_data.csv")

# Convert 'Year' to integer for proper sorting
df["Year"] = df["Year"].astype(int)

# Sort data in ascending order by Year
df = df.sort_values("Year")

print("✅ Data Loaded & Sorted!")
print(df.head())  # Preview first 5 rows

# 🟢 Basic Matplotlib Plot
plt.figure(figsize=(10, 5))
plt.plot(df["Year"], df["GDP (USD)"], marker="o", linestyle="-", color="b")
plt.xlabel("Year")
plt.ylabel("GDP (USD)")
plt.title(f"GDP of {df['Country'][0]} Over Time")
plt.grid(True)
plt.show()

# 🟢 Enhanced Seaborn Visualization
sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))
sns.lineplot(x=df["Year"], y=df["GDP (USD)"], marker="o", color="b")
plt.xlabel("Year", fontsize=12)
plt.ylabel("GDP (USD)", fontsize=12)
plt.title(f"GDP Trend for {df['Country'][0]}", fontsize=14)
plt.xticks(rotation=45)
plt.show()