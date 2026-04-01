"""
carousel_generator.py — renders carousel slide HTML templates and screenshots them via Playwright
"""
from __future__ import annotations
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TOOLS_DIR = Path(__file__).parent
TEMPLATES_DIR = TOOLS_DIR / "templates" / "carousel"
OUTPUT_DIR = TOOLS_DIR / "output"

SLIDE_TEMPLATES = {
    "cover": "slide_cover.html",
    "text": "slide_text.html",
    "stat": "slide_stat.html",
    "cta": "slide_cta.html",
}


def generate_carousel(tool_result: dict, config: dict, tools_dir: Path | None = None) -> list[Path]:
    tools_dir = tools_dir or TOOLS_DIR
    slides = tool_result.get("carousel_slides", [])
    slug = tool_result["slug"]
    category = tool_result["category"]

    out_dir = tools_dir / "output" / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
    )

    # Hard cap — Claude sometimes ignores the 5-8 slide instruction
    slides = slides[:10]
    total_slides = len(slides)
    png_paths = []

    for i, slide in enumerate(slides):
        slide_type = slide.get("type", "text")
        tmpl_name = SLIDE_TEMPLATES.get(slide_type, "slide_text.html")
        tmpl = env.get_template(tmpl_name)

        # Inject category into cover slides
        slide_ctx = dict(slide)
        if slide_type == "cover" and not slide_ctx.get("category"):
            slide_ctx["category"] = category

        html = tmpl.render(
            slide=slide_ctx,
            slide_index=i,
            total_slides=total_slides,
        )

        html_path = out_dir / f"slide_{i+1:02d}.html"
        html_path.write_text(html, encoding="utf-8")

        png_path = out_dir / f"slide_{i+1:02d}.png"
        _screenshot(html_path, png_path, config["carousel"]["width"], config["carousel"]["height"])
        png_paths.append(png_path)
        print(f"  Slide {i+1}/{total_slides} ({slide_type}): {png_path.name}")

    return png_paths


def _screenshot(html_path: Path, out_path: Path, width: int = 1080, height: int = 1080) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(f"file://{html_path.absolute()}")
        # Wait for Google Fonts to load
        try:
            page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            pass  # Timeout is fine — just screenshot what we have
        page.screenshot(
            path=str(out_path),
            clip={"x": 0, "y": 0, "width": width, "height": height},
        )
        browser.close()
