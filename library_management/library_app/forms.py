from datetime import timedelta
from django import forms

from .models import (Category, Author, Book, Member, BorrowerList)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock <= 0:
            raise forms.ValidationError('Stock can not be 0')
        return stock


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'phone']


class BorrowerForm(forms.ModelForm):
    class Meta:
        model = BorrowerList
        fields = ['book', 'member', 'borrow_date', 'due_date']
        widgets = {
            'borrow_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_date'].disabled = True
        self.fields['due_date'].required = False

    def clean(self):
        cleaned_data = super().clean()
        book = self.cleaned_data.get('book')
        borrow_date = self.cleaned_data.get('borrow_date')
        
        if borrow_date:
            cleaned_data['due_date'] = borrow_date + timedelta(days=7)
        if book and book.stock <= 0:
            raise forms.ValidationError("Books stocks can't be 0")

        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": 'Password'}))
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]
    theme = forms.ChoiceField(choices=THEME_CHOICES, required=False)

class BookSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search books by title, author or category...',
            'class': 'search-input'
        })
    )

