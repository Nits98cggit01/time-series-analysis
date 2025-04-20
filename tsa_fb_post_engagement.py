import os
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime
import re
from wordcloud import WordCloud


class TrafficPostAnalyzer:
    def __init__(self, traffic_pages):
        self.traffic_pages = traffic_pages
        self.post_summary = None
        self.traffic_posts = None
        self.bucket_counts = None

    def load_and_clean_data(self, filepath):
        self.post_summary = pd.read_excel(filepath)

        # Remove rows with invalid datetime formats
        valid_time_mask = self.post_summary['createdTime'].str.contains(r'^\d{4}-\d{2}-\d{2}T', na=False)
        self.post_summary = self.post_summary[valid_time_mask]

        # Convert to datetime and drop rows with NaT
        self.post_summary['createdTime'] = pd.to_datetime(self.post_summary['createdTime'], errors='coerce')
        self.post_summary.dropna(subset=['createdTime'], inplace=True)

    def filter_traffic_posts(self):
        self.traffic_posts = self.post_summary[self.post_summary['postedBy'].isin(self.traffic_pages)]

    def assign_time_buckets(self):
        def get_bucket(datetime_obj):
            return (datetime_obj.hour * 60 + datetime_obj.minute) // 15 + 1

        self.traffic_posts['timeBucket'] = self.traffic_posts['createdTime'].apply(get_bucket)

    def compute_bucket_counts(self):
        grouped = self.traffic_posts.groupby(['postedBy', 'timeBucket']).size().unstack(fill_value=0)
        self.bucket_counts = grouped.reindex(columns=range(1, 97), fill_value=0)

    def get_results(self):
        return self.traffic_pages, self.bucket_counts

# Reusable Functions
def get_bucket(dt):
    return (dt.hour * 60 + dt.minute) // 15 + 1

def generate_plot(page_list, bucket_count, plot_attributes, output_filename):
    # Ensure the output directory exists
    os.makedirs("Exercise output", exist_ok=True)

    plt.figure(figsize=(14, 6))
    for page in page_list:
        plt.plot(range(1, 97), bucket_count.loc[page], label=page)

    plt.title(plot_attributes[0])
    plt.xlabel(plot_attributes[1])
    plt.ylabel(plot_attributes[2])
    plt.legend()
    plt.grid(True)

    # Save the plot
    filepath = os.path.join("Exercise output", output_filename)
    plt.savefig(filepath)
    plt.close()  # Close the figure after saving

def save_bucket_counts(bucket_count, output_filename):
    os.makedirs("bucket_count", exist_ok=True)

    filepath = os.path.join("bucket_count", output_filename)
    bucket_count.to_excel(filepath, index=True)

def e1_trafficpages_post_engagement(filepath, plot_filename, bucketcount_filename):
    start_time = time.time()
    # print(f'The analysis started --- {start_time}')
    # print(f'Analysing the traffic post engagement -- Starts')
    traffic_pages = ["Bengaluru Traffic Police", "Kolkata Traffic Police", "Hyderabad Traffic Police"]

    # print(f'Loading the class for analyser object')
    analyzer = TrafficPostAnalyzer(traffic_pages)

    analyzer.load_and_clean_data(filepath)
    # print(f'Dataset cleaning task completed')
    analyzer.filter_traffic_posts()

    # print(f'Filtered required records')
    analyzer.assign_time_buckets()

    # print(f'Computing the bucket count')
    analyzer.compute_bucket_counts()

    pages, counts = analyzer.get_results()

    plot_attributes = [
        "Posting Behavior of Traffic Pages (Ck(p))",
        "15-minute Buckets (1 = 12:00 AM - 12:15 AM)",
        "Number of Posts"
    ]
    # print(f'Plot attributes declared -- proceeding with plotting')
    # print(f'Hold tight, this might take some time')

    generate_plot(pages, counts, plot_attributes, plot_filename)
    # print(f'The plot image is saved onto the output folder in the same directory')

    save_bucket_counts(counts, bucketcount_filename)
    # print(f'Saving the bucketcount for each post engagament analysis')

    end_time = time.time()
    time_taken = round(end_time - start_time, 2)
    # print(f'The analysis closed -- {end_time}')


    return time_taken

