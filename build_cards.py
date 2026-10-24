"""Builds the ApplyEase carousel card images (1000x500 PNG) — no official logos, one consistent design per sector."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1000, 500
FONT = "C:/Windows/Fonts/segoeuib.ttf" if os.path.exists("C:/Windows/Fonts/segoeuib.ttf") else "arialbd.ttf"
FONT_R = "C:/Windows/Fonts/segoeui.ttf" if os.path.exists("C:/Windows/Fonts/segoeui.ttf") else "arial.ttf"
SECTORS = {  # label, gradient start, gradient end
    "ssc": ("STAFF SELECTION · CENTRAL GOVT", "#312e81", "#6366f1"),
    "rail": ("RAILWAYS", "#134e4a", "#14b8a6"),
    "defence": ("DEFENCE · OFFICER ENTRY", "#365314", "#65a30d"),
    "police": ("POLICE · CAPF", "#0f172a", "#475569"),
    "upsc": ("UNION PUBLIC SERVICE", "#7f1d1d", "#dc2626"),
    "bank": ("BANKING", "#1e3a8a", "#3b82f6"),
    "engg": ("ENGINEERING", "#7c2d12", "#f97316"),
    "state": ("STATE GOVT", "#581c87", "#a855f7"),
    "demo": ("DEMO VACANCY · FULL PIPELINE", "#4c1d95", "#db2777"),
    "ladder": ("CAREER LADDER · TIER 2", "#0c4a6e", "#06b6d4"),
    "docs": ("DOCUMENT CHECK · GEMINI VISION", "#064e3b", "#10b981"),
}
JOBS = [  # id, sector, title, subtitle, chip
    ("ssc-chsl-2026", "ssc", "SSC CHSL", "Staff Selection Commission · 10+2 level", "Level 2–5 · ₹19,900–92,300"),
    ("rrb-ntpc-ug-2026", "rail", "RRB NTPC (UG)", "Railway Recruitment Boards · Clerk posts", "Level 2–3"),
    ("ssc-gd-2027", "police", "SSC GD Constable", "BSF · CISF · CRPF · SSB · ITBP · AR", "Level 3 · ₹21,700–69,100"),
    ("rrb-group-d-2026", "rail", "RRB Group D", "Railway Recruitment Boards · Level 1", "₹18,000 basic"),
    ("upsc-nda-i-2027", "defence", "UPSC NDA & NA", "Army · Navy · Air Force officer entry", "Level 10 after training"),
    ("ssc-mts-2026", "ssc", "SSC MTS & Havaldar", "Staff Selection Commission · 10th pass", "Level 1 · ₹18,000"),
    ("rrb-je-2026", "engg", "RRB Junior Engineer", "Railway Recruitment Boards · Diploma / B.Tech", "Level 6 · ₹35,400+"),
    ("mpesb-sub-eng-2026", "state", "MPESB Sub Engineer", "MP Employee Selection Board", "MP Pay Level 9"),
    ("ssc-cpo-si-2026", "police", "SSC CPO Sub-Inspector", "Delhi Police · CAPF · Graduate", "Level 6 · ₹35,400+"),
    ("ssc-cgl-2027", "ssc", "SSC CGL", "Staff Selection Commission · Graduate", "Level 4–7 · up to ₹1,42,400"),
    ("ibps-po-xiv", "bank", "IBPS PO", "Institute of Banking Personnel Selection", "JMGS-I · ₹48,480 basic"),
    ("upsc-cds-i-2027", "defence", "UPSC CDS", "Combined Defence Services · Graduate", "Level 10"),
    ("upsc-cse-2027", "upsc", "UPSC Civil Services", "IAS · IPS · IFS and allied services", "Level 10 onwards"),
    ("adrb-cgle-demo-2026", "demo", "ADRB CGLE 2026", "Demo board · notification PDF + Google Form", "1,700 posts · apply via Agent 2"),
    ("adrb-mts-demo-2026", "demo", "ADRB MTS 2026", "Demo board · 10th pass · age 18–25", "2,400 posts · apply via Agent 2"),
    ("adrb-constable-demo-2026", "demo", "ADRB Constable (GD)", "Demo board · 10th pass · physical test", "3,000 posts · apply via Agent 2"),
    ("adrb-ldc-demo-2026", "demo", "ADRB LDC & DEO 2026", "Demo board · 12th pass · typing test", "1,800 posts · apply via Agent 2"),
    ("adrb-tech-demo-2026", "demo", "ADRB Junior Technician", "Demo board · Engineering diploma", "900 posts · apply via Agent 2"),
    ("adrb-aso-demo-2026", "demo", "ADRB ASO 2026", "Demo board · Graduate · age 20–30", "600 posts · apply via Agent 2"),
    ("adrb-senior-asst-demo-2026", "demo", "ADRB Senior Assistant", "Demo board · Graduate · age 25–40", "300 posts · apply via Agent 2"),
    ("adrb-research-demo-2026", "demo", "ADRB Research Officer", "Demo board · Post-graduate · age 21–35", "150 posts · apply via Agent 2"),
    ("career-ladder", "ladder", "Career Ladder", "Posts you unlock next — gap, age, attempts", "Tier 2 analysis"),
    ("document-check", "docs", "Check My Documents", "Class 10 vs Aadhaar · certificates · affidavit", "Upload with +"),
] + [(f"sector-{k}", k, v[0].split(" · ")[0].title(), "Government recruitment", "ApplyEase") for k, v in SECTORS.items()
     if k not in ("demo", "ladder", "docs")]


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def card(sector, title, subtitle, chip):
    label, a, b = SECTORS[sector]
    a, b = rgb(a), rgb(b)
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        for x in range(W):
            t = (x / W) * 0.65 + (y / H) * 0.35
            px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
    deco = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(deco)
    for r, alpha in ((330, 26), (240, 22), (150, 18)):
        dd.ellipse([W - 120 - r, -60 - r, W - 120 + r, -60 + r], outline=(255, 255, 255, alpha), width=3)
    dd.ellipse([W - 260, H - 210, W + 60, H + 110], fill=(255, 255, 255, 14))
    img = Image.alpha_composite(img.convert("RGBA"), deco.filter(ImageFilter.GaussianBlur(0.6)))
    f = lambda n, bold=True: ImageFont.truetype(FONT if bold else FONT_R, n)
    chip_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))  # translucent chip must be blended, not drawn opaque
    tw = ImageDraw.Draw(chip_layer).textlength(label, font=f(20))
    ImageDraw.Draw(chip_layer).rounded_rectangle([56, 52, 56 + tw + 36, 92], radius=20, fill=(255, 255, 255, 52))
    img = Image.alpha_composite(img, chip_layer)
    d = ImageDraw.Draw(img)
    d.text((74, 72), label, font=f(20), fill="white", anchor="lm")
    size = 76
    while d.textlength(title, font=f(size)) > W - 140 and size > 44:
        size -= 4
    d.text((56, 215), title, font=f(size), fill="white", anchor="ls")
    d.text((58, 265), subtitle, font=f(28, False), fill=(255, 255, 255, 225), anchor="ls")
    cw = d.textlength(chip, font=f(24))
    d.rounded_rectangle([56, 330, 56 + cw + 40, 378], radius=24, fill=(255, 255, 255, 235))
    d.text((76, 354), chip, font=f(24), fill=a, anchor="lm")
    d.text((W - 56, H - 46), "ApplyEase", font=f(26), fill=(255, 255, 255, 200), anchor="rs")
    return img.convert("RGB")


if __name__ == "__main__":
    os.makedirs("cards", exist_ok=True)
    for cid, sector, title, sub, chip in JOBS:
        card(sector, title, sub, chip).save(f"cards/{cid}.png", optimize=True)
    print(len(JOBS), "cards")
