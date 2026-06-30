# 💼 Job Market Tracker & Analytics Pipeline

A web application and automated data pipeline designed to collect, store, and visualize specialized job postings in real time. 

The project uses a hybrid architecture: a local automation script handles data collection to avoid standard cloud server blocks, saves the data to a hosted PostgreSQL database, and a live Django application serves the data to an interactive dashboard.

## 🔗 Live Project Links
* **Interactive Dashboard:** [https://tech-job-market-tracker.onrender.com/dashboard/](https://tech-job-market-tracker.onrender.com/dashboard/)
* **Live REST API Core:** [https://tech-job-market-tracker.onrender.com/api/v1/](https://tech-job-market-tracker.onrender.com/api/v1/)

---

## 🎯 Project Purpose (Why I Built This)
I built this project to solve a practical problem I faced while looking for remote work: manually scrolling through job boards everyday is slow, repetitive, and makes it hard to see overall market trends. I wanted to create an automated system that handles the data collection for me, stores it securely, and visualizes the results on a clean dashboard so I can spot tech job trends at a glance.

---

## ✨ Core Features

* **Automated Data Ingestion:** Uses Selenium to navigate job boards, extract raw listing details, and parse them cleanly.
* **Duplicate Prevention:** Checks incoming data against existing database records before saving to prevent duplicate entries.
* **REST API Endpoints:** Built with Django REST Framework to expose clean, filterable JSON data endpoints.
* **Dynamic Frontend Dashboard:** Uses a Tailwind CSS interface combined with native **JavaScript Fetch API** to pull data from the API endpoints and update the dashboard UI without requiring full page reloads.

---

## 🏗️ Architecture & Technical Choices

The project is split into separate components to keep operations reliable and infrastructure costs low:

```text
[ Local Automated Script ] 
   └─ Selenium Custom Scraper (Runs on a local network to prevent cloud bot blocks)
          │
          ▼ (Secure Network Connection)
[ Hosted Database (Neon.tech) ]
   └─ PostgreSQL Relational Database (Centralized data storage)
          ▲
          │ (API Requests / Data Retrieval)
[ Web Application Server (Render) ]
   └─ Django + REST API + Tailwind Frontend Dashboard
```

---

## 🛠️ Tech Stack

* **Backend Framework:** *Django & Python*

* **API Architecture:** *Django REST Framework (DRF)*

* **Database Engine:** *PostgreSQL (Hosted via Neon.tech)*

* **Web Automation:** *Selenium Web Driver (Headless Chrome)*

* **Frontend Interface:** *HTML5, Tailwind CSS, and JavaScript (Fetch API)*

* **Production Server Environment:** *Gunicorn & WhiteNoise*

---

## 🧠 Technical Design Decisions
* **Separating the Scraper from the Web App:** Instead of putting the scraper inside the web server, I kept it as a separate script. Web servers are built to respond to user requests quickly, not to run heavy browser automation tasks. Keeping them separate ensures the website stays fast and responsive.

* **Using Vanilla JavaScript Fetch API:** Instead of overcomplicating the frontend with a massive framework like React or Vue, I used native JavaScript `fetch()` requests. This kept the code incredibly lightweight, fast, and easy to debug while still allowing the dashboard to update without full page reloads.

* **PostgreSQL over SQLite:** While SQLite is great for local testing, it doesn't handle multiple cloud connections well. Switching to PostgreSQL (via Neon.tech) allowed both my local script and my live Render app to safely read and write to the same database at the same time.

* **Environment Isolation (`django-environ`):** Sensitive credentials, such as database passwords and secret keys, are decoupled from the codebase. They reside in local hidden `.env` files during development and in secure environment variables during production.

* **Static Asset Handling (`WhiteNoise`):** Configured WhiteNoise middleware to allow the Django application to serve its own static interface files (such as the default Django Admin and REST Framework styling sheets) directly through Gunicorn, removing the need for a separate proxy server setup.

---

## ⚖️ Engineering Tradeoffs
* **The Local Automation Tradeoff:** * *The Benefit:* Running the Selenium script locally on a residential network costs $0 and avoids getting blocked by the target platform's cloud-filtering security.
  * *The Tradeoff:* The script only runs when my local computer is turned on and connected to the internet. It isn't a hands-off, 24/7 cloud solution.
* **Database Credentials Handling:** * *The Benefit:* Using `django-environ` keeps all passwords out of GitHub, meaning my repository is completely safe to share publicly.
  * *The Tradeoff:* It requires manually configuring matching environment variables on the Render dashboard, adding an extra setup step during deployment.

---

## 🔮 Future Improvements
If I had more time or a budget to expand this project, I would focus on:
1. **Cloud Migration with Proxies:** Moving the scraper script to a cloud worker (like AWS or Google Cloud) and routing the traffic through a residential proxy network so it can run 24/7 without needing my home computer.
2. **Automated Email Alerts:** Adding a background task helper (like Celery) to automatically email users a weekly summary of new job listings that match specific high-demand keywords (e.g., "React", "Django", "Data Entry").

---

## 🛡️ Ethical Considerations & Compliance
This project was built strictly for educational research, personal career development, and market analysis.
* **Data Privacy:** The pipeline exclusively aggregates public job descriptions. It does not collect, track, or store any user profiles or personally identifiable information (PII).
* **Server Respect:** The automation engine includes random, conservative delays (`time.sleep`) between actions to make sure it does not spam requests or burden the target platform's server infrastructure.
---

## ⚙️ Local Setup & Installation (Reference Guide)

> ⚠️ **Note on Code Showcase:** This repository functions primarily as a portfolio architecture showcase. To comply with the target platform's Terms of Service and protect data privacy, the active scraping URL is omitted from this public documentation. The instructions below are provided as a reference to demonstrate how the local environment and pipeline are structured.

**1. Clone the Repository & Initialize Environment**
```bash
git clone https://github.com/mas-wehttam/tech-job-market-tracker.git

cd tech-job-market-tracker

# Create and activate a Python virtual environment
python -m venv .venv

source .venv/Scripts/activate  # On Windows use: .venv\Scripts\activate
```
**2. Configure Environment Variables**

Create a file named .env in the root directory of the project and add your specific configurations:
```text
DEBUG=True
SECRET_KEY=your_local_secret_key
DATABASE_URL=postgres://your_database_connection_string
SCRAPER_TARGET_URL=https://the-target-remote-job-board.com
```
**3. Install Dependencies & Run Migrations**
```bash
pip install -r requirements.txt
python manage.py migrate
```

**4. Run Operations**

**Manual Data Collection:** Run the custom Django management command directly from your terminal:
```bash
python manage.py scrape_jobs
```
**Automated Data Collection (Windows Batch Script):** Run the automated batch script (ideal for scheduling via Windows Task Scheduler to run the pipeline on a set interval without manual input):
To start the local development server:

```bash
# Double-click the file or execute via terminal:
run_scraper.bat
```
**Start the Local Web Server:** Launch the local development server to view the dashboard and API locally:
```bash
python manage.py runserver
```

Navigate to `http://127.0.0.1:8000/dashboard/` in your browser to view the application.

---

## 🚀 Cloud Deployment Configuration

For hosting the live presentation tier on platforms like **Render** or **Railway**, use the following environment specifications:

* **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`

* **Start Command:** `gunicorn project_name.wsgi:application` *(Note: Replace `project_name` with your root Django configuration folder name)*

* **Required Environment Variables:** `DEBUG` (set to `False`), `SECRET_KEY`, `DATABASE_URL`, and `ALLOWED_HOSTS`.

---


## Thank you for taking the time to review my project!
