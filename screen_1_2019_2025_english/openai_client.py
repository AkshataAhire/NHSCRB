import time
from openai import OpenAI

def create_openai_client():
    return OpenAI(api_key="API KEY")

def call_gpt_api(client, system_prompt, user_prompt, model="gpt-4o", max_retries=3):
    """
    Sends a prompt to the GPT model and returns the response text.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[Error - Attempt {attempt + 1}] {e}")
            time.sleep(5)
    
    return None
