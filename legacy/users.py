
class User:
    def __init__(self,id,name):
        self.id=id
        self.name=name
        self.issued_books=[]#fix 1: user_books to issued_books
    def issue_book(self,book):#fix2:issuing to issue_book
        if book.available:
            self.issued_books.append(book)#user_books to issued_books
            book.available=False
            print(f"'{book.title}' is issued to user'{self.id}'")
        else:
            print("the book is not available.")


    # NEW METHOD
    # Needed later for return operation

    def return_book(self, book):

        if book in self.issued_books:

            self.issued_books.remove(book)

            book.available = True

            print(f"'{book.title}' returned successfully.")

        else:

            print("This user did not issue this book.")

    #fix3:show_book()-> to show_issued_books()    
    def  show_issued_book(self):
        print("List of issued books by the users : ")
        if (self.users_books==[]):
            print(" No Books are issued by the users.")
            
        else:
            for book in self.users_books:
               print(book.title)
            
        print("no. of issued  books by the users :",len(self.users_books))