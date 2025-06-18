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

4. For email reports the following environment variables are required:
   - `GMAIL_USER` / `GMAIL_PASSWORD`
   - `EMPLOYER_EMAIL` (address that receives the monthly summary)

## Features

- Admin login (Supabase Auth)
- Add/view employees (name, email, salary)
- Auto-calculate EPF/ETF, net salary, employer cost
- Monthly email of payslips and employer summary via `send_monthly_reports.py`
- GitHub Actions workflow runs the summary automatically on the 1st of every month
