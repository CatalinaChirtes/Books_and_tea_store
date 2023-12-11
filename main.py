from json import JSONDecodeError

from categories import Categories
from category import Category
from order import Order
from orders import Orders
from product import Product
from products import Products

if __name__ == "__main__":
    global enter_other_menu

    # display menus
    # ----------------------------------------------------------


    def display_main_menu():
        print("----------------------------------------------------------\n")
        print("1. Categories")
        print("2. Products")
        print("3. Orders")
        print("4. Exit")
        print()


    def display_categories_menu():
        print("----------------------------------------------------------\n")
        print("1. Add a category")
        print("2. Remove a category")
        print("3. Display all the categories")
        print("4. Back")
        print()


    def display_products_menu():
        print("----------------------------------------------------------\n")
        print("1. Add a product")
        print("2. Remove a product")
        print("3. Display all the products")
        print("4. Back")
        print()


    def display_orders_menu():
        print("----------------------------------------------------------\n")
        print("1. Place a new order")
        print("2. Display all orders")
        print("3. Back")
        print()


    # main options
    # ----------------------------------------------------------


    def categories_option():
        while enter_other_menu:
            display_categories_menu()
            option1 = input("Enter an option between 1 and 4: ")
            print()
            categories_action = categories_actions.get(option1, error_handler)
            categories_action()


    def products_option():
        while enter_other_menu:
            display_products_menu()
            option2 = input("Enter an option between 1 and 4: ")
            print()
            products_action = products_actions.get(option2, error_handler)
            products_action()


    def orders_option():
        while enter_other_menu:
            display_orders_menu()
            option3 = input("Enter an option between 1 and 3: ")
            print()
            orders_action = orders_actions.get(option3, error_handler)
            orders_action()


    def exit_option():
        exit("Exiting the store. Thanks for coming by :)")


    # categories options
    # ----------------------------------------------------------


    def add_category():
        while True:
            category_name = input("Type the name of the category you want to add: ")
            category = Category(category_name)
            added_successfully = Categories.add_category(category)
            if added_successfully:
                print("\nCategory added successfully.")
                break
            print()
        print()


    def remove_category():
        while True:
            category_name = input("Type the name of the category you want to remove: ")
            category = Category(category_name)
            removed_successfully = Categories.remove_category(category)
            if removed_successfully:
                print("\nCategory removed successfully.")
                break
            print()
        print()


    def display_categories():
        try:
            categories = Categories.load_categories()
            for cat in categories:
                print(cat.name)
        except JSONDecodeError as e:
            categories = None
        print()


    # products options
    # ----------------------------------------------------------


    def add_product():
        while True:
            product_name = input("Type the name of the product you want to add: ")
            product_category = input("Type the category in which you want to add your product: ")
            product_stock = input("Type how many products you want to add: ")

            category_exists = False
            Categories.load_categories()

            for existing_category in Categories.categories:
                if existing_category.name == product_category:
                    category_exists = True
                    break

            if category_exists:
                if product_stock.isdigit():
                    product = Product(product_name, product_category, int(product_stock))
                    added_successfully = Products.add_product(product)
                    if added_successfully:
                        print("\nProduct added successfully.")
                        break
                else:
                    print("\nThe entered stock is not a valid input. Please enter a valid integer for the stock amount.")
            else:
                print("\nThe entered category does not exist. Please enter a valid category.")
            print()

        print()


    def remove_product():
        while True:
            product = input("Type the name of the product you want to remove: ")
            removed_successfully = Products.remove_product(product)
            if removed_successfully:
                print("\nProduct removed successfully.")
                break
            print()
        print()


    def display_products():
        try:
            products = Products.load_products()
            for prod in products:
                print("Product Name: " + prod.name + "\n" +
                      "Category: " + prod.category + "\n" +
                      "Stock: " + str(prod.stock) + "\n")
        except JSONDecodeError as e:
            products = None
        print()


    # orders options
    # ----------------------------------------------------------


    def place_order():
        buyer_name = input("Type the name of the buyer: ")
        destination_address = input("Type the destination address for the order: ")

        ordered_products = {}
        add_more_products = True

        while add_more_products:
            product_name = input("Type the name of the product you want to order: ")

            product_found = False
            for prod in Products.load_products():
                if prod.name == product_name:
                    product_found = True
                    available_stock = prod.stock
                    break

            if product_found:
                amount = input(f"Type the amount of {product_name}: ")

                if amount.isdigit():
                    if int(amount) == 0:
                        print("\nThe minimum order amount is 1.")
                    else:
                        if int(amount) <= available_stock:
                            ordered_products[prod] = amount
                            print("\nProduct added to the order.")
                        else:
                            print("\nThe stock is insufficient. You can't order this many products.")
                else:
                    print("\nThe entered amount is not a valid input. Please enter a valid integer for the stock amount.")

            else:
                print("\nProduct not found. Please enter a valid product.")

            add_more = input("\nDo you want to add more products to the order? (yes/no): ").lower()
            print()
            if add_more == "yes":
                add_more_products = True
            elif add_more == "no":
                add_more_products = False

        if ordered_products:
            new_order = Order(ordered_products, buyer_name, destination_address)
            Orders.add_order(new_order)
            print("Order placed successfully.\n")
        else:
            print("No products added to the order.\n")


    def display_orders():
        Orders.refresh_orders()
        try:
            orders = Orders.load_orders()
            for ord in orders:
                print("Buyer: " + ord.buyer_name + "\n" +
                      "Destination address: " + ord.destination_address)
                print("{")
                for product_name in ord.ordered_products:  # Iterate through product names
                    amount = ord.ordered_products[product_name].get("amount")
                    print("    Product Name: " + str(product_name) + "\n" +
                          "    Amount: " + str(amount) + "\n")
                print("}\n")
        except JSONDecodeError as e:
            orders = None
        print()


    # general options
    # ----------------------------------------------------------


    def back_option():
        global enter_other_menu
        enter_other_menu = False


    def error_handler():
        print("Invalid option. Please try again.\n")


    main_actions = {
        "1": categories_option,
        "2": products_option,
        "3": orders_option,
        "4": exit_option
    }

    categories_actions = {
        "1": add_category,
        "2": remove_category,
        "3": display_categories,
        "4": back_option
    }

    products_actions = {
        "1": add_product,
        "2": remove_product,
        "3": display_products,
        "4": back_option
    }

    orders_actions = {
        "1": place_order,
        "2": display_orders,
        "3": back_option
    }

    while True:
        global enter_other_menu
        enter_other_menu = True
        display_main_menu()
        option = input("Enter an option between 1 and 4: ")
        print()
        main_action = main_actions.get(option, error_handler)
        main_action()
