from flask import Flask
from flask_cors import CORS
from openai import OpenAI
import requests, dotenv, os, time

dotenv.load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')

current_wallpaper = {
    "url": None,
    "description": None
}

last_updated_date = time.localtime().tm_mday

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = Flask(__name__)
CORS(app)

def create_wallpaper_description(image_url, location):
    system_prompt = '''
    Generate a concise sentence that describes the image by analyzing its content.

    # Steps

    - Identify the main subject or features of the image.
    - Review metadata for additional context like location or significance.
    - Combine both to create a brief, evocative sentence.

    # Output

    A single, descriptive sentence.

    # Examples

    - "The green leaves reflect the fragility of the forest."
    - "China’s river stands as a national landmark."
    - "New York’s skyline is world-renowned."
    - "This beach sunset is breathtaking."
    - "An ideal spot for relaxation after a long day."
    - "Newport Beach offers stunning views and attractions."
    - "Skyscrapers provide extraordinary views in big cities."
    - "Palm Springs is known for its deserts and nightlife."

    # Notes

    - Ensure relevance to both image and metadata.
    - Focus on visual and contextual appeal.
    '''

    if location == None:
        location = "location not specified"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Location: " + location},
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                    },
                ],
            }
        ],
        max_tokens=500
    )

    description = response.choices[0].message.content

    return description

def set_new_wallpaper():
    global current_wallpaper

    url = "https://api.unsplash.com/photos/random?orientation=landscape&topics=6sMVjTLSkeQ&client_id=" + UNSPLASH_ACCESS_KEY
    response = requests.get(url)
    data = response.json()

    full_url = data['urls']['full']
    regular_url = data['urls']['regular']
    location = data['location']['name']

    description = create_wallpaper_description(regular_url, location)

    current_wallpaper = {
        "url": full_url,
        "description": description
    }

@app.route('/api/daily-wallpaper')
def daily_wallpaper():
    global current_wallpaper, last_updated_date

    current_date = time.localtime().tm_mday

    if current_date != last_updated_date:
        set_new_wallpaper()
        last_updated_date = current_date

    return current_wallpaper

@app.route('/api/reset-wallpaper')
def reset_wallpaper():
    set_new_wallpaper()
    return "200 OK"

if __name__ == '__main__':
    set_new_wallpaper()
    app.run(host="0.0.0.0", port=5509)