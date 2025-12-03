from django.contrib import admin
from .models import Book, Author, Category, Member, BorrowerList

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Member)
admin.site.register(BorrowerList)
