import os

from src.config.settings import load_config


def test_load_config_reads_local_environment(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)

    config = load_config("config/application.yaml")

    assert config["app"]["environment"] == "local"
    assert config["spark"]["master"] == "local[*]"
    assert config["datasets"]["customers"]["source"] == "./data/landing/customers"
    assert config["datasets"]["products"]["target"] == "ecommerce_bronze.products"


def test_load_config_reads_databricks_environment(monkeypatch):
    monkeypatch.setenv("APP_ENV", "databricks")

    config = load_config("config/application.yaml")

    assert config["app"]["environment"] == "databricks"
    assert config["catalog"] == "ecommerce"
    assert config["datasets"]["orders"]["source"] == "/Volumes/ecommerce/raw/orders"
    assert config["datasets"]["category"]["target"] == "ecommerce.bronze.category"
