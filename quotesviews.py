import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import UserRegisterForm, AuthorForm, QuoteForm
from .models import Author, Quote


def home(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes/home.html', {'quotes': quotes})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'quotes/register.html', {'form': form})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            return redirect('home')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})


def author_detail(request, pk):
    author = Author.objects.get(pk=pk)
    quotes = Quote.objects.filter(author=author)
    return render(request, 'quotes/author_detail.html', {'author': author, 'quotes': quotes})


@login_required
def scrape_data(request):
    response = requests.get('http://quotes.toscrape.com/')
    soup = BeautifulSoup(response.content, 'html.parser')
    
    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').get_text()
        author_name = quote.find('small', class_='author').get_text()

        author, created = Author.objects.get_or_create(name=author_name)

        Quote.objects.get_or_create(text=text, author=author, user=request.user)

    return HttpResponse("Data scraped and saved successfully.")
