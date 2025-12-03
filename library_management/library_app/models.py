from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# Model for creating category and we use Unauthorized as a default category
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    # Using classmethod to call the model function 
    @classmethod
    def default_category(cls):
        category, created = cls.objects.get_or_create(name="Unauthorized")
        return category
    

# Model for creating Authors model
class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    

# creating model book, referencing authors and category
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="book")
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, 
                                 default=Category.default_category, related_name="book")
    stock = models.IntegerField(default=1)

    class Meta:
        ordering = ['title']
        
    def __str__(self):
        return self.title
    

# class for creating members and used a member_number for the member identification
class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=15)
    member_number = models.CharField(max_length=10, unique=True, blank=True)

    class Meta:
        ordering = ['member_number']

    # creates a custome sequence for member-number
    def save(self, *args, **kwargs):
        if not self.member_number:
            last_member = Member.objects.order_by('-id').first()
            if last_member:
                member_no = last_member.id + 1
            else: 
                member_no = 1
            self.member_number = f"MEM-{member_no}"

        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.member_number
    

# class to creates a borrwer list
class BorrowerList(models.Model):    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrower')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrower')
    borrow_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    due_date = models.DateField()

    class Meta:
        ordering = ['due_date']
        permissions = [
            ("borrowBook", "Can borrow a book"),
            ("returnBook", "Can return a book"),
        ]

    # chekcing overdue with the current date, due date and returned field
    @property
    def is_overdue(self):
        return not self.returned and timezone.now().date() > self.due_date
    
    def __str__(self):
        return f"{self.book.title} is borrowed by {self.member.name}({self.member.member_number})"

