# YouTube Trending Recommendation Pipeline

This repository is a university project for Data Mining & Business Intelligence (3rd year). It fetches YouTube trending videos, processes them through a data pipeline, clusters them, and serves recommendations via a simple web UI.

## Features

- **Data pipeline**: raw -> staging -> cleansing -> presentation -> prediction zones, with metadata logging and quality checks.
- **Clustering & analysis**: KMeans clustering on prepared data and automatic viral cluster detection.
- **Recommendation API**: FastAPI backend serving top videos per category and cluster.
- **Frontend**: minimal HTML/JS showing category dropdown (populated from DB) and recommendation cards.
- **MySQL storage** for intermediate results.

## Running the project

1. **Start the API server** (requires Python with dependencies installed):
   ```bash
   cd C:\Users\tent9\OneDrive\Desktop\DMBI_Project
   uvicorn api_server:app --reload
   ```

2. **Serve the frontend** from `frontend` directory (avoids CORS/file restrictions):
   ```bash
   cd frontend
   python -m http.server 5500
   ```
   Then browse to http://localhost:5500/ or http://localhost:5500/index.html

3. **API endpoints**:
   - `GET /` health check
   - `GET /recommend/{category_id}` top 5 recommendations for a category (0 = all)
   - `GET /categories` list of available categories (ID + name)

## Scheduling the pipeline

You can automate rhythmic data pulls and processing using:

- **Windows Task Scheduler**:
  - Create a basic task that runs a small batch file, for example `run_pipeline.bat` containing:
    ```bat
    cd /d C:\Users\tent9\OneDrive\Desktop\DMBI_Project
    python fetch_youtube.py >> C:\Users\tent9\OneDrive\Desktop\DMBI_Project\fetch.log 2>&1
    ```
    The redirection (`>> ... 2>&1`) ensures both stdout and stderr are appended to the log.
  - Alternatively, set `Program/script` to `python` and in `Add arguments` put:
    `fetch_youtube.py >> C:\path\to\fetch.log 2>&1` but note Task Scheduler will launch Python directly, not through a shell, so using a `.bat` is safer.
  - Check the task's **History** tab and `fetch.log` to confirm it ran.

- Alternatively, embed a scheduler in Python using [`APScheduler`](https://apscheduler.readthedocs.io/).
  Example snippet:
  ```python
  from apscheduler.schedulers.blocking import BlockingScheduler
  from fetch_youtube import main

  scheduler = BlockingScheduler()
  scheduler.add_job(main, 'interval', hours=1)
  scheduler.start()
  ```

Be sure to verify the task history or log files to confirm execution.

## Suggestions for extension

1. **UI/UX improvements**
   - Clean HTML/CSS layout with a dark/light mode toggle (using a simple button).
   - Added a search box so users can filter results by video title.
   - Recommendation cards now show thumbnail images fetched from YouTube.
   - Spinner is displayed and the button is disabled while fetching results.
   - Dashboard still uses Chart.js for a category distribution bar chart.

2. **Backend enhancements**
   - Cache category list and recommendation results to reduce DB load.
   - Add endpoints for cluster visualization or statistics.
   - Implement authentication if you plan to share the API.

3. **Pipeline features**
   - Store more metadata (e.g. time fetched, data source versions).
   - Add error handling notifications (email/slack) when pipeline fails.
   - Build a small dashboard to view pipeline status and quality reports.

4. **Deployment**
   - Containerize the app (Docker) for easier distribution.
   - Use a cron job or a cloud function for scheduling.
   - Deploy frontend and backend to a simple host (GitHub Pages + Heroku/Render). 

5. **Presentation tweaks**
   - Include a project description and architecture diagram on the webpage.
   - Add a “refresh” button to re-run the recommendation without reloading the page.

6. **Data mining/B.I. extras**
   - Perform time-series analysis of trending categories.
   - Create a report of cluster characteristics (e.g. typical view counts).
   - Build a recommendation explanation (e.g. "Because you selected Music, here's what’s viral").

These improvements will make your project look more polished and demonstrate deeper understanding to your instructor.

## Testing endpoints

### Dashboard
To see simple pipeline metrics, open `/frontend/dashboard.html` via your static server (e.g. `http://localhost:5500/dashboard.html`). It calls the `/stats` API which returns row count, last run time and category breakdown.

The dashboard now uses **Bootstrap** for responsive layout, and **Chart.js** to render a bar chart of how many rows are stored for each YouTube category. You can view it on desktop or mobile without layout issues.


Use `curl` or a browser:
```bash
curl http://localhost:8000/categories
curl http://localhost:8000/recommend/10
```

## Notes

- The `/categories` endpoint dynamically reads from the database, so it always reflects your latest data.  
- If you ever accidentally delete or modify it, restore from this file – it’s defined in `api_server.py`.

Good luck with your submission! Feel free to ask if you need help implementing any of the above suggestions.