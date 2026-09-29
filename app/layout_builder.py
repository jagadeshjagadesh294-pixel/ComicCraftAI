def build_comic_layout(outlines, stories, image_paths):
    """
    Combine comic outlines, story content,
    and generated image paths into one layout.
    """

    layout = []

    # Create a lookup for story panels
    story_lookup = {}

    for story in stories:
        panel_number = story.get("panel_number")

        story_lookup[panel_number] = story

    # Combine outline + story + image
    for index, outline in enumerate(outlines):

        panel_number = outline.get(
            "panel_number",
            index + 1
        )

        story = story_lookup.get(
            panel_number,
            {}
        )

        image_path = ""

        if index < len(image_paths):
            image_path = image_paths[index]

        panel = {
            "panel_number": panel_number,

            "title": outline.get(
                "title",
                f"Panel {panel_number}"
            ),

            "scene_description": outline.get(
                "scene_description",
                ""
            ),

            "image_prompt": outline.get(
                "image_prompt",
                ""
            ),

            "image_path": image_path,

            "caption": story.get(
                "caption",
                ""
            ),

            "narration": story.get(
                "narration",
                ""
            ),

            "dialogue": story.get(
                "dialogue",
                ""
            )
        }

        layout.append(panel)

    return layout