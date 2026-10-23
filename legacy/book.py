
class Book:
    def __init__(self,id,title,author):
        self.id=id
        self.title=title
        self.author=author
        self.available=True
    #fix 1:renamed from book_issue()
    def issue_book(self,issuedate):
        if(self.available==True):
            self.issue_date=issuedate
            self.available=False
        else:
            print("Sorry!The Book is not available now.")
    #fix2:renamed from book_ return()
    def book_return(self,returndate):
        if(self.available==False):
            self.return_date=returndate
            self.available=True
        else:
           print("Check again! the book is already available.")
    def status(self):
        #fix 3 : simplified boolean check (self.available==True) to self.available
        if self.available:
            print("The book is Available now.")
        else:
            print("The book is already issued. It is not available now.")
    def description(self):
        print("\nBook id: ",self.id)
        print("\nname of the book: ",self.title)
        print("\nauthor of the book: ",self.author)
        if(self.available==True):
            print("\nAvailable.")
        else:
            print("\nIssued.")



