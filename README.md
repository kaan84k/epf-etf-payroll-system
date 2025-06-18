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

## Features

- Admin login (Supabase Auth)
- Add/view employees (name, email, salary)
- Auto-calculate EPF/ETF, net salary, employer cost
