import requests
from bs4 import BeautifulSoup

def get_wikipedia_intro(query):
    try:
        search_url = f"https://html.duckduckgo.com/html?q={query} Wikipedia"
        response = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        # Zoek de eerste Wikipedia-link
        wiki_link = None
        for a in soup.select(".result__title a"):
            href = a.get("href", "")
            if "wikipedia.org" in href:
                wiki_link = href
                break

        if not wiki_link:
            return {"error": "Geen Wikipedia-pagina gevonden."}

        # Wikipedia-pagina openen en eerste paragraaf scrapen
        wiki_response = requests.get(wiki_link, headers={"User-Agent": "Mozilla/5.0"})
        wiki_soup = BeautifulSoup(wiki_response.text, "html.parser")
        first_paragraph = wiki_soup.select_one("p")

        return {
            "wikipedia_url": wiki_link,
            "intro": first_paragraph.text.strip() if first_paragraph else "Geen intro gevonden."
        }
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def handler(request):
    # Verkrijg query uit de request
    query = request.args.get('query', '')
    
    if not query:
        return {
            "statusCode": 400,
            "body": "Error: Missing 'query' parameter."
        }
    
    result = get_wikipedia_intro(query)
    
    return {
        "statusCode": 200,
        "body": result
    }
