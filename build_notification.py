"""
Builds the DEMO recruitment notification used by the ApplyEase agents:
  notification.pdf   — the notice Agent 1 reads with Gemini (looks like a real advertisement)
  notification.json  — the same facts, structured; ground truth to check Gemini's extraction

Fictional: the "ApplyEase Demo Recruitment Board" does not exist and this is not a government notice.
Run:  python build_notification.py
"""
import json
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScWbD6ApjwoqGoubmz9i4qrvZNCnt2nNhasSe8kiQ3Feqko7w/viewform"

N = {
    "board": "ApplyEase Demo Recruitment Board (ADRB)",
    "demo": True,
    "advertisement_no": "ADRB/CGLE-DEMO/2026/01",
    "notice_date": "24/10/2026",
    "exam": "Combined Graduate Level Examination (Demo), 2026",
    "posts": [
        {"post": "Junior Assistant", "pay_level": "Level 4 (Rs. 25,500–81,100)", "group": "Group C",
         "vacancies": {"UR": 506, "OBC": 337, "EWS": 125, "SC": 188, "ST": 94}, "total": 1250},
        {"post": "Data Entry Supervisor", "pay_level": "Level 5 (Rs. 29,200–92,300)", "group": "Group C",
         "vacancies": {"UR": 182, "OBC": 121, "EWS": 45, "SC": 68, "ST": 34}, "total": 450},
    ],
    "total_vacancies": 1700,
    "pwbd_reservation": "4% of vacancies, horizontal, across categories",
    "dates": {
        "application_opens": "24/10/2026",
        "application_closes": "25/11/2026 (23:00 hrs)",
        "fee_payment_last_date": "26/11/2026 (23:00 hrs)",
        "correction_window": "28/11/2026 – 29/11/2026",
        "tier1_exam": "January – February 2027 (tentative)",
    },
    "age": {
        "cutoff_date": "01/01/2027",
        "min": 18, "max": 27,
        "born_between": "02/01/2000 and 01/01/2009 (both days inclusive)",
        "relaxation_years": {"OBC (Non-Creamy Layer)": 3, "SC": 5, "ST": 5, "PwBD (UR)": 10, "PwBD (OBC)": 13,
                             "PwBD (SC/ST)": 15, "Ex-Servicemen": "3 years after deduction of military service"},
        "ews_note": "No age relaxation for EWS candidates.",
    },
    "education": "Bachelor's Degree in any discipline from a recognised University, obtained on or before 01/01/2027.",
    "fee": {"General/OBC/EWS": "Rs. 100", "Women, SC, ST, PwBD, Ex-Servicemen": "Exempted"},
    "selection": ["Tier-I: Computer Based Examination (200 marks, 60 minutes; Reasoning, General Awareness, "
                  "Quantitative Aptitude, English; 0.50 negative marking)",
                  "Tier-II: Computer Based Examination incl. Data Entry Speed Test (DEST) for Data Entry Supervisor",
                  "Document Verification"],
    "application_form_url": FORM_URL,
    "application_form_fields": [
        "Full Name", "Aadhaar Number", "Gender", "Date of Birth", "Father's Name", "Mother's Name",
        "10th Examination Board", "Roll Number (10th Standard)", "12th Examination Board", "Roll Number (12th Standard)",
        "Highest Educational Qualification Level", "Mobile Number", "Email Address", "Permanent Address",
        "Present Address", "Category", "Nationality"],
    "required_documents": [
        {"document": "Class 10 (Matriculation) certificate / marksheet", "for": "All candidates",
         "purpose": "Proof of name and date of birth — the only document accepted for date of birth"},
        {"document": "Class 12 (Higher Secondary) marksheet", "for": "All candidates", "purpose": "Roll number and board"},
        {"document": "Graduation degree certificate and marksheets", "for": "All candidates",
         "purpose": "Essential qualification (provisional certificate accepted if issued on or before the cut-off date)"},
        {"document": "Aadhaar card (masked — first 8 digits hidden)", "for": "All candidates", "purpose": "Photo identity"},
        {"document": "OBC-NCL certificate in the Central Government format", "for": "OBC candidates",
         "purpose": "Reservation and age relaxation; must be issued on or after 01/04/2026 (FY 2026-27)"},
        {"document": "EWS Income & Asset certificate for FY 2026-27", "for": "EWS candidates", "purpose": "Reservation"},
        {"document": "SC / ST certificate from the competent authority", "for": "SC/ST candidates",
         "purpose": "Reservation, age relaxation and fee exemption"},
        {"document": "Disability certificate (40% or more)", "for": "PwBD candidates", "purpose": "Reservation and relaxation"},
        {"document": "Recent passport-size photograph and signature", "for": "All candidates", "purpose": "Admit card and identity"},
        {"document": "Name-change affidavit / Gazette notification", "for": "Only if the name differs across documents",
         "purpose": "Proof that the names refer to the same person"},
    ],
    "important_instructions": [
        "Enter your name, father's name, mother's name and date of birth EXACTLY as recorded in the Class 10 certificate.",
        "If your name differs between documents (e.g. Class 10 vs Aadhaar), produce a notarised affidavit or Gazette "
        "notification at Document Verification; candidature is otherwise liable to be cancelled.",
        "Category status is determined as on the closing date of the online application (25/11/2026).",
        "Only one application per candidate. Multiple applications will be rejected.",
        "Candidates are advised to keep originals and two self-attested copies of every document ready for "
        "Document Verification.",
    ],
}

