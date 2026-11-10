# GETting Culture Across APIs

This project connects Open Library records for *The Hobbit* to its English Wikipedia article. It uses the Open Library Search API and the MediaWiki Action API.

## Run

```sh
python -m pip install -r requirements.txt
python getting_culture.py
```

No API key is required. The script prints the responses and saves three files:

- `openlibrary_books.json`: three book search results.
- `wikipedia_articles.json`: the article introduction and page details.
- `openlibrary_wikipedia_connection.json`: the selected book and article identifiers.

## What the data shows

The selected Open Library work is `/works/OL27482W`; the Wikipedia page ID is `30292`. Both describe Tolkien's book published in 1937. The script checks the author and publication year because a title search can also find adaptations or collections. The link is a candidate match, since the services do not share an identifier.

Open Library provides catalog details such as authors, publication years, and edition counts. Wikipedia provides descriptive prose. Both offer public JSON APIs, but ask clients to follow identification and rate-limit rules. Their different catalog and editorial choices can also affect which cultural works are easy to find and connect.

## Sources

- [Open Library API guidelines](https://openlibrary.org/developers/api) and [Search API](https://openlibrary.org/dev/docs/api/search)
- [Wikimedia API rate limits](https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits) and [API etiquette](https://www.mediawiki.org/wiki/API:Etiquette)
- [Open Library](https://openlibrary.org/about) and [Wikimedia Foundation](https://wikimediafoundation.org/about/)

The saved introduction comes from [The Hobbit](https://en.wikipedia.org/wiki/The_Hobbit), revision 1384221043, by Wikipedia contributors, under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
