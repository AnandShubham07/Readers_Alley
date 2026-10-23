
from library import Library

def main():
    lib = Library()
   
    while True:
        print("\n===== Library Management System =====")
        print("1. Add Book")
        print("2. remove book")
        print("3. Display Books")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Add User")
        print("7. Display Users")
        print("8. Search book")
        print("0. Exit")

        choice = input("Enter your choice: ")
         
        #ADD BOOKS
        if choice == '1':
            lib.add_books()
         
        #REMOVE BOOKS
        elif choice == '2':
            lib.remove_book()


        #DISPLAY BOOKS
        elif choice == '3':
            lib.show_book()

        #ISSUE BOOK
        elif choice == '4':
            user_id = input("Enter user ID: ")
            book_id = input("Enter book ID: ")
            lib.issuing(user_id, book_id)
          
        #RETURN BOOK
        elif choice == '5':
            user_id = input("Enter user ID: ")
            book_id = input("Enter book ID: ")
            lib.returning(user_id, book_id)

        #ADD USER
        elif choice == '6':
            lib.add_user()
         
        #DISPLAY USERS
        elif choice == '7':
            lib.display_users()

        #SEARCH BOOKS
        elif choice == '8':
            book_id = input("Enter book ID: ")
            lib.search_book(book_id)

        #Show User's issued books
        elif choice =='9':
            lib.show_user_books()


        #EXIT
        elif choice == '0':
            print("Exiting system...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()