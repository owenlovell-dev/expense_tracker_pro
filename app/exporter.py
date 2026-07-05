from pathlib import Path
import csv
from datetime import datetime

from app.database import (
    get_expenses,
    get_income_entries,
    get_budgets,
)


BASE_DIR = Path(__file__).resolve().parent.parent
EXPORT_DIR = BASE_DIR / "exports"


def write_csv(filename, headers, rows):
    EXPORT_DIR.mkdir(exist_ok=True)

    file_path = EXPORT_DIR / filename

    with file_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        writer.writerows(rows)

    return file_path


def export_all_data_to_csv():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    exported_files = []

    expenses_file = write_csv(
        filename=f"expenses_{timestamp}.csv",
        headers=["id", "amount", "category", "description", "created_at"],
        rows=get_expenses(),
    )
    exported_files.append(("Expenses", expenses_file))

    income_file = write_csv(
        filename=f"income_{timestamp}.csv",
        headers=["id", "amount", "source", "description", "created_at"],
        rows=get_income_entries(),
    )
    exported_files.append(("Income", income_file))

    budgets_file = write_csv(
        filename=f"budgets_{timestamp}.csv",
        headers=["category", "monthly_limit", "updated_at"],
        rows=get_budgets(),
    )
    exported_files.append(("Budgets", budgets_file))

    return exported_files
