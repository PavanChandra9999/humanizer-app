from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

app = Flask(__name__, template_folder='.')

# Ensure you have GOOGLE_API_KEY in your .env file
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-pro')

# --- PROMPT TEMPLATES ---
PROMPT_LOW = """
Act as a professional editor. Polish the text below.
Rules:
1. Fix grammar and sentence flow.
2. Keep the professional tone.
3. Remove robotic transitions (e.g., "In conclusion", "Furthermore").
"""

PROMPT_MEDIUM = """
Act as a casual blogger. Rewrite the text below to be conversational.
Rules:
1. Use contractions (can't, won't, I'm).
2. Ask 1 or 2 rhetorical questions.
3. Sound confident but personal.
"""

PROMPT_HIGH = """
Act as a casual, opinionated human writer. Rewrite the text below completely.
You MUST follow these STRICT RULES to avoid AI detection:
1. Burstiness: Mix very short sentences (2-4 words) with very long, winding ones.
2. High Perplexity: Choose unexpected words.
3. Start with Conjunctions: Start sentences with "And", "But", "So".
4. BANNED WORDS: "delve", "tapestry", "landscape", "nuance", "crucial".
5. Contractions: ALWAYS use "can't", "won't", "it's".
6. Fragments: Use sentence fragments. Like this.
7. Run-ons: Occasionally use a run-on sentence.
8. Idioms: Use phrases like "hit the nail on the head".
9. Subjectivity: Use "I feel," "In my opinion."
10. Hedging: Use "probably," "sort of."
11. No Lists: Write in paragraphs only.
12. No Markdown: NO bold (**), NO italics (*).
13. Typos: Include 1 intentional minor typo.
14. Slang: Use mild slang like "totally".
15. Digressions: Go slightly off-topic.
16. Pacing: Fast parts and slow parts.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt')
    if not prompt: return jsonify({"error": "No prompt provided"}), 400

    try:
        response = model.generate_content(f"Write a plain text response to: {prompt}")
        return jsonify({"result": response.text.replace('**', '').replace('##', '').strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/humanize', methods=['POST'])
def humanize():
    data = request.json
    text = data.get('text')
    intensity = data.get('intensity', 100)
    keywords = data.get('keywords', '')

    if not text: return jsonify({"error": "No text provided"}), 400

    if intensity < 35:
        base_prompt = PROMPT_LOW
    elif intensity < 75:
        base_prompt = PROMPT_MEDIUM
    else:
        base_prompt = PROMPT_HIGH

    keyword_instruction = ""
    if keywords:
        keyword_instruction = f"\nCRITICAL RULE: Do NOT change, remove, or translate the following words/phrases: {keywords}\n"

    final_prompt = base_prompt + keyword_instruction + "\nTEXT TO REWRITE:\n" + text

    try:
        response = model.generate_content(final_prompt)
        return jsonify({"result": response.text.replace('**', '').replace('##', '').strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)