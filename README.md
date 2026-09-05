# FILMO — Talent Showcase & Filmmaker Casting Platform

A web-based platform built with Flask and Firebase (Firestore) for performers to showcase their talents and for filmmakers to discover and cast talent for projects.

---

## 🛠️ Prerequisites

Before running the project on a new machine, make sure you have:
* **Python 3.8+** installed ([Download Python](https://www.python.org/downloads/)).  
  *(Make sure to check the box: **"Add python.exe to PATH"** during installation)*
* **Git** (optional, if cloning via command line)

---

## 🚀 Setup & Run Instructions

### 1. Download the Project
Either clone via Git:
```bash
git clone <REPOSITORY_URL>
cd <PROJECT_FOLDER>
```
Or download the project as a **ZIP** from GitHub and extract it into a folder.

---

### 2. Configure Firebase Credentials (Important)

This project connects to Google Cloud Firebase (Firestore). Because Firebase credentials are confidential, the private key is not included in the repository.

1. Obtain the `serviceAccountKey.json` file:
   * **Option A:** Get the official `serviceAccountKey.json` from the project owner.
   * **Option B (Using your own Firebase project):**
     * Go to [Firebase Console](https://console.firebase.google.com/).
     * Create a project and enable **Firestore Database**.
     * Go to **Project Settings** (gear icon) > **Service accounts** tab.
     * Click **Generate new private key**.
2. Rename the downloaded file to `serviceAccountKey.json`.
3. Place `serviceAccountKey.json` directly into the root folder of this project (next to `app.py`).

*(A reference template is available in `serviceAccountKey.json.example`)*

---

### 3. Set Up Virtual Environment & Dependencies

Open a terminal (Command Prompt / PowerShell) in the project folder and run:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS / Linux:
# source venv/bin/activate

# Install required Python packages
pip install -r requirements.txt
```

---

### 4. Initialize Database (First-Time Setup)

If connecting to a clean database, run the admin seed script:

```bash
python seed_admin.py
```
*(Creates the default administrator account: `admin@filmo.com` / `admin123`)*

*(Optional)* To populate sample filmmakers and performers for testing/demo:
```bash
python seed_demo.py
```
*(Or double-click `add_demo_data.bat` on Windows)*

---

### 5. Start the Website

**On Windows:**
Simply double-click `run.bat` or run:
```bash
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5001
```

---

## 🔑 Default Accounts

* **Admin Portal:**
  * **Email:** `admin@filmo.com`
  * **Password:** `admin123`
* **Demo Accounts (if demo data seeded):**
  * Password for all demo accounts: `demo123`
