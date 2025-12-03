from django.urls import path
from . import views

urlpatterns = [
    # Authentication and dashboard urls
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('', views.dashboardView, name='dashboard'),

    # Category CRUD urls
    path('createCategory/', views.create_category, name='createCategory'),
    path('listCategory/', views.list_category, name='listCategory'),
    path('updateCategory/<int:pk>/', views.update_category, name='updateCategory'),
    path('deleteCategory/<int:pk>/', views.delete_category, name='deleteCategory'),

    # Author CRUD urls
    path('createAuthor/', views.create_author, name='createAuthor'),
    path('listAuthor/', views.list_author, name='listAuthor'),
    path('updateAuthor/<int:pk>/', views.update_author, name='updateAuthor'),
    path('deleteAuthor/<int:pk>/', views.delete_author, name='deleteAuthor'),

    # Member CRUD urls
    path('createMember/', views.create_member, name='createMember'),
    path('listMember/', views.list_member, name='listMember'),
    path('updateMember/<int:pk>/', views.update_member, name='updateMember'),
    path('deleteMember/<int:pk>/', views.delete_member, name='deleteMember'),

    # Book CRUD urls
    path('createBook/', views.create_book, name='createBook'),
    path('listBook/', views.list_book, name='listBook'),
    path('updateBook/<int:pk>/', views.update_book, name='updateBook'),
    path('deleteBook/<int:pk>/', views.delete_book, name='deleteBook'),

    # Borrower CRUD urls
    path('borrowBook/', views.borrow_book, name='borrowBook'),
    path('listBorrower/', views.list_borrower, name='listBorrower'),
    path('returnBook/<int:pk>/', views.return_book, name='returnBook'),
]