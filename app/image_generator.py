import os
import re
from datetime import datetime
from pathlib import Path

from huggingface_hub import InferenceClient


PROJECT_DIR = Path(__file__).resolve().parent.parent

PANELS_DIR = PROJECT_DIR / "static" / "panels"

PANELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def clean_filename(text):
    text = str(text)

    text = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        text
    )

    text = text.strip("_")

    if not text:
        text = "panel"

    return text[:50]


def generate_image(image_prompt, panel_number):

    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        raise ValueError(
            "HF_TOKEN is missing. "
            "Please add HF_TOKEN to your .env file."
        )

    model_name = os.getenv(
        "HF_IMAGE_MODEL",
        "black-forest-labs/FLUX.1-schnell"
    )

    prompt = f"""
Professional comic book illustration.

{image_prompt}

Requirements:
- High quality
- Detailed environment
- Clear composition
- Consistent character
- Expressive character
- Cinematic lighting
- Comic book style
- No text
- No letters
- No logo
- No watermark
- No speech bubbles
"""

    try:

        client = InferenceClient(
            provider="auto",
            api_key=hf_token
        )

        image = client.text_to_image(
            prompt=prompt,
            model=model_name
        )

    except Exception as error:

        raise RuntimeError(
            "Hugging Face image generation failed: "
            + str(error)
        ) from error

    if image is None:
        raise RuntimeError(
            "Hugging Face returned an empty image."
        )

    filename = (
        "panel_"
        + str(panel_number)
        + "_"
        + clean_filename(image_prompt)
        + "_"
        + datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )
        + ".png"
    )

    file_path = PANELS_DIR / filename

    try:

        image.save(file_path)

    except Exception as error:

        raise RuntimeError(
            "Could not save generated image: "
            + str(error)
        ) from error

    return "/static/panels/" + filename