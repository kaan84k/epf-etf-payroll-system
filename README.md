# EPF/ETF Payroll Admin Dashboard

## Setup

1. Install requirements:
   ```
   pip install -r requirements.txt
   ```

2. Set Streamlit secrets (`.streamlit/secrets.toml`):
   ```
   [default]
   SUPABASE_URL = "your_supabase_url"
   SUPABASE_KEY = "your_supabase_service_role_key"
   ```

3. Run the app:
   ```
   streamlit run app.py
   ```

## Supabase Database Setup

Before running the dashboard, create a new project in Supabase and execute the
SQL script in `db/supabase_schema.sql` using the Supabase SQL editor (or `psql`).
This script creates the `employees` table required by the application.

## Features

- Admin login (Supabase Auth)
- Add/view employees (name, email, salary)
- Auto-calculate EPF/ETF, net salary, employer cost
