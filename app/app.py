import os
import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file, abort

from .webscraper import run_osint_scraper, check_internet, get_gemini_api_key

app = Flask(__name__)

# Directory where CSVs are saved (root directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_compiled_targets():
    """Scans the directory for compiled targets and reads their metadata."""
    targets = []
    for file in os.listdir(BASE_DIR):
        if file.endswith("_osint.csv"):
            filepath = os.path.join(BASE_DIR, file)
            # Extracted ID is the filename minus the suffix
            target_id = file.replace("_osint.csv", "")
            
            try:
                # Read target details from the first data row in the CSV
                with open(filepath, mode='r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    header = next(reader, None)
                    first_row = next(reader, None)
                    
                    if first_row and len(first_row) >= 2:
                        target_name = first_row[0]
                        target_email = first_row[1]
                    else:
                        # Fallback to id-derived title if empty
                        target_name = target_id.replace("_", " ").title()
                        target_email = "Unknown"
                
                # Format last modified timestamp
                mtime = os.path.getmtime(filepath)
                last_modified = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                
                targets.append({
                    "id": target_id,
                    "name": target_name,
                    "email": target_email,
                    "last_modified": last_modified
                })
            except Exception as e:
                # Log error and skip corrupt/locked files
                app.logger.warning(f"Could not parse file {file}: {e}")
                
    # Sort by last modified descending (newest first)
    targets.sort(key=lambda x: x["last_modified"], reverse=True)
    return targets

@app.context_processor
def inject_global_vars():
    """Injects whether the system is connected to the internet and if Gemini is configured."""
    return {
        "online": check_internet(),
        "gemini_active": bool(get_gemini_api_key())
    }

@app.route("/save_api_key", methods=["POST"])
def save_api_key():
    """Saves the Gemini API Key into the .env file and sets it in memory."""
    api_key = request.form.get("gemini_api_key", "").strip()
    env_path = os.path.join(BASE_DIR, ".env")
    
    lines = []
    key_updated = False
    
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("GEMINI_API_KEY="):
                        lines.append(f"GEMINI_API_KEY={api_key}\n")
                        key_updated = True
                    else:
                        lines.append(line)
        except Exception as e:
            app.logger.error(f"Failed to read .env file: {e}")
            
    if not key_updated:
        lines.append(f"GEMINI_API_KEY={api_key}\n")
        
    try:
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        # Also update in current memory environment immediately
        os.environ["GEMINI_API_KEY"] = api_key
    except Exception as e:
        app.logger.error(f"Failed to write to .env: {e}")
        
    return redirect(url_for("index"))

@app.route("/")
def index():
    """Dashboard homepage listing all targets and stats."""
    targets = get_compiled_targets()
    return render_template("dashboard.html", targets=targets)

@app.route("/scrape", methods=["POST"])
def scrape():
    """Handles triggering the scraping process for a new target."""
    target_name = request.form.get("target_name", "").strip()
    target_email = request.form.get("target_email", "").strip()
    github_username = request.form.get("github_username", "").strip()
    
    if not target_name:
        return redirect(url_for("index"))
        
    try:
        # If github_username is empty string, pass None to fallback
        github_val = github_username if github_username else None
        email_val = target_email if target_email else None
        csv_path, _ = run_osint_scraper(target_name, email_val, github_val)
        
        # Get target_id from the resulting filename
        filename = os.path.basename(csv_path)
        target_id = filename.replace("_osint.csv", "")
        
        return redirect(url_for("profile", target_id=target_id))
    except Exception as e:
        app.logger.error(f"Scrape failed: {e}")
        return redirect(url_for("index"))

@app.route("/profile/<target_id>")
def profile(target_id):
    """Detailed profile view of a compiled target."""
    filename = f"{target_id}_osint.csv"
    filepath = os.path.join(BASE_DIR, filename)
    
    if not os.path.exists(filepath):
        abort(404)
        
    rows = []
    target_name = ""
    target_email = ""
    
    try:
        with open(filepath, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            
            for row in reader:
                if row:
                    rows.append(row)
                    if not target_name and len(row) >= 2:
                        target_name = row[0]
                        target_email = row[1]
                        
        if not target_name:
            target_name = target_id.replace("_", " ").title()
            
    except Exception as e:
        app.logger.error(f"Failed to read target {target_id}: {e}")
        abort(500)
        
    return render_template(
        "profile.html",
        target_id=target_id,
        target_name=target_name,
        target_email=target_email,
        rows=rows
    )

@app.route("/download/<target_id>")
def download(target_id):
    """Endpoint to download the target CSV."""
    filename = f"{target_id}_osint.csv"
    filepath = os.path.join(BASE_DIR, filename)
    
    if not os.path.exists(filepath):
        abort(404)
        
    return send_file(
        filepath,
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )

@app.route("/delete/<target_id>", methods=["POST"])
def delete_target(target_id):
    """Deletes the target CSV profile from the dashboard."""
    filename = f"{target_id}_osint.csv"
    filepath = os.path.join(BASE_DIR, filename)
    
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            app.logger.error(f"Failed to delete {filename}: {e}")
            
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Start app on port 5090 as per user requirements
    app.run(host="0.0.0.0", port=5090, debug=True)
