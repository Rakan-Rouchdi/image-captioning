from dotenv import load_dotenv
import os
import openai

# Load API key from .env file
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_prompt(object_labels, spatial_descriptions, environment=None):
    """
    Build a structured prompt from objects, spatial relationships, and environment.
    """
    objects_str = ", ".join(sorted(set(object_labels)))
    spatial_str = "; ".join(spatial_descriptions)

    base = f"Generate a short, fluent, and accessible caption for an image that contains the following objects: {objects_str}."
    
    if spatial_str:
        base += f" The spatial relationships between the objects are: {spatial_str}."
    
    if environment:
        base += f" The environment appears to be: {environment}."

    base += " Make the caption descriptive but concise, suitable for a screen reader."
    return base

def generate_caption(prompt, model="gpt-3.5-turbo"):
    """
    Send the structured prompt to OpenAI and return the caption.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert image captioning assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ Error during GPT caption generation:", e)
        return None
