import pandas as pd
import os
from datetime import datetime, timedelta

# Define the folder and files
folder = 'bucket_count'
files = ['ecomm_posting_bucketcount.xlsx', 'traffic_posting_bucketcount.xlsx']

# Function to generate bucket-to-time mapping
def get_bucket_time_mapping():
    bucket_map = {}
    start_time = datetime.strptime("00:00", "%H:%M")
    for i in range(96):
        start = start_time + timedelta(minutes=15 * i)
        end = start + timedelta(minutes=15)
        time_range = f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"
        bucket_map[str(i + 1)] = time_range
    return bucket_map

bucket_time_map = get_bucket_time_mapping()

# Function to analyze a single DataFrame
def analyze_bucket_counts(df, file_name):
    print(f"\nAnalysis Report for: {file_name}")
    print("-" * 50)

    # Drop any non-numeric columns except 'postedBy'
    df_clean = df.copy()
    numeric_columns = [col for col in df.columns if col != 'postedBy']
    df_clean[numeric_columns] = df_clean[numeric_columns].apply(pd.to_numeric, errors='coerce').fillna(0)

    # Total counts per category
    df_clean['Total'] = df_clean[numeric_columns].sum(axis=1)
    leading_category = df_clean.loc[df_clean['Total'].idxmax(), 'postedBy']
    print(f"🔝 Leading category (highest total count): {leading_category}")

    deficit_category = df_clean.loc[df_clean['Total'].idxmin(), 'postedBy']
    print(f"🔝 Least category (lowest total count): {deficit_category}")


    # Max, Min, and Average bucket count per category
    for _, row in df_clean.iterrows():
        category = row['postedBy']
        values = row[numeric_columns]
        max_bucket = values.idxmax()
        max_value = values[max_bucket]
        min_bucket = values.idxmin()
        min_value = values[min_bucket]
        avg_value = values.mean()

        # Count ranges
        count_0 = (values == 0).sum()
        count_1_10 = ((values >= 1) & (values <= 10)).sum()
        count_11_25 = ((values >= 11) & (values <= 25)).sum()
        count_26_50 = ((values >= 26) & (values <= 50)).sum()
        count_50plus = (values > 50).sum()

        # Timeslot listings
        zero_buckets = [bucket_time_map[str(col)] for col in values.index if values[col] == 0]
        over50_buckets = [bucket_time_map[str(col)] for col in values.index if values[col] > 50]


        print(f"\nCategory: {category}")
        print(f"  ➤ Max count in bucket {max_bucket} ({bucket_time_map[str(max_bucket)]}) = {max_value}")
        print(f"  ➤ Min count in bucket {min_bucket} ({bucket_time_map[str(min_bucket)]}) = {min_value}")
        print(f"  ➤ Average count = {avg_value:.2f}")
        print(f"  ➤ Count Ranges:")
        print(f"     - 0 counts      : {count_0}")
        print(f"     - 1 to 10 counts    : {count_1_10}")
        print(f"     - 11 to 25 counts   : {count_11_25}")
        print(f"     - 26 to 50 counts   : {count_26_50}")
        print(f"     - More than 50 counts    : {count_50plus}")
        print(f"  ➤ Time slots with 0 counts:")
        print(f"     {', '.join(zero_buckets) if zero_buckets else 'None'}")
        print(f"  ➤ Time slots with >50 counts:")
        print(f"     {', '.join(over50_buckets) if over50_buckets else 'None'}")

# Run analysis for each file
for file in files:
    path = os.path.join(folder, file)
    if os.path.exists(path):
        df = pd.read_excel(path)
        analyze_bucket_counts(df, file)
    else:
        print(f"File not found: {path}")
