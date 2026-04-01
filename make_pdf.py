"""
Quantex — Besplatni vodič PDF
Generisano programski sa ReportLab — Inter font, pravi logo, poliran dizajn
"""
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_DIR = "/home/aceman/Documents/quantex.rs/assets/fonts/"
pdfmetrics.registerFont(TTFont("Inter",       FONT_DIR + "Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-M",     FONT_DIR + "Inter-Medium.ttf"))
pdfmetrics.registerFont(TTFont("Inter-SB",    FONT_DIR + "Inter-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("Inter-B",     FONT_DIR + "Inter-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Inter-XB",    FONT_DIR + "Inter-ExtraBold.ttf"))
pdfmetrics.registerFont(TTFont("Inter-BL",    FONT_DIR + "Inter-Black.ttf"))
pdfmetrics.registerFont(TTFont("Inter-L",     FONT_DIR + "Inter-Light.ttf"))

# ── Palette ────────────────────────────────────────────────────────────────────
BG_DARK   = HexColor("#060912")
BLUE      = HexColor("#3b82f6")
CYAN      = HexColor("#06b6d4")
BLUE_LIGHT= HexColor("#60a5fa")
TEXT_DARK  = HexColor("#0f172a")
TEXT_MID   = HexColor("#334155")
TEXT_SOFT  = HexColor("#64748b")
TEXT_MUTE  = HexColor("#94a3b8")
TEXT_LIGHT = HexColor("#f1f5f9")
TEXT_WHITE = HexColor("#f8fafc")
RULE       = HexColor("#e2e8f0")
METRIC_BG  = HexColor("#eff6ff")
METRIC_BRD = HexColor("#bfdbfe")
EX_BG      = HexColor("#f0f9ff")
EX_BRD     = HexColor("#93c5fd")
COVER_CARD = HexColor("#0c1425")
COVER_BORD = HexColor("#1a2d50")
ERR_BG     = HexColor("#fef2f2")
ERR_BRD    = HexColor("#fecaca")
ERR_ICON   = HexColor("#ef4444")
CTA_BOX_BG = HexColor("#0c1830")
CTA_BOX_BRD= HexColor("#1e3a6e")

W, H = A4

# ── Low-level helpers ──────────────────────────────────────────────────────────
def pt(v): return v * mm

def rrect(c, x, y, w, h, r, fill=None, stroke=None, lw=0.5):
    if fill:  c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke); c.setLineWidth(lw)
    else:
        c.setStrokeColor(Color(0,0,0,alpha=0))
    c.roundRect(x, y, w, h, r, fill=1 if fill else 0, stroke=1 if stroke else 0)

def txt(c, s, x, y, font="Inter", size=10, color=TEXT_DARK, align="left"):
    c.setFont(font, size); c.setFillColor(color)
    if align == "center":   c.drawCentredString(x, y, s)
    elif align == "right":  c.drawRightString(x, y, s)
    else:                   c.drawString(x, y, s)

def hline(c, x1, x2, y, color=RULE, lw=0.5):
    c.setStrokeColor(color); c.setLineWidth(lw); c.line(x1, y, x2, y)

def gradient_bar(c, x, y, w, h, c1=BLUE, c2=CYAN, steps=30):
    sw = w / steps
    for i in range(steps):
        t = i / steps
        r = c1.red   + (c2.red   - c1.red)   * t
        g = c1.green + (c2.green - c1.green) * t
        b = c1.blue  + (c2.blue  - c1.blue)  * t
        c.setFillColorRGB(r, g, b)
        c.rect(x + i * sw, y, sw + 0.5, h, fill=1, stroke=0)

def wrap(c, s, x, y, max_w, font="Inter", size=9.5, color=TEXT_MID, lh=14):
    c.setFont(font, size); c.setFillColor(color)
    words = s.split(); lines = []; cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if c.stringWidth(test, font, size) <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    for line in lines:
        c.drawString(x, y, line); y -= lh
    return y

def soft_glow(c, cx, cy, radius, color, layers=12):
    """Soft radial glow via concentric translucent circles."""
    for i in range(layers, 0, -1):
        t = i / layers
        r = radius * t
        alpha = 0.03 * (1 - t) + 0.005
        c.setFillColor(Color(color.red, color.green, color.blue, alpha=alpha))
        c.circle(cx, cy, r, fill=1, stroke=0)

# ── Logo — Network Q constellation ─────────────────────────────────────────────
def draw_q_mark(c, ox, oy, s, on_dark=True):
    """
    Draw the Quantex network-Q logo mark.
    ox, oy = bottom-left of bounding box;  s = size (width=height).
    Based on favicon.svg viewBox 0 0 64 64, center at 30,30, radius 20.
    """
    # Scale factor: SVG is 64x64
    f = s / 64.0
    # Helper to convert SVG coords to PDF coords (SVG y is top-down, PDF is bottom-up)
    def sx(v): return ox + v * f
    def sy(v): return oy + (64 - v) * f

    # Q outer circle
    c.setStrokeColor(BLUE); c.setLineWidth(1.4 * f)
    c.circle(sx(30), sy(30), 20 * f, fill=0, stroke=1)

    # Q tail
    c.setStrokeColor(BLUE_LIGHT); c.setLineWidth(2.5 * f); c.setLineCap(1)
    c.line(sx(44), sy(44), sx(54), sy(54))

    # Internal network lines (subtle cross)
    grid_color = Color(BLUE.red, BLUE.green, BLUE.blue, alpha=0.3)
    c.setStrokeColor(grid_color); c.setLineWidth(0.6 * f); c.setLineCap(0)
    for x1,y1,x2,y2 in [(10,30,50,30),(30,10,30,50),(16,16,44,44),(44,16,16,44)]:
        c.line(sx(x1),sy(y1),sx(x2),sy(y2))

    # Constellation spokes
    spoke_color = Color(BLUE_LIGHT.red, BLUE_LIGHT.green, BLUE_LIGHT.blue, alpha=0.5)
    c.setStrokeColor(spoke_color); c.setLineWidth(0.85 * f)
    for x1,y1,x2,y2 in [(30,10,50,30),(50,30,30,50),(30,10,10,30)]:
        c.line(sx(x1),sy(y1),sx(x2),sy(y2))
    spoke2 = Color(BLUE_LIGHT.red, BLUE_LIGHT.green, BLUE_LIGHT.blue, alpha=0.4)
    c.setStrokeColor(spoke2); c.setLineWidth(0.75 * f)
    c.line(sx(10),sy(30),sx(30),sy(50))

    # Inner hexagon ring
    hex_color = Color(0.576, 0.773, 0.992, alpha=0.5)  # #93c5fd
    c.setStrokeColor(hex_color); c.setLineWidth(0.8 * f)
    hex_pts = [(30,18),(40,24),(40,36),(30,42),(20,36),(20,24)]
    for i in range(len(hex_pts)):
        x1,y1 = hex_pts[i]; x2,y2 = hex_pts[(i+1) % len(hex_pts)]
        c.line(sx(x1),sy(y1),sx(x2),sy(y2))

    # Outer nodes
    outer_nodes = [(30,10,2.2,"#bfdbfe"),(44,16,1.8,"#93c5fd"),(50,30,1.8,"#93c5fd"),
                   (44,44,1.8,"#93c5fd"),(30,50,1.8,"#93c5fd"),(16,44,1.8,"#93c5fd"),
                   (10,30,1.8,"#93c5fd"),(16,16,1.8,"#93c5fd")]
    for nx,ny,nr,nc in outer_nodes:
        c.setFillColor(HexColor(nc))
        c.circle(sx(nx), sy(ny), nr * f, fill=1, stroke=0)

    # Inner hexagon nodes
    for nx,ny in hex_pts:
        c.setFillColor(HexColor("#dbeafe"))
        c.circle(sx(nx), sy(ny), 1.5 * f, fill=1, stroke=0)

    # Center node (white)
    c.setFillColor(white)
    c.circle(sx(30), sy(30), 3 * f, fill=1, stroke=0)

    # Q tail endpoint
    c.setFillColor(BLUE_LIGHT)
    c.circle(sx(54), sy(54), 2 * f, fill=1, stroke=0)


def draw_logo(c, x, y, size=pt(9), with_text=True, text_color=TEXT_LIGHT, with_tagline=False):
    """Draw network-Q mark + 'QUANTEX' text + optional tagline."""
    draw_q_mark(c, x, y, size)
    if with_text:
        txt(c, "QUANTEX", x + size + pt(2), y + size * 0.42,
            "Inter-XB", size * 0.42, text_color)
        if with_tagline:
            txt(c, "AI AUTOMATION AGENCY", x + size + pt(2.3), y + size * 0.15,
                "Inter-M", size * 0.14, BLUE_LIGHT)
    return x + size

# ── Footer ─────────────────────────────────────────────────────────────────────
def draw_footer(c, page_num=None, dark=False):
    fc = HexColor("#1e2d4a") if dark else RULE
    tc = TEXT_SOFT if dark else TEXT_MUTE
    hline(c, pt(20), W - pt(20), pt(14), fc)
    txt(c, "quantex.rs", pt(20), pt(8), "Inter-M", 7, tc)
    if page_num:
        txt(c, str(page_num), W - pt(20), pt(8), "Inter", 7, tc, "right")


# ══════════════════════════════════════════════════════════════════════════════
#  COVER PAGE
# ══════════════════════════════════════════════════════════════════════════════
def draw_cover(c):
    c.setFillColor(BG_DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Soft glows instead of crude circles
    soft_glow(c, W * 0.82, H * 0.88, pt(100), BLUE, layers=18)
    soft_glow(c, W * 0.1, H * 0.08, pt(70), CYAN, layers=14)
    # Tiny hint of glow mid-left
    soft_glow(c, W * 0.3, H * 0.5, pt(50), BLUE, layers=10)

    # Top bar
    top_y = H - pt(14)
    draw_logo(c, pt(16), top_y - pt(10), pt(12), with_tagline=True)

    # Badge top-right
    badge = "Besplatni vodič · 2026"
    bw = c.stringWidth(badge, "Inter-SB", 7) + pt(8)
    bx = W - pt(16) - bw
    rrect(c, bx, top_y - pt(6.5), bw, pt(7.5), pt(3.5),
          fill=HexColor("#0d1f42"), stroke=HexColor("#1e4080"), lw=0.5)
    txt(c, badge, bx + bw/2, top_y - pt(3), "Inter-SB", 7, HexColor("#93c5fd"), "center")

    # Eyebrow
    ey = H - pt(54)
    txt(c, "AI AUTOMATIZACIJA ZA SRPSKE FIRME", pt(16), ey, "Inter-B", 8, CYAN)

    # Title
    ty = ey - pt(18)
    txt(c, "10 poslovnih procesa", pt(16), ty, "Inter-BL", 30, TEXT_WHITE)
    txt(c, "koji se mogu", pt(16), ty - pt(14), "Inter-BL", 30, TEXT_WHITE)
    # Accent bar
    gradient_bar(c, pt(16), ty - pt(24), pt(55), pt(1.3), BLUE, CYAN)
    txt(c, "automatizovati danas", pt(16), ty - pt(36), "Inter-BL", 30, BLUE)

    # Subtitle
    sy = ty - pt(52)
    wrap(c,
        "Praktičan pregled procesa koje srpske firme i dalje rade ručno, "
        "koliko to košta u satima i novcu, i kako izgleda kad sistem preuzme taj posao.",
        pt(16), sy, W - pt(32), "Inter", 10.5, TEXT_MUTE, pt(5.5))

    # Rule
    ry = sy - pt(22)
    gradient_bar(c, pt(16), ry, pt(20), pt(1.2), BLUE, CYAN)

    # Meta
    my = ry - pt(9)
    meta = ["12 minuta čitanja", "Za direktore i vlasnike firmi", "Odmah primenjivo"]
    mx = pt(16)
    for item in meta:
        c.setFillColor(BLUE); c.circle(mx + 2, my + 3, 2.5, fill=1, stroke=0)
        txt(c, item, mx + pt(2.5), my, "Inter", 8, TEXT_SOFT)
        mx += c.stringWidth(item, "Inter", 8) + pt(14)

    # Metric cards
    cy2 = my - pt(44)
    cw = (W - pt(32) - pt(6)) / 3
    cards = [
        ("78%", "repetitivnih zadataka može biti automatizovano"),
        ("14h", "prosečno izgubljenih sati nedeljno u firmama"),
        ("4 mes.", "prosečan period povrata investicije"),
    ]
    for i, (val, lbl) in enumerate(cards):
        cx2 = pt(16) + i * (cw + pt(3))
        rrect(c, cx2, cy2, cw, pt(36), pt(3), fill=COVER_CARD, stroke=COVER_BORD, lw=0.6)
        txt(c, val, cx2 + pt(5), cy2 + pt(25), "Inter-BL", 19, BLUE_LIGHT)
        wrap(c, lbl, cx2 + pt(5), cy2 + pt(15), cw - pt(10), "Inter", 7.5, TEXT_SOFT, pt(4.2))

    # Footer
    fy = pt(10)
    hline(c, pt(16), W - pt(16), fy + pt(5), HexColor("#1a2d50"))
    txt(c, "© 2026 Quantex · Sva prava zadržana", pt(16), fy, "Inter", 7.5, HexColor("#475569"))
    txt(c, "quantex.rs", W - pt(16), fy, "Inter-SB", 7.5, TEXT_SOFT, "right")


# ══════════════════════════════════════════════════════════════════════════════
#  TOC PAGE
# ══════════════════════════════════════════════════════════════════════════════
def draw_toc(c):
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Blue accent top bar
    gradient_bar(c, 0, H - pt(1.2), W, pt(1.2), BLUE, CYAN)

    y = H - pt(22)
    # Tag
    tag = "Sadržaj"
    tw = c.stringWidth(tag, "Inter-SB", 7) + pt(9)
    rrect(c, pt(20), y - pt(2), tw, pt(8), pt(3), fill=METRIC_BG, stroke=METRIC_BRD, lw=0.5)
    txt(c, tag, pt(20) + tw/2, y + pt(1.5), "Inter-SB", 7, BLUE, "center")

    y -= pt(14)
    txt(c, "Šta ćete naći u ovom vodiču", pt(20), y, "Inter-XB", 18, TEXT_DARK)
    y -= pt(12)
    hline(c, pt(20), W - pt(20), y)

    # Intro box
    y -= pt(6)
    intro = (
        "Prosečna srpska firma od 10 do 50 zaposlenih gubi između 800 i 3.000 sati godišnje "
        "na zadatke koje sistem može da obavi. To je ekvivalent jednog do dva zaposlena koji "
        "rade isključivo repetitivne zadatke. Ovaj vodič govori o tome šta postoji danas, "
        "šta je implementirano kod firmi poput vaše, i kako izgleda u praksi."
    )
    box_h = pt(22)
    rrect(c, pt(20), y - box_h + pt(4), W - pt(40), box_h, pt(2.5),
          fill=EX_BG, stroke=EX_BRD, lw=0.5)
    # Left accent bar on intro box
    gradient_bar(c, pt(20), y - box_h + pt(4), pt(1), box_h, BLUE, CYAN)
    wrap(c, intro, pt(26), y - pt(0.5), W - pt(52), "Inter", 8.2, TEXT_MID, pt(4.8))

    y -= box_h + pt(7)

    # Processes
    txt(c, "PROCESI", pt(20), y, "Inter-SB", 7, TEXT_SOFT)
    y -= pt(3.5); hline(c, pt(20), W - pt(20), y); y -= pt(1.5)

    toc = [
        ("01","Odgovaranje na upite klijenata","4"),
        ("02","Zakazivanje termina i podsetnici","4"),
        ("03","Pronalaženje i kvalifikacija novih klijenata","5"),
        ("04","Obrada mejlova i interne poruke","5"),
        ("05","Nedeljni i mesečni izveštaji","5"),
        ("06","Uvođenje novih zaposlenih","6"),
        ("07","Fakturisanje i praćenje naplate","6"),
        ("08","Interni Q&A sistem za tim","6"),
        ("09","Upravljanje društvenim mrežama","7"),
        ("10","Unos i obrada podataka između sistema","7"),
    ]
    for num, title, pg in toc:
        y -= pt(8)
        # Number pill
        nw = pt(8.5)
        rrect(c, pt(20), y - pt(1.5), nw, pt(6.5), pt(1), fill=METRIC_BG)
        txt(c, num, pt(20) + nw/2, y + pt(0.5), "Inter-SB", 6.5, BLUE, "center")
        # Title
        txt(c, title, pt(31), y + pt(0.5), "Inter", 8.5, TEXT_DARK)
        # Dot leader
        ds = pt(31) + c.stringWidth(title, "Inter", 8.5) + pt(3)
        de = W - pt(30)
        c.setFillColor(HexColor("#cbd5e1"))
        dx = ds
        while dx < de:
            c.circle(dx, y + pt(2.5), 0.7, fill=1, stroke=0)
            dx += pt(2.8)
        txt(c, pg, W - pt(20), y + pt(0.5), "Inter-SB", 8.5, TEXT_SOFT, "right")
        y -= pt(0.5)
        hline(c, pt(20), W - pt(20), y, HexColor("#f1f5f9"))

    # Tools section
    y -= pt(8)
    txt(c, "ALATI ZA ODLUČIVANJE", pt(20), y, "Inter-SB", 7, TEXT_SOFT)
    y -= pt(3.5); hline(c, pt(20), W - pt(20), y); y -= pt(1.5)
    tools = [
        ("→","Koji proces automatizovati prvi: cheklista","8"),
        ("→","4 greške koje firme najčešće prave","9"),
    ]
    for num, title, pg in tools:
        y -= pt(8)
        txt(c, num, pt(22), y + pt(0.5), "Inter-SB", 9, BLUE)
        txt(c, title, pt(31), y + pt(0.5), "Inter", 8.5, TEXT_DARK)
        ds = pt(31) + c.stringWidth(title, "Inter", 8.5) + pt(3)
        de = W - pt(30)
        c.setFillColor(HexColor("#cbd5e1"))
        dx = ds
        while dx < de:
            c.circle(dx, y + pt(2.5), 0.7, fill=1, stroke=0)
            dx += pt(2.8)
        txt(c, pg, W - pt(20), y + pt(0.5), "Inter-SB", 8.5, TEXT_SOFT, "right")
        y -= pt(0.5)
        hline(c, pt(20), W - pt(20), y, HexColor("#f1f5f9"))

    draw_footer(c)


# ══════════════════════════════════════════════════════════════════════════════
#  PROCESS BLOCK
# ══════════════════════════════════════════════════════════════════════════════
def draw_process(c, num, title, category, desc, metrics, example, y):
    # Number + title row
    txt(c, num, pt(20), y, "Inter-BL", 22, BLUE)
    txt(c, title, pt(36), y + pt(1), "Inter-B", 11.5, TEXT_DARK)
    # Category pill
    cy2 = y - pt(6.5)
    cw2 = c.stringWidth(category, "Inter-SB", 6.5) + pt(7)
    rrect(c, pt(36), cy2 - pt(1.5), cw2, pt(6.5), pt(2.5),
          fill=METRIC_BG, stroke=METRIC_BRD, lw=0.5)
    txt(c, category, pt(36) + cw2/2, cy2 + pt(0.5), "Inter-SB", 6.5, BLUE, "center")

    y -= pt(13)
    hline(c, pt(20), W - pt(20), y)
    y -= pt(5)

    # Description
    y = wrap(c, desc, pt(20), y, W - pt(40), "Inter", 8.5, TEXT_MID, pt(4.8))
    y -= pt(3)

    # Metrics
    mw = (W - pt(40) - pt(4)) / 3
    for i, (val, lbl) in enumerate(metrics):
        mx = pt(20) + i * (mw + pt(2))
        rrect(c, mx, y - pt(16), mw, pt(18), pt(2.5), fill=METRIC_BG, stroke=METRIC_BRD, lw=0.5)
        # Left accent on first metric
        if i == 0:
            gradient_bar(c, mx, y - pt(16), pt(0.8), pt(18), BLUE, CYAN)
        txt(c, val, mx + pt(4), y - pt(3.5), "Inter-B", 9.5, BLUE)
        wrap(c, lbl, mx + pt(4), y - pt(10), mw - pt(8), "Inter", 6.8, TEXT_SOFT, pt(3.8))
    y -= pt(20)

    # Example box
    words = example.split(); lines_c = []; cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if c.stringWidth(test, "Inter", 7.8) <= W - pt(40) - pt(14):
            cur = test
        else:
            lines_c.append(cur); cur = w
    if cur: lines_c.append(cur)
    eh = pt(8) + len(lines_c) * pt(4.5) + pt(4)
    rrect(c, pt(20), y - eh + pt(3), W - pt(40), eh, pt(2.5), fill=EX_BG, stroke=EX_BRD, lw=0.5)
    # Left accent bar
    gradient_bar(c, pt(20), y - eh + pt(3), pt(0.8), eh, BLUE, CYAN)
    txt(c, "Primer iz prakse", pt(27), y, "Inter-SB", 7, HexColor("#0369a1"))
    ey = y - pt(6)
    for line in lines_c:
        txt(c, line, pt(27), ey, "Inter", 7.8, TEXT_MID); ey -= pt(4.5)
    y -= eh + pt(2)
    return y


# ══════════════════════════════════════════════════════════════════════════════
#  CHECKLIST PAGE
# ══════════════════════════════════════════════════════════════════════════════
def draw_chapter_hdr(c, tag, title, subtitle, y):
    tw = c.stringWidth(tag, "Inter-SB", 7) + pt(9)
    rrect(c, pt(20), y - pt(2), tw, pt(8), pt(3), fill=METRIC_BG, stroke=METRIC_BRD, lw=0.5)
    txt(c, tag, pt(20) + tw/2, y + pt(1.5), "Inter-SB", 7, BLUE, "center")
    y -= pt(13)
    txt(c, title, pt(20), y, "Inter-XB", 16, TEXT_DARK)
    y -= pt(8)
    wrap(c, subtitle, pt(20), y, W - pt(40), "Inter", 8.5, TEXT_SOFT, pt(4.8))
    y -= pt(8)
    gradient_bar(c, pt(20), y, pt(16), pt(1.5), BLUE, CYAN)
    y -= pt(5)
    return y

def draw_checklist(c):
    c.setFillColor(white); c.rect(0, 0, W, H, fill=1, stroke=0)
    gradient_bar(c, 0, H - pt(1.2), W, pt(1.2), BLUE, CYAN)

    y = H - pt(22)
    y = draw_chapter_hdr(c,
        "Alat za odlučivanje", "Koji proces automatizovati prvi?",
        "Odgovorite na ova pitanja za svaki proces koji razmatrate. Proces koji dobije "
        "najviše potvrdnih odgovora ima prioritet.", y)

    y = wrap(c,
        "Ne treba automatizovati sve odjednom. Firme koje pokušaju to završe sa skupim sistemima "
        "koji ne rade dobro ni jedan zadatak. Koristite ovu cheklistu da izaberete prvi korak.",
        pt(20), y, W - pt(40), "Inter", 8.5, TEXT_MID, pt(4.8))
    y -= pt(5)

    checks = [
        ("Dešava se više od 5 puta nedeljno?",
         "Procesi koji se retko dešavaju nisu dobri kandidati. Vreme podešavanja nije opravdano."),
        ("Sledi predvidivi redosled koraka svaki put?",
         "Što je proces konzistentniji, lakše se automatizuje i manje grešaka je moguće."),
        ("Teško je naći ili zadržati osobu koja to radi?",
         "Ako imate visoku fluktuaciju na toj poziciji, automatizacija uklanja taj rizik."),
        ("Postoji digitalni input i output?",
         "Procesi u digitalnim sistemima se lako automatizuju. Fizički su kompleksniji."),
        ("Greške imaju vidljive posledice?",
         "Posebno vredna automatizacija gde greška znači gubitak klijenta ili novčanu štetu."),
        ("Tim se žali na ovaj zadatak?",
         "Procesi koji frustriraju tim su prvi kandidati. Oslobađate energiju za kreativniji rad."),
    ]
    item_h = pt(18)
    cols = 2
    col_w = (W - pt(40) - pt(4)) / cols
    for i, (q, a) in enumerate(checks):
        col = i % cols
        row = i // cols
        ix = pt(20) + col * (col_w + pt(4))
        iy = y - row * (item_h + pt(3))
        rrect(c, ix, iy - item_h + pt(3), col_w, item_h, pt(2.5),
              fill=HexColor("#f8fafc"), stroke=HexColor("#e2e8f0"), lw=0.5)
        # Checkbox
        rrect(c, ix + pt(4), iy - pt(3), pt(5), pt(5), pt(0.8),
              fill=white, stroke=BLUE, lw=0.8)
        txt(c, q, ix + pt(12), iy - pt(0.5), "Inter-SB", 7.3, TEXT_DARK)
        wrap(c, a, ix + pt(12), iy - pt(6.5), col_w - pt(16),
             "Inter", 6.8, TEXT_SOFT, pt(3.8))

    y -= (len(checks)//cols) * (item_h + pt(3)) + pt(5)

    # Score legend
    scores = [("1–2", "Niska prioritetnost"), ("3–4", "Dobar kandidat"), ("5–6", "Automatizujte odmah")]
    sw = (W - pt(40) - pt(4)) / 3
    for i, (val, lbl) in enumerate(scores):
        sx = pt(20) + i * (sw + pt(2))
        rrect(c, sx, y - pt(16), sw, pt(18), pt(2.5), fill=METRIC_BG, stroke=METRIC_BRD, lw=0.5)
        txt(c, val, sx + pt(4), y - pt(4), "Inter-BL", 13, BLUE)
        txt(c, lbl, sx + pt(4), y - pt(12), "Inter", 7, TEXT_SOFT)

    draw_footer(c, 8)


# ══════════════════════════════════════════════════════════════════════════════
#  MISTAKES PAGE
# ══════════════════════════════════════════════════════════════════════════════
def draw_mistakes(c):
    c.setFillColor(white); c.rect(0, 0, W, H, fill=1, stroke=0)
    gradient_bar(c, 0, H - pt(1.2), W, pt(1.2), BLUE, CYAN)

    y = H - pt(22)
    y = draw_chapter_hdr(c,
        "Česte greške", "Šta firme najčešće rade pogrešno",
        "Ovo su četiri greške koje vidimo kod gotovo svake firme koja prvi put ulazi u automatizaciju.", y)
    y -= pt(2)

    mistakes = [
        ("Pokušavaju da automatizuju previše odjednom",
         "Firme koje žele sve i odmah završe sa skupim sistemima koji ne rade dobro ni jedan zadatak. "
         "Počnite sa jednim procesom koji ima jasan ROI, implementirajte ga do kraja i izmerite rezultate."),
        ("Biraju alat pre nego što razumeju problem",
         "Kupiti ChatGPT pretplatu i čekati da se nešto desi nije strategija. Automatizacija kreće od analize "
         "procesa, ne od alata. Koji problem rešavamo? Gde se gubi vreme? Alati su poslednji korak."),
        ("Ne prate rezultate nakon implementacije",
         "Automatizacija bez merenja nije automatizacija, to je nada. Svaki proces mora imati jasne "
         "metrike: broj zahteva, vreme odgovora, ušteda sati. Bez merenja ne znate da li zarađujete."),
        ("Zaboravljaju da informišu tim",
         "Zaposleni koji ne razumeju zašto sistem radi ono što radi neće ga koristiti. Onboarding tima "
         "nije opcija, to je deo implementacije. Svaka uspešna automatizacija ima komunikacijsku komponentu."),
    ]

    for title_m, body in mistakes:
        # Estimate box height
        words = body.split(); lc = []; cur = ""
        bw = W - pt(40) - pt(22)
        for w in words:
            test = (cur + " " + w).strip()
            if c.stringWidth(test, "Inter", 8.3) <= bw: cur = test
            else: lc.append(cur); cur = w
        if cur: lc.append(cur)
        bh = pt(10) + len(lc) * pt(4.8) + pt(5)

        rrect(c, pt(20), y - bh + pt(3), W - pt(40), bh, pt(2.5),
              fill=ERR_BG, stroke=ERR_BRD, lw=0.5)
        # Red left bar
        c.setFillColor(ERR_ICON)
        c.rect(pt(20), y - bh + pt(3), pt(1), bh, fill=1, stroke=0)
        # Red X circle
        c.setFillColor(ERR_ICON)
        c.circle(pt(32), y - pt(3), pt(4), fill=1, stroke=0)
        txt(c, "✕", pt(32), y - pt(5.3), "Inter-B", 7, white, "center")
        # Title
        txt(c, title_m, pt(40), y - pt(0.5), "Inter-B", 9.5, TEXT_DARK)
        # Body
        wrap(c, body, pt(40), y - pt(8), bw, "Inter", 8.3, TEXT_MID, pt(4.8))
        y -= bh + pt(3)

    draw_footer(c, 9)


# ══════════════════════════════════════════════════════════════════════════════
#  CTA PAGE — clean, no grid
# ══════════════════════════════════════════════════════════════════════════════
def draw_cta(c):
    c.setFillColor(BG_DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # NO grid — only soft subtle glows
    soft_glow(c, W/2, H * 0.55, pt(120), HexColor("#1e3a8a"), layers=20)
    soft_glow(c, W * 0.3, H * 0.4, pt(60), CYAN, layers=10)
    soft_glow(c, W * 0.7, H * 0.65, pt(50), BLUE, layers=10)

    # Logo centered at top
    logo_size = pt(14)
    logo_x = W/2 - (logo_size + pt(2) + c.stringWidth("QUANTEX", "Inter-XB", logo_size * 0.42)) / 2
    draw_logo(c, logo_x, H - pt(32), logo_size, with_text=True, text_color=TEXT_LIGHT, with_tagline=True)

    # Eyebrow
    cy = H - pt(52)
    txt(c, "SLEDEĆI KORAK", W/2, cy, "Inter-B", 8, CYAN, "center")

    # Thin accent bar
    gradient_bar(c, W/2 - pt(12), cy - pt(5), pt(24), pt(0.8), BLUE, CYAN)

    cy -= pt(18)
    txt(c, "Koji procesi gube novac", W/2, cy, "Inter-BL", 24, TEXT_WHITE, "center")
    cy -= pt(12)

    # Two-color line
    p1 = "u "
    p2 = "vašoj firmi?"
    tw2 = c.stringWidth(p1, "Inter-BL", 24) + c.stringWidth(p2, "Inter-BL", 24)
    lx = W/2 - tw2/2
    txt(c, p1, lx, cy, "Inter-BL", 24, TEXT_WHITE)
    txt(c, p2, lx + c.stringWidth(p1, "Inter-BL", 24), cy, "Inter-BL", 24, BLUE_LIGHT)

    cy -= pt(18)
    desc = ("Ovaj vodič daje opštu sliku. Razgovor od 45 minuta analizira vaše konkretne "
            "procese, daje prioritete i okvirnu procenu troškova i ušteda. Bez obaveze. Bez žargona.")
    wrap(c, desc, W/2 - pt(72), cy, pt(144), "Inter", 9.5, TEXT_MUTE, pt(5.5))

    cy -= pt(26)
    bullets = [
        "Analiza gde vaš tim gubi vreme",
        "Top 3 prilike za automatizaciju",
        "Okvirna procena troškova i ušteda",
        "Bez obaveze i bez žargona",
    ]
    for b in bullets:
        bfw = c.stringWidth(b, "Inter-M", 9) + pt(8)
        bx = W/2 - bfw/2
        # Bullet dot
        c.setFillColor(BLUE)
        c.circle(bx + 2, cy + 3, 2.2, fill=1, stroke=0)
        txt(c, b, bx + pt(3), cy, "Inter-M", 9, TEXT_LIGHT)
        cy -= pt(8)

    cy -= pt(8)

    # CTA box
    box_w = pt(130)
    box_x = W/2 - box_w/2
    box_h = pt(30)
    rrect(c, box_x, cy - box_h + pt(4), box_w, box_h, pt(3.5),
          fill=CTA_BOX_BG, stroke=CTA_BOX_BRD, lw=1)
    # Accent top border on CTA box
    gradient_bar(c, box_x + pt(3), cy + pt(3), box_w - pt(6), pt(0.8), BLUE, CYAN)
    txt(c, "Zakažite besplatan razgovor", W/2, cy - pt(9), "Inter-SB", 8, TEXT_MUTE, "center")
    # URL
    url1 = "quantex"
    url2 = ".rs"
    uw = c.stringWidth(url1, "Inter-BL", 18) + c.stringWidth(url2, "Inter-BL", 18)
    ux = W/2 - uw/2
    txt(c, url1, ux, cy - pt(20), "Inter-BL", 18, TEXT_WHITE)
    txt(c, url2, ux + c.stringWidth(url1, "Inter-BL", 18), cy - pt(20), "Inter-BL", 18, BLUE_LIGHT)

    cy -= box_h + pt(5)
    txt(c, "ili pišite na office@quantex.rs", W/2, cy, "Inter", 8, TEXT_SOFT, "center")

    # Footer
    hline(c, pt(20), W - pt(20), pt(14), HexColor("#1a2d50"))
    txt(c, "© 2026 Quantex · quantex.rs · office@quantex.rs",
        W/2, pt(8), "Inter", 7.5, HexColor("#475569"), "center")


# ══════════════════════════════════════════════════════════════════════════════
#  DATA
# ══════════════════════════════════════════════════════════════════════════════
PROCESSES = [
    ("01", "Odgovaranje na upite klijenata", "Korisnička podrška · AI Agent",
     "Svaka firma prima iste ili slične upite: cena, rok isporuke, dostupnost, radno vreme. "
     "Vaš tim provodi sate svake nedelje odgovarajući ručno. AI agent obučen na vašim podacima "
     "odgovara za sekunde, tačno i konzistentno, 24 sata dnevno, bez grešaka.",
     [("8–20 sati","prosečna ušteda nedeljno"),("94%+","tačnost odgovora"),("3–5 mes.","povrat investicije")],
     "Stomatološka klinika uvela AI agenta koji preuzima 85% pitanja o cenama i terminima. "
     "Broj poziva na recepciji pao za 60%. Osoblje sada provodi vreme sa pacijentima."),
    ("02", "Zakazivanje termina i podsetnici", "Operacije · Automatizacija zakazivanja",
     "Ručno zakazivanje je jedna od najvećih gubljenja vremena u uslužnim firmama. Sistem preuzima sve: "
     "klijent sam bira termin, dobija automatski potvrdu i podsetnike, a otkazani termin se nudi čekaocu.",
     [("do 65%","smanjenje ne-dolazaka"),("5–12 sati","admin ušteda nedeljno"),("2–4 mes.","povrat investicije")],
     "Agencija za nekretnine eliminisala 10 mejlova po klijentu za koordinaciju obilazaka. "
     "U prvoj nedelji sistem je automatski potvrdio 43 termina bez ijednog ručnog poziva."),
    ("03", "Pronalaženje i kvalifikacija novih klijenata", "Prodaja · Generisanje lidova",
     "Ručno istraživanje tržišta i praćenje odgovora troši sate dnevno. Automatizovani sistem pronalazi firme "
     "po idealnom profilu, stupa u kontakt i prosleđuje zainteresovane prodajnom timu.",
     [("15–25","kvalifikovanih lidova nedeljno"),("2–4x","poboljšanje konverzije"),("4–6 mes.","povrat investicije")],
     "Distributer prehrambenih proizvoda sa 15 do 20 kvalifikovanih lidova nedeljno. Prodajni tim se bavi "
     "isključivo firmama koje su već pokazale interes."),
    ("04", "Obrada mejlova i interne poruke", "Produktivnost · AI obrada teksta",
     "Prosečan zaposleni potroši 2,5 sata dnevno na mejlove. AI čita svaki dolazni mejl, kategorizuje ga, "
     "šalje automatski odgovor na tipične ili prosleđuje sa sažetkom. Ništa se ne gubi, ništa ne čeka.",
     [("60–80%","mejlova automatski obrađeno"),("1–1,5 sat","ušteda po zaposlenom dnevno"),("3–5 mes.","povrat investicije")],
     "Logistička firma automatizovala obradu 450 mejlova dnevno. Svaki mejl se kategorizuje za 3 sekunde. "
     "Nema više propuštenih hitnih zahteva."),
    ("05", "Nedeljni i mesečni izveštaji", "Upravljanje · Automatizacija podataka",
     "Svaki ponedeljak neko provede jutro skupljajući podatke iz različitih sistema i šaljući direktoru. "
     "Sistem automatski prikuplja podatke, formatira izveštaj i šalje ga u sanduče, gotov za čitanje.",
     [("80–200 sati","godišnja ušteda"),("100%","tačnost podataka"),("2–3 mes.","povrat investicije")],
     "E-commerce firma: integracija WooCommerce, Gmail i Sheets. Svaki ponedeljak u 7h direktor "
     "dobija izveštaj o prodaji, zalihama i narudžbinama. Ranije je to trajalo 2,5 sata."),
    ("06", "Uvođenje novih zaposlenih", "HR · Onboarding automatizacija",
     "Svaki novi zaposleni prolazi kroz iste korake i pita ista pitanja. Automatizovani sistem vodi "
     "svakog novog zaposlenog kroz strukturisan program i odgovara iz baze znanja.",
     [("70%+","pitanja rešena automatski"),("40–60%","skraćeno vreme uvođenja"),("3–5 mes.","povrat investicije")],
     "Firma sa 120 zaposlenih uvela AI asistenta za onboarding. HR tim prima 70% manje internih "
     "pitanja od novih zaposlenih. Asistent dostupan 24 sata."),
    ("07", "Fakturisanje i praćenje naplate", "Finansije · Automatizacija toka novca",
     "Generisanje faktura, slanje, podsetnici, evidentiranje uplata — sve ručno u većini srpskih firmi. "
     "Sistem generiše fakturu posle svake usluge, prati status i šalje podsetnike.",
     [("35–50%","ubrzanje naplate"),("3–8 sati","admin ušteda nedeljno"),("2–4 mes.","povrat investicije")],
     "IT firma sa 25 klijenata: fakturisanje oduzimalo 5 sati nedeljno. Sada automatski, "
     "upozorenja samo kad je potrebna ljudska intervencija."),
    ("08", "Interni Q&A sistem za tim", "Znanje · Interni AI asistent",
     "Zaposleni gube vreme tražeći interne informacije. AI asistent obučen na pravilnicima i procedurama "
     "odgovara za sekunde, dostupan 24 sata, nikad nije na odsustvu.",
     [("75–90%","internih upita rešenih"),("15 min → 10 sek","vreme pronalaska info"),("3–5 mes.","povrat investicije")],
     "Distribucijska firma sa 80 zaposlenih: tim svakodnevno slao mejlove HR-u za procedure. "
     "Asistent sada odgovara za sekunde iz baze od 200+ dokumenata."),
    ("09", "Upravljanje društvenim mrežama", "Marketing · Automatizacija komunikacije",
     "Odgovaranje na komentare, poruke, prikupljanje recenzija, praćenje pominjanja brenda. "
     "Sistem odgovara na standardne komentare, prosleđuje kompleksne i upozorava na negativna pominjanja.",
     [("3–5x","rast broja recenzija"),("12h → 2 min","vreme odgovora"),("3–4 mes.","povrat investicije")],
     "Restoran: Google recenzije porasle sa 40 na 180 za tri meseca. Negativne recenzije se "
     "otkrivaju odmah, menadžer reaguje pre eskalacije."),
    ("10", "Unos i obrada podataka između sistema", "Operacije · RPA automatizacija",
     "Prepisivanje podataka iz jednog sistema u drugi, popunjavanje formulara, ažuriranje tabela. "
     "Najčistiji primer posla koji sistem može obaviti savršenije i brže od čoveka. Svaki put. Bez grešaka.",
     [("99,9%","eliminacija grešaka"),("100x brže","od ručnog unosa"),("2–4 mes.","povrat investicije")],
     "Računovodstvena agencija automatizovala unos iz klijentskih sistema. Eliminisano 15 sati "
     "nedeljnog ručnog unosa i sve greške u procesu."),
]


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    out = Path("/home/aceman/Documents/quantex.rs/vodic-besplatni.pdf")
    c = canvas.Canvas(str(out), pagesize=A4)
    c.setTitle("10 poslovnih procesa koji se mogu automatizovati danas | Quantex")
    c.setAuthor("Quantex")
    c.setSubject("AI automatizacija za srpske firme")

    # Page 1: Cover
    draw_cover(c); c.showPage()

    # Page 2: TOC
    draw_toc(c); c.showPage()

    # Process pages
    groups = [[0,1], [2,3,4], [5,6,7], [8,9]]
    page_num = 4
    for group in groups:
        c.setFillColor(white); c.rect(0, 0, W, H, fill=1, stroke=0)
        gradient_bar(c, 0, H - pt(1.2), W, pt(1.2), BLUE, CYAN)

        if group[0] == 0:
            y = H - pt(22)
            y = draw_chapter_hdr(c,
                "Procesi 01–10", "Šta možete automatizovati već ovog meseca",
                "Za svaki proces navedeni su realni primeri, tipična ušteda u satima i procena perioda povrata.", y)
        else:
            y = H - pt(18)

        for idx in group:
            p = PROCESSES[idx]
            y = draw_process(c, *p, y)
            if idx != group[-1]:
                hline(c, pt(20), W - pt(20), y, HexColor("#f1f5f9"), lw=0.8)
                y -= pt(4)

        draw_footer(c, page_num)
        page_num += 1
        c.showPage()

    # Page 7: Checklist
    draw_checklist(c); c.showPage()

    # Page 8: Mistakes
    draw_mistakes(c); c.showPage()

    # Page 9: CTA
    draw_cta(c); c.showPage()

    c.save()
    print(f"PDF: {out}  ({out.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    main()
