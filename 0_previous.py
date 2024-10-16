import os
from elevenlabs_s3 import VoiceSettings, text_to_speech

from dotenv import load_dotenv
load_dotenv()

text="Sweetheart, you're gonna make it."

try:
    result = text_to_speech(
        text=text,
        elevenlabs_api_key=os.environ.get("ELEVENLABS_API_KEY"),
        aws_s3_bucket_name=os.environ.get("AWS_S3_BUCKET_NAME"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_region_name=os.environ.get("AWS_REGION_NAME"),
        voice_id="K8lgMMdmFr7QoEooafEf",
        model_id="eleven_turbo_v2_5",
        # previous_text="Sweetie, there's something I'd like to say in your ear:",
        # next_text="My honey. My dear person. You are incredible. You are the kindest person on earth",
        previous_request_ids=["iXwjt8SA344P5PcHat7G"],
        next_request_ids=["vuz10xzwF1YyJw0y4jsC"],
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.5,
            use_speaker_boost=True,
        ),
    )

    print(result)
except Exception as e: print(e)