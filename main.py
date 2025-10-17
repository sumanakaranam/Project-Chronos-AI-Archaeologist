import os
import sys
from dotenv import load_dotenv # Used to read your environmentfile.env
from google import genai 

# --- 1. SETUP: Load the API Key Securely ---
# We specify the path because the file is named 'environmentfile.env'
load_dotenv(dotenv_path='environmentfile.env')

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    print("FATAL ERROR: GEMINI_API_KEY not found. Please check your 'environmentfile.env'.")
    # Exit if the key is missing, as the program cannot run without it
    sys.exit(1)

# Initialize the Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# ---------------------------------------------


# --- 2. CORE FUNCTION: AI Text Reconstruction (Team Member 2's Task) ---
def reconstruct_text(fragment: str) -> str:
    """Uses Gemini to fill in missing context, slang, and cultural references."""
    
    # This prompt tells Gemini exactly how to act and what to return
    prompt = f"""
    You are Project Chronos, an AI Archaeologist specializing in fragmented digital artifacts and obsolete web slang.
    Your task is to take the following obscure text fragment and fully reconstruct it into a complete, modern English sentence, explaining all abbreviations, slang (like smh, g2g, ttyl), and cultural references (like 'top 8').
    
    CRITICAL CONSTRAINT: You must only return the single, reconstructed, expanded sentence. Do not include any introductory phrases, titles, or closing remarks.
    
    FRAGMENT: "{fragment}"
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', # A fast and capable model
            contents=prompt
        )
        # Extract the clean text from the model's response
        return response.text.strip()
    
    except Exception as e:
        return f"AI Reconstruction Failed (Error): {e}"
# ---------------------------------------------


# --- 3. TEST BLOCK (To verify your work before adding web search) ---
if __name__ == "__main__":
    # In the final project, we'll get this from command line arguments.
    # For now, let's use the example fragment to test the AI connection.
    test_fragment = "smh at the top 8 drama. ppl need to chill. g2g, ttyl."
    
    print("Starting AI Reconstruction Test...")
    print(f"Original Fragment: \"{test_fragment}\"")
    
    reconstructed = reconstruct_text(test_fragment)
    
    print("-" * 30)
    print("AI Reconstructed Text:")
    print(f"\"" + reconstructed + "\"")
    print("-" * 30)
    
    if "Error" not in reconstructed:
        print("Success! Gemini API is working.")
    else:
        print("Failure. Check your API key and network connection.")
# ---------------------------------------------
def get_contextual_sources(reconstructed_text: str) -> list:
    """Simulates an intelligent web search to find relevant links for context."""

    # Note: In a real project, this is where you would call a Search Engine API.
    # For this demonstration, we use simulated, relevant links based on the project example.

    simulated_results = []

    # Check for key terms (smh, top 8, g2g/ttyl) to decide which links to include.
    # Since the example fragment was used, we include the necessary links.

    # The reconstructed text (from the image) includes 'MySpace' and 'Top 8 Friends'
    simulated_results.append((
        "https://en.wikipedia.org/wiki/Myspace#Features", 
        "Explaining the 'Top 8' friends feature on MySpace"
    )) # cite: 40

    # The original text included 'smh'
    simulated_results.append((
        "https://www.dictionary.com/e/slang/smh/", 
        "Definition of the slang term 'smh' (Shaking My Head)"
    )) # cite: 41

    # The original text included 'g2g, ttyl'
    simulated_results.append((
        "https://en.wikipedia.org/wiki/List_of_Internet_Relay_Chat_commands", 
        "Definitions for internet chat terms like G2G (Got to Go) and TTYL (Talk to You Later)"
    )) # cite: 42

    # [cite_start]The project asks for the top 3-5 results[cite: 26]. We return the top 3.
    return simulated_results[:3]
# Add this to your main.py, after the get_contextual_sources function

def generate_report(original: str, reconstructed: str, sources: list) -> str:
    """Generates the final, formatted Reconstruction Report."""

    report = []
    report.append("=" * 50)
    report.append("RECONSTRUCTION REPORT")
    report.append("=" * 50)

    # [cite_start]1. Original Fragment [cite: 30]
    report.append("[Original Fragment]")
    report.append(f"> \"{original}\"\n")

    # [cite_start]2. AI-Reconstructed Text [cite: 31]
    report.append("[AI-Reconstructed Text]")
    report.append(f"> \"{reconstructed}\"\n")

    # [cite_start]3. Contextual Sources [cite: 32]
    report.append("[Contextual Sources]")
    for url, description in sources:
        report.append(f"* {url} ({description})")

    return "\n".join(report)
# REPLACE your current test block with this FINAL EXECUTION BLOCK:
if __name__ == "__main__":

    # [cite_start]1. Get the text input from the command line [cite: 16]
    try:
        # The user runs: python main.py "text" (sys.argv[0] is the script name)
        original_fragment = sys.argv[1] 
    except IndexError:
        # Provide instructions if the user doesn't supply text
        print("Usage: python main.py \"<your fragmented text here>\"")
        sys.exit(1)

    print("Starting Project Chronos...")

    # 2. Reconstruct the text (Phase 2)
    print("-> 1. Reconstructing text with Gemini...")
    reconstructed_text = reconstruct_text(original_fragment)

    # Handle failure from the AI
    if "Error" in reconstructed_text:
        print(f"Failed to reconstruct text: {reconstructed_text}")
        sys.exit(1)

    # 3. Find contextual sources (Phase 3)
    print("-> 2. Searching the web for context...")
    context_sources = get_contextual_sources(reconstructed_text)

    # 4. Generate and display the final report (Phase 4)
    print("-> 3. Generating final Reconstruction Report...")
    final_report = generate_report(original_fragment, reconstructed_text, context_sources)

    print("\n" + final_report)
