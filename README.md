# PyAirbyte GA4 Data Pipeline

A Python-based data pipeline that extracts data from **Google Analytics 4 (GA4)** using [PyAirbyte](https://github.com/airbytehq/pyairbyte) and loads it into a local DuckDB cache for analysis.

---

## Overview

This project uses PyAirbyte's `source-google-analytics-data-api` connector to:

- Connect to your GA4 property using OAuth2 credentials
- List all available GA4 streams (dimensions/metrics reports)
- Read stream data into pandas DataFrames for further analysis or export

---

## Project Structure

```
pyairbyte-ga4/
├── .cache/
│   └── default_cache/        # DuckDB cache directory (data files excluded from git)
├── .env.example              # Template for environment variables
├── .gitignore
├── requirements.txt
├── test_ga4.py               # Main pipeline script
└── README.md
```

---

## Prerequisites

- Python 3.9+
- A Google Analytics 4 property
- OAuth2 credentials (Client ID, Client Secret, Refresh Token, Access Token)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Abdullah-DSTS/pyairbyte-ga4.git
cd pyairbyte-ga4
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
GA4_PROPERTY_ID=YOUR_PROPERTY_ID
GA4_CLIENT_ID=YOUR_CLIENT_ID
GA4_CLIENT_SECRET=YOUR_CLIENT_SECRET
GA4_REFRESH_TOKEN=YOUR_REFRESH_TOKEN
GA4_ACCESS_TOKEN=YOUR_ACCESS_TOKEN
GA4_START_DATE=2025-01-01
GA4_END_DATE=2025-01-02
```

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GA4_PROPERTY_ID` | Your GA4 property ID (numeric, e.g. `123456789`) | Yes |
| `GA4_CLIENT_ID` | OAuth2 Client ID from Google Cloud Console | Yes |
| `GA4_CLIENT_SECRET` | OAuth2 Client Secret | Yes |
| `GA4_REFRESH_TOKEN` | OAuth2 Refresh Token | Yes |
| `GA4_ACCESS_TOKEN` | OAuth2 Access Token | Yes |
| `GA4_START_DATE` | Start date for data extraction (`YYYY-MM-DD`) | No (default: `2025-01-01`) |
| `GA4_END_DATE` | End date for data extraction (`YYYY-MM-DD`) | No (default: `2025-01-02`) |

---

## How to Get GA4 OAuth2 Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable the **Google Analytics Data API**
3. Go to **APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID**
4. Set application type to **Desktop App**
5. Download the credentials JSON
6. Use [Google OAuth Playground](https://developers.google.com/oauthplayground/) to generate `refresh_token` and `access_token`
   - Scope: `https://www.googleapis.com/auth/analytics.readonly`

---

## Usage

Run the main pipeline script:

```bash
python test_ga4.py
```

The script will:

1. Verify the connection to your GA4 property
2. Print all available streams
3. Read the `daily_active_users` stream
4. Display the first 10 rows as a DataFrame

### Sample Output

```
Checking connection...

Available streams:
  - daily_active_users
  - weekly_active_users
  - four_weekly_active_users
  - ...

Reading stream: daily_active_users

Rows: 2
   property_id  date  activeUsers  ...
```

---

## Changing the Target Stream

To extract a different stream, update `TARGET_STREAM` in `test_ga4.py`:

```python
TARGET_STREAM = "weekly_active_users"  # change to any available stream
```

---

## Notes

- The `.cache/` folder stores data locally using DuckDB. It is excluded from version control via `.gitignore` (`*.duckdb`).
- The `.env` file is excluded from version control. Never commit it.
- The CDK bug workaround in `test_ga4.py` patches `ConcurrentDeclarativeSource.configure()` to prevent user config from being dropped when injected Python components are present.

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `airbyte` | 0.47.1 | PyAirbyte core library |
| `airbyte-cdk` | 7.23.1 | Airbyte connector development kit |
| `python-dotenv` | 1.2.2 | Load environment variables from `.env` |
| `pandas` | 2.2.3 | DataFrame operations |
| `duckdb` | 1.4.3 | Local data cache |
