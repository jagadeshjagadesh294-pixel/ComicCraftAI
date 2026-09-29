import os
import json

from google import genai


def generate_outline(
    story_prompt,
    character_name,
    setting,
    tone,
    art_style
):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Please add it to your .env file."
        )

    client = genai.Client(
        api_key=api_key
    )

    prompt = f"""
Create exactly 5 comic panels.

Story:
{story_prompt}

Main Character:
{character_name}

Setting:
{setting}

Tone:
{tone}

Art Style:
{art_style}

For each panel provide:

panel_number
title
scene_description
image_prompt

The story must have:

1. Beginning
2. Development
3. Conflict
4. Climax
5. Ending

Keep the character consistent throughout all panels.

Return ONLY valid JSON in this format:

{{
  "panels": [
    {{
      "panel_number": 1,
      "title": "Title",
      "scene_description": "Description",
      "image_prompt": "Detailed image prompt"
    }}
  ]
}}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    if not response.text:
        raise ValueError(
            "Gemini returned an empty response."
        )

    text = response.text.strip()

    # Remove Markdown JSON code fences
    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    try:
        data = json.loads(text)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Gemini returned invalid JSON: {error}"
        )

    panels = data.get("panels")

    if not panels:
        raise ValueError(
            "Gemini response does not contain panels."
        )

    if len(panels) != 5:
        raise ValueError(
            f"Expected 5 panels but received {len(panels)}."
        )

    result = []

    for number, panel in enumerate(
        panels,
        start=1
    ):
        result.append({
            "panel_number": number,

            "title": panel.get(
                "title",
                f"Panel {number}"
            ),

            "scene_description": panel.get(
                "scene_description",
                ""
            ),

            "image_prompt": panel.get(
                "image_prompt",
                ""
            )
        })

    return result