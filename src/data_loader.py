import pandas as pd
import numpy as np
import glob
import os

class NetworkDataLoader:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def load_and_merge_data(self) -> pd.DataFrame:
        all_files = glob.glob(self.data_dir + "/*.csv")
        dfs_list = []
        for file in all_files:
            data = pd.read_csv(file)
            dfs_list.append(data)
        return pd.concat(dfs_list, ignore_index=True)

    def clean_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = df.columns.str.strip()
        return df

    def handle_missing_and_inf(self, df: pd.DataFrame) -> pd.DataFrame:

        missing_removed = df.replace([np.inf, -np.inf], np.nan)
        final_data = missing_removed.dropna()
        return final_data

    def get_clean_data(self) -> pd.DataFrame:
        data = self.load_and_merge_data()
        clean_data = self.clean_columns(data)
        final_data = self.handle_missing_and_inf(clean_data)
        return final_data