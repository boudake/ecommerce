from pathlib import Path

from src.bronze.copy_data import copy_data_to_landing


def test_copy_data_to_landing_copies_csv_files(tmp_path):
    source_dir = tmp_path / "data"
    landing_dir = tmp_path / "landing"
    source_dir.mkdir()

    customers = source_dir / "customers.csv"
    products = source_dir / "products.csv"
    customers.write_text("customer_id,name\n1,Alice\n", encoding="utf-8")
    products.write_text("product_id,name\n10,Book\n", encoding="utf-8")

    copied = copy_data_to_landing(source_dir, landing_dir)

    assert sorted(path.name for path in copied) == ["customers.csv", "products.csv"]
    assert (landing_dir / "customers.csv").read_text(encoding="utf-8") == "customer_id,name\n1,Alice\n"
    assert (landing_dir / "products.csv").read_text(encoding="utf-8") == "product_id,name\n10,Book\n"
