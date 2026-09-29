from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from .config import EXPORTS_DIR


def save_pdf(layout):
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    pdf_path = EXPORTS_DIR / f"comic_{timestamp}.pdf"

    styles = getSampleStyleSheet()

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    story = []

    story.append(
        Paragraph(
            "ComicCraft - AI Generated Comic",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    for panel in layout:
        panel_number = panel.get("panel_number", "")
        title = panel.get("title", f"Panel {panel_number}")
        scene = panel.get("scene_description", "")
        caption = panel.get("caption", "")
        narration = panel.get("narration", "")
        dialogue = panel.get("dialogue", "")
        image_path = panel.get("image_path", "")

        story.append(
            Paragraph(
                f"Panel {panel_number} - {title}",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 8))

        if image_path:
            image_file = Path(image_path)

            if not image_file.is_absolute():
                image_file = Path.cwd() / image_path.lstrip("/")

            if image_file.exists():
                try:
                    img = Image(str(image_file))

                    max_width = 6.5 * inch
                    max_height = 7.5 * inch

                    width = img.imageWidth
                    height = img.imageHeight

                    scale = min(
                        max_width / width,
                        max_height / height,
                        1
                    )

                    img.drawWidth = width * scale
                    img.drawHeight = height * scale

                    story.append(img)
                    story.append(Spacer(1, 12))

                except Exception as error:
                    print("PDF IMAGE ERROR:", error)

        if scene:
            story.append(
                Paragraph(
                    f"<b>Scene:</b> {scene}",
                    styles["BodyText"]
                )
            )
            story.append(Spacer(1, 6))

        if caption:
            story.append(
                Paragraph(
                    f"<b>Caption:</b> {caption}",
                    styles["BodyText"]
                )
            )
            story.append(Spacer(1, 6))

        if narration:
            story.append(
                Paragraph(
                    f"<b>Narration:</b> {narration}",
                    styles["BodyText"]
                )
            )
            story.append(Spacer(1, 6))

        if dialogue:
            story.append(
                Paragraph(
                    f"<b>Dialogue:</b> {dialogue}",
                    styles["BodyText"]
                )
            )

        story.append(Spacer(1, 15))

    document.build(story)

    if not pdf_path.exists():
        raise RuntimeError(
            f"PDF file was not created: {pdf_path}"
        )

    print("PDF CREATED:", str(pdf_path))

    return str(pdf_path)
