"""Connect an Open Library book record to a Wikipedia article."""

import json
from pathlib import Path
import time

import requests


OUTPUT = Path(__file__).resolve().parent
HEADERS = {
    "User-Agent": "GettingCulture/1.0 (https://github.com/masontle/is310-coding-assignments)",
}


def get_json(url, params):
    """Check HTTP status before parsing; a failed lookup returns None."""
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        if response.status_code != 200:
            print(f"Request failed: HTTP {response.status_code} from {url}")
            if response.status_code == 429:
                print("Rate limited; wait before running again.")
            return None
        data = response.json()
        if not isinstance(data, dict):
            print(f"Unexpected response structure from {url}")
            return None
        if "error" in data:
            print("API error:", data["error"])
            return None
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return data
    except (requests.RequestException, ValueError) as error:
        print(f"Lookup failed: {error}")
        return None


def save_items(filename, items):
    """Save item records only, leaving out response/request metadata."""
    (OUTPUT / filename).write_text(
        json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main():
    print("Open Library response:")
    library = get_json("https://openlibrary.org/search.json", {
        "title": "The Hobbit", "author": "J. R. R. Tolkien", "limit": 3,
        "fields": "key,title,author_name,first_publish_year,edition_count",
    })
    books = library.get("docs", []) if library else []
    if library is not None:
        save_items("openlibrary_books.json", books)

    # Prefer an exact title; do not silently connect a study guide or adaptation.
    book = next((item for item in books
                 if item.get("title", "").casefold() == "the hobbit"
                 and item.get("first_publish_year") == 1937
                 and any("tolkien" in name.casefold()
                         for name in item.get("author_name", []))), None)
    title = book["title"] if book else "The Hobbit"
    if book is None:
        print("No exact book match; query Wikipedia independently and report the gap.")

    time.sleep(1)
    print("Wikipedia MediaWiki Action API response:")
    wiki = get_json("https://en.wikipedia.org/w/api.php", {
        "action": "query", "format": "json", "formatversion": 2,
        "titles": title, "redirects": 1, "prop": "extracts|info|pageprops",
        "exintro": 1, "explaintext": 1, "inprop": "url", "maxlag": 5,
    })
    pages = wiki.get("query", {}).get("pages", []) if wiki else []
    if wiki is not None:
        save_items("wikipedia_articles.json", pages)

    page = next((item for item in pages if "missing" not in item), None)
    if book and page:
        ambiguous = "disambiguation" in page.get("pageprops", {})
        connection = {
            "openlibrary_key": book["key"], "book_title": book["title"],
            "authors": book.get("author_name", []),
            "wikipedia_pageid": page["pageid"], "wikipedia_title": page["title"],
            "wikipedia_url": page.get("fullurl"),
            "match_status": "ambiguous" if ambiguous else "candidate_title_match",
            "match_note": "Selected title, Tolkien authorship, and 1937 publication year; verify article subject manually.",
        }
        save_items("openlibrary_wikipedia_connection.json", [connection])
        print("Connection:", json.dumps(connection, indent=2))
    else:
        print("Connection could not be completed; inspect the lookup messages.")
    return 0 if book and page else 1


if __name__ == "__main__":
    raise SystemExit(main())
