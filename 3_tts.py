import json
import os
from elevenlabs_s3 import text_to_speech, VoiceSettings
from dotenv import load_dotenv
load_dotenv()

elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY")
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
aws_s3_bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")
aws_region_name = os.environ.get("AWS_REGION_NAME")
aws_s3_output_folder = "tts"

with open("2_gen.json", "r", encoding='utf-8') as infile:
    tts_data = json.load(infile)

def generate_speech(text, voice_id):
    try:
        result = text_to_speech(
            text=text,
            elevenlabs_api_key=elevenlabs_api_key,
            aws_s3_output_folder=aws_s3_output_folder,
            aws_s3_bucket_name=aws_s3_bucket_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_region_name=aws_region_name, 
            voice_id=voice_id,
            model_id="eleven_turbo_v2_5",
            previous_request_ids=["iXwjt8SA344P5PcHat7G"],
            next_request_ids=["vuz10xzwF1YyJw0y4jsC"],
            voice_settings=VoiceSettings(
                stability=0.5, 
                similarity_boost=0.75, 
                style=0.5,
                use_speaker_boost=True
            )
        )
        print(f"Audio generated: {result["s3_file_name"]}")
        return result
    except Exception as e:
        print(f"Error generating speech for text: {text}")
        print(e)
        return None

for entry in tts_data:
    if "generated_text" in entry and entry["generated_text"]:
        generated_text = entry["generated_text"]
        voice_id = entry["audio_file"]

        speech_result = generate_speech(generated_text, voice_id)

        if speech_result:
            entry["audio_file"] = speech_result.get("s3_file_name")
        
        del entry["generated_text"]

with open("3_tts.json", "w", encoding='utf-8') as outfile:
    json.dump(tts_data, outfile, indent=2)

print("TTS generation completed and saved to 3_tts.json")
