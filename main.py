from app.database import (
    init_db,
    add_expense,
    delete_expense,
    get_expenses,
    get_total_spent,
    get_category_totals,
    get_current_month_total,
    get_current_month_category_totals,
)


def show_menu():
    print()
    print("Expense Tracker Pro")
    print("-------------------")
    print("1. Add expense")
    print("2. View summary")
    print("3. View all expenses")
    print("4. Delete expense")
    print("5. Monthly summary")
    print("6. Exit")


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


def view_summary():
    total = get_total_spent()
    category_totals = get_category_totals()

    print()
    print("Overall Summary")
    print("---------------")
    print(f"Total spent: €{total:.2f}")

    if not category_totals:
        print("No expenses yet.")
        return

    print()
    print("By category:")
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


def view_monthly_summary():
    monthly_total = get_current_month_total()
    monthly_category_totals = get_current_month_category_totals()

    print()
    print("Current Month Summary")
    print("---------------------")
    print(f"Total spent this month: €{monthly_total:.2f}")

    if not monthly_category_totals:
        print("No expenses for this month yet.")
        return

    print()
    print("By category this month:")
    for category, category_total in monthly_category_totals:
        print(f"- {category}: €{category_total:.2f}")


def main():
    init_db()

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense_flow()
        elif choice == "2":
            view_summary()
        elif choice == "3":
            view_all_expenses()
        elif choice == "4":
            delete_expense_flow()
        elif choice == "5":
            view_monthly_summary()
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please choose 1-6.")


if __name__ == "__main__":
    main()
