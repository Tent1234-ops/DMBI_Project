import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def run_clustering(input_path, output_path):

    df = pd.read_csv(input_path)

    # ใช้เฉพาะ Feature เชิงตัวเลข
    features = df[["views", "likes"]]

    # Scale ข้อมูล
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # ใช้ K-Means
    kmeans = KMeans(n_clusters=3, random_state=42)
    df["cluster"] = kmeans.fit_predict(scaled_features)

    df.to_csv(output_path, index=False)

    print("Clustering Complete")
