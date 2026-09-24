from pathlib import Path

from src.bronze.copy_data import copy_data_to_landing
from src.config.settings import load_config


if __name__ == "__main__":
    config = load_config()

    landing_dir = Path(config["paths"]["landing"])
    source_dir = Path("data")

    copied_files = copy_data_to_landing(source_dir, landing_dir)

    print(f"Environnement actif : {config['app']['environment']}")
    print(f"Fichiers copiés dans le landing zone : {[p.name for p in copied_files]}")
    print(f"Chemin source customers : {config['datasets']['customers']['source']}")
    print(f"Target customers : {config['datasets']['customers']['target']}")