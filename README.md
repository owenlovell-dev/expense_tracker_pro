# Expense Tracker Pro

Expense Tracker Pro is a Python command-line application for tracking personal cash flow.

The app helps users record expenses, record income, view summaries, set monthly category budgets, and export data to CSV files. It uses SQLite for local data storage and is built as a practical portfolio project focused on clean Python structure, database usage, and real-world money tracking features.

## Features

- Add expenses with amount, category, description, and timestamp
- View all expenses
- Delete expenses by ID
- Add income with amount, source, description, and timestamp
- View all income entries
- Delete income entries by ID
- View an overall financial summary
- View a current-month summary
- See spending totals by category
- Set monthly budget limits per category
- View monthly budget status
- Get warnings when a category is over budget
- Export expenses, income, and budgets to CSV files

## Tech Stack

- Python 3.11
- SQLite
- pathlib
- csv module
- Git and GitHub
- Command-line interface

## Project Structure

```text
expense_tracker_pro/
├── app/
│   ├── __init__.py
│   ├── database.py
│   └── exporter.py
├── data/
│   └── expenses.db
├── exports/
│   └── exported CSV files
├── .gitignore
├── README.md
└── main.py
```

## Local Data

The app stores data locally in a SQLite database:

```text
data/expenses.db
```

The database is ignored by Git because it contains personal/local user data.

CSV exports are saved locally in:

```text
exports/
```

Exported CSV files are also ignored by Git.

## How to Run the Project

Clone the repository:

```powershell
git clone https://github.com/owenlovell-dev/expense_tracker_pro.git
cd expense_tracker_pro
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Run the app:

```powershell
python main.py
```

## Current Menu

```text
Expense Tracker Pro
-------------------
1. Add expense
2. Add income
3. View summary
4. View all expenses
5. View all income
6. Delete expense
7. Delete income
8. Set monthly budget
9. View budgets
10. Monthly summary
11. Export data to CSV
12. Exit
```

## Example Monthly Budget Output

```text
Budget status this month:
- Food: €12.50 / €10.00 - OVER by €2.50
```

## Example Summary Output

```text
Overall Summary
---------------
Total income: €1000.00
Total spent: €250.00
Remaining balance: €750.00
```

## Roadmap

Planned future improvements:

- Edit existing expenses
- Edit existing income entries
- Delete budgets
- Monthly CSV reports
- Better input validation
- Automated tests
- Simple dashboard
- Possible web version with Flask or FastAPI

## Purpose of This Project

This project is part of my long-term path toward building practical Python, automation, and software development skills.

The goal is to create real portfolio projects that can support future freelance work, automation services, and eventually small SaaS or tool-based products.

## Author

Owen Lovell  
GitHub: https://github.com/owenlovell-dev
