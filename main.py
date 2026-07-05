def show_menu():
    print("\n=== Expense Tracker Pro ===")
    print("1. Add expense")
    print("2. View summary")
    print("3. Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            print("Add expense coming soon...")
        elif choice == "2":
            print("Summary coming soon...")
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
