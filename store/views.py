from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    book=Book.objects.get(id=bid)
    
    
    count=BookCopy.objects.filter(book__exact=book,status=True)

    context = {
        'book': book, # set this to an instance of the required book
        'num_available': len(count), # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    # START YOUR CODE HERE
    
    
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    
    template_name = 'store/book_list.html'
    get_data = request.GET
    print(type(get_data))
    print(get_data)
    # titles=get_data.get('title')
    # # if(titles==None):
    # #     titles=''
   
    books=(Book.objects.filter(
        title__icontains=get_data.get('title',''),
        author__icontains=get_data.get('author',''),
        genre__icontains=get_data.get('genre','')
    ))

    context = {
        'books': books, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    }
    
    # START YOUR CODE HERE
    
    
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    current_user=request.user
    # print(current_user)
    books=BookCopy.objects.filter(borrower=current_user)
    # print(books)

    
    template_name = 'store/loaned_books.html'


    context = {
        'books': books,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE

    


    return render(request, template_name, context=context)

@csrf_exempt
def loanBookView(request):
    alpha=request.user.is_authenticated
    if not alpha:
        return JsonResponse({"message":"login plz"})
    book_id=request.POST['bid']
    books=BookCopy.objects.filter(book_id=book_id,status=True)
    if books:

        book=books[0]
        book.borrower=request.user
        book.status=False
        book.borrow_date=datetime.date.today()

        book.save()
        return JsonResponse({"message":"book successfully loaned"})

    else:
        return JsonResponse({"message":"no copy remaining"})
    return JsonResponse({"message":"Server problem"})



    
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    


    
'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    if request.method=="POST":
        try:
            book_id=request.POST['bid']
            book=BookCopy.objects.get(pk=book_id)
            book.status=True
            book.borrower=None
            book.borrow_date=None
            book.save()

            return JsonResponse({'message':"book successfull return"})

        except:
            return JsonResponse({'message':"Try again"})


    return JsonResponse({'message':"BAD BOY"})

@csrf_exempt
@login_required 
def rateBookView(request):
    if request.method=="POST":
        star=request.POST["stars"]
        book_id=request.POST["bid"]
        current_user=request.user
        rating=Rating.objects.filter(book__exact=BookCopy.objects.get(id=book_id).book,user__exact=current_user)
        if rating:
            rating01=rating[0]
            rating01.stars=star
            rating01.save()
            return JsonResponse({"message":"rating has been updated"})
        else:
            rating01=Rating.objects.create(user=current_user,book=BookCopy.objects.get(id=book_id).book,stars=star)
            rating01.save()
            return JsonResponse({"message":"Thanks for first time rating"})
    return({"message:unable to rate the boom"})
        
    
        


