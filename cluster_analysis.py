import pandas as pd

def analyze_clusters(input_path):

    df = pd.read_csv(input_path)

    summary = df.groupby("cluster")[["views", "likes"]].mean()

    print("\nCluster Summary:")
    print(summary)

    return summary
