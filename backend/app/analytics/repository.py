from pathlib import Path

import pandas as pd


class CSVPerformanceRepository:
    REQUIRED_COLUMNS = {"date", "category", "views", "registrations", "ad_spend"}

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def load(self) -> pd.DataFrame:
        df = pd.read_csv(self._file_path, parse_dates=["date"])

        missing = self.REQUIRED_COLUMNS - set(df.columns)

        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        if df.empty:
            raise ValueError("The dataset is empty.")

        numeric = ["views", "registrations", "ad_spend"]

        for column in numeric:
            df[column] = pd.to_numeric(df[column], errors="raise")

        if df[list(self.REQUIRED_COLUMNS)].isna().any().any():
            raise ValueError("Dataset contains missing values.")

        if not (df[numeric] >= 0).all().all():
            raise ValueError("Metrics cannot be negative.")

        if not (df["registrations"] <= df["views"]).all():
            raise ValueError("Registrations cannot exceed views.")

        if (df["category"].str.strip().eq("").any() or df["category"].str.strip().ne(df["category"]).any()):
            raise ValueError("Invalid category name.")

        if df.duplicated(["date", "category"]).any():
            raise ValueError("Duplicate date/category records.")

        return df