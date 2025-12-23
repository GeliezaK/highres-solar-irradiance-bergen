# =====================================================================================
# This script contains function to merge the cloud cover tables as exported from 
# Google Earth Engine. 
# =====================================================================================

import pandas as pd
import os
import glob 


def merge_all_cloud_cover_tables(input_folder="data/processed/s2_cloud_cover_tables", 
                                 output_file="data/processed/s2_cloud_cover_table_small_and_large.csv"):
    """Merges all cloud cover tables in input_folder into a single .csv table with small & large ROI info."""
    files = glob.glob(os.path.join(input_folder, "*.csv"))

    dfs_small, dfs_large = [], []

    for f in files:
        df = pd.read_csv(f)

        if "small" in f:
            # Filter full ROI coverage
            df = df[df["total_pixels"] >= 1.25e7]
            df = df[df["start_time_range"] <= 60000] #1 min in millis

            # Rename columns for small ROI
            df = df.rename(columns={
                "system:time_start": "system:time_start_small",
                "start_time_range": "start_time_range_small",
                "cloud_cover": "cloud_cover_small"
            })
            df = df[["date", "system:index", "system:time_start_small", "start_time_range_small", "cloud_cover_small"]]
            dfs_small.append(df)

        elif "large" in f:
            # Filter full ROI coverage
            df = df[df["total_pixels"] >= 1.63e8]
            df = df[df["start_time_range"] <= 60000] #1 min in millis

            # Rename columns for large ROI
            df = df.rename(columns={
                "system:time_start": "system:time_start_large",
                "start_time_range": "start_time_range_large",
                "cloud_cover": "cloud_cover_large"
            })
            df = df[["date", "system:index", "system:time_start_large", "start_time_range_large", "cloud_cover_large"]]
            dfs_large.append(df)

        else:
            raise ValueError(f"Filename {f} does not contain 'small' or 'large'.")

    # Concatenate each group
    df_small = pd.concat(dfs_small, ignore_index=True)
    df_large = pd.concat(dfs_large, ignore_index=True)

    # Merge only on date
    df_merged = pd.merge(df_small, df_large, on="date", suffixes=("_small", "_large"))

    # Drop any duplicate system:index columns if both exist
    if "system:index_small" in df_merged and "system:index_large" in df_merged:
        df_merged = df_merged.drop(columns=["system:index_large"])
        df_merged = df_merged.rename(columns={"system:index_small": "system:index"})

    # Save to CSV
    df_merged.to_csv(output_file, index=False)

    print(f"Merged dataframe saved to {output_file}")
    print("\nHead of dataframe:\n", df_merged.head())
    print("\nDescription:\n", df_merged.describe(include="all"))

    return df_merged

    
if __name__ == "__main__":
    # Define your own paths here
    infolder = "data/processed/S2_cloud_cover_tables_thresh_40"
    merged_outpath = "data/processed/s2_cloud_cover_large_thresh_40.csv"
    merge_all_cloud_cover_tables(input_folder=infolder, output_file=merged_outpath)
    
