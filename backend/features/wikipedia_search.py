import re
import requests
import json
import time
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def search_wikipedia(query):
    # 1. Remove the word "wikipedia" anywhere, case-insensitively
    clean = re.sub(r'\bwikipedia\b', '', query, flags=re.IGNORECASE).strip()
    if not clean:
        return "What do you want to search on Wikipedia?"

    # 2. Remove common stop words at the beginning (only, to keep meaningful phrases)
    stop_words = {'about', 'of', 'for', 'on', 'the', 'a', 'an', 'to', 'from', 'with', 'by'}
    words = clean.split()
    # Keep removing stop words from the front until we hit a non-stop word
    while words and words[0].lower() in stop_words:
        words = words[1:]
    clean = ' '.join(words)

    # 3. If after removal the query is empty, ask again
    if not clean:
        return "Please specify what you want to search for on Wikipedia."

    # (Optional) Capitalize the first letter of each word for proper names – but be careful!
    # clean = ' '.join(w.capitalize() for w in clean.split())  # only if needed

    # Debug: print what we actually search
    print(f"DEBUG: searching Wikipedia for: '{clean}'")

    # Wikipedia API request (unchanged)
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": clean,
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "redirects": True
    }
    headers = {
        "User-Agent": "JarvisAssistant/1.0 (https://github.com/yourusername/jarvis; your-email@example.com)"
    }

    max_retries = 3
    delay = 1

    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", delay))
                print(f"Rate limit hit. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                delay *= 2
                continue
            response.raise_for_status()
            break
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                print(f"Timeout, retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
                continue
            return "The request to Wikipedia timed out. Please try again."
        except requests.exceptions.ConnectionError:
            return "Could not connect to Wikipedia. Please check your internet connection."
        except requests.exceptions.HTTPError as e:
            if attempt < max_retries - 1:
                print(f"HTTP error {e.response.status_code}, retrying...")
                time.sleep(delay)
                delay *= 2
                continue
            return f"Wikipedia returned an error: {e}"
        except Exception as e:
            return f"Sorry, I couldn't search Wikipedia right now. Error: {str(e)}"

    try:
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page in pages.items():
            if "missing" in page:
                return f"No Wikipedia page found for '{clean}'. Please try a different term."
            extract = page.get("extract", "").strip()
            if not extract:
                return f"Sorry, I couldn't find any content for '{clean}'."
            sentences = extract.split(". ")
            summary = ". ".join(sentences[:3]) + "."
            return summary
        return "Sorry, I couldn't find that on Wikipedia."
    except json.JSONDecodeError:
        return "Wikipedia service returned invalid data. Please try again later."