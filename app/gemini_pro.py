import os
import json

from google import genai


def generate_story(
    panels,
    character_name,
    tone
):
    """
    Generate narration, captions and dialogue
    for the comic panels using Gemini.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Please add it to your .env file."
        )

    client = genai.Client(
        api_key=api_key
    )

    outline_text = json.dumps(
        panels,
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
You are a professional comic book writer.

Create the complete story for these 5 comic panels.

Main character:
{character_name}

Story tone:
{tone}

Comic outline:
{outline_text}

For every panel create:

1. panel_number
2. caption
3. narration
4. dialogue

Requirements:

- Keep exactly 5 panels.
- Keep the same character throughout the story.
- Follow the supplied panel outline.
- Make the story flow naturally from panel to panel.
- Make the narration interesting and concise.
- Make the dialogue natural.
- Keep the story family-friendly.
- Use an empty string for dialogue if dialogue is not needed.

Return ONLY valid JSON in this format:

{{
  "panels": [
    {{
      "panel_number": 1,
      "caption": "Short caption",
      "narration": "Narration for the panel",
      "dialogue": "Character dialogue"
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

    story_panels = data.get("panels")

    if not story_panels:
        raise ValueError(
            "Gemini response does not contain panels."
        )

    if len(story_panels) != 5:
        raise ValueError(
            f"Expected 5 panels but received "
            f"{len(story_panels)}."
        )

    result = []

    for number, panel in enumerate(
        story_panels,
        start=1
    ):
        result.append({
            "panel_number": number,

            "caption": panel.get(
                "caption",
                ""
            ),

            "narration": panel.get(
                "narration",
                ""
            ),

            "dialogue": panel.get(
                "dialogue",
                ""
            )
        })

    return result