from book import Book
from users import User
from database import get_connection
from datetime import date, timedelta
class Library: 
   
    def __init__(self):
        #fix1:
        #lib_book to books
        self.books=[]
        self.users=[]
    def add_books(self):
        book_id = input("Enter book ID: ")
        title = input("Enter title: ")
        author = input("Enter author: ")
        try :
                connection=get_connection()
                cursor=connection.cursor()
                cursor.execute("""
                insert into books(book_id,title,author,available)
                values(%s,%s,%s,%s)
                """,
                (book_id,title,author,True)
            )
                connection.commit()
                print(title,"Book added successfully")
        except Exception as e:
            print("error:",e)
        finally:
                cursor.close()
                connection.close()
        # new_book = Book(book_id, title, author)
        # self.books.append(new_book)  #lib_book to books
        # print(f"'{new_book.title}' added to  library")
    def remove_book(self):#removed  title parameter
        book_id=input("enter the book_id")
        try:
            connection=get_connection()
            cursor=connection.cursor()
            cursor.execute("""SELECT * FROM books WHERE (book_id=%s)""",
                           (book_id,)
                           )
            book=cursor.fetchone()

            if not book:
                print("book not found!")
            else:
                cursor.execute("""delete from books where (book_id=%s)""",
                               (book[0],))
                connection.commit()
                print("Book removed successfully")
        except Exception as e:
            print("error : ",e)
        finally:
            connection.close()
            cursor.close()
            
        # title =input("enter book title to remove")    
        # for book in self.books:#lib_book to books
        #     if (book.title==title):
        #             if not book.available:#don't allow the removal of the issued book
        #                  print("cannot return this book because it is currently issued .")
        #                  return 
        #             self.books.remove(book)#  #lib_book to books
        #             print(f"'{book.title}' is removed from the library.")
        #             return  
        # FIX 5:
        # Your old code used book.title here.#{book.title}is not found
        # If no book was found, 'book' could be undefined.
        # print("Book not found.")

    # ---------------- DISPLAY BOOKS ----------------
        
     

    def show_book(self):
            try:

                connection = get_connection()

                cursor = connection.cursor()

                cursor.execute(
                    """
                    SELECT book_id, title, author, available
                    FROM books
                    ORDER BY book_id
                    """
                )

                books = cursor.fetchall()

                if not books:

                    print("No books available.")
                    return

                print("\n========== LIBRARY BOOKS ==========")

                available_count = 0

                for book in books:

                    status = "Available" if book[3] else "Issued"

                    if book[3]:
                        available_count += 1

                    print(
                        f"ID: {book[0]} | "
                        f"Title: {book[1]} | "
                        f"Author: {book[2]} | "
                        f"Status: {status}"
                    )

                print("\nNumber of available books:", available_count)

            except Exception as e:

                print("Error:", e)

            finally:

                cursor.close()
                connection.close()
         
        # if not self.books:#lib_book to books
        #       print("No  books is available in the library.")
        #       return 
        # print("\n======== LIBRARY BOOKS ========")
        # for book in self.books:#lib_book to books
                
        #         print(f"'{book.id}' : '{book.title}' :  '{book.available}' ")
                
        # print("No. of available books are : ",sum(1 for book in self.books if book.available == True))#lib_book to books

        # while True:
        #      c= input("Do you want book description of any book:Y/N")
        #      if(c=='Y'):
        #          id=input("enter the id of the book.")
        #          found =False
        #          for book in self.books: #lib_book to books
        #                 if (book.id==id):
        #                    book.description()
        #                    found=True
                           
        #          if not found:
        #                print("book  is not found with the respective book id")
        #      else:
        #           break
    def searching(self):                          
        id=input("enter the id of the book.")
        found =False
        for book in self.books: #lib_book to books
                if (book.id==id):
                    book.description()
                    found=True
                    
        if not found:
                print("book  is not found with the respective book id")

    def add_user(self):
        user_id = input("Enter user ID: ")
        name = input("Enter user name: ")
        try :
             connection=get_connection()
             cursor=connection.cursor()
             cursor.execute("""
                insert into users(user_id,name)
                values(%s,%s)
             """,
             (user_id,name)
            )
             connection.commit()
             print("User added successfully")
        except Exception as e:
            print("error:",e)
        finally:
             cursor.close()
             connection.close()
            
       
        # new_user = User(user_id, name)

       
        # self.users.append(new_user)

        #print("User added successfully!")
    def issuing(self, user_id, book_id):
        

        try:

            connection = get_connection()
            cursor = connection.cursor()

            # Check user exists
            cursor.execute(
                "SELECT * FROM users WHERE user_id = %s",
                (user_id,)
            )

            if cursor.fetchone() is None:

                print("User not found.")
                return

            # Check book exists and availability
            cursor.execute(
                """
                SELECT available
                FROM books
                WHERE book_id = %s
                """,
                (book_id,)
            )

            result = cursor.fetchone()

            if result is None:

                print("Book not found.")
                return

            if result[0] is False:

                print("Book is already issued.")
                return

            issue_date = date.today()

            due_date = issue_date + timedelta(days=14)

            # Insert issue record
            cursor.execute(
                """
                INSERT INTO issued_books
                (user_id, book_id, issue_date, due_date)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, book_id, issue_date, due_date)
            )

            # Update availability
            cursor.execute(
                """
                UPDATE books
                SET available = FALSE
                WHERE book_id = %s
                """,
                (book_id,)
            )

            connection.commit()

            print("Book issued successfully!")

        except Exception as e:

            print("Error:", e)

        finally:

            cursor.close()
            connection.close()
        # user = None
        # book = None

        # for u in self.users:
        #     if u.id == userid:
        #         user = u
        #         break

        # if not user:
        #      print("User not found")
        #      return
  
        # for b in self.books: #lib_book to books
        #    if b.id == bookid:
        #       book = b
        #       break

        # if book  is  None:#if not book:
        #       print("Book not found")
        #       return

        # if  not book.available:
        #      print("Book is already issued ")
        #      return 
   
        # user.issue_book(book) #fix due to user file issuing to issue#fix7
    # ---------------- RETURN BOOK ----------------

    # FIX 8:
    # This method did not exist in your original library.py.
    # main.py was already calling it, so we need to add it.

    def returning(self, user_id, book_id):

        try:

            connection = get_connection()
            cursor = connection.cursor()

            # Check active issue record
            cursor.execute(
                """
                SELECT issue_id
                FROM issued_books
                WHERE user_id = %s
                AND book_id = %s
                AND return_date IS NULL
                """,
                (user_id, book_id)
            )

            record = cursor.fetchone()

            if record is None:

                print("No active issue record found.")
                return

            # Update return date
            cursor.execute(
                """
                UPDATE issued_books
                SET return_date = %s
                WHERE issue_id = %s
                """,
                (date.today(), record[0])
            )

            # Make book available again
            cursor.execute(
                """
                UPDATE books
                SET available = TRUE
                WHERE book_id = %s
                """,
                (book_id,)
            )

            connection.commit()

            print("Book returned successfully!")

        except Exception as e:

            print("Error:", e)

        finally:

            cursor.close()
            connection.close()

        # user = None
        # book = None

        # # Find user
        # for u in self.users:

        #     if u.id == user_id:
        #         user = u
        #         break

        # if user is None:

        #     print("User not found.")
        #     return

        # # Find book
        # for b in self.books:

        #     if b.id == book_id:
        #         book = b
        #         break

        # if book is None:

        #     print("Book not found.")
        #     return

        # # Return the book through User class
        # user.return_book(book)

    # ---------------- SEARCH BOOK ----------------

    def search_book(self, book_id):        
            try:

                connection = get_connection()

                cursor = connection.cursor()

                cursor.execute(
                    """
                    SELECT book_id, title, author, available
                    FROM books
                    WHERE book_id = %s
                    """,
                    (book_id,)
                )

                book = cursor.fetchone()

                if book:

                    print("\n========== BOOK DETAILS ==========")

                    print("Book ID :", book[0])
                    print("Title   :", book[1])
                    print("Author  :", book[2])

                    if book[3]:
                        print("Status  : Available")
                    else:
                        print("Status  : Issued")

                else:

                    print("Book not found.")

            except Exception as e:

                print("Error:", e)

            finally:

                cursor.close()
                connection.close()

        # FIX 9:
        # Your original code used self.books,
        # but your __init__ had self.lib_book.
        # We have now consistently used self.books.
            # """
            #     def search_book(self,book_id):
            #          for b in self.books:
            #            if b.id == book_id:
            #               book = b
            #               break
            #          book.description() """

            # for book in self.books:

            #     if book.id == book_id:

            #         book.description()
            #         return

        # FIX 10:
        # Prevents error when the book doesn't exist.
            # print("Book not found.")

    # ---------------- SHOW USER'S BOOKS ----------------

    # NEW FEATURE
    # This wasn't in your original Library class.
    # It lets us see which books a particular user has.

    def show_user_books(self):
            
        user_id = input("Enter user ID: ")

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT b.book_id, b.title
                FROM books b
                JOIN issued_books i
                ON b.book_id = i.book_id
                WHERE i.user_id = %s
                AND i.return_date IS NULL
                """,
                (user_id,)
            )

            books = cursor.fetchall()

            if not books:

                print("No books currently issued.")
                return

            print("\n===== ISSUED BOOKS =====")

            for book in books:

                print(f"{book[0]} - {book[1]}")

        except Exception as e:

            print("Error:", e)

        finally:

            cursor.close()
            connection.close()

        # user_id = input("Enter user ID: ")

        # for user in self.users:

        #     if user.id == user_id:

        #         user.show_issued_books()
        #         return

        # print("User not found.")

#=============================
    def display_users(self):
        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT user_id, name
                FROM users
                ORDER BY user_id
                """
            )

            users = cursor.fetchall()

            if not users:

                print("No users found.")
                return

            print("\n========== USERS ==========")

            for user in users:

                print(
                    f"ID: {user[0]} | "
                    f"Name: {user[1]}"
                )

        except Exception as e:

            print("Error:", e)

        finally:

            cursor.close()
            connection.close()
        # if not self.users:
        #     print("No users found")


        # else:
        #     for user in self.users:
        #         print(user.id, "-", user.name)
    

        
         
            
             

                     