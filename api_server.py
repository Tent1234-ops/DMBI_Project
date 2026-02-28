from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import mysql.connector
import pandas as pd

app = FastAPI()

# ----------------------------
# CORS (แก้ปัญหา frontend)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# MySQL Connection
# ----------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="youtube_pipeline"
    )

# ----------------------------
# Home
# ----------------------------
@app.get("/")
def home():
    return {"message": "YouTube Recommendation API Running"}

# ----------------------------
# Recommendation API
# ----------------------------
@app.get("/recommend/{category_id}")
def recommend(category_id: int):

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM prediction_zone_data", conn)
    conn.close()

    # ✅ ถ้าไม่มีข้อมูลเลย
    if df.empty:
        return {"error": "No data in prediction_zone_data table"}

    # ----------------------------
    # FIX DATATYPE (สำคัญมาก)
    # ----------------------------
    df["category"] = df["category"].astype(str)
    df["views"] = pd.to_numeric(df["views"], errors="coerce")
    df["cluster"] = pd.to_numeric(df["cluster"], errors="coerce")

    # ----------------------------
    # หา cluster ที่วิวเฉลี่ยสูงสุด
    # ----------------------------
    viral_cluster = df.groupby("cluster")["views"].mean().idxmax()

    # ----------------------------
    # กรองตาม category + cluster
    # ----------------------------
    filtered = df[
        (df["category"] == str(category_id)) &
        (df["cluster"] == viral_cluster)
    ]

    # ----------------------------
    # 🔥 FALLBACK ถ้าไม่มีข้อมูลใน cluster นั้น
    # ----------------------------
    if filtered.empty:
        filtered = df[df["category"] == str(category_id)]

    # ----------------------------
    # 🔥 ถ้ายังไม่มีอีก → เอา top ทั้งหมด
    # ----------------------------
    if filtered.empty:
        filtered = df

    # ----------------------------
    # เรียงวิวมากไปน้อย
    # ----------------------------
    result = filtered.sort_values("views", ascending=False).head(5)

    return result.to_dict(orient="records")


# ----------------------------
# Category list API
# ----------------------------
@app.get("/categories")
def list_categories():
    """Return all unique category IDs present in prediction_zone_data with optional names."""
    conn = get_connection()
    df = pd.read_sql("SELECT DISTINCT category FROM prediction_zone_data", conn)
    conn.close()

    if df.empty:
        return []

    cat_names = {
        1: "Film & Animation",
        10: "Music",
        15: "Pets & Animals",
        17: "Sports",
        18: "Short Movies",
        19: "Travel & Events",
        20: "Gaming",
        21: "Videoblogging",
        22: "People & Blogs",
        23: "Comedy",
        24: "Entertainment",
        25: "News & Politics",
        26: "Howto & Style",
        27: "Education",
        28: "Science & Technology",
        29: "Nonprofits & Activism",
        30: "Movies",
        31: "Anime/Animation",
        32: "Action/Adventure",
        33: "Classics",
        34: "Comedy",
        35: "Documentary",
        36: "Drama",
        37: "Family",
        38: "Foreign",
        39: "Horror",
        40: "Sci-Fi/Fantasy",
        41: "Thriller",
        42: "Shorts",
        43: "Shows",
        44: "Trailers",
    }

    cats = sorted(df["category"].astype(int).tolist())
    output = []
    for c in cats:
        output.append({"id": c, "name": cat_names.get(c, str(c))})
    return output


# ----------------------------
# Stats / dashboard data
# ----------------------------
@app.get("/stats")
def stats():
    """Return basic statistics for dashboard (row count + last pipeline timestamp)."""
    conn = get_connection()
    try:
        row_count = pd.read_sql("SELECT COUNT(*) AS c FROM prediction_zone_data", conn).iloc[0,0]
        cat_df = pd.read_sql("SELECT category, COUNT(*) AS cnt FROM prediction_zone_data GROUP BY category", conn)
    finally:
        conn.close()

    # read last timestamp from metadata file if present
    latest = None
    try:
        meta = pd.read_csv("pipeline_metadata.csv")
        if not meta.empty:
            latest = meta["timestamp"].max()
    except Exception:
        latest = None

    # map category ids to names (reuse cat_names from above or define minimal)
    cat_names = {
        1: "Film & Animation",
        10: "Music",
        15: "Pets & Animals",
        17: "Sports",
        18: "Short Movies",
        19: "Travel & Events",
        20: "Gaming",
        21: "Videoblogging",
        22: "People & Blogs",
        23: "Comedy",
        24: "Entertainment",
        25: "News & Politics",
        26: "Howto & Style",
        27: "Education",
        28: "Science & Technology",
        29: "Nonprofits & Activism",
        30: "Movies",
        31: "Anime/Animation",
        32: "Action/Adventure",
        33: "Classics",
        34: "Comedy",
        35: "Documentary",
        36: "Drama",
        37: "Family",
        38: "Foreign",
        39: "Horror",
        40: "Sci-Fi/Fantasy",
        41: "Thriller",
        42: "Shorts",
        43: "Shows",
        44: "Trailers",
    }
    categories = []
    for _, row in cat_df.iterrows():
        cid = int(row['category'])
        categories.append({
            'id': cid,
            'name': cat_names.get(cid, str(cid)),
            'count': int(row['cnt'])
        })

    return {"prediction_rows": int(row_count), "last_run": latest, "category_stats": categories}
