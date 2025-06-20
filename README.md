# Horse Description App

A simple web app to add/remove horses (name + description) and fetch the list via API.

## How to Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the app:
   ```
   python app.py
   ```
3. Open [http://localhost:5000](http://localhost:5000) in your browser.

## API
- `GET /api/horses` — List all horses (JSON)
- `POST /api/horses` — Add a horse (`{"name": ..., "description": ...}`)
- `DELETE /api/horses/<name>` — Remove a horse by name

## Deployment
- The app is self-contained and can be hosted on any platform that supports Python/Flask (e.g., Heroku, PythonAnywhere, etc). 