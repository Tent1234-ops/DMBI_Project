import pandas as pd

def recommend_content(input_path, user_category):

    df = pd.read_csv(input_path)

    # แปลงให้ type ตรงกัน
    df["category"] = df["category"].astype(str)

    # ==============================
    # 🎯 Category Mapping (YouTube)
    # ==============================
    category_map = {
        "1": "Film & Animation",
        "2": "Autos & Vehicles",
        "10": "Music",
        "15": "Pets & Animals",
        "17": "Sports",
        "19": "Travel & Events",
        "20": "Gaming",
        "22": "People & Blogs",
        "23": "Comedy",
        "24": "Entertainment",
        "25": "News & Politics",
        "26": "Howto & Style",
        "27": "Education",
        "28": "Science & Technology"
    }

    print("\nAvailable Categories:")
    for cat in df["category"].unique():
        print(f"{cat} - {category_map.get(cat, 'Unknown')}")

    print("\nAvailable Clusters:", df["cluster"].unique())

    # ตรวจสอบ category ว่ามีไหม
    if str(user_category) not in df["category"].unique():
        print("❌ Category not found in dataset")
        return pd.DataFrame()

    print(f"\nUser Selected Category: {user_category} - {category_map.get(str(user_category), 'Unknown')}")

    # เลือก category ที่ user สนใจ
    filtered = df[df["category"] == str(user_category)]

    # หา cluster ที่ avg views สูงสุด
    cluster_avg = df.groupby("cluster")["views"].mean()
    viral_cluster = cluster_avg.idxmax()
    
    print(f"\n Viral Cluster (Highest Avg Views): {viral_cluster}")

    # กรองเฉพาะ viral cluster
    filtered_cluster = filtered[filtered["cluster"] == viral_cluster]

    # ถ้าไม่มีข้อมูลใน cluster นั้น → fallback
    if filtered_cluster.empty:
        print(" No data in selected cluster, fallback to top category videos")
        filtered_cluster = filtered

    # เรียงตาม views
    filtered_cluster = filtered_cluster.sort_values(by="views", ascending=False)

    print("\n Recommended Videos:")
    print(filtered_cluster[["title", "views", "likes"]].head(5))

    return filtered_cluster.head(5)
