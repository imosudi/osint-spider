# OSINT Spider

OSINT Spider is a premium, enterprise-grade Open-Source Intelligence (OSINT) digital footprint compiler. It features a modern, glassmorphic Web Dashboard and a high-concurrency Python CLI engine to harvest, synthesize, and visualize public digital footprints. 

Equipped with Gemini AI integration, it compiles highly tailored, dynamic profile analysis records across multiple platforms, falling back gracefully to concurrency-optimized scrapers and local templates when offline or unconfigured.

---

## Features

### 💻 Web Command Center
- **Glassmorphic UI**: High-fidelity dark mode designed with responsive layouts, hover micro-animations, and styled visual cards.
- **Dynamic Scrape Forms**: Run Lookups with just a Name, or enrich searches with optional Email and GitHub usernames.
- **Interactive API Settings**: Save and persist your `GEMINI_API_KEY` to secure `.env` files directly from the browser interface.
- **Visual Status Badges**: Live indicators for connectivity status (`Online Mode` / `Offline Fallback`) and the current search engine (`Gemini AI Active` / `Local Fallback`).
- **CSV Exporters**: Download compiled target footprints as standardized CSV files directly from the profile views.

### ⚙️ Concurrency & Scraper Engines
- **Gemini AI Engine**: Generates realistic, target-specific footprint profiles and description summaries using `gemini-2.5-flash` when an API key is provided.
- **Multi-Platform Scrapers**: Built-in concurrent scraper modules running on a `ThreadPoolExecutor` to pull live data from GitHub, Medium, Steam, and TechCabal Radar in sub-2 seconds.
- **Anti-Blocking Measures**: Rotates User-Agents dynamically and implements exponential backoff retries to handle rate limits (HTTP 429).
- **Graceful Fallbacks**: Automatically falls back to offline template generators if network connectivity is lost.

---

## Directory Structure

```text
osint-spider/
├── app.py                  # Flask Web Application Server & API Gateway
├── webscraper.py           # Core OSINT Scraper Engine & CLI Entry Point
├── .env                    # Key storage (ignored from commits)
├── .gitignore              # Git ignore rules configuration
├── static/
│   ├── css/
│   │   └── style.css       # Custom Glassmorphic CSS Styling
│   └── js/
│       └── main.js         # Client-side UI animations & form handling
├── templates/
│   ├── base.html           # Main HTML page layout, loader overlay, and nav
│   ├── dashboard.html      # Landing dashboard, form controls, and target lists
│   └── profile.html        # Detailed platform cards view & export button
└── README.md               # Project documentation
```

---

## Installation & Setup

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Installation Steps
Clone the repository and enter the project folder:
```bash
git clone https://github.com/imosudi/osint-spider.git
cd osint-spider
```

Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:
```bash
pip install flask google-genai
```

### 3. Environment Configuration
Create a `.env` file in the root directory to store your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*Note: This file is listed in `.gitignore` to prevent sensitive keys from being committed to public repositories.*

---

## Usage

### 1. Launching the Web App
Run the Flask server:
```bash
python3 app.py
```
By default, the server runs on port `5090`. Open your browser and navigate to:
```text
http://localhost:5090/
```

### 2. Running the CLI Scraper
Run lookups directly in the terminal by passing command-line arguments:
```bash
python3 webscraper.py --name "Target Name" --email "target@example.com" --github "github_username"
```
If arguments are omitted, the script executes in interactive mode, prompting you for input:
```bash
python3 webscraper.py
```

---

## Data Schema & Outputs

Scrape outputs are generated in the project root directory as CSV files, named using the format: `{cleaned_target_name}_osint.csv` (e.g., `anifa_bello_osint.csv`). 

Each file contains the following column layout:
| Column | Description |
|---|---|
| `Target Name` | Name of the scanned individual |
| `Target Email` | Email address (if provided) |
| `Platform` | Identified platform name (e.g., GitHub, NEAR, Discord) |
| `Handle / Username` | Username used by the target on the platform |
| `Profile URL` | Direct link to the target's profile page |
| `Key Findings & Description` | Gathered intelligence description or AI analysis |
| `Source Reference` | Origin description for the lookup (e.g. Platform API, Gemini Search) |
