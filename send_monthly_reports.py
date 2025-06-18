import os
from supabase import create_client
import pandas as pd
import smtplib
from email.message import EmailMessage

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise SystemExit("Missing SUPABASE credentials")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_employees():
    res = supabase.table("employees").select("*").execute()
    return res.data or []

def calculate_contributions(salary):
    epf_employee = round(salary * 0.08, 2)
    epf_employer = round(salary * 0.12, 2)
    etf = round(salary * 0.03, 2)
    net_salary = round(salary - epf_employee, 2)
    employer_cost = round(salary + epf_employer + etf, 2)
    return epf_employee, epf_employer, etf, net_salary, employer_cost

def send_email(to_address: str, subject: str, body: str) -> None:
    gmail_user = os.environ.get("GMAIL_USER")
    gmail_password = os.environ.get("GMAIL_PASSWORD")
    if not gmail_user or not gmail_password:
        raise SystemExit("Missing Gmail credentials")
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = to_address
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.send_message(msg)

def main():
    employer_email = os.environ.get("EMPLOYER_EMAIL")
    employees = fetch_employees()
    if not employees:
        print("No employees found.")
        return
    df = pd.DataFrame(employees)
    df["EPF"], df["Employer EPF"], df["ETF"], df["Net"], df["Cost"] = zip(
        *df["salary"].apply(calculate_contributions)
    )
    # Send payslips to employees
    for _, row in df.iterrows():
        body = (
            f"Hello {row['name']},\n\n"
            f"Gross Salary: {row['salary']:.2f}\n"
            f"EPF (Employee 8%): {row['EPF']:.2f}\n"
            f"EPF (Employer 12%): {row['Employer EPF']:.2f}\n"
            f"ETF (3%): {row['ETF']:.2f}\n"
            f"Net Salary: {row['Net']:.2f}\n"
        )
        send_email(row["email"], "Monthly Payslip", body)
    # Prepare employer summary
    summary = df[["name", "salary", "EPF", "Employer EPF", "ETF", "Cost"]]
    total_line = pd.DataFrame(
        {
            "name": ["Total"],
            "salary": [summary["salary"].sum()],
            "EPF": [summary["EPF"].sum()],
            "Employer EPF": [summary["Employer EPF"].sum()],
            "ETF": [summary["ETF"].sum()],
            "Cost": [summary["Cost"].sum()],
        }
    )
    summary = pd.concat([summary, total_line], ignore_index=True)
    body = summary.to_string(index=False)
    if employer_email:
        send_email(employer_email, "Monthly Payroll Summary", body)

if __name__ == "__main__":
    main()
