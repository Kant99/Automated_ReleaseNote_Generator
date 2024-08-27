import requests
import sys
import os

def generate_commit_message(old_code, new_code):
    """
    Generate a commit message based on the differences between old_code and new_code using the Gemini model.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    endpoint = "https://api.google.com/v1/generate"  # Replace with actual Gemini API endpoint
    
    prompt = (
        "Generate a meaningful commit message based on the following code changes:\n\n"
        "Previous Code:\n"
        f"{old_code}\n\n"
        "Modified Code:\n"
        f"{new_code}\n\n"
        "Commit Message:"
    )

    response = requests.post(
        endpoint,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "prompt": prompt,
            "max_tokens": 50  # Adjust as needed
        }
    )

    response.raise_for_status()
    commit_message = response.json().get("choices")[0].get("text").strip()
    return commit_message

if __name__ == "__main__":
    old_code = sys.argv[1]
    new_code = sys.argv[2]
    
    message = generate_commit_message(old_code, new_code)
    print(message)
