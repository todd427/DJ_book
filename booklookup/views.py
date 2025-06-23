
import requests
from django.shortcuts import render
from .forms import AuthorSearchForm
from .models import Book
from bs4 import BeautifulSoup

def fetch_books(author):
    results = []

    # Open Library
    ol_url = f"https://openlibrary.org/search.json?author={author}"
    ol_data = requests.get(ol_url).json()
    for doc in ol_data.get("docs", []):
        results.append({
            "title": doc.get("title"),
            "authors": ", ".join(doc.get("author_name", [])),
            "isbn_10": doc.get("isbn")[0] if "isbn" in doc else None,
            "isbn_13": doc.get("isbn")[1] if "isbn" in doc and len(doc["isbn"]) > 1 else None,
            "asin": None,
            "source": "Open Library"
        })

    # Google Books
    gb_url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}"
    gb_data = requests.get(gb_url).json()
    for item in gb_data.get("items", []):
        volume_info = item.get("volumeInfo", {})
        identifiers = volume_info.get("industryIdentifiers", [])
        isbn_10 = isbn_13 = asin = None
        for ident in identifiers:
            if ident["type"] == "ISBN_10":
                isbn_10 = ident["identifier"]
            elif ident["type"] == "ISBN_13":
                isbn_13 = ident["identifier"]
        asin = item.get("id")

        results.append({
            "title": volume_info.get("title"),
            "authors": ", ".join(volume_info.get("authors", [])),
            "isbn_10": isbn_10,
            "isbn_13": isbn_13,
            "asin": asin,
            "source": "Google Books"
        })

    return results

def get_purchase_url(isbn_or_asin):
    return f"https://www.amazon.com/dp/{isbn_or_asin}"

def scrape_price(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        price = soup.select_one("#priceblock_ourprice, .a-color-price")
        return price.text.strip() if price else "N/A"
    except:
        return "N/A"

def book_search_view(request):
    form = AuthorSearchForm()
    books = []

    if request.method == "POST":
        form = AuthorSearchForm(request.POST)
        if form.is_valid():
            author = form.cleaned_data["author"]
            raw_books = fetch_books(author)
            books = []

            for book in raw_books:
                isbn_or_asin = book["isbn_10"] or book["isbn_13"] or book["asin"]
                url = get_purchase_url(isbn_or_asin) if isbn_or_asin else None
                price = scrape_price(url) if url else "N/A"
                book["purchase_url"] = url
                book["price"] = price

                Book.objects.create(**book)
                books.append(book)

    return render(request, "booklookup/results.html", {"form": form, "books": books})
