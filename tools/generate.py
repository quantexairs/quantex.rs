#!/usr/bin/env python3
"""
Quantex Blog + Instagram Carousel Generator

Usage:
    python tools/generate.py --topic "kako AI chatbot smanjuje opterecenje korisnickog servisa"
    python tools/generate.py --topic "..." --blog-only
    python tools/generate.py --topic "..." --carousel-only
"""
from __future__ import annotations
import argparse
import os
import subprocess
import sys
from pathlib import Path


def _ensure(package: str, pip_name: str | None = None) -> None:
    """Install package for this exact Python if it's missing."""
    try:
        __import__(package)
    except ImportError:
        print(f"Instaliram {pip_name or package}...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--break-system-packages", "-q",
             pip_name or package],
            stdout=sys.stdout, stderr=sys.stderr,
        )


_ensure("anthropic")
_ensure("jinja2")
_ensure("yaml", "pyyaml")
_ensure("bs4", "beautifulsoup4")
_ensure("playwright")

import anthropic
import yaml

TOOLS_DIR = Path(__file__).parent
ROOT_DIR = TOOLS_DIR.parent

# ── System prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Ti si stručni pisac za Quantex, agenciju za AI automatizaciju poslovanja sa sedištem u Srbiji. Pišeš blog post za sajt quantex.rs.

PRAVILA PISANJA:
- Piši iz perspektive Quantex tima, u trećem ili prvom licu množine ("mi", "naš tim")
- Ton je formalan, direktan, bez ulepšavanja. Piši kao da razgovaraš sa direktorom koji ima 5 minuta
- Koristi "vi" formu kada se obraćaš čitaocima
- Piši prirodnim srpskim jezikom (ekavica), ne prevedenim sa engleskog
- Tehničke termine (AI, CRM, API, ROI, chatbot, lead scoring, pipeline) ostavi na engleskom
- Svaki post mora sadržati konkretne brojke, procente ili vremenske okvire gde je moguće
- Izbegavaj generičke savete. Svaki paragraf mora dati čitaocu nešto konkretno i primenljivo
- Post treba da bude od 1000 do 2000 reči
- Kreiraj od 3 do 5 FAQ pitanja sa odgovorima
- Svaki post završi pozivom na besplatan analitički razgovor

ZABRANJENO:
- NIKAKO ne koristi crtu (dash) ni dugu (—) ni kratku (–) ni srednju (-) kao interpunkciju u rečenicama
- Umesto crte koristi zarez, tačku i zarez, ili preformuliši rečenicu
- Opsege piši rečima: "od 3 do 5 radnih dana", NE "3-5 radnih dana"
- Ne koristi sledeće reči: delve, tapestry, vibrant, landscape, realm, embark, excels, vital, comprehensive, intricate, pivotal, moreover, arguably, notably, thrilled, robust, seamless, cutting-edge, state-of-the-art, unparalleled, game-changing, revolutionary, synergy, empower, unleash, future-proof, mission-critical, turnkey, streamlined, best-in-class, top-tier
- Ne koristi hrvatske reči ni izraze, samo srpski ekavica
- Ne pisati "ukoliko" već "ako"

KONTEKST QUANTEX-a:
- Quantex pruža: AI agente obučene na podacima firme, automatizovano generisanje lidova, interne AI sisteme za zaposlene, automatizaciju zakazivanja i komunikacije
- Proces: analitički razgovor → revizija infrastrukture → arhitektura rešenja → iterativna implementacija → monitoring i podrška
- Od prvog razgovora do živog sistema za 30 dana
- Sajt: quantex.rs
- Kontakt: kroz formu na sajtu ili zakazivanje razgovora

SEO ZAHTEVI:
- Prirodno uključi ciljani keyword od 3 do 5 puta u tekstu
- H2 naslovi treba da budu deskriptivni, sa relevantnim pojmovima
- Meta description: od 150 do 160 karaktera
- Predloži slug za URL (latinica, bez dijakritika, sa crticama)
- Svaki H2 tag mora imati id atribut baziran na sadržaju (npr. <h2 id="zasto-firme-ignorisu">)

SRPSKI PRAVOPIS:
- Uz brojeve 5 i više koristi genitiv množine
- "nijedan/nijedna/nijedno" piši kao jednu reč
- Gramatičko slaganje roda, broja i padeža mora biti ispravno
- Zarez pre "koji/koja/što" u zavisnoj rečenici

