# OSINT Spider

A premium, Flask-based OSINT web dashboard and dynamic command-line tool to scan, compile, and visualize digital footprints across public networks.

---

## Suggested GitHub Repository Details

- **Repository Name**: `osint-spider` (alternative: `digital-footprint-compiler`)
- **Description**: `A premium, Flask-based OSINT web dashboard and dynamic command-line tool to scan, compile, and visualize digital footprints across public networks.`
- **Topics**: `osint`, `web-scraping`, `flask`, `digital-footprint`, `cybersecurity`, `python`, `dashboard`, `intelligence-gathering`, `github-api`, `glassmorphism`

---

## Features

### 💻 OSINT Command Center (Web App)
- **Glassmorphic UI**: Beautiful dark-mode interface designed with responsive glass layouts, micro-animations, and styled visual cards.
- **Dynamic Scrape Forms**: Scan custom targets by inputting a Name, Email address, and optional GitHub username.
- **Support for 7 Platforms**: Generates visual footprint records for GitHub, Medium, NEAR Protocol, IoTeX Ecosystem, Discord, TechCabal Radar, and Steam.
- **CSV Download & Management**: Allows downloading compiled target footprints as standardized CSV files directly from the dashboard and deleting completed scans.
- **Online & Offline Status Indicators**: Detects internet connectivity to query live APIs (such as the GitHub User API) or fallback to pre-compiled offline research data.

### ⚙️ Intelligence Scraper (CLI Tool)
- **Dynamic Parameters**: No longer hardcoded. Query targets by passing arguments via the terminal.
- **Interactive Prompts**: Prompts the user step-by-step for the target's credentials if command-line arguments are omitted.
- **Zero-Dependency Core**: The command-line engine uses only standard Python libraries (`urllib` and `csv`), maintaining maximum portability.

---

## Folder Structure

```
anifa_webscrap/
├── app.py                  # Flask Application Server
├── webscraper.py           # OSINT Core Scraper Engine & CLI Tool
├── static/
│   ├── css/
│   │   └── style.css       # Premium Dark-Theme Glassmorphic CSS
│   └── js/
│       └── main.js         # Frontend animations & overlay controls
├── templates/
│   ├── base.html           # Main layout shell, navbar, and loader overlay
│   ├── dashboard.html      # Stats counters, scrape form, target lists
│   └── profile.html        # Platform footprint cards and actions
└── README.md               # Repository documentation
```

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/osint-spider.git
   cd osint-spider
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Flask**:
   ```bash
   pip install flask
   ```

---

## Usage Instructions

### 1. Launch the Web Application
Start the Flask local development server on port **`5090`**:
```bash
python3 app.py
```
Open your browser and navigate to:
```text
http://localhost:5090/
```

### 2. Run the CLI Scraper Tool
You can run the intelligence compiler directly in the command line using arguments:
```bash
python3 webscraper.py --name "Target Name" --email "target@example.com" --github "github_username"
```
If you omit the arguments, the tool will enter an interactive mode, prompting you to enter the credentials:
```bash
python3 webscraper.py
```

### Outputs
The generated reports are exported as CSV files in the project root directory, named after the target:
- File naming format: `{lowercase_target_name}_osint.csv` (e.g., `mosudi_isiaka_osint.csv`).
- Output schema: `Target Name`, `Target Email`, `Platform`, `Handle / Username`, `Profile URL`, `Key Findings & Description`, `Source Reference`.
