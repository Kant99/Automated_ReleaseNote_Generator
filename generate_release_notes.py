import os
import subprocess
import google.generativeai as genai

# Initialize Google Generative AI with the model
model = genai.GenerativeModel('gemini-1.5-flash')

def get_commits_since_last_tag():
    """Get commit messages since the last tag."""
    try:
        # Get the most recent tag
        latest_tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode('utf-8').strip()
        # Get commits since the latest tag
        commits = subprocess.check_output(['git', 'log', f'{latest_tag}..HEAD', '--oneline']).decode('utf-8').strip()
        return commits
    except subprocess.CalledProcessError as e:
        print(f"Error fetching commits: {e}")
        return ""

def generate_release_notes(commits):
    """Generate release notes using Google Generative AI."""
    prompt = f"Generate release notes for the following commits:\n{commits}"
    
    # Generate text using the model
    response = model.generate_text(prompt=prompt, max_tokens=500)
    
    # Extract the generated text
    release_notes = response['text']
    return release_notes

def main():
    # Get commit messages since the last tag
    commits = get_commits_since_last_tag()
    
    if not commits:
        print("No commits found or error retrieving commits.")
        return
    
    # Generate release notes
    release_notes = generate_release_notes(commits)

    # Write release notes to a file
    with open('release_notes.md', 'w') as file:
        file.write(release_notes)
    print("Release notes generated and saved to release_notes.md")

if __name__ == "__main__":
    main()
