# PhishSense

**PhishSense** is a web + CLI application that helps users detect phishing attempts in:

- URLs
- Email content (subject + body)
- QR codes

The application combines two machine learning models (one for URLs, one for email text) with heuristic rules (common phishing phrases) and provides an explainable verdict (`safe` / `suspicious`), along with confidence score and indicators used.

---

## Repository Link

- GitHub: [https://github.com/andutu0/PhishSense](https://github.com/andutu0/PhishSense)

---

## Technologies Used

### Backend & ML

- **Python 3.11**
- **Flask** – REST API + web interface
- **scikit-learn** – classification models (Logistic Regression)
- **pandas, numpy** – dataset processing
- **pyzbar, Pillow** – QR code decoding and image processing

### Frontend

- **HTML, CSS, JavaScript** (vanilla)
- **Fetch API** for calls to Flask endpoints

### Other

- **Docker** – containerized deployment
- **zbar (libzbar0)** – system dependency for QR scanning
- **Log format**: JSON Lines (`data/scans.jsonl`)

---

## Key Features

### URL Scanning
- Extracts features (length, number of dots, digits, IP usage, suspicious words, etc.)
- Passes features through ML model trained on `data/urls_dataset.csv`
- Returns verdict (`benign` / `phishing`) + confidence score

### Email Scanning
- Analyzes subject + body + sender
- Extracts all URLs from email and classifies them with the URL model
- Calculates `phishing_phrase_hits` based on `data/email_dataset.csv`
- Uses a second ML model trained on email phrases (`email_model.pkl`)
- Aggregates results (links + text + phrases) into a single verdict

### QR Code Scanning
- Decodes QR code image
- If result is a URL, sends it through the URL pipeline
- Otherwise sends it through the text (email) pipeline

### CLI Interface
- `scan-url` – analyze URL from terminal
- `scan-email` – analyze email (subject + body + sender)
- `history` – display recent scans from `data/scans.jsonl`

### Web UI
- Form for URL input
- Form for email input
- Image upload for QR codes
- Display verdict + confidence score

---

## Project Structure

```
PhishSense/
├── app/
│   ├── __init__.py              # create_app, Flask endpoint definitions
│   ├── routes.py                # API routes
│   ├── analysis/
│   │   ├── pipeline.py          # main analysis logic (URL/email/QR)
│   │   ├── url_utils.py         # URL feature extraction
│   │   ├── feature_extractor.py # feature preparation for model
│   │   ├── email_parser.py      # email text analysis + phishing phrases
│   │   └── qr_parser.py         # QR code decoding
│   ├── ml/
│   │   ├── model_loader.py      # load URL model
│   │   ├── predict.py           # predict_proba for URLs
│   │   ├── email_model_loader.py # load email model
│   │   └── email_predict.py     # predict_proba for email text
│   ├── storage/
│   │   └── json_storage.py      # log scans to data/scans.jsonl
│   └── templates/, static/      # HTML, CSS, JS for web interface
├── data/
│   ├── urls_dataset.csv         # labeled URL dataset
│   ├── email_dataset.csv        # email phrases + labels (phishing/benign)
│   └── scans.jsonl              # scan logs (generated at runtime)
├── model/
│   ├── model.joblib             # URL ML model
│   ├── vectorizer.joblib        # TfidfVectorizer for URLs
│   ├── email_model.pkl          # email text ML model
│   └── email_vectorizer.pkl     # TfidfVectorizer for email text
├── ml_offline/
│   ├── train.py                 # URL model training script
│   └── train_email.py           # email model training script
├── cli.py                       # CLI interface
├── run.py                       # Flask entrypoint (app.run)
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Installation & Usage Instructions

### 1. Local Setup (Python)

#### 1.1. Dependencies

- **Python 3.11+**
- **pip**
- **(Linux)** System dependencies for zbar, e.g., on Debian/Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y libzbar0 libzbar-dev
```

#### 1.2. Clone and Setup

```bash
git clone https://github.com/andutu0/PhishSense.git
cd PhishSense

# (Optional, recommended) Virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 1.3. Train Models

**URL Model:**

```bash
python3 ml_offline/train.py --csv data/urls_dataset.csv
```

**Email Model:**

```bash
python3 ml_offline/train_email.py --csv data/email_dataset.csv
```

After running, the `model/` directory should contain:
- `model.joblib`, `vectorizer.joblib` – URL model + vectorizer
- `email_model.pkl`, `email_vectorizer.pkl` – email model + vectorizer

#### 1.4. Start Flask Server (port 60000)

```bash
python3 run.py
```

The application starts at:
```
http://127.0.0.1:60000
```

#### 1.5. Using the Web Interface

Open in browser: **http://localhost:60000**

**URL Section:**
- Enter a URL (e.g., `http://paypal-dispute-resolution.org`)
- Click **Analyze** → displays verdict + confidence score

**Email Section:**
- Fill in Subject, Body, Sender
- Click **Analyze** → displays verdict with details about found links + scores

**QR Section:**
- Upload an image with a QR code
- If QR contains a URL, it will be analyzed like in the URL section
- Else, it will be analyzed like in the email section (text)

---

### 2. Running with Docker

#### 2.1. Build Image

From project root:

```bash
docker build -t phishsense:latest .
```

The Dockerfile:
- Installs Python dependencies
- Installs libzbar for QR scanning
- Copies source code
- Runs training scripts:
  - `python3 ml_offline/train.py --csv data/urls_dataset.csv`
  - `python3 ml_offline/train_email.py --csv data/email_dataset.csv`
- Starts application with `python3 run.py` on port 60000 (binding to 0.0.0.0)

#### 2.2. Run Container

```bash
docker run --rm -p 60000:60000 phishsense:latest
```

Then open in browser:
```
http://localhost:60000
```

---

### 3. CLI Usage

The CLI uses the same pipeline as the API and optionally logs to `data/scans.jsonl`.

#### 3.1. Scan URL

```bash
python3 cli.py scan-url http://paypal-dispute-resolution.org --log
```

#### 3.2. Scan Email

```bash
python3 cli.py scan-email \
  --subject "Urgent action required" \
  --body "Please verify your account or it will be suspended." \
  --sender "support@fake-bank.com" \
  --log
```

#### 3.3. View History

```bash
python3 cli.py history --limit 20
```

---

## Team Member Contributions

### Andrei Lungu

- Focused on designing, training and integrating the final machine learning models (URL and email).
- Curated and extended the datasets used for training, improving class balance and model behavior.
- Refined and extended the analysis pipeline, especially the ML integration and decision logic.
- Implemented and adjusted several frontend changes and fixed issues related to frontend–backend communication (API responses, JSON formats, error handling).

### Mihaela-Elena Jipa

- Implemented the initial version of the core application: basic parsers, a first (smaller) model and the initial analysis pipeline that the final solution builds upon.
- Developed the CLI interface for scanning URLs and emails from the terminal.
- Designed and implemented most of the web frontend (forms, result views, styling).
- Implemented the history / storage functionality for scans (logging to persistent storage and displaying recent results).

---

## Challenges Faced and Solutions

### 1. Datasets
**Problem:** We couldn't find some good datasets for what we needed, most of what we found were in random languages from around the world, and they contained way more parameters than what we wanted.

**Solution:** We constructed two small datasets tailored to our needs, which proved to be quite the challenge if we wanted to get somewhat accurate results.

### 2. Model Score Calibration (safe vs suspicious)
**Problem:** Certain "realistic" phishing URLs (e.g., domains imitating brands) weren't marked as suspicious due to simple features and limited data.

**Solution:** Adjusted classification threshold, enriched dataset with more varied examples, and clearly documented model limitations and improvement directions.

### 3. Backend–Frontend Integration (JSON format, API routes)
**Problem:** Initially, the JSON response structure from backend wasn't aligned with what JavaScript expected, so we ran in a ton of problems and the web site was basically unusable.

**Solution:** After testing the CLI commands, we noticed that our models were indeed calculating good scores, but there were discrepancies between our pipeline and our frontend, so we deduced that the problem might be in the .js file or in the routes. In reality, both were messed up so we modified them both and got it to work.

### 4. Docker Networking Issues
**Problem:** In the first version, Flask was started in the container on `127.0.0.1`, making the application inaccessible from the host even though the port was mapped (`-p 60000:60000`).

**Solution:** Modified `run.py` to start the application with `host="0.0.0.0"` in Docker environment, making the exposed port visible outside the container.

### 5. Integrating Two ML Models (URL + Email)
**Problem:** We started with only one model, but we soon realized that it was impractical if we wanted to analyze both emails and URLs.

**Solution:** Created two different training scripts in order to generate two models, one for each type of input.

---

## Possible Improvements

1. **Extend datasets** with public sources (PhishTank, UCI, etc.) for more robust models
2. **Additional URL features** (e.g., similarity to legitimate brand domains, homograph detection)
3. **Dedicated ML model** for complete emails (subject + body), not just isolated phrases
4. **Database persistence** (SQLite/PostgreSQL) for history and advanced analytics
5. **Real-time URL checking** against live threat intelligence feeds
6. **Browser extension** for automatic URL checking while browsing
