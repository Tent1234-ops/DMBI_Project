import pandas as pd
from datetime import datetime

def assess_quality(file_path, zone_name):

    df = pd.read_csv(file_path)

    total_rows = df.shape[0]

    # 1. Missing Value %
    missing_percent = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100

    # 2. Duplicate %
    duplicate_percent = (df.duplicated().sum() / total_rows) * 100

    # 3. Validity Check (views & likes ต้องเป็นตัวเลข)
    validity_issues = 0
    if not pd.api.types.is_numeric_dtype(df["views"]):
        validity_issues += 1
    if not pd.api.types.is_numeric_dtype(df["likes"]):
        validity_issues += 1

    # 4. Negative Values Check
    negative_views = (pd.to_numeric(df["views"], errors="coerce") < 0).sum()
    negative_likes = (pd.to_numeric(df["likes"], errors="coerce") < 0).sum()

    report = {
        "zone": zone_name,
        "rows": total_rows,
        "missing_percent": round(missing_percent, 2),
        "duplicate_percent": round(duplicate_percent, 2),
        "validity_issues": validity_issues,
        "negative_views": int(negative_views),
        "negative_likes": int(negative_likes),
        "assessment_time": datetime.now()
    }

    report_df = pd.DataFrame([report])
    report_df.to_csv("quality_report_before.csv", index=False)

    print("Data Quality Assessment (Before Cleansing) Complete")