# New Function for E-Commerce Post Engagement
def e2_ecomm_post_engagement(post_filepath, comment_filepath, plot_filename, bucketcount_filename):
    start_time = time.time()

    # Load data
    post_summary = pd.read_excel(post_filepath)
    comments_df = pd.read_excel(comment_filepath)

    # Clean post data
    valid_time_mask = post_summary['createdTime'].str.contains(r'^\d{4}-\d{2}-\d{2}T', na=False)
    post_summary = post_summary[valid_time_mask]
    post_summary['createdTime'] = pd.to_datetime(post_summary['createdTime'], errors='coerce')
    post_summary.dropna(subset=['createdTime'], inplace=True)

    # Filter relevant pages
    ecom_pages = ["Flipkart", "Amazon India", "Snapdeal", "Myntra"]
    ecom_posts = post_summary[post_summary['postedBy'].isin(ecom_pages)]

    # Merge posts with comments
    merged_df = pd.merge(comments_df, ecom_posts[['pid', 'postedBy']], on='pid', how='inner')

    # Extract comment timestamps
    def extract_timestamps(text):
        if pd.isnull(text):
            return []
        parts = re.split(r'\?\#\+\@', text)
        timestamps = []
        for part in parts:
            matches = re.findall(r'\d{4} \d{2} \d{2}T\d{2}:\d{2}:\d{2}\+0000', part)
            for ts in matches:
                try:
                    dt = datetime.strptime(ts, '%Y %m %dT%H:%M:%S+0000')
                    timestamps.append(dt)
                except:
                    continue
        return timestamps

    merged_df['commentTimestamps'] = merged_df['commentsText'].apply(extract_timestamps)

    # Explode and bucketize
    exploded = merged_df.explode('commentTimestamps').dropna(subset=['commentTimestamps'])
    exploded['timeBucket'] = exploded['commentTimestamps'].apply(get_bucket)

    # Group and reindex
    bucket_counts = exploded.groupby(['postedBy', 'timeBucket']).size().unstack(fill_value=0)
    bucket_counts = bucket_counts.reindex(columns=range(1, 97), fill_value=0)

    # Plot attributes
    plot_attributes = [
        "User Reaction Behavior (Qk(p)) for E-Commerce Pages",
        "15-minute Buckets (1 = 12:00 AM - 12:15 AM)",
        "Number of Reactions (Comments)"
    ]

    generate_plot(ecom_pages, bucket_counts, plot_attributes, plot_filename)
    save_bucket_counts(bucket_counts, bucketcount_filename)

    end_time = time.time()
    return round(end_time - start_time, 2)

def e3_avg_likes_per_category(post_filepath, output_filename):
    start_time = time.time()

    # Load post data
    post_summary = pd.read_excel(post_filepath)

    post_summary = post_summary[post_summary['createdTime'].str.contains(r'^\d{4}-\d{2}-\d{2}T', na=False)]
    post_summary['createdTime'] = pd.to_datetime(post_summary['createdTime'], errors='coerce')
    post_summary = post_summary.dropna(subset=['createdTime'])

    # Clean likes count
    post_summary['likesCount_clean'] = (
        post_summary['likesCount']
        .astype(str)
        .str.replace(',', '', regex=False)
        .str.extract(r'(\d+\.?\d*)')  # Extract numeric portion
        .astype(float)
    )

    # Compute average likes per category
    likes_per_category = (
        post_summary.groupby('category')['likesCount_clean']
        .mean()
        .sort_values(ascending=False)
    )

    # Save result
    # os.makedirs("bucket_count", exist_ok=True)
    filepath = os.path.join(output_filename)
    likes_per_category.to_excel(filepath, sheet_name='AvgLikes')

    end_time = time.time()
    return round(end_time - start_time, 2)

def e3_wordcloud(post_filepath):
    start_time = time.time()

    # Load and clean
    post_summary = pd.read_excel(post_filepath)
    post_summary = post_summary[post_summary['createdTime'].str.contains(r'^\d{4}-\d{2}-\d{2}T', na=False)]
    post_summary['createdTime'] = pd.to_datetime(post_summary['createdTime'], errors='coerce')
    post_summary.dropna(subset=['createdTime'], inplace=True)
    post_summary.dropna(subset=['message'], inplace=True)

    # Output directory
    output_dir = 'wordclouds_by_organization_1'
    os.makedirs(output_dir, exist_ok=True)

    # Group and generate word clouds
    for org, group in post_summary.groupby('postedBy'):
        text = ' '.join(group['message'].dropna().astype(str))

        if text.strip():
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                colormap='viridis'
            ).generate(text)

            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout()

            filename = f"{org.strip().replace(' ', '_').replace('/', '_')}.png"
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, format='png')
            plt.close()
            print(f'Plot saved with filename {filename}')

    end_time = time.time()
    return round(end_time - start_time, 2)

# Example usage
if __name__ == "__main__":
    time1 = e1_trafficpages_post_engagement(
        filepath="Post Summary.xlsx",
        plot_filename="exercise1_traffic_posting_behavior.png",
        bucketcount_filename="traffic_posting_bucketcount.xlsx"
    )
    print(f"Traffic engagement processing time: {time1} seconds")

    time2 = e2_ecomm_post_engagement(
        post_filepath="Post Summary.xlsx",
        comment_filepath="Comments.xlsx",
        plot_filename="exercise2_ecomm_reaction_behavior.png",
        bucketcount_filename="ecomm_posting_bucketcount.xlsx"
    )
    print(f"E-commerce engagement processing time: {time2} seconds")

    time3 = e3_avg_likes_per_category(
        post_filepath="Post Summary.xlsx",
        output_filename="average_likes_per_category.xlsx"
    )
    print(f"Average likes per category processing time: {time3} seconds")

    time4 = e3_wordcloud("Post Summary.xlsx")
    print(f"Wordclouds generated in {time4} seconds")
