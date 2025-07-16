# utils/caption.py
from dotenv import load_dotenv
import openai
import os

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_prompt(objects, relationships, environment, style="default", context=""):
    """
    Build a rich and natural prompt for GPT to generate a first-person caption
    based on visual cues (objects, spatial hints, environment) and the desired tone.
    """

    style_prefix = {
        "Humorous": "Write a funny, witty first-person caption inspired by this scene.",
        "Dramatic": "Write a dramatic, cinematic first-person caption inspired by this moment.",
        "Poetic": "Write a poetic, imaginative first-person caption that captures the mood of the scene.",
        "Instagram": "Write an instagram-like, trendy, new gen, first-person caption for a post.",
        "Professional": "Write a clear, thoughtful first-person caption suitable for a personal blog.",
        "Default": "Write a natural, first-person caption that describes the scene casually and clearly."
    }.get(style, "Write a natural, first-person caption that describes the scene casually and clearly.")

    # Visual cues as supporting context, not for literal output
    object_part = f"Objects in the scene: {', '.join(objects)}." if objects else ""
    relation_part = f"Relative positions between them: {', '.join(relationships)}." if relationships else ""
    environment_part = f"Scene context: {environment}."
    context_part = f"Here is additional information/context from the user: {context}"

    # Prompt for GPT
    prompt = (
        f"{style_prefix}\n"
        "Use the following visual cues to imagine the moment and write a caption that feels human, relatable, and natural.\n"
        f"{object_part}\n"
        f"{relation_part}\n"
        f"{environment_part}\n"
        f"{context_part}\n"
        "Do not name or list the objects directly or literally. Don’t describe their spatial relationships or positions. Instead, use them to mentally visualise the photo.\n"
        "Use the information given to you to paint the picture, so you can deduce the image and context if possible.\n"
        "Capture the mood, activity, or emotion in the scene from a first-person perspective.\n"
        "Don't limit your imagination/creativity with additional info/context part use it as a guide but don't rely on it.\n"
        "If additional context/info is provided - do not make it the center of content."
        "Avoid sounding robotic or overly literal — keep it smooth and realistic.\n"
        "Always ensure the caption sounds natural."
    )

    return prompt.strip()


def generate_caption(prompt):
    """
    Use OpenAI's GPT to generate a caption from the prompt.
    """
    try:
        print(prompt)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful image captioning assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error during caption generation: {e}")
        return "Could not generate caption."

