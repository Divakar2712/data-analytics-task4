import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 1. Load & Basic Setup
# -----------------------------
file_path = "cleaned_superstore.csv"
df = pd.read_csv(file_path, encoding="latin1")

# Standardize column names (strip spaces)
df.columns = [c.strip() for c in df.columns]

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

# Create extra time features
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

# -----------------------------
# 2. Data Cleaning Checks
# -----------------------------
print("===== DATA OVERVIEW =====")
print(df.head())
print("\nMissing Values:\n", df.isnull().sum())

# Fill simple missing (if any)
df["Profit"] = df["Profit"].fillna(0)
df["Sales"] = df["Sales"].fillna(0)
df["Quantity"] = df["Quantity"].fillna(0)

# -----------------------------
# 3. KPI Calculations
# -----------------------------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_quantity = df["Quantity"].sum()

print("\n===== KPIs =====")
print(f"Total Sales: {total_sales:,.2f}")
print(f"Total Profit: {total_profit:,.2f}")
print(f"Total Quantity: {total_quantity:,.0f}")

# -----------------------------
# 4. Aggregations (Insights Base)
# -----------------------------
sales_by_region = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
profit_by_region = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)

sales_by_category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
sales_by_segment = df.groupby("Segment")["Sales"].sum().sort_values(ascending=False)

monthly_sales = df.groupby("Month")["Sales"].sum().sort_index()

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n===== SALES BY REGION =====\n", sales_by_region)
print("\n===== PROFIT BY REGION =====\n", profit_by_region)
print("\n===== SALES BY CATEGORY =====\n", sales_by_category)
print("\n===== SALES BY SEGMENT =====\n", sales_by_segment)
print("\n===== TOP 10 PRODUCTS =====\n", top_products)

# -----------------------------
# 5. Save Tables (for GitHub)
# -----------------------------
sales_by_region.to_csv("task4_sales_by_region.csv")
profit_by_region.to_csv("task4_profit_by_region.csv")
sales_by_category.to_csv("task4_sales_by_category.csv")
sales_by_segment.to_csv("task4_sales_by_segment.csv")
monthly_sales.to_csv("task4_monthly_sales.csv")
top_products.to_csv("task4_top_products.csv")

# -----------------------------
# 6. Visualizations
# -----------------------------
sns.set(style="whitegrid")

# 6.1 Sales by Region
plt.figure(figsize=(6,4))
sns.barplot(x=sales_by_region.index, y=sales_by_region.values)
plt.title("Sales by Region")
plt.ylabel("Sales")
plt.xlabel("Region")
plt.tight_layout()
plt.savefig("task4_sales_by_region.png")
plt.close()

# 6.2 Profit by Region
plt.figure(figsize=(6,4))
sns.barplot(x=profit_by_region.index, y=profit_by_region.values)
plt.title("Profit by Region")
plt.ylabel("Profit")
plt.xlabel("Region")
plt.tight_layout()
plt.savefig("task4_profit_by_region.png")
plt.close()

# 6.3 Sales by Category
plt.figure(figsize=(6,4))
sns.barplot(x=sales_by_category.index, y=sales_by_category.values)
plt.title("Sales by Category")
plt.ylabel("Sales")
plt.xlabel("Category")
plt.tight_layout()
plt.savefig("task4_sales_by_category.png")
plt.close()

# 6.4 Monthly Sales Trend
plt.figure(figsize=(8,4))
plt.plot(monthly_sales.index, monthly_sales.values, marker="o")
plt.xticks(rotation=45)
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("task4_monthly_sales.png")
plt.close()

# 6.5 Sales vs Profit (Scatter)
plt.figure(figsize=(6,4))
sns.scatterplot(x=df["Sales"], y=df["Profit"], alpha=0.5)
plt.title("Sales vs Profit")
plt.xlabel("Sales")
plt.ylabel("Profit")
plt.tight_layout()
plt.savefig("task4_sales_vs_profit.png")
plt.close()

# -----------------------------
# 7. Simple Programmatic Insights
# -----------------------------
best_region = sales_by_region.idxmax()
worst_region = sales_by_region.idxmin()
best_category = sales_by_category.idxmax()
best_segment = sales_by_segment.idxmax()

insights = [
    f"Highest sales region: {best_region}",
    f"Lowest sales region: {worst_region}",
    f"Top category by sales: {best_category}",
    f"Top segment by sales: {best_segment}",
    f"Overall profit is {'positive' if total_profit >= 0 else 'negative'}",
]

print("\n===== INSIGHTS =====")
for i, s in enumerate(insights, 1):
    print(f"{i}. {s}")

# Save insights to file
with open("task4_insights.txt", "w") as f:
    for i, s in enumerate(insights, 1):
        f.write(f"{i}. {s}\n")

print("\nAll outputs saved (CSV, PNG, TXT).")