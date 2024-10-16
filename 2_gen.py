import json
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

def generate_text(prompt):
    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://honeyaudio.github.io",
                "X-Title": "honey 🍯 audio".encode('utf-8'),
            },
            messages=[
                {"role": "system", "content": "You are a loving parent who will always affectionately support your child by addressing them with affectionate words."},
                {"role": "user", "content": "Message up to 200 characters, as pleasant as possible, free form, use more punctuation. Do not write anything extra besides the message, do not use emoji. It is IMPORTANT that this message is the middle of a larger text, don't end it with a short slogan, let it be understated. " 
                       + prompt}],
            model="openai/gpt-4o-mini",
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating text for prompt: {prompt}")
        print(e)
        return None

with open("1_prompt.json", "r", encoding='utf-8') as infile:
    tts_data = json.load(infile)

for entry in tts_data:
    if "prompt" in entry:
        generated_text = generate_text(entry["prompt"])
        print("Text:", generated_text)
        if generated_text:
            entry["generated_text"] = generated_text
            entry["symbols"] = len(generated_text)
        
        del entry["prompt"] 

with open("2_gen.json", "w", encoding='utf-8') as outfile:
    json.dump(tts_data, outfile, indent=2)