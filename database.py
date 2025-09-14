import sqlite3

def create_table():
    conn = sqlite3.connect("employees.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            company TEXT,
            linkedin_url TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_employee(name, company, linkedin_url):
    conn = sqlite3.connect("employees.db")
    c = conn.cursor()
    c.execute("INSERT INTO employees (name, company, linkedin_url) VALUES (?, ?, ?)", 
              (name, company, linkedin_url))
    conn.commit()
    conn.close()

def fetch_employees_by_company(company):
    conn = sqlite3.connect("employees.db")
    c = conn.cursor()
    c.execute("SELECT name, linkedin_url FROM employees WHERE company LIKE ?", ('%' + company + '%',))
    rows = c.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    create_table()
