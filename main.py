from app.database import (
    init_db,
    add_expense,
    get_expenses,
    get_total_spent,
    get_category_totals,
)


def show_menu():
    print("\n=== Expense Tracker Pro ===")
    print("1. Add expense")
    print("2. View summary")
    print("3. View all expenses")
    print("4. Exit")


def add_expense_flow():
    amount_input = input("Amount in EUR: ")

    try:
        amount = float(amount_input.replace(",", "."))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    category = input("Category: ").strip()
    if not category:
        print("Category cannot be empty.")
        return

    description = input("Description: ").strip()

    add_expense(amount, category, description)
    print(f"Saved expense: {amount:.2f} EUR - {category}")


def view_summary():
    total = get_total_spent()
    category_totals = get_category_totals()

    print("\n=== Summary ===")
    print(f"Total spent: {total:.2f} EUR")

    if not category_totals:
        print("No expenses yet.")
        return

    print("\nBy category:")
    for item in category_totals:
        print(f"- {item['category']}: {item['total']:.2f} EUR")


def view_all_expenses():
    expenses = get_expenses()

    print("\n=== All Expenses ===")

    if not expenses:
        print("No expenses yet.")
        return

    for expense in expenses:
        print(
            f"{expense['id']}. "
            f"{expense['amount']:.2f} EUR | "
            f"{expense['category']} | "
            f"{expense['description']} | "
            f"{expense['created_at']}"
        )


def main():
    init_db()

    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            add_expense_flow()
        elif choice == "2":
            view_summary()
        elif choice == "3":
            view_all_expenses()
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
