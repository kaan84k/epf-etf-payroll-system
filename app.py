import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- Supabase config ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Helper functions ---
def login(email, password):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return user
    except Exception:
        return None

def fetch_employees():
    res = supabase.table("employees").select("*").execute()
    return res.data if res.data else []

def add_employee(name, email, salary):
    supabase.table("employees").insert({
        "name": name,
        "email": email,
        "salary": salary
    }).execute()

def calculate_contributions(salary):
    epf_employee = round(salary * 0.08, 2)
    epf_employer = round(salary * 0.12, 2)
    etf = round(salary * 0.03, 2)
    net_salary = round(salary - epf_employee, 2)
    employer_cost = round(salary + epf_employer + etf, 2)
    return epf_employee, epf_employer, etf, net_salary, employer_cost

# --- Streamlit UI ---
st.set_page_config(page_title="EPF/ETF Payroll Admin", layout="centered")
st.title("EPF/ETF Payroll Admin Dashboard")

if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    st.subheader("Admin Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login(email, password)
        if user:
            st.session_state.user = user
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials.")
    st.stop()

st.sidebar.success("Logged in as admin")
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.experimental_rerun()

st.header("Add Employee")
with st.form("add_employee_form"):
    name = st.text_input("Name")
    emp_email = st.text_input("Employee Email")
    salary = st.number_input("Salary", min_value=0.0, step=100.0)
    submitted = st.form_submit_button("Add Employee")
    if submitted and name and emp_email and salary > 0:
        add_employee(name, emp_email, salary)
        st.success("Employee added!")

st.header("Employee List")
employees = fetch_employees()
if employees:
    df = pd.DataFrame(employees)
    df["EPF (8%)"], df["Employer EPF (12%)"], df["ETF (3%)"], df["Net Salary"], df["Employer Cost"] = zip(
        *df["salary"].apply(calculate_contributions)
    )
    st.dataframe(df[["name", "email", "salary", "EPF (8%)", "Employer EPF (12%)", "ETF (3%)", "Net Salary", "Employer Cost"]])
else:
    st.info("No employees found.")
