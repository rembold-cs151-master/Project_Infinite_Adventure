from openai import OpenAI # You'll need to install with pip install openai
import requests
import os
from io import BytesIO
from PIL import Image

# Note: if you use your own key to generate some images, you probably want to
# not upload it back to your submission. Or make sure you've set up very tight
# limits on what can be charged to that key.
client = OpenAI(api_key="your personal OpenAI key")

def generate_img(scene_description, scene_key):
    path = f"./imgs/{scene_key}.jpg"
    if os.path.exists(path): # Don't generate an image an existing picture
        return path

    prompt = f"Craft a vivid and engaging illustration for an immersive game in the style of an award winning Digital Painting, designed to capture the imagination and awe of its audience, bringing to life a world that players can lose themselves in. The art style should evoke a sense of wonder, blending elements of fantasy and realism to create a visually stunning experience. Colors should be rich and vibrant, with lighting that enhances the mood and depth of the scene. Critically important: NEVER ADD TEXT TO THE ILLUSTRATION. Render this scene: {scene_description}"

    response = client.images.generate(
      model="dall-e-3",   # the image model. DallE-3 costs around 4 cents per image
      prompt=prompt,
      size="1024x1024",   # The default size
      quality="standard", # The cheapest quality (which is usually good enough)
      n=1,                # How many images you want back. Here, we want just 1
    )

    # get the url
    image_url = response.data[0].url

    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    image = image.resize((600, 600)) # Resize to 600x600 to match other images

    # Check if the image has an alpha channel and convert it to RGB if it does
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    image.save(path, "JPEG")
    return path

    
