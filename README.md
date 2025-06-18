# EPF/ETF Payroll Admin Dashboard

## Setup

1. Install requirements:
   ```
   pip install -r requirements.txt
   ```

2. Copy the example secrets and environment files and fill in your values:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   cp .env.example .env
   ```
   Edit the files to include your Supabase and email credentials.

3. Run the app:
   ```
   streamlit run app.py
   ```


## Supabase Database Setup

Before running the dashboard, create a new project in Supabase and execute the
SQL script in `db/supabase_schema.sql` using the Supabase SQL editor (or `psql`).
This script creates the `employees` table required by the application.
=======


## Features

- Admin login (Supabase Auth)
- Add/view employees (name, email, salary)
- Auto-calculate EPF/ETF, net salary, employer cost
- Monthly email of payslips and employer summary via `send_monthly_reports.py`
- GitHub Actions workflow runs the summary automatically on the 1st of every month
