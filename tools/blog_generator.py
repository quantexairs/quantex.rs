"""
blog_generator.py — generates blog post HTML and updates blog/index.html
"""
from __future__ import annotations
import json
import re
import shutil
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

TOOLS_DIR = Path(__file__).parent
ROOT_DIR = TOOLS_DIR.parent
TEMPLATES_DIR = TOOLS_DIR / "templates"

SR_MONTHS = [
    "", "januar", "februar", "mart", "april", "maj", "jun",
    "jul", "avgust", "septembar", "oktobar", "novembar", "decembar",
]

# Existing posts for related-posts sidebar (slug → title)
EXISTING_POSTS = [
    ("sati-izgubljeni-na-repetitivne-zadatke", "Koliko sati mesečno vaš tim gubi na zadatke koje AI može da uradi", "Produktivnost"),
    ("ai-agent-vs-chatgpt-razlika", "AI agent i ChatGPT nisu ista stvar: šta je razlika i zašto je to bitno", "AI tehnologija"),
    ("automatizacija-generisanja-lidova", "Automatizacija generisanja lidova: kako firme pune prodajni levak bez hladnih poziva", "Prodaja"),
    ("roi-vestacke-inteligencije-poslovanje", "Povrat na ulaganje veštačke inteligencije: kako izračunati povrat", "Finansije"),
    ("kako-uvesti-ai-u-firmu", "Kako uvesti AI u firmu bez internog IT tima: vodič za direktore", "Implementacija"),
    ("poslovni-procesi-za-automatizaciju", "5 poslovnih procesa koje svaka firma treba da automatizuje pre kraja 2026.", "Strategija"),
    ("automatizacija-zakazivanja-komunikacije", "Zašto firme gube klijente dok čekaju da im neko odgovori", "Klijentski servis"),
    ("interni-ai-asistent-zaposleni", "Interni AI asistent za zaposlene: šta je, kako radi i šta može da uradi za vaš tim", "Interni procesi"),
]


def format_date_sr(d: date) -> str:
    return f"{d.day}. {SR_MONTHS[d.month]} {d.year}."


def slugify_id(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[šŠ]", "s", text)
    text = re.sub(r"[čćČĆ]", "c", text)
    text = re.sub(r"[žŽ]", "z", text)
    text = re.sub(r"[đĐ]", "d", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def extract_lead(body_html: str) -> str:
    """Extract first <p> as the lead paragraph."""
    soup = BeautifulSoup(body_html, "html.parser")
    p = soup.find("p")
    return p.get_text(" ", strip=True) if p else ""


def extract_toc(body_html: str) -> list[dict]:
    """Extract H2 headings and ensure they have ids."""
    soup = BeautifulSoup(body_html, "html.parser")
    toc = []
    for h2 in soup.find_all("h2"):
        text = h2.get_text(" ", strip=True)
        hid = h2.get("id") or slugify_id(text)
        if not h2.get("id"):
            h2["id"] = hid
        toc.append({"id": hid, "text": text})
    return toc, str(soup)


def pick_related(slug: str, category: str, n: int = 3) -> list[dict]:
    """Pick related posts — same category first, then others."""
    same = [(s, t, c) for s, t, c in EXISTING_POSTS if c == category and s != slug]
    other = [(s, t, c) for s, t, c in EXISTING_POSTS if c != category and s != slug]
    picks = (same + other)[:n]
    return [{"href": f"{s}.html", "title": t} for s, t, _ in picks]


def derive_tags(category: str, slug: str) -> list[str]:
    tags = [category.lower()]
    words = [w for w in slug.replace("-", " ").split() if len(w) > 3][:3]
    tags += words
    tags.append("AI automatizacija")
    return list(dict.fromkeys(tags))[:5]  # dedupe, max 5


def build_schemas(post_data: dict, today: date) -> tuple[str, str, str]:
    iso = today.isoformat()
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post_data["title"],
        "datePublished": iso,
        "dateModified": iso,
        "author": {"@type": "Organization", "name": "Quantex"},
        "publisher": {
            "@type": "Organization",
            "name": "Quantex",
            "logo": {"@type": "ImageObject", "url": "https://quantex.rs/assets/logo.svg"},
        },
        "description": post_data["meta_description"],
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Početna", "item": "https://quantex.rs/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://quantex.rs/blog/"},
            {"@type": "ListItem", "position": 3, "name": post_data["title"]},
        ],
    }
    faq_schema = None
    if post_data.get("faq"):
        faq_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["question"],
                    "acceptedAnswer": {"@type": "Answer", "text": item["answer"]},
                }
                for item in post_data["faq"]
            ],
        }
    return (
        json.dumps(article, ensure_ascii=False),
        json.dumps(breadcrumb, ensure_ascii=False),
        json.dumps(faq_schema, ensure_ascii=False) if faq_schema else "",
    )


