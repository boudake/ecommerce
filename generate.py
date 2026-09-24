from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_DIR = Path("data")

NUM_CATEGORIES = 20
NUM_PRODUCTS = 500
NUM_CUSTOMERS = 2_000
NUM_ORDERS = 20_000

SEED = 42

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 9, 1)

random.seed(SEED)


# ============================================================
# HELPERS
# ============================================================

def random_date(start: datetime, end: datetime) -> datetime:
    """Generate a random datetime between two dates."""

    delta = end - start

    return start + timedelta(
        days=random.randint(0, delta.days),
        seconds=random.randint(0, 86399),
    )


def write_csv(
    filename: str,
    rows: list[dict],
    fieldnames: list[str],
) -> None:

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    path = OUTPUT_DIR / filename

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        f"Generated {filename}: "
        f"{len(rows):,} rows"
    )


# ============================================================
# 1. CATEGORIES
# ============================================================

category_names = [
    "Electronics",
    "Computers",
    "Smartphones",
    "Audio",
    "Gaming",
    "TV & Video",
    "Home",
    "Kitchen",
    "Furniture",
    "Sports",
    "Outdoor",
    "Fashion",
    "Shoes",
    "Beauty",
    "Books",
    "Toys",
    "Automotive",
    "Garden",
    "Pet",
    "Office",
]

categories = []

for category_id, category_name in enumerate(
    category_names[:NUM_CATEGORIES],
    start=1,
):

    created_at = random_date(
        datetime(2022, 1, 1),
        datetime(2024, 1, 1),
    )

    categories.append(
        {
            "category_id": category_id,
            "category_name": category_name,
            "created_at": created_at.strftime(
                "%Y-%m-%d"
            ),
        }
    )


write_csv(
    "category.csv",
    categories,
    [
        "category_id",
        "category_name",
        "created_at",
    ],
)


# ============================================================
# 2. CUSTOMERS
# ============================================================

first_names = [
    "John",
    "Sarah",
    "Michael",
    "Emma",
    "David",
    "Sophie",
    "James",
    "Olivia",
    "Daniel",
    "Lucas",
    "Thomas",
    "Anna",
    "Alex",
    "Marie",
    "Paul",
    "Laura",
    "Nicolas",
    "Claire",
]

last_names = [
    "Smith",
    "Johnson",
    "Brown",
    "Martin",
    "Williams",
    "Miller",
    "Wilson",
    "Taylor",
    "Anderson",
    "Thomas",
    "Moore",
    "Jackson",
    "White",
    "Harris",
]

countries = [
    "France",
    "Germany",
    "Spain",
    "Italy",
    "Belgium",
    "Netherlands",
    "Switzerland",
    "United Kingdom",
]

customers = []

for customer_id in range(
    1,
    NUM_CUSTOMERS + 1,
):

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    # Make the email unique
    email = (
        f"{first_name.lower()}."
        f"{last_name.lower()}."
        f"{customer_id}"
        f"@example.com"
    )

    created_at = random_date(
        START_DATE,
        datetime(2026, 6, 1),
    )

    customers.append(
        {
            "customer_id": customer_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "country": random.choice(countries),
            "created_at": created_at.strftime(
                "%Y-%m-%d"
            ),
        }
    )


write_csv(
    "customers.csv",
    customers,
    [
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "country",
        "created_at",
    ],
)


# ============================================================
# 3. PRODUCTS
# ============================================================

brands = [
    "Apple",
    "Samsung",
    "Sony",
    "Dell",
    "Lenovo",
    "Nike",
    "Adidas",
    "LG",
    "Bosch",
    "Philips",
    "Amazon",
    "Logitech",
    "HP",
    "Asus",
    "JBL",
]

products = []

for product_id in range(
    1,
    NUM_PRODUCTS + 1,
):

    category = random.choice(categories)

    brand = random.choice(brands)

    product_created_at = random_date(
        datetime(2023, 1, 1),
        datetime(2026, 6, 1),
    )

    price = round(
        random.uniform(10, 2500),
        2,
    )

    products.append(
        {
            "product_id": product_id,
            "product_name": (
                f"{brand} "
                f"{category['category_name']} "
                f"Product {product_id}"
            ),
            "category_id": category["category_id"],
            "brand": brand,
            "price": price,
            "stock_quantity": random.randint(
                0,
                500,
            ),
            "created_at": product_created_at.strftime(
                "%Y-%m-%d"
            ),
            "is_active": random.choice(
                [True, True, True, True, False]
            ),
        }
    )


write_csv(
    "products.csv",
    products,
    [
        "product_id",
        "product_name",
        "category_id",
        "brand",
        "price",
        "stock_quantity",
        "created_at",
        "is_active",
    ],
)


# ============================================================
# 4. ORDERS
# ============================================================

orders = []

order_statuses = [
    "COMPLETED",
    "COMPLETED",
    "COMPLETED",
    "SHIPPED",
    "PROCESSING",
    "CANCELLED",
    "RETURNED",
]


# ------------------------------------------------------------
# Create lookup dictionaries
# ------------------------------------------------------------

customers_by_id = {
    customer["customer_id"]: customer
    for customer in customers
}

products_by_id = {
    product["product_id"]: product
    for product in products
}


# ------------------------------------------------------------
# Generate orders
# ------------------------------------------------------------

for order_id in range(
    1,
    NUM_ORDERS + 1,
):

    # Select a customer
    customer = random.choice(customers)

    # Customer cannot order before registration
    earliest_order_date = datetime.strptime(
        customer["created_at"],
        "%Y-%m-%d",
    )

    # Select a product
    product = random.choice(products)

    # Product must already exist
    earliest_product_date = datetime.strptime(
        product["created_at"],
        "%Y-%m-%d",
    )

    # Order date must be after BOTH:
    # - customer registration
    # - product creation
    earliest_date = max(
        earliest_order_date,
        earliest_product_date,
    )

    # Skip impossible combinations
    if earliest_date >= END_DATE:
        continue

    order_date = random_date(
        earliest_date,
        END_DATE,
    )

    quantity = random.randint(1, 5)

    unit_price = product["price"]

    total_amount = round(
        quantity * unit_price,
        2,
    )

    status = random.choice(
        order_statuses
    )

    orders.append(
        {
            "order_id": order_id,
            "customer_id": customer["customer_id"],
            "product_id": product["product_id"],
            "order_date": order_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "quantity": quantity,
            "unit_price": unit_price,
            "total_amount": total_amount,
            "status": status,
        }
    )


write_csv(
    "orders.csv",
    orders,
    [
        "order_id",
        "customer_id",
        "product_id",
        "order_date",
        "quantity",
        "unit_price",
        "total_amount",
        "status",
    ],
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 60)
print("DATA GENERATION COMPLETED")
print("=" * 60)

print(
    f"Categories : {len(categories):,}"
)

print(
    f"Customers  : {len(customers):,}"
)

print(
    f"Products   : {len(products):,}"
)

print(
    f"Orders     : {len(orders):,}"
)

print()
print(f"Output directory: {OUTPUT_DIR}")

