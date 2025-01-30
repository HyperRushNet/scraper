import requests, bs4, urllib.parse

def get_wikipedia_content(query):
    search_url = f"https://html.duckduckgo.com/html?q={query} Wikipedia"
    response = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # Zoek de eerste Wikipedia-link
    wiki_link = None
    for a in soup.select(".result__title a"):
        href = a.get("href", "")
        if "wikipedia.org" in href:
            wiki_link = href  # Directe Wikipedia-link
            break
        elif href.startswith("/l/?uddg="):
            wiki_link = "https://duckduckgo.com" + href  # Fix relatieve URL
            break

    if not wiki_link:
        return "Geen Wikipedia-pagina gevonden."

    # Decodeer DuckDuckGo doorstuur-link
    if "/l/?uddg=" in wiki_link:
        wiki_link = urllib.parse.unquote(wiki_link.split("uddg=")[-1].split("&")[0])

    # Wikipedia-pagina openen en inhoud scrapen
    wiki_response = requests.get(wiki_link, headers={"User-Agent": "Mozilla/5.0"})
    wiki_soup = bs4.BeautifulSoup(wiki_response.text, "html.parser")

    # Haal de titel en intro (eerste paragraaf) op
    title = wiki_soup.find("h1").text.strip()
    paragraphs = wiki_soup.select("p")
    intro = paragraphs[0].text.strip() if paragraphs else "Geen intro gevonden."

    # Scrape volledige inhoud zonder referenties
    content = []
    for p in wiki_soup.select("p"):
        text = p.get_text().strip()
        if text and not text.startswith("["):
            content.append(text)

    return {
        "title": title,
        "wikipedia_url": wiki_link,
        "intro": intro,
        "full_content": "\n\n".join(content[:5])  # Max 5 paragrafen om kort te houden
    }

# 🔍 Voer een zoekopdracht in
query = input("Zoekterm: ")
result = get_wikipedia_content(query)
print(result)