def generate_blog(tool_result: dict, config: dict, root_dir: Path | None = None) -> Path:
    root_dir = root_dir or ROOT_DIR
    blog_dir = root_dir / "blog"
    today = date.today()

    slug = tool_result["slug"]
    body_html = tool_result["body_html"]
    category = tool_result["category"]

    # Extract lead from first <p> if not stored separately
    lead = extract_lead(body_html)

    # Ensure TOC ids are set in body_html
    toc, body_html_with_ids = extract_toc(body_html)

    schema_article, schema_breadcrumb, schema_faq = build_schemas(tool_result, today)

    cat_config = config["categories"].get(category, {})

    post = {
        "slug": slug,
        "title": tool_result["title"],
        "meta_title": tool_result["meta_title"],
        "meta_description": tool_result["meta_description"],
        "category": category,
        "category_slug": tool_result["category_slug"],
        "reading_time": tool_result["reading_time"],
        "body_html": body_html_with_ids,
        "faq": tool_result.get("faq", []),
        "lead": lead,
        "date_display": format_date_sr(today),
        "date_iso": today.isoformat(),
        "toc": toc,
        "related_posts": pick_related(slug, category),
        "tags": derive_tags(category, slug),
        "breadcrumb_short": " ".join(slug.replace("-", " ").split()[:4]).capitalize(),
        "schema_article": schema_article,
        "schema_breadcrumb": schema_breadcrumb,
        "schema_faq": schema_faq,
        "card_gradient": cat_config.get("gradient", "linear-gradient(135deg, rgba(59,130,246,0.15), rgba(6,182,212,0.1))"),
        "card_icon": cat_config.get("icon", '<circle cx="12" cy="12" r="10"/>'),
        "excerpt": _make_excerpt(lead),
    }

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
    )

    # Render blog post
    tmpl = env.get_template("blog_post.html")
    html = tmpl.render(post=post)
    out_path = blog_dir / f"{slug}.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"  Blog post: {out_path}")

    # Update blog/index.html
    _prepend_card(blog_dir / "index.html", post, env)

    return out_path


def _make_excerpt(lead: str, max_chars: int = 200) -> str:
    if len(lead) <= max_chars:
        return lead
    return lead[:max_chars].rsplit(" ", 1)[0] + "…"


def _prepend_card(index_path: Path, post: dict, env: Environment) -> None:
    # Backup
    shutil.copy(index_path, index_path.with_suffix(".html.bak"))

    card_tmpl = env.get_template("blog_card.html")
    card_html = card_tmpl.render(post=post)

    soup = BeautifulSoup(index_path.read_text(encoding="utf-8"), "html.parser")
    grid = soup.find("div", class_="blog-grid")
    if not grid:
        print("  WARNING: .blog-grid not found in blog/index.html — skipping index update")
        return

    card_soup = BeautifulSoup(card_html, "html.parser")
    # Prepend as first child of .blog-grid
    grid.insert(0, card_soup)

    index_path.write_text(str(soup), encoding="utf-8")
    print(f"  blog/index.html updated (backup at index.html.bak)")
