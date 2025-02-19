export default async function handler(req, res) {
  const query = req.query.params;

  if (!query) {
    return res.status(400).json({ error: "No search query" });
  }

  try {
    let formattedQuery = query.trim().replace(/ /g, "+");
    let url = `https://api.codetabs.com/v1/proxy/?quest=https://search.yahoo.com/search?p=${formattedQuery}`;

    const response = await fetch(url);
    const text = await response.text();

    let links = [...text.matchAll(/<a[^>]+href="(https?:\/\/[^"]+)"[^>]*>(.*?)<\/a>/g)]
      .map(m => ({
        url: m[1].replace("wikipedia.org", "m.wikipedia.org"), // Zet Wikipedia om naar de mobiele versie
        title: m[2].replace(/<[^>]+>/g, '').trim()
      }))
      .filter(link => link.title && link.url.includes("m.wikipedia.org"));

    if (links.length) {
      return res.status(200).json(links);
    } else {
      return res.status(404).json({ error: "Geen Wikipedia-links gevonden" });
    }
  } catch (error) {
    return res.status(500).json({ error: "Er is een fout opgetreden bij het ophalen van de gegevens" });
  }
}
