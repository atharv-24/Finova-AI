# FINOVA AI — Smart Expense Tracker

A software-only B.Tech project starter for personal expense tracking, AI-assisted categorization, monthly forecasting, unusual-spending review, budgets, insights and PDF reports.

## Important scope notes
- This is a runnable **starter/MVP**, not a finished production banking product.
- It does not connect to bank accounts and does not request bank credentials.
- Categorization currently uses a transparent keyword baseline. An optional TF-IDF + Logistic Regression training script is included.
- Forecasting uses a simple linear trend and needs at least two months of recorded expenses.
- Anomaly review uses an IQR baseline in this starter; it is not fraud detection.
- Use synthetic/sample data for demos. Protect personal financial data.

## Setup (Windows)
1. Install Python 3.10 or newer.
2. Extract the ZIP.
3. Open Command Prompt/PowerShell in the extracted `FINOVA-AI` folder.
4. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Start the app:

```bash
streamlit run app.py
```

The app opens in your browser. The SQLite database `finova.db` is created automatically.

## Run tests

```bash
pytest
```

## Optional ML classifier training
Prepare `data/raw/expense_categories.csv` with exactly these columns:

```csv
description,category
Swiggy dinner,Food
Uber ride,Travel
```

Use a sufficiently large, diverse and correctly labelled dataset. Then run:

```bash
python training/train_classifier.py
```

The training script saves a TF-IDF + Logistic Regression pipeline in `models/`. The current UI still uses the rule-based baseline; connect the saved model in `modules/categorization.py` as a next integration task.

## Team responsibility mapping
- Isha: dataset preparation, TF-IDF + Logistic Regression training and evaluation.
- Atharv: Streamlit UI, dashboard, navigation and visual design.
- Sarthak: improve forecasting and anomaly models; evaluate them with suitable metrics.
- Dnyaneshwari: database, schema, transaction CRUD and validation.
- Janvi: PDF report improvements, test plan, functional/integration tests and documentation.

Team leader is not assigned.

## Suggested next development steps
1. Add edit transaction and CSV import.
2. Integrate the trained classifier pipeline into the app.
3. Compare forecasting models using chronological validation and MAE/RMSE.
4. Replace IQR baseline with Isolation Forest after preparing features and test cases.
5. Add user accounts only if required; hash passwords and isolate user data.
6. Add stronger input validation, backup/restore and deployment configuration.
