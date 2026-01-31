import kagglehub
import shutil
from pathlib import Path

def download_dataco_dataset():
    """
    Download DataCo Smart Supply Chain dataset from Kaggle
    and save it into data/raw directory.
    """

    # Download dataset
    path = kagglehub.dataset_download(
        "shashwatwork/dataco-smart-supply-chain-for-big-data-analysis"
    )

    print("Dataset downloaded to:", path)

    # Target directory
    raw_data_dir = Path("data/raw")
    raw_data_dir.mkdir(parents=True, exist_ok=True)

    # Copy all files to data/raw
    for file in Path(path).iterdir():
        if file.is_file():
            shutil.copy(file, raw_data_dir / file.name)

    print("Dataset copied to data/raw/ successfully.")


if __name__ == "__main__":
    download_dataco_dataset()
