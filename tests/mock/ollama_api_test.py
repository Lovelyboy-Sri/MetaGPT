import ollama, requests, json

DEFAULT_MODEL = "mistral:7b"
OLLAMA_API_URL = "https://03ef5b24c906.ngrok-free.app/api/generate"

def run_ollama_query(model: str, prompt: str):
    """
    Sends a prompt to the Ollama API and streams back the model's response.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False  # Set True if you want streaming output
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        
        # Ollama returns JSON; extract text part
        data = response.json()
        print("✅ Model Response:\n")
        print(data)

    except requests.exceptions.RequestException as e:
        print("❌ Error communicating with Ollama API:", e)

# Example usage
if __name__ == "__main__":
    model_name = "llama3.1:8b"  # Change to any model available in your Ollama setup
    user_prompt = "Write a Python function that reverses a string."
    
    run_ollama_query(model_name, user_prompt)
