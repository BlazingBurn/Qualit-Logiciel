import os
import subprocess
import anthropic

# Step 1: Capture the output of `git diff`
def get_git_diff():
    try:
        result = subprocess.run(['git', 'diff', 'HEAD~1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error obtaining git diff: {e.stderr}"

# Step 2: Use the captured diff output as the message content
diff_content = get_git_diff()

try:
    ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
except KeyError:
    ANTHROPIC_API_KEY = "Token not available!"
    
client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1000,
    temperature=0,
    system="You are a Lead developer. Analyse the code and return recommendatation.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": diff_content
                }
            ]
        }
    ]
)
print(message.content)