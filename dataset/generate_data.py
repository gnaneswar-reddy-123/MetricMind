import random
from datetime import datetime, timedelta
import csv
from pathlib import Path

random.seed(42)

OUTPUT_FILE = Path(__file__).parent / "sales_data.csv"
TOTAL_ROWS = 5000

regions = {
    "Europe": ["Germany", "France", "United Kingdom", "Italy", "Spain"],
    "North America": ["United States", "Canada", "Mexico"],
    "Asia Pacific": ["India", "Japan", "Australia", "Singapore"],
    "South America": ["Brazil", "Argentina", "Chile"]
}

products = {
    "Technology": [
        "Laptop Pro",
        "Smartphone X",
        "Business Tablet",
        "Cloud Server"
    ],
    "Office Supplies": [
        "Premium Paper",
        "Office Chair",
        "Printer",
        "Desk Organizer"
    ],
    "Furniture": [
        "Executive Desk",
        "Conference Table",
        "Ergonomic Chair",
        "Storage Cabinet"
    ]
}

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)

days_range = (end_date - start_date).days

rows = []

for _ in range(TOTAL_ROWS):
    random_days = random.randint(0, days_range)
    order_date = start_date + timedelta(days=random_days)

    region = random.choice(list(regions.keys()))
    country = random.choice(regions[region])

    product_category = random.choice(list(products.keys()))
    product_name = random.choice(products[product_category])

    revenue = round(random.uniform(500, 10000), 2)

    material_cost = revenue * random.uniform(0.30, 0.45)
    shipping_cost = revenue * random.uniform(0.03, 0.08)

    # Intentionally create a margin drop in Europe during Q4 2025
    if (
        region == "Europe"
        and order_date.year == 2025
        and order_date.month in [10, 11, 12]
    ):
        material_cost = revenue * random.uniform(0.48, 0.58)
        shipping_cost = revenue * random.uniform(0.10, 0.16)

    cost = material_cost + shipping_cost

    rows.append([
        order_date.strftime("%Y-%m-%d"),
        region,
        country,
        product_category,
        product_name,
        round(revenue, 2),
        round(cost, 2),
        round(shipping_cost, 2),
        round(material_cost, 2)
    ])

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "order_date",
        "region",
        "country",
        "product_category",
        "product_name",
        "revenue",
        "cost",
        "shipping_cost",
        "material_cost"
    ])

    writer.writerows(rows)

print(f"Dataset created successfully!")
print(f"Rows created: {TOTAL_ROWS}")
print(f"File: {OUTPUT_FILE}")