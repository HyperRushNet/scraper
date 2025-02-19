async function sendMessageToAI(req, res) {
    try {
        // Haal de berichtinhoud op uit de URL-paden
        const message = req.query.params || "Geen bericht meegegeven"; // Als er geen bericht is, gebruik een fallback bericht

        // Statisch systeembericht
        const messages = [
            { 
                "role": "system", 
                "content": "You are an AI that always responds in valid HTML but without unnecessary elements like <!DOCTYPE html>, <html>, <head>, or <body>. Only provide the essential HTML elements, such as <p>text</p>, or other inline and block elements depending on the context. Style links without the underline and #5EAEFF text. Mathjax is integrated. When the user wants to generate code, give them a link to /codegenerate.html"
            },
            { 
                "role": "user", 
                "content": message // Het bericht uit de URL gebruiken
            }
        ];

        const response = await fetch('https://text.pollinations.ai/openai', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                messages: messages,
                max_tokens: 100
            }),
        });

        if (!response.ok) {
            throw new Error(`API response failed with status: ${response.status}`);
        }

        const data = await response.json();

        if (data.choices && data.choices.length > 0) {
            // Stuur alleen de pure tekst terug zonder JSON
            res.status(200).send(data.choices[0].message.content);
        } else {
            res.status(400).send("Geen keuze gevonden in de API-respons.");
        }
    } catch (error) {
        console.error("Fout gedetailleerd:", error);
        res.status(500).send("Er is een fout opgetreden, probeer het later opnieuw.");
    }
}

// Exporteer de serverless functie (werkt met Vercel)
export default sendMessageToAI;
