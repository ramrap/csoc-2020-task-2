from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    description = models.TextField(null=True)
    mrp = models.PositiveIntegerField()
    rate = models.FloatField(default=0.0)

    def no_of_rating(self):
        ratings=Rating.objects.filter(book=self)
        return len(ratings)
    def avg_ratings(self):
        ratings=Rating.objects.filter(book=self)
        sum=0.0
        for rating in ratings:
            sum+=rating.stars
        if len(ratings)==0:
            return 0
        else:
            return sum/len(ratings)

        
    
    

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return f'{self.title} by {self.author}'


class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(null=True, blank=True)
    # True status means that the copy is available for issue, False means unavailable
    status = models.BooleanField(default=False)
    borrower = models.ForeignKey(User, related_name='borrower', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.borrow_date:
            return f'{self.book.title}, {str(self.borrow_date)}'
        else:
            return f'{self.book.title} - Available'

class Rating(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    stars=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)])



    def __str__(self):
        return f"{self.book} by {self.user}"