#!/usr/bin/env python

import os
import sys
import json
from openai import OpenAI
from elevenlabs_s3 import VoiceSettings, text_to_speech

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def main():
    # Collect user inputs
    language = input("Enter the language (default is English): ").strip() or 'English'
    voice_gender = input("Enter the voice gender (male/female, default is female): ").strip().lower() or 'female'
    user_name = input("Enter your name (optional): ").strip() or None
    user_gender = input("Enter your gender (male/female, optional): ").strip().lower() or None
    category = input("Enter the category (e.g., support, motivation, consolation): ").strip() or None
    
    # Load or initialize the database
    database_file = 'db.json'
    if not os.path.exists(database_file):
        # 560
        db = {
            "languages": [
                { "name": "🇺🇸 English", "code": "en" },
            ],
            "voices": [
                { "name": "👩 Female voice", "gender": "female", "language_id": 0 },
                { "name": "👨 Male voice", "gender": "male", "language_id": 0 },
            ],
            "names": [
                { "name": "James", "gender": "male", "language_id": 0 },
                { "name": "Mary", "gender": "female", "language_id": 0 },
                { "name": "Michael", "gender": "male", "language_id": 0 },
                { "name": "Jennifer", "gender": "female", "language_id": 0 },
                { "name": "John", "gender": "male", "language_id": 0 },
                { "name": "Jessica", "gender": "female", "language_id": 0 },
            ],
            "categories": [
                { "name": "🙏 Support", "language_id": 0 },
                { "name": "👍 Affirmation", "language_id": 0 },
                { "name": "🫵 Motivation", "language_id": 0 },
                { "name": "🎉 Congratulations", "language_id": 0 },
                { "name": "💪 Encouragement", "language_id": 0 },
                { "name": "🎓 Education", "language_id": 0 },
                { "name": "✨ Gratitude", "language_id": 0 },
                { "name": "🌟 Recognition", "language_id": 0 },
            ],
            "tts": []
        }
        with open(database_file, 'w') as f:
            json.dump(db, f, indent=4)
    else:
        with open(database_file, 'r') as f:
            db = json.load(f)
    
    # Check if language exists
    language_entry = next((d for d in db['languages'] if d["name"].lower() == language.lower()), None)
    if language_entry is None:
        print(f"Error: Language '{language}' not found in the database.")
        sys.exit(1)
    language_id = db['languages'].index(language_entry)
    
    # Check if voice exists
    voice_entry = next(
        (d for d in db['voices'] if d["gender"].lower() == voice_gender.lower() and d["language_id"] == language_id),
        None
    )
    if voice_entry is None:
        print(f"Error: Voice with gender '{voice_gender}' in language '{language}' not found in the database.")
        sys.exit(1)
    voice_id = db['voices'].index(voice_entry)
    elevenlabs_voice_id = voice_entry['elevenlabs_voice_id']
    
    # Generate personalized text using OpenAI API
    prompt = generate_prompt(language, user_name, user_gender, category)
    generated_text = generate_text(prompt)
    
    # Convert text to speech using ElevenLabs TTS
    tts_result = tts(generated_text, elevenlabs_voice_id)
    
    # Update the database and save the text
    update_database(db, database_file, generated_text, tts_result, language_id, voice_id, user_name, user_gender, category)
    
    print("Database and texts updated successfully.")
    print("TTS Result:", tts_result)
    print("Generated Text:", generated_text)
    print("You can access the audio file at:", tts_result.get('s3_presigned_url', 'Local file: ' + tts_result['file_path']))
    
def generate_prompt(language, user_name, user_gender, category):
    # Generate a prompt for the OpenAI API based on the inputs
    if user_name:
        prompt = f"Generate a {category} message in {language} for {user_name}. The message should be warm and personalized. Use the name in the MIDDLE of the text, first communicate to the user with general pleasant addresses."
    else:
        # Use affectionate terms suitable for the user's gender
        if user_gender == 'male':
            affectionate_term = 'buddy'
        elif user_gender == 'female':
            affectionate_term = 'dear'
        else:
            affectionate_term = 'friend'
        prompt = f"Generate a {category} message in {language} for a {affectionate_term}. The message should be warm and encouraging."
    return prompt + """ 
        Don't use the emoji. 
        Communicate with the user like a mom communicates with a small child, affectionately, sweetly. 
        Take into account that this text is a continuation and will stand in the middle of another text.
        Only 100 character affirmation/motivation/support text and nothing else in the reply."""

def generate_text(prompt):
    # Use OpenAI API to generate the text
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use the appropriate model
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    # Extract the assistant's reply
    generated_text = response.choices[0].message.content.strip()
    return generated_text

def tts(text, elevenlabs_voice_id):
    
    return {
        'file_path': 'path/to/audio.mp3',
        's3_file_name': 'audio.mp3',
        's3_bucket_name': 'your_s3_bucket',
        's3_presigned_url': 'https://s3.amazonaws.com/your_s3_bucket/audio.mp3'
    }

    result = text_to_speech(
        text=text,
        elevenlabs_api_key=os.environ.get("ELEVENLABS_API_KEY"),
        output_folder="audio_files",
        aws_s3_bucket_name=os.environ.get("AWS_S3_BUCKET_NAME"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_region_name=os.environ.get("AWS_REGION_NAME"),
        voice_id=elevenlabs_voice_id,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.5,
            use_speaker_boost=True,
        ),
    )

    return result

def update_database(db, database_file, generated_text, tts_result, language_id, voice_id, user_name, user_gender, category):
    # Update the database JSON file and save the text separately
    
    # Handle name
    name_id = None
    if user_name:
        name_entry = next(
            (d for d in db['names'] if d["name"].lower() == user_name.lower() and d["language_id"] == language_id),
            None
        )
        if name_entry is None:
            name_id = len(db['names'])
            db['names'].append({
                "name": user_name,
                "gender": user_gender or 'unknown',
                "language_id": language_id
            })
        else:
            name_id = db['names'].index(name_entry)
    
    # Handle category
    category_entry = next(
        (d for d in db['categories'] if d["name"].lower() == category.lower() and d["language_id"] == language_id),
        None
    )
    if category_entry is None:
        category_id = len(db['categories'])
        db['categories'].append({
            "name": category,
            "language_id": language_id
        })
    else:
        category_id = db['categories'].index(category_entry)
    
    # Handle TTS entry
    tts_entry = {
        "voice_id": voice_id,
        "category_id": category_id,
        "name_id": name_id,
        "language_id": language_id,
        "audio_file": tts_result['s3_file_name'],
        "symbols": len(generated_text)
    }
    tts_id = len(db['tts'])
    db['tts'].append(tts_entry)
    
    # Save database
    with open(database_file, 'w') as f:
        json.dump(db, f, indent=4)
    
    # Save text in texts.json
    texts_file = 'texts.json'
    if not os.path.exists(texts_file):
        texts_db = {}
    else:
        with open(texts_file, 'r') as f:
            texts_db = json.load(f)
    texts_db[str(tts_id)] = generated_text
    with open(texts_file, 'w') as f:
        json.dump(texts_db, f, indent=4)
    
if __name__ == "__main__":
    main()
