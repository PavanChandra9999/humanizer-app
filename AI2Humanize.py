import google.generativeai as genai
import os
import re

# --- CONFIGURATION ---
# Replace this with your actual API key
GOOGLE_API_KEY = "AIzaSyCNciZZgz5NLGair60wxr22GSrc9kyL-J4"

if not GOOGLE_API_KEY or GOOGLE_API_KEY == "AIzaSyCNciZZgz5NLGair60wxr22GSrc9kyL-J4":
    print("❌ Error: You must paste your Google API Key in the script.")
    exit()

genai.configure(api_key=GOOGLE_API_KEY)
# Using the model you specified (valid in your 2025 context)
model = genai.GenerativeModel('gemini-2.5-pro')

# --- HELPER: REMOVE FORMATTING ---
def clean_text(text):
    """
    Removes Markdown artifacts like **bold**, *italics*, and # headers
    to ensure the output is pure plain text.
    """
    # Remove bold/italic markers (* or _)
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'_+', '', text)
    # Remove header markers (#)
    text = re.sub(r'#+\s', '', text)
    # Remove code block ticks (```)
    text = text.replace('```', '')
    return text.strip()

# --- AGENT 1: GENERATOR ---
def generate_content(prompt):
    try:
        # We explicitly ask for plain text in the system instruction
        sys_instruction = "Generate the content in plain text only. Do not use markdown formatting like asterisks (*), bold, or headers."
        response = model.generate_content(f"{sys_instruction}\n\nUser Request: {prompt}")
        return clean_text(response.text)
    except Exception as e:
        return f"Error: {e}"

# --- AGENT 2: HUMANIZER ---
def humanize_content(ai_text):
    try:
        humanize_prompt = f"""
        Act as a professional human editor.
        Rewrite the following text to make it sound more human-like.
        
        RULES:
        1. Output PLAIN TEXT only. No markdown, no asterisks, no special formatting.
        2. Use varied sentence structures.
        3. Use a conversational, engaging tone (mix 2nd and 3rd person).
        4. Remove robotic transitions.
        5. Intentionally make some minor typos (e.g., 'mistkae', 'smiple') to mimic human speed.
        
        Text to rewrite:
        {ai_text}
        """
        response = model.generate_content(humanize_prompt)
        return clean_text(response.text)
    except Exception as e:
        return f"Error: {e}"

# --- MAIN APP LOOP (The Local Interface) ---
def main():
    print("=================================================")
    print("🤖 AI Content Agent (Local Terminal Version)")
    print("   Type 'exit' to quit.")
    print("=================================================\n")

    while True:
        # 1. Get User Input
        user_prompt = input("\n📝 Enter your prompt: ")
        if user_prompt.lower() in ['exit', 'quit']:
            break
        
        print("\n⏳ Generating content...")
        
        # 2. Generate
        ai_result = generate_content(user_prompt)
        print("\n--- [AI Generated Version] ---")
        print(ai_result)
        print("------------------------------")

        # 3. Ask to Humanize
        choice = input("\n✨ Humanize this content? (y/n): ")
        if choice.lower() == 'y':
            print("\n⏳ Humanizing...")
            human_result = humanize_content(ai_result)
            
            print("\n--- [Humanized Version] ---")
            print(human_result)
            print("---------------------------")
        else:
            print("Okay, starting over.")

if __name__ == "__main__":
    main()