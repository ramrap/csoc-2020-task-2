from django.shortcuts import render,redirect
from .forms import RegisterForm
# Create your views here.


def loginView(request):
    pass

def logoutView(request):
    pass

def registerView(response):

    form=RegisterForm()
    if(response.method=="POST"):
        form=RegisterForm(response.POST)
       
        if form.is_valid():
            form.save()
        return redirect('/books')
    else:
            form=RegisterForm()


    return render(response,"register.html",{'form':form})


    