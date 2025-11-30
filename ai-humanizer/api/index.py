from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

# Initialize Flask
app = Flask(__name__, template_folder='../templates')

# Configure Gemini
# We use os.environ to get the key securely from Vercel settings
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-pro')
# test

# --- THE 50-POINT PROMPT ---
HUMANIZE_PROMPT = """
Act as a casual, opinionated human writer. Rewrite the text below completely.
You MUST follow these 50 STRICT RULES to avoid AI detection:

1. Burstiness: Mix very short sentences with very long, winding ones.
2. High Perplexity: Choose unexpected words.
3. Start with Conjunctions: Start sentences with "And", "But", "So".
4. BANNED WORDS: "delve", "tapestry", "landscape", "nuance", "crucial".
5. Contractions: ALWAYS use "can't", "won't", "it's".
6. Fragments: Use sentence fragments. Like this.
7. Run-ons: Occasionally use a run-on sentence.
8. Vague Words: Use "stuff", "things".
9. Idioms: Use "hit the nail on the head".
10. Subjectivity: Use "I feel," "In my opinion."
11. Hedging: Use "probably," "sort of."
12. Direct Address: Talk to the reader ("You know?").
13. No Lists: Write in paragraphs only.
14. No Markdown: NO bold (**), NO italics (*).
15. Typos: Include 1 intentional minor typo.
16. Slang: Use mild slang like "totally".
17. Fillers: Start with "Well," or "Honestly."
18. Simplification: Explain like I'm 12.
19. Transitions: AVOID "Furthermore," "In conclusion."
20. Casual Transitions: Use "Anyway," "By the way."
21. Hyperbole: Exaggerate slightly.
22. Understatement: Downplay things.
23. Sensory Details: How does it feel/look?
24. Empathy: Acknowledge the reader.
25. Digressions: Go slightly off-topic.
26. Lowercase Emphasis: occasionally use lowercase.
27. Exclamation Points: Use them!
28. Question Tags: End with ", right?".
29. No "Introduction": Just start writing.
30. No "Summary": Just stop.
31. Pacing: Fast parts and slow parts.
32. Preserve Meaning: Keep the core message.
(Add the rest of your rules mentally or paste the full list here)

TEXT TO REWRITE:
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        # Standard Generation
        response = model.generate_content(f"Write a plain text response to: {prompt}")
        clean_text = response.text.replace('**', '').replace('##', '').strip()
        return jsonify({"result": clean_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/humanize', methods=['POST'])
def humanize():
    data = request.json
    text_to_humanize = data.get('text')

    if not text_to_humanize:
        return jsonify({"error": "No text provided"}), 400

    try:
        # 50-Point Humanization
        final_prompt = HUMANIZE_PROMPT + "\n" + text_to_humanize
        response = model.generate_content(final_prompt)
        clean_text = response.text.replace('**', '').replace('##', '').strip()
        return jsonify({"result": clean_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Required for Vercel to identify the entry point
if __name__ == '__main__':
    app.run(debug=True)