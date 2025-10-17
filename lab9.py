import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 1. Load dataset
data = pd.read_csv("customerTransactions.csv")
print("Dataset loaded successfully!")
print(data.head())

# 2. Data Cleaning
print("\nMissing values before cleaning:")
print(data.isnull().sum())

data.dropna(subset=["Customer ID"], inplace=True)
data.drop_duplicates(inplace=True)

print("\nData cleaned successfully!")
print(f"Total records after cleaning: {len(data)}")

# 3. Descriptive Statistics
print("\nDescriptive Statistics:")
print(data[["Total Amount Spent", "Total Items Purchased"]].describe())

# 4. Clustering Preparation
X = data[["Total Amount Spent", "Total Items Purchased", "Average Purchase Value"]]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. Apply K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
data["Cluster"] = kmeans.fit_predict(X_scaled)

# 6. Visualization
plt.figure(figsize=(8, 6))
plt.scatter(data["Total Amount Spent"], data["Total Items Purchased"],
            c=data["Cluster"], cmap="viridis", s=100, edgecolors='k')
plt.title("Customer Segmentation based on Spending and Purchase Behavior")
plt.xlabel("Total Amount Spent")
plt.ylabel("Total Items Purchased")
plt.colorbar(label="Cluster")
plt.show()

# 7. Segment Summary
print("\nCustomer Segment Summary:")
segment_summary = data.groupby("Cluster")[["Total Amount Spent", "Total Items Purchased", "Average Purchase Value"]].mean()
print(segment_summary)

# 8. Assign segment labels
cluster_labels = {
    0: "Low-Value Customers (Inactive/Occasional Shoppers)",
    1: "Mid-Tier Customers (Moderate Shoppers)",
    2: "High-Value Customers (Frequent & High Spenders)"
}
data["Segment"] = data["Cluster"].map(cluster_labels)

# 9. Insights & Recommendations
print("\nCustomer Engagement Recommendations:")
print("""
1️⃣ High-Value Customers:
   - Offer loyalty rewards, exclusive previews, or premium deals.
   - Personalized product recommendations.

2️⃣ Mid-Tier Customers:
   - Targeted marketing emails with discounts to boost spending.
   - Encourage subscription or bundle offers.

3️⃣ Low-Value/Inactive Customers:
   - Send reactivation offers, reminders, and special limited-time discounts.
   - Analyze their drop-off reasons (delivery time, pricing, etc.)
""")

print("\nSegmentation complete!")
