# Shopping list program

def display_menu():
    print("\n--- Shopping List Menu ---")
    print("1. View shopping list")
    print("2. Add item to shopping list")
    print("3. Remove item from shopping list")
    print("4. Clear the shopping list")
    print("5. Exit\n")

def display_list(shopping_list):
    if not shopping_list:
        print("Your shopping list is empty!")
    else:
        print("\nYour Shopping List:")
        for i, item in enumerate(shopping_list, 1):
            print(f"{i}. {item}")

def main():
    shopping_list = []
    while True:
        display_menu()
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == "1":
            display_list(shopping_list)
        
        elif choice == "2":
            item = input("Enter the item to add: ").strip()
            if item:
                shopping_list.append(item)
                print(f"'{item}' has been added to your shopping list.")
            else:
                print("Invalid input. Please enter a valid item.")
        
        elif choice == "3":
            display_list(shopping_list)
            try:
                index = int(input("Enter the number of the item to remove: "))
                if 1 <= index <= len(shopping_list):
                    removed_item = shopping_list.pop(index - 1)
                    print(f"'{removed_item}' has been removed from your shopping list.")
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        elif choice == "4":
            shopping_list.clear()
            print("Shopping list has been cleared.")
        
        elif choice == "5":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

# Run the shopping list program
if __name__ == "__main__":
    main()