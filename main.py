from app.database import (
    init_db,
    add_expense,
    add_income,
    set_budget,
    delete_expense,
    delete_income,
    get_expenses,
    get_income_entries,
    get_budgets,
    get_total_spent,
    get_total_income,
    get_category_totals,
    get_current_month_total,
    get_current_month_income,
    get_current_month_category_totals,
    get_budget_status_for_current_month,
)


def show_menu():
    print()
    print("Expense Tracker Pro")
    print("-------------------")
    print("1. Add expense")
    print("2. Add income")
    print("3. View summary")
    print("4. View all expenses")
    print("5. View all income")
    print("6. Delete expense")
    print("7. Delete income")
    print("8. Set monthly budget")
    print("9. View budgets")
    print("10. Monthly summary")
    print("11. Exit")


def add_expense_flow():
    amount_input = input("Amount: ").replace(",", ".")

    try:
        amount = float(amount_input)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    if amount <= 0:
        print("Amount must be greater than 0.")
        return

    category = input("Category: ").strip()
    description = input("Description: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    add_expense(amount, category, description)
    print("Expense added successfully.")


def add_income_flow():
    amount_input = input("Income amount: ").replace(",", ".")

    try:
        amount = float(amount_input)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    if amount <= 0:
        print("Amount must be greater than 0.")
        return

    source = input("Source: ").strip()
    description = input("Description: ").strip()

    if not source:
        print("Source cannot be empty.")
        return

    add_income(amount, source, description)
    print("Income added successfully.")


def set_budget_flow():
    category = input("Category to budget for: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    monthly_limit_input = input("Monthly budget limit: ").replace(",", ".")

    try:
        monthly_limit = float(monthly_limit_input)
    except ValueError:
        print("Invalid budget limit. Please enter a number.")
        return

    if monthly_limit <= 0:
        print("Budget limit must be greater than 0.")
        return

    set_budget(category, monthly_limit)
    print(f"Monthly budget for {category} set to €{monthly_limit:.2f}.")


def view_summary():
    total_income = get_total_income()
    total_spent = get_total_spent()
    remaining_balance = total_income - total_spent
    category_totals = get_category_totals()

    print()
    print("Overall Summary")
    print("---------------")
    print(f"Total income: €{total_income:.2f}")
    print(f"Total spent: €{total_spent:.2f}")
    print(f"Remaining balance: €{remaining_balance:.2f}")

    if not category_totals:
        print()
        print("No expenses yet.")
        return

    print()
    print("Expenses by category:")
    for category, category_total in category_totals:
        print(f"- {category}: €{category_total:.2f}")


def view_all_expenses():
    expenses = get_expenses()

    print()
    print("All Expenses")
    print("------------")

    if not expenses:
        print("No expenses yet.")
        return

    for expense_id, amount, category, description, created_at in expenses:
        print(
            f"ID: {expense_id} | "
            f"€{amount:.2f} | "
            f"{category} | "
            f"{description} | "
            f"{created_at}"
        )


def view_all_income():
    income_entries = get_income_entries()

    print()
    print("All Income")
    print("----------")

    if not income_entries:
        print("No income yet.")
        return

    for income_id, amount, source, description, created_at in income_entries:
        print(
            f"ID: {income_id} | "
            f"€{amount:.2f} | "
            f"{source} | "
            f"{description} | "
            f"{created_at}"
        )


def view_budgets():
    budgets = get_budgets()

    print()
    print("Monthly Budgets")
    print("---------------")

    if not budgets:
        print("No budgets set yet.")
        return

    for category, monthly_limit, updated_at in budgets:
        print(
            f"{category}: €{monthly_limit:.2f} "
            f"| Updated: {updated_at}"
        )


def delete_expense_flow():
    view_all_expenses()

    expense_id_input = input("Enter the ID of the expense to delete: ").strip()

    try:
        expense_id = int(expense_id_input)
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    deleted = delete_expense(expense_id)

    if deleted:
        print("Expense deleted successfully.")
    else:
        print("No expense found with that ID.")


def delete_income_flow():
    view_all_income()

    income_id_input = input("Enter the ID of the income entry to delete: ").strip()

    try:
        income_id = int(income_id_input)
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    deleted = delete_income(income_id)

    if deleted:
        print("Income entry deleted successfully.")
    else:
        print("No income entry found with that ID.")


def view_monthly_summary():
    monthly_income = get_current_month_income()
    monthly_spent = get_current_month_total()
    monthly_remaining = monthly_income - monthly_spent
    monthly_category_totals = get_current_month_category_totals()
    budget_status = get_budget_status_for_current_month()

    print()
    print("Current Month Summary")
    print("---------------------")
    print(f"Income this month: €{monthly_income:.2f}")
    print(f"Spent this month: €{monthly_spent:.2f}")
    print(f"Remaining this month: €{monthly_remaining:.2f}")

    print()
    print("Expenses by category this month:")

    if not monthly_category_totals:
        print("No expenses for this month yet.")
    else:
        for category, category_total in monthly_category_totals:
            print(f"- {category}: €{category_total:.2f}")

    print()
    print("Budget status this month:")

    if not budget_status:
        print("No budgets set yet.")
        return

    for category, monthly_limit, spent in budget_status:
        difference = monthly_limit - spent

        if difference >= 0:
            print(
                f"- {category}: €{spent:.2f} / €{monthly_limit:.2f} "
                f"- €{difference:.2f} left"
            )
        else:
            print(
                f"- {category}: €{spent:.2f} / €{monthly_limit:.2f} "
                f"- OVER by €{abs(difference):.2f}"
            )


def main():
    init_db()

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense_flow()
        elif choice == "2":
            add_income_flow()
        elif choice == "3":
            view_summary()
        elif choice == "4":
            view_all_expenses()
        elif choice == "5":
            view_all_income()
        elif choice == "6":
            delete_expense_flow()
        elif choice == "7":
            delete_income_flow()
        elif choice == "8":
            set_budget_flow()
        elif choice == "9":
            view_budgets()
        elif choice == "10":
            view_monthly_summary()
        elif choice == "11":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please choose 1-11.")


if __name__ == "__main__":
    main()
