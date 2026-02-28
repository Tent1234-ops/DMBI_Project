import requests
import pandas as pd
import shutil
import os

from metadata_logger import log_metadata
from data_quality_assessment import assess_quality
from data_cleansing import cleanse_data
from data_preparation import prepare_data
from clustering import run_clustering
from cluster_analysis import analyze_clusters
import requests
import pandas as pd
import shutil
import os

from metadata_logger import log_metadata
from data_quality_assessment import assess_quality
from data_cleansing import cleanse_data
from data_preparation import prepare_data
from clustering import run_clustering
from cluster_analysis import analyze_clusters
from recommendation import recommend_content
from database_writer import save_to_mysql


def main():
    # create folders
    zones = [
        "data_pipeline/raw_zone",
        "data_pipeline/staging_zone",
        "data_pipeline/cleansing_zone",
        "data_pipeline/presentation_zone",
        "data_pipeline/prediction_zone",
    ]
    for z in zones:
        os.makedirs(z, exist_ok=True)

    # -----------------------------
    # DATA COLLECTION (RAW) with thumbnail
    # -----------------------------
    API_KEY = "AIzaSyDhOhynT56w6a-IbnCIXXIeWx3phPR4xu0"
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": "TH",
        "maxResults": 50,
        "key": API_KEY,
    }

    resp = requests.get(url, params=params)
    data = resp.json()
    if "items" not in data:
        print("API Error:", data)
        return

    videos = []
    for item in data["items"]:
        thumb = None
        try:
            thumb = item["snippet"].get("thumbnails", {}).get("high", {}).get("url")
        except Exception:
            thumb = None

        videos.append({
            "title": item["snippet"].get("title"),
            "category": item["snippet"].get("categoryId"),
            "views": item.get("statistics", {}).get("viewCount"),
            "likes": item.get("statistics", {}).get("likeCount"),
            "publish_time": item["snippet"].get("publishedAt"),
            "thumbnail": thumb,
        })

    raw_path = "data_pipeline/raw_zone/raw_trending.csv"
    pd.DataFrame(videos).to_csv(raw_path, index=False)
    log_metadata(raw_path, "Raw Zone", "Success")
    assess_quality(raw_path, "Raw Zone")
    save_to_mysql(raw_path, "raw_zone_data")
    print("Raw Zone Complete")

    # -----------------------------
    # STAGING
    # -----------------------------
    staging_path = "data_pipeline/staging_zone/staging_trending.csv"
    shutil.copy(raw_path, staging_path)
    log_metadata(staging_path, "Staging Zone", "Success")
    assess_quality(staging_path, "Staging Zone")
    save_to_mysql(staging_path, "staging_zone_data")
    print("Staging Zone Complete")

    # -----------------------------
    # CLEANSING
    # -----------------------------
    clean_path = "data_pipeline/cleansing_zone/clean_trending.csv"
    cleanse_data(staging_path, clean_path)
    log_metadata(clean_path, "Cleansing Zone", "Success")
    assess_quality(clean_path, "After Cleansing")
    save_to_mysql(clean_path, "cleansing_zone_data")
    print("Cleansing Zone Complete")

    # -----------------------------
    # PRESENTATION
    # -----------------------------
    presentation_path = "data_pipeline/presentation_zone/presentation_trending.csv"
    shutil.copy(clean_path, presentation_path)
    log_metadata(presentation_path, "Presentation Zone", "Success")
    save_to_mysql(presentation_path, "presentation_zone_data")
    print("Presentation Zone Complete")

    # -----------------------------
    # PREPARATION
    # -----------------------------
    prepared_path = "data_pipeline/prediction_zone/prepared_trending.csv"
    prepare_data(presentation_path, prepared_path)
    print("Data Preparation Complete")

    # -----------------------------
    # CLUSTERING
    # -----------------------------
    clustered_path = "data_pipeline/prediction_zone/clustered_trending.csv"
    run_clustering(prepared_path, clustered_path)
    log_metadata(clustered_path, "Prediction Zone - Clustered", "Success")
    save_to_mysql(clustered_path, "prediction_zone_data")
    analyze_clusters(clustered_path)
    print("Prediction Zone Complete")

    # -----------------------------
    # RECOMMEND
    # -----------------------------
    recommend_content(clustered_path, user_category=10)
    print("Pipeline Finished Successfully")

    from datetime import datetime
    with open('pipeline.log', 'a') as f:
        f.write(f"{datetime.now()}: pipeline finished\n")


if __name__ == '__main__':
    main()