DISCLAIMER = ("DEMO DOCUMENT — The 'ApplyEase Demo Recruitment Board' is fictional. This is not a Government "
              "notification and no recruitment is being conducted. Created to demonstrate the ApplyEase multi-agent "
              "system (Fetch.ai / ASI Hackathon). Use only dummy data in the linked form.")


def build_pdf(path: str) -> None:
    ss = getSampleStyleSheet()
    H = ParagraphStyle("H", parent=ss["Title"], fontSize=15, leading=19, spaceAfter=2)
    SUB = ParagraphStyle("SUB", parent=ss["Normal"], alignment=TA_CENTER, fontSize=9.5, leading=12)
    H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=11.5, leading=14, spaceBefore=9, spaceAfter=4,
                        textColor=colors.HexColor("#0b2a5b"))
    B = ParagraphStyle("B", parent=ss["Normal"], fontSize=9.5, leading=12.5, alignment=TA_JUSTIFY)
    SMALL = ParagraphStyle("S", parent=B, fontSize=8, leading=10, textColor=colors.HexColor("#7a1f1f"))

    def table(rows, widths, head=True):
        t = Table(rows, colWidths=widths, repeatRows=1 if head else 0)
        t.setStyle(TableStyle([
            ("FONT", (0, 0), (-1, -1), "Helvetica", 8.8),
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.8) if head else ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.8),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dfe7f3")) if head else ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef2f8")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#8a97ab")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        return t

    def p(text):
        return Paragraph(text, B)

    story = [
        Paragraph(N["board"].upper(), H),
        Paragraph("(A fictional board created for a software demonstration)", SUB),
        Spacer(1, 4),
        Paragraph(f"<b>NOTICE — {N['exam']}</b>", SUB),
        Paragraph(f"Advertisement No. <b>{N['advertisement_no']}</b> &nbsp;&nbsp;|&nbsp;&nbsp; Dated: <b>{N['notice_date']}</b>", SUB),
        Spacer(1, 6),
        Paragraph(DISCLAIMER, SMALL),
        Paragraph("1. Introduction", H2),
        p(f"The {N['board']} will hold the <b>{N['exam']}</b> for recruitment to the Group C posts listed below. "
          "Candidates must apply <b>online only</b> through the official application form linked in Section 8. "
          "Applications by any other mode will not be accepted."),
        Paragraph("2. Important Dates", H2),
        table([["Event", "Date"]] + [[{"tier1_exam": "Tier-I exam"}.get(k, k.replace("_", " ").capitalize()), v]
                                     for k, v in N["dates"].items()], [70 * mm, 95 * mm]),
        Paragraph("3. Vacancies (category-wise)", H2),
        table([["Post", "Pay Level", "UR", "OBC", "EWS", "SC", "ST", "Total"]]
              + [[x["post"], x["pay_level"], *[x["vacancies"][c] for c in ("UR", "OBC", "EWS", "SC", "ST")], x["total"]]
                 for x in N["posts"]]
              + [["Total", "", *[sum(x["vacancies"][c] for x in N["posts"]) for c in ("UR", "OBC", "EWS", "SC", "ST")],
                  N["total_vacancies"]]],
              [38 * mm, 44 * mm, 13 * mm, 13 * mm, 13 * mm, 13 * mm, 13 * mm, 15 * mm]),
        Spacer(1, 3),
        p(f"PwBD reservation: {N['pwbd_reservation']}. Vacancies are provisional and may change."),
        Paragraph("4. Age Limit", H2),
        p(f"<b>{N['age']['min']}–{N['age']['max']} years as on {N['age']['cutoff_date']}</b>, i.e. candidates must have "
          f"been born between <b>{N['age']['born_between']}</b>. Upper age relaxation:"),
        Spacer(1, 3),
        table([["Category", "Relaxation (years)"]] + [[k, str(v)] for k, v in N["age"]["relaxation_years"].items()],
              [70 * mm, 95 * mm]),
        Spacer(1, 3),
        p(N["age"]["ews_note"]),
        Paragraph("5. Educational Qualification", H2),
        p(N["education"]),
        PageBreak(),
        Paragraph("6. Application Fee", H2),
        table([["Category", "Fee"]] + [[k, v] for k, v in N["fee"].items()], [95 * mm, 70 * mm]),
        Paragraph("7. Scheme of Selection", H2),
        *[p(f"({chr(97 + i)}) {s}") for i, s in enumerate(N["selection"])],
        *([Paragraph("Physical Standards & Physical Efficiency Test", H2)]
          + [p(f"• {x}") for x in N["physical_standards"]] if N.get("physical_standards") else []),
        Paragraph("8. How to Apply", H2),
        p("Apply only through the official online application form:"),
        p(f'<link href="{FORM_URL}" color="blue"><u>{FORM_URL}</u></link>'),
        Spacer(1, 3),
        p("The form asks for the following (keep these details ready, exactly as in your documents): "
          + "; ".join(N["application_form_fields"]) + "."),
        Paragraph("9. Documents Required (to be produced at Document Verification)", H2),
        table([["#", "Document", "Required from", "Purpose / condition"]]
              + [[str(i), Paragraph(d["document"], B), Paragraph(d["for"], B), Paragraph(d["purpose"], B)]
                 for i, d in enumerate(N["required_documents"], 1)],
              [8 * mm, 58 * mm, 34 * mm, 70 * mm]),
        KeepTogether([Paragraph("10. Important Instructions", H2)]
                     + [p(f"({i}) {s}") for i, s in enumerate(N["important_instructions"], 1)]),
        Spacer(1, 10),
        p("Sd/-<br/>Controller of Examinations (Demo)<br/>" + N["board"]),
    ]

    def page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 60)
        canvas.setFillColor(colors.Color(0.85, 0.1, 0.1, alpha=0.08))
        canvas.translate(A4[0] / 2, A4[1] / 2)
        canvas.rotate(35)
        canvas.drawCentredString(0, 0, "DEMO — NOT A GOVT NOTICE")
        canvas.restoreState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.grey)
        canvas.drawString(15 * mm, 10 * mm, f"{N['advertisement_no']} · {N['board']} · fictional demo document")
        canvas.drawRightString(A4[0] - 15 * mm, 10 * mm, f"Page {doc.page}")

    SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=15 * mm,
                      bottomMargin=17 * mm, title=f"{N['exam']} — {N['advertisement_no']}",
                      author=N["board"], subject="Demo recruitment notification").build(story, onFirstPage=page,
                                                                                        onLaterPages=page)


if __name__ == "__main__":
    build_pdf("notification.pdf")
    with open("notification.json", "w", encoding="utf-8") as f:
        json.dump({**N, "disclaimer": DISCLAIMER, "generated": date.today().isoformat()}, f, ensure_ascii=False, indent=2)
    print("built notification.pdf and notification.json")
