"""db.py - database layer for the Salary Analyzer."""
import sqlite3
from contextlib import closing

DB_PATH = "salaries.db"

# (name, department, role, annual salary in INR)
SAMPLE_DATA = [
    ("Aarav Sharma", "Engineering", "Software Engineer", 900000),
    ("Meera Iyer", "Engineering", "Senior Engineer", 1500000),
    ("Rohan Gupta", "Engineering", "Intern", 240000),
    ("Sneha Verma", "HR", "HR Executive", 480000),
    ("Kabir Singh", "HR", "HR Manager", 900000),
    ("Ananya Das", "Sales", "Sales Associate", 420000),
    ("Vikram Rao", "Sales", "Sales Manager", 1100000),
    ("Pooja Nair", "Finance", "Accountant", 600000),
    ("Imran Khan", "Finance", "Finance Manager", 1300000),
    ("Diya Mehta", "Marketing", "Content Strategist", 550000),
]


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(seed=True):
    """Create the employees table if missing; insert sample data if empty."""
    with closing(_connect()) as conn, conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS employees (
                   id         INTEGER PRIMARY KEY AUTOINCREMENT,
                   name       TEXT NOT NULL,
                   department TEXT NOT NULL,
                   role       TEXT NOT NULL,
                   salary     REAL NOT NULL CHECK (salary >= 0)
               )"""
        )
        count = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
        if seed and count == 0:
            conn.executemany(
                "INSERT INTO employees (name, department, role, salary) "
                "VALUES (?, ?, ?, ?)",
                SAMPLE_DATA,
            )


def add_employee(name, department, role, salary):
    """Insert one employee. Returns the new id."""

    if not str(name).strip():
        raise ValueError("Name cannot be empty.")

    if not str(department).strip():
        raise ValueError("Department cannot be empty.")

    if not str(role).strip():
        raise ValueError("Role cannot be empty.")

    try:
        salary = float(salary)
    except (TypeError, ValueError):
        raise ValueError("Salary must be a number.")

    if salary < 0:
        raise ValueError("Salary cannot be negative.")

    with closing(_connect()) as conn, conn:
        cur = conn.execute(
            "INSERT INTO employees (name, department, role, salary) "
            "VALUES (?, ?, ?, ?)",
            (name.strip(), department.strip(), role.strip(), salary),
        )
        return cur.lastrowid


def get_employees(department=None):
    """Return a list of dicts: id, name, department, role, salary."""
    query = "SELECT id, name, department, role, salary FROM employees"
    params = ()
    if department:
        query += " WHERE department = ?"
        params = (department,)
    query += " ORDER BY id"
    with closing(_connect()) as conn:
        return [dict(row) for row in conn.execute(query, params).fetchall()]


def get_salaries(department=None):
    """Return a plain list of salary numbers (for numpy)."""
    return [e["salary"] for e in get_employees(department)]


def delete_employee(employee_id):
   def update_employee(employee_id, name, department, role, salary):
    """Update an employee. Returns True if updated."""

    if not str(name).strip():
        raise ValueError("Name cannot be empty.")

    if not str(department).strip():
        raise ValueError("Department cannot be empty.")

    if not str(role).strip():
        raise ValueError("Role cannot be empty.")

    try:
        salary = float(salary)
    except (TypeError, ValueError):
        raise ValueError("Salary must be a number.")

    if salary < 0:
        raise ValueError("Salary cannot be negative.")

    with closing(_connect()) as conn, conn:
        cur = conn.execute(
            """UPDATE employees
               SET name = ?, department = ?, role = ?, salary = ?
               WHERE id = ?""",
            (
                name.strip(),
                department.strip(),
                role.strip(),
                salary,
                employee_id,
            ),
        )

        return cur.rowcount > 0


def list_departments():
    """Return a sorted list of distinct department names."""
    with closing(_connect()) as conn:
        rows = conn.execute(
            "SELECT DISTINCT department FROM employees ORDER BY department"
        ).fetchall()
        return [r["department"] for r in rows]


if __name__ == "__main__":
    init_db()
    print(get_employees())
    print(list_departments())
    print(get_salaries("Engineering"))
