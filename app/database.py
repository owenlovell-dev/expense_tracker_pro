from pathlib import Path
import sqlite3
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "expenses.db"


def get_connection():
    DATA_DIR.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                source TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS budgets (
                category TEXT PRIMARY KEY,
                monthly_limit REAL NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        conn.commit()


def add_expense(amount, category, description):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO expenses (amount, category, description, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (amount, category, description, created_at),
        )
        conn.commit()


def add_income(amount, source, description):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO income (amount, source, description, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (amount, source, description, created_at),
        )
        conn.commit()


def set_budget(category, monthly_limit):
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO budgets (category, monthly_limit, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(category) DO UPDATE SET
                monthly_limit = excluded.monthly_limit,
                updated_at = excluded.updated_at
            """,
            (category, monthly_limit, updated_at),
        )
        conn.commit()


def delete_expense(expense_id):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,),
        )
        conn.commit()

        return cursor.rowcount > 0


def delete_income(income_id):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM income WHERE id = ?",
            (income_id,),
        )
        conn.commit()

        return cursor.rowcount > 0


def get_expenses():
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT id, amount, category, description, created_at
            FROM expenses
            ORDER BY created_at DESC
            """
        )
        return cursor.fetchall()


def get_income_entries():
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT id, amount, source, description, created_at
            FROM income
            ORDER BY created_at DESC
            """
        )
        return cursor.fetchall()


def get_budgets():
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT category, monthly_limit, updated_at
            FROM budgets
            ORDER BY category
            """
        )
        return cursor.fetchall()


def get_total_spent():
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            """
        )
        return cursor.fetchone()[0]


def get_total_income():
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM income
            """
        )
        return cursor.fetchone()[0]


def get_category_totals():
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT category, SUM(amount) AS total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
            """
        )
        return cursor.fetchall()


def get_current_month_total():
    current_month = datetime.now().strftime("%Y-%m")

    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE created_at LIKE ?
            """,
            (f"{current_month}%",),
        )
        return cursor.fetchone()[0]


def get_current_month_income():
    current_month = datetime.now().strftime("%Y-%m")

    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM income
            WHERE created_at LIKE ?
            """,
            (f"{current_month}%",),
        )
        return cursor.fetchone()[0]


def get_current_month_category_totals():
    current_month = datetime.now().strftime("%Y-%m")

    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT category, SUM(amount) AS total
            FROM expenses
            WHERE created_at LIKE ?
            GROUP BY category
            ORDER BY total DESC
            """,
            (f"{current_month}%",),
        )
        return cursor.fetchall()


def get_budget_status_for_current_month():
    current_month = datetime.now().strftime("%Y-%m")

    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT
                budgets.category,
                budgets.monthly_limit,
                COALESCE(SUM(expenses.amount), 0) AS spent
            FROM budgets
            LEFT JOIN expenses
                ON expenses.category = budgets.category
                AND expenses.created_at LIKE ?
            GROUP BY budgets.category, budgets.monthly_limit
            ORDER BY budgets.category
            """,
            (f"{current_month}%",),
        )
        return cursor.fetchall()
