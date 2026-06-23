import os

#os.system("cat > /home/kali/book_finder.py << 'PYEOF'")



#!/usr/bin/env python3
"""
Free Book Finder — пошук безкоштовних книг через публічні API
Джерела: Project Gutenberg, Internet Archive, Open Library, Standard Ebooks
"""

import json
import sys
import urllib.request
import urllib.parse
import urllib.error

SOURCE_ICONS = {
    "gutenberg":   "📗",
    "archive":     "🏛️",
    "openlibrary": "📚",
    "standard":    "✨",
}


def fetch_json(url: str, timeout: int = 8) -> dict | list | None:
    req = urllib.request.Request(url, headers={"User-Agent": "BookFinder/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None


# ── Gutenberg (gutendex API) ──────────────────────────────────────────────────

def search_gutenberg(query: str) -> list[dict]:
    q = urllib.parse.quote(query)
    data = fetch_json(f"https://gutendex.com/books/?search={q}&languages=en,uk")
    if not data or "results" not in data:
        return []
    books = []
    for b in data["results"][:3]:
        authors = ", ".join(a["name"] for a in b.get("authors", []))
        bid = b["id"]
        books.append({
            "title": b.get("title", "—"),
            "author": authors or "Невідомо",
            "year": None,
            "source": "gutenberg",
            "sourceLabel": "Project Gutenberg",
            "desc": f"Книга #{bid}. Завантажень: {b.get('download_count', 0):,}",
            "links": [
                {"label": "Читати онлайн", "url": f"https://www.gutenberg.org/ebooks/{bid}"},
                {"label": "EPUB", "url": f"https://www.gutenberg.org/ebooks/{bid}.epub.noimages"},
            ],
        })
    return books


# ── Open Library ─────────────────────────────────────────────────────────────

def search_openlibrary(query: str) -> list[dict]:
    q = urllib.parse.quote(query)
    data = fetch_json(f"https://openlibrary.org/search.json?q={q}&limit=3&fields=title,author_name,first_publish_year,key,ia")
    if not data or "docs" not in data:
        return []
    books = []
    for b in data["docs"][:3]:
        key = b.get("key", "")
        ia = b.get("ia", [])
        links = [{"label": "Open Library", "url": f"https://openlibrary.org{key}"}]
        if ia:
            links.append({"label": "Internet Archive", "url": f"https://archive.org/details/{ia[0]}"})
        books.append({
            "title": b.get("title", "—"),
            "author": ", ".join(b.get("author_name", ["Невідомо"]))[:60],
            "year": b.get("first_publish_year"),
            "source": "openlibrary",
            "sourceLabel": "Open Library",
            "desc": None,
            "links": links,
        })
    return books


# ── Internet Archive ──────────────────────────────────────────────────────────

def search_archive(query: str) -> list[dict]:
    q = urllib.parse.quote(query)
    url = (
        f"https://archive.org/advancedsearch.php"
        f"?q={q}+AND+mediatype:texts+AND+licenseurl:*creativecommons*"
        f"&fl=identifier,title,creator,year,description"
        f"&rows=3&page=1&output=json"
    )
    data = fetch_json(url)
    if not data:
        return []
    docs = data.get("response", {}).get("docs", [])
    books = []
    for b in docs:
        iid = b.get("identifier", "")
        desc = b.get("description", "")
        if isinstance(desc, list):
            desc = desc[0] if desc else ""
        desc = (desc[:100] + "...") if len(desc) > 100 else desc
        books.append({
            "title": b.get("title", "—"),
            "author": b.get("creator", "Невідомо"),
            "year": b.get("year"),
            "source": "archive",
            "sourceLabel": "Internet Archive",
            "desc": desc or None,
            "links": [
                {"label": "Читати / завантажити", "url": f"https://archive.org/details/{iid}"},
            ],
        })
    return books


# ── Standard Ebooks (RSS/HTML пошук) ─────────────────────────────────────────

def search_standard(query: str) -> list[dict]:
    """Standard Ebooks не має публічного API — повертаємо пошукове посилання."""
    q = urllib.parse.quote(query)
    return [{
        "title": f"Пошук «{query}» на Standard Ebooks",
        "author": "Різні автори",
        "year": None,
        "source": "standard",
        "sourceLabel": "Standard Ebooks",
        "desc": "Безкоштовні, якісно відформатовані електронні книги у відкритому доступі.",
        "links": [
            {"label": "Пошук", "url": f"https://standardebooks.org/ebooks?q={q}"},
        ],
    }]


# ── Виведення ─────────────────────────────────────────────────────────────────

def print_book(book: dict, index: int) -> None:
    icon = SOURCE_ICONS.get(book.get("source", ""), "📖")
    year = f" ({book['year']})" if book.get("year") else ""
    source = book.get("sourceLabel", "")
    print(f"\n  {index}. {book['title']}{year}")
    print(f"     Автор: {book.get('author', '—')}")
    print(f"     {icon} {source}")
    if book.get("desc"):
        print(f"     {book['desc']}")
    for link in book.get("links", []):
        print(f"     🔗 {link['label']}: {link['url']}")


def run_search(query: str) -> bool:
    print(f"\n{'═' * 62}")
    print(f"  🔍 Запит: «{query}»")
    print(f"{'═' * 62}")

    all_books: list[dict] = []
    sources = [
        ("Gutenberg",     search_gutenberg),
        ("Open Library",  search_openlibrary),
        ("Archive.org",   search_archive),
        ("Standard Ebooks", search_standard),
    ]

    for name, fn in sources:
        print(f"  ↳ {name}...", end=" ", flush=True)
        try:
            found = fn(query)
            print(f"{len(found)} результатів")
            all_books.extend(found)
        except Exception as e:
            print(f"помилка ({e})")

    if not all_books:
        print("\n  Нічого не знайдено.")
        return False

    print(f"\n  Всього знайдено: {len(all_books)} книг")
    for i, book in enumerate(all_books, 1):
        print_book(book, i)
    return True


def interactive_mode() -> None:
    print("=" * 62)
    print("  📚  Free Book Finder")
    print("  Gutenberg · Open Library · Archive.org · Standard Ebooks")
    print("=" * 62)
    print("  Введи назву книги, автора або тему (або 'вихід' для виходу)\n")
    while True:
        query = input("  > ").strip()
        if not query:
            continue
        if query.lower() in ("вихід", "exit", "quit", "q"):
            print("\n  До побачення!\n")
            break
        run_search(query)
        print()


def batch_mode(queries: list[str]) -> None:
    results = []
    for q in queries:
        ok = run_search(q)
        results.append((q, ok))
        print()

    print("\n" + "=" * 62)
    print("  ПІДСУМОК")
    print("=" * 62)
    for q, ok in results:
        print(f"  {'✅' if ok else '❌'}  «{q}»")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        batch_mode(sys.argv[1:])
    else:
        interactive_mode()
#PYEOF
#echo "OK"
