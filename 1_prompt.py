import itertools
import json

languages = [
    {"name": "🇺🇸 English", "code": "en", "id": 0},
]

voices = [
    {"name": "👩 Female voice", "gender": "female", "language_id": 0, "id": 0, "elevenlabs_id": "K8lgMMdmFr7QoEooafEf"},
    {"name": "👨 Male voice", "gender": "male", "language_id": 0, "id": 1, "elevenlabs_id": "UvSWlWKwkwKAshx25ieK"},
]

names = [
    {"name": "James", "gender": "male", "language_id": 0, "id": 0},
    {"name": "Mary", "gender": "female", "language_id": 0, "id": 1},
    {"name": "Michael", "gender": "male", "language_id": 0, "id": 2},
    {"name": "Jennifer", "gender": "female", "language_id": 0, "id": 3},
    {"name": "John", "gender": "male", "language_id": 0, "id": 4},
    {"name": "Jessica", "gender": "female", "language_id": 0, "id": 5},
]

# Categories with prompt templates for future text generation
categories = [
  {
    "name": "🙏 Support",
    "language_id": 0,
    "id": 0,
    "prompt": {
      "personal": [
        "Create a supportive message where {name} is reassured and comforted, but {name} is not mentioned at the beginning of the sentence. Keep the message soft, calming, and nurturing."
      ],
      "general": [
        "Generate a supportive message without mentioning gender. Use soothing terms like 'precious one' or 'darling', focusing on reassurance and offering a sense of peace and comfort.",
        "Craft a calming, supportive message using endearing language like 'little dove' or 'sweetheart'. Emphasize comfort and encouragement without any gender references.",
        "Compose a gentle message of support, avoiding gendered language. Use tender terms of endearment like 'dearest' or 'beloved' to wrap the listener in warmth and care.",
        "Create a message that provides emotional support, using comforting, non-gendered terms. Incorporate soft imagery like fluffy clouds or warm sunbeams to evoke a sense of safety and care.",
        "Write a supportive message that feels like a gentle embrace, addressing the listener without gender references. Use phrases like 'precious heart' or 'dear one' to convey deep care and understanding."
      ]
    }
  },
  {
    "name": "👍 Affirmation",
    "language_id": 0,
    "id": 1,
    "prompt": {
      "personal": [
        "Write an affirmation where {name} is praised and encouraged, but {name} is mentioned in the middle of the sentence. Focus on appreciation and positive reinforcement."
      ],
      "general": [
        "Create an affirmation that praises and uplifts the listener, without gender references. Use endearing terms like 'bright star' or 'cherished one' to emphasize their unique value and potential.",
        "Compose an affirmation that boosts confidence without mentioning gender, using affectionate phrases like 'treasure' or 'dear heart'. Craft a message that's both supportive and empowering.",
        "Generate a message that affirms the listener's strength and capabilities, avoiding gendered language. Use warm, nurturing terms like 'precious soul' or 'beloved' to create a supportive atmosphere.",
        "Write a positive affirmation that encourages the listener to persist. Avoid gender-specific terms and instead use endearing phrases like 'sweet pea' or 'darling' to convey care and belief in their abilities.",
        "Craft an uplifting affirmation using tender language, like 'little love' or 'sunshine', to express unwavering support without any gender references."
      ]
    }
  },
  {
    "name": "🫵 Motivation",
    "language_id": 0,
    "id": 2,
    "prompt": {
      "personal": [
        "Create a motivational message for {name}, where {name} is mentioned later in the sentence. Focus on encouragement and belief in {name}'s abilities."
      ],
      "general": [
        "Compose a motivational message that inspires the listener to keep moving forward, without gender-specific language. Include encouraging phrases like 'brave heart' or 'shining star'.",
        "Write a motivating message that offers support and encouragement, using terms like 'dear one' or 'precious soul' without referring to the listener's gender.",
        "Generate a motivational message that gently urges the listener to stay strong, avoiding gendered terms. Use warm language and incorporate inspiring imagery like soaring birds or blooming flowers.",
        "Craft a message to motivate the listener, focusing on their inner strength and potential, without gender references. Use affectionate terms like 'sweetheart' or 'cherished one'.",
        "Create a message that motivates the listener to stay focused and determined, while avoiding any gender-specific references. Include uplifting imagery like a phoenix rising or a river flowing steadily."
      ]
    }
  },
  {
    "name": "🎉 Congratulations",
    "language_id": 0,
    "id": 3,
    "prompt": {
      "personal": [
        "Write a congratulatory message for {name}, where {name} is celebrated and praised in the middle of the sentence. The message should express joy and pride in {name}'s achievement."
      ],
      "general": [
        "Compose a celebratory message that congratulates the listener on their achievement, without gender references. Use warm, affectionate language like 'shining star' or 'precious gem'.",
        "Create a message that celebrates the listener's success, avoiding gendered terms. Use endearing phrases like 'dear heart' or 'beloved' to express joy and pride.",
        "Generate a message to congratulate the listener on their accomplishment, using non-gendered language and uplifting imagery like 'radiant sun' or 'soaring eagle'.",
        "Craft a celebratory message that expresses pride and happiness in the listener's success, while avoiding gendered terms. Use warm, comforting language like 'treasured one'.",
        "Write a congratulatory message that makes the listener feel deeply appreciated and recognized, without using gender-specific language. Use tender terms like 'little miracle' or 'precious soul'."
      ]
    }
  },
  {
    "name": "💪 Encouragement",
    "language_id": 0,
    "id": 4,
    "prompt": {
      "personal": [
        "Write an encouraging message for {name}, focusing on {name}'s strength and perseverance. Ensure {name} is not mentioned at the start of the sentence."
      ],
      "general": [
        "Generate an encouraging message that empowers the listener without using gendered terms. Use inspiring imagery like 'mighty oak' or 'resilient wildflower' to convey strength and support.",
        "Create a message that gently encourages the listener to keep going, avoiding any gendered references. Use soft, non-specific terms like 'brave heart' or 'precious soul'.",
        "Compose a message that encourages the listener, focusing on their inner strength and resilience, while avoiding gender-specific language. Use affectionate imagery like 'shining star' or 'steadfast mountain'.",
        "Craft an empowering message that motivates the listener to stay strong, without using gender-specific language. Use warm, comforting phrases like 'dear one' or 'beloved' to convey encouragement.",
        "Write an encouraging message that reassures the listener of their inner power and ability, using affectionate terms like 'sweet soul' and avoiding gendered language."
      ]
    }
  },
  {
    "name": "🎓 Education",
    "language_id": 0,
    "id": 5,
    "prompt": {
      "personal": [
        "Write an educational encouragement message for {name}, focusing on {name}'s progress and learning. Ensure {name} is mentioned in the middle of the sentence."
      ],
      "general": [
        "Create an encouraging message that motivates the listener to continue learning, avoiding gender-specific terms. Use inspiring imagery like 'curious explorer' or 'budding scholar'.",
        "Generate a message that encourages the listener's educational progress, without referring to their gender. Use nurturing terms like 'bright mind' or 'eager learner'.",
        "Compose an educational encouragement message that supports the listener's growth, avoiding gendered references. Use warm, comforting language to emphasize the joy of discovery and learning.",
        "Craft a message that encourages the listener to keep expanding their knowledge, avoiding gendered terms. Use affectionate phrases like 'little genius' or 'inquisitive soul' to make the message feel warm and supportive.",
        "Write a message that gently encourages the listener to explore and learn more, using non-gendered terms like 'precious student' or 'beloved scholar'."
      ]
    }
  },
  {
    "name": "✨ Gratitude",
    "language_id": 0,
    "id": 6,
    "prompt": {
      "personal": [
        "Write a message of gratitude for {name}, expressing appreciation for something kind {name} has done. {name} should be mentioned in the middle of the sentence."
      ],
      "general": [
        "Create a message of gratitude that expresses deep appreciation for the listener, avoiding any gender-specific terms. Use affectionate imagery like 'precious gem' or 'radiant soul'.",
        "Generate a thank-you message that conveys heartfelt gratitude for the listener, without referring to their gender. Use warm language like 'dear heart' or 'beloved friend'.",
        "Compose a message of gratitude that expresses profound appreciation, using non-gendered terms like 'treasured one' and focusing on the impact of their kindness.",
        "Craft a thank-you message that shows deep appreciation for the listener's generosity and care, avoiding gendered terms. Use affectionate phrases like 'sweet angel' to convey warmth.",
        "Write a message of gratitude that makes the listener feel truly valued, without using gendered language. Use tender terms like 'precious soul' or 'cherished one'."
      ]
    }
  },
  {
    "name": "🌟 Recognition",
    "language_id": 0,
    "id": 7,
    "prompt": {
      "personal": [
        "Write a message recognizing {name}'s efforts and accomplishments, where {name} is mentioned in the middle of the sentence. Focus on showing appreciation and pride."
      ],
      "general": [
        "Generate a message that recognizes the listener's efforts, without referring to their gender. Use affectionate language like 'shining star' or 'precious gem' to express admiration.",
        "Create a message that acknowledges the listener's hard work and dedication, avoiding gendered language. Use inspiring imagery like 'mighty oak' or 'soaring eagle' to show appreciation.",
        "Compose a message that recognizes the listener's efforts and accomplishments, without using gender-specific language. Use warm, affectionate terms like 'dear heart' to express pride.",
        "Craft a message that shows recognition for the listener's contributions, avoiding any gendered terms. Use affectionate phrases like 'treasured one' to convey deep appreciation.",
        "Write a message that expresses admiration for the listener's hard work, without referring to gender. Use uplifting language like 'brilliant mind' or 'inspiring soul'."
      ]
    }
  }
]

# Generate personal audio file combinations with prompts
personal_tts = []
for voice, category, name, language in itertools.product(voices, categories, names, languages):
    personal_tts.append({
        "voice_id": voice["id"],
        "category_id": category["id"],
        "name_id": name["id"],
        "language_id": language["id"],
        "audio_file": voice['elevenlabs_id'],
        "symbols": 0,
        "prompt": category["prompt"]['personal'][0].replace('{name}', name['name']) 
        + f" MUST use the person's name {name['name']} in the middle of the message."
    })

# Generate general audio file combinations (five for each category)
general_tts = []
for voice, category, language in itertools.product(voices, categories, languages):
    for i, general_prompt in enumerate(category["prompt"]["general"]):
        general_tts.append({
            "voice_id": voice["id"],
            "category_id": category["id"],
            "name_id": None,
            "language_id": language["id"],
            "audio_file": voice['elevenlabs_id'],
            "symbols": 0,
            "prompt": general_prompt
        })

# Combine both lists
all_tts = personal_tts + general_tts

# Optionally, print or save the result
print(json.dumps(all_tts, indent=2))

# Save to a JSON file
with open("1_prompt.json", "w", encoding='utf-8') as outfile:
    json.dump(all_tts, outfile, indent=2)
