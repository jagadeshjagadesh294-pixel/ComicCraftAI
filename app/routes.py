from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from .config import TEMPLATES_DIR
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .exporters import save_pdf


router = APIRouter()

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "error": None
        }
    )


@router.get("/test")
async def test():

    return {
        "message": "ComicCraft routes are working"
    }


@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):

    try:

        outlines = generate_outline(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style
        )

        stories = generate_story(
            panels=outlines,
            character_name=character_name,
            tone=tone
        )

        image_paths = []

        for panel in outlines:

            image_path = generate_image(
                image_prompt=panel.get(
                    "image_prompt",
                    ""
                ),
                panel_number=panel.get(
                    "panel_number",
                    1
                )
            )

            image_paths.append(image_path)

        layout = build_comic_layout(
            outlines=outlines,
            stories=stories,
            image_paths=image_paths
        )

        request.app.state.current_layout = layout

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "layout": layout
            }
        )

    except Exception as error:

        print("COMIC GENERATION ERROR:")
        print(type(error).__name__)
        print(str(error))

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": str(error)
            },
            status_code=500
        )


@router.get("/export/pdf")
async def export_pdf(request: Request):

    try:

        layout = getattr(
            request.app.state,
            "current_layout",
            None
        )

        if not layout:

            return HTMLResponse(
                content="""
                <h1>No Comic Available</h1>
                <p>Please generate a comic first.</p>
                <a href="/">Go Back</a>
                """,
                status_code=400
            )

        pdf_path = save_pdf(layout)

        pdf_file = Path(pdf_path)

        if not pdf_file.exists():

            return HTMLResponse(
                content=f"""
                <h1>PDF Error</h1>
                <p>PDF was not created.</p>
                <p>{pdf_path}</p>
                """,
                status_code=500
            )

        print("PDF CREATED:", str(pdf_file))

        return FileResponse(
            path=str(pdf_file),
            media_type="application/pdf",
            filename=pdf_file.name
        )

    except Exception as error:

        print("")
        print("==============================")
        print("PDF EXPORT ERROR")
        print("==============================")
        print(type(error).__name__)
        print(str(error))
        print("==============================")
        print("")

        return HTMLResponse(
            content=f"""
            <h1>PDF Export Error</h1>

            <h3>{type(error).__name__}</h3>

            <pre>{str(error)}</pre>

            <br>

            <a href="/">Go Back</a>
            """,
            status_code=500
        )