INSTAGRAM CAROUSEL — OBAVEZNO TACNO OD 5 DO 8 SLAJDOVA, NE VISE:
- MAKSIMALAN BROJ SLAJDOVA JE 8. Ne pravi vise od 8 slajdova ni pod kojim uslovima.
- Slajd 1: cover (naslov kao hook, kratak subtitle)
- Slajdovi 2 do 6: text ili stat (konkretan savet ili podatak po slajdu, po jedan po slajdu)
- Poslednji slajd (slajd 6, 7 ili 8): cta (poziv na akciju)
- Svaki slajd mora biti razumljiv bez konteksta ostalih
- stat slajdovi: prominentni broj/procenat + kratko objasnjenje""".strip()

# ── Tool schema ───────────────────────────────────────────────────────────────

BLOG_TOOL = {
    "name": "create_blog_post",
    "description": "Kreira blog post sa svim potrebnim poljima",
    "input_schema": {
        "type": "object",
        "properties": {
            "slug": {"type": "string"},
            "title": {"type": "string"},
            "meta_title": {"type": "string", "description": "Do 60 karaktera"},
            "meta_description": {"type": "string", "description": "150 do 160 karaktera"},
            "category": {
                "type": "string",
                "enum": [
                    "Produktivnost", "AI tehnologija", "Prodaja", "Finansije",
                    "Implementacija", "Strategija", "Klijentski servis", "Interni procesi",
                ],
            },
            "category_slug": {
                "type": "string",
                "enum": [
                    "produktivnost", "ai-tehnologija", "prodaja", "finansije",
                    "implementacija", "strategija", "klijentski-servis", "interni-procesi",
                ],
            },
            "reading_time": {"type": "integer"},
            "body_html": {"type": "string"},
            "faq": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "answer": {"type": "string"},
                    },
                    "required": ["question", "answer"],
                },
            },
            "instagram_caption": {"type": "string"},
            "carousel_slides": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "enum": ["cover", "text", "stat", "cta"]},
                        "headline": {"type": "string"},
                        "subtitle": {"type": "string"},
                        "body": {"type": "string"},
                        "stat_number": {"type": "string", "description": "npr. '80%', '4h', '23x'"},
                        "stat_label": {"type": "string"},
                        "tip_number": {"type": "integer"},
                    },
                    "required": ["type", "headline"],
                },
            },
        },
        "required": [
            "slug", "title", "meta_title", "meta_description", "category",
            "category_slug", "reading_time", "body_html", "faq",
            "instagram_caption", "carousel_slides",
        ],
    },
}


# ── Claude API call ────────────────────────────────────────────────────────────

def call_claude(topic: str, model: str, max_tokens: int) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("ERROR: ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)
    print(f"Generating content for: {topic!r}")
    print(f"Model: {model}  |  max_tokens: {max_tokens}")
    print("Calling Claude API...")

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        tools=[BLOG_TOOL],
        tool_choice={"type": "tool", "name": "create_blog_post"},
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Napiši blog post na temu: {topic}"}],
    )

    for block in response.content:
        if block.type == "tool_use" and block.name == "create_blog_post":
            return block.input

    raise ValueError("Claude did not return a tool_use block — check the response.")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Quantex blog post + carousel generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--topic", required=True, help="Topic for the blog post (in Serbian)")
    parser.add_argument("--blog-only", action="store_true", help="Generate blog post only, skip carousel")
    parser.add_argument("--carousel-only", action="store_true", help="Generate carousel only, skip blog post")
    args = parser.parse_args()

    config_path = TOOLS_DIR / "config.yaml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    tool_result = call_claude(
        topic=args.topic,
        model=config["claude"]["model"],
        max_tokens=config["claude"]["max_tokens"],
    )

    print(f"\nSlug: {tool_result['slug']}")
    print(f"Title: {tool_result['title']}")
    print(f"Category: {tool_result['category']}")
    print(f"Reading time: {tool_result['reading_time']} min")
    print(f"FAQ items: {len(tool_result.get('faq', []))}")
    print(f"Carousel slides: {len(tool_result.get('carousel_slides', []))}")

    if not args.carousel_only:
        from blog_generator import generate_blog
        print("\nGenerating blog post...")
        blog_path = generate_blog(tool_result, config, ROOT_DIR)
        print(f"Blog post saved: {blog_path.relative_to(ROOT_DIR)}")

    if not args.blog_only:
        from carousel_generator import generate_carousel
        print("\nGenerating carousel slides...")
        png_paths = generate_carousel(tool_result, config, TOOLS_DIR)
        print(f"Carousel: {len(png_paths)} slides in tools/output/{tool_result['slug']}/")

    if tool_result.get("instagram_caption"):
        print("\n" + "─" * 60)
        print("INSTAGRAM CAPTION:")
        print("─" * 60)
        print(tool_result["instagram_caption"])
        print("─" * 60)

    print("\nDone.")


if __name__ == "__main__":
    main()
