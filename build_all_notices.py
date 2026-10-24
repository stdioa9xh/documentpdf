"""
Builds the 8 DEMO vacancy notices (notices/<id>.pdf + .json) — one per qualification level and age band, all
applying through the same demo Google Form. Fictional board; not Government notifications.
Run:  python build_all_notices.py      (needs reportlab; reuses the layout in build_notification.py)
"""
import json
import os
from datetime import date

import build_notification as bn

CUTOFF = date(2027, 1, 1)
EDU_DOCS = {  # qualification → documents beyond Class 10 / Aadhaar
    "10th": [],
    "12th": [("Class 12 (Higher Secondary) marksheet", "All candidates", "Essential qualification")],
    "diploma": [("Diploma certificate in Engineering (3-year, AICTE / State Board)", "All candidates",
                 "Essential qualification — Civil, Mechanical or Electrical")],
    "graduate": [("Class 12 (Higher Secondary) marksheet", "All candidates", "Roll number and board"),
                 ("Graduation degree certificate and marksheets", "All candidates", "Essential qualification")],
    "postgraduate": [("Class 12 (Higher Secondary) marksheet", "All candidates", "Roll number and board"),
                     ("Graduation degree certificate", "All candidates", "Prerequisite for the PG degree"),
                     ("Post-graduate degree certificate and marksheets", "All candidates", "Essential qualification")],
}
EDU_TEXT = {
    "10th": "Matriculation (Class 10) pass from a recognised Board, on or before 01/01/2027.",
    "12th": "Higher Secondary (Class 12) pass from a recognised Board, on or before 01/01/2027.",
    "diploma": "3-year Diploma in Civil, Mechanical or Electrical Engineering from an AICTE-approved institute or "
               "State Board of Technical Education, on or before 01/01/2027. B.E./B.Tech holders are also eligible.",
    "graduate": "Bachelor's Degree in any discipline from a recognised University, obtained on or before 01/01/2027.",
    "postgraduate": "Master's Degree in Economics, Statistics, Mathematics, Commerce or Public Policy from a recognised "
                    "University, obtained on or before 01/01/2027.",
}


def split(total):
    """Category-wise split (UR 40.5%, OBC 27%, EWS 10%, SC 15%, ST 7.5%) adding up to total."""
    shares = {"OBC": 0.27, "EWS": 0.10, "SC": 0.15, "ST": 0.075}
    v = {k: round(total * s) for k, s in shares.items()}
    return {"UR": total - sum(v.values()), **v}


def notice(vid, no, exam, post, pay, total, edu, lo, hi, closes, selection, extra_docs=(), physical=None):
    born_from = date(CUTOFF.year - hi - 1, 1, 2).strftime("%d/%m/%Y")
    born_to = date(CUTOFF.year - lo, 1, 1).strftime("%d/%m/%Y")
    docs = [{"document": "Class 10 (Matriculation) certificate / marksheet", "for": "All candidates",
             "purpose": "Proof of name and date of birth — the only document accepted for date of birth"}]
    docs += [{"document": d, "for": f, "purpose": p} for d, f, p in EDU_DOCS[edu]]
    docs += [{"document": d, "for": f, "purpose": p} for d, f, p in extra_docs]
    docs += [d for d in bn.N["required_documents"] if d["document"].startswith(
        ("Aadhaar", "OBC-NCL", "EWS", "SC / ST", "Disability", "Recent passport", "Name-change"))]
    n = json.loads(json.dumps(bn.N))  # same structure as the CGLE notice
    n.update({
        "id": vid, "advertisement_no": f"ADRB/{no}-DEMO/2026/01", "exam": exam,
        "posts": [{"post": post, "pay_level": pay, "group": "Group C", "vacancies": split(total), "total": total}],
        "total_vacancies": total,
        "age": {**n["age"], "min": lo, "max": hi, "born_between": f"{born_from} and {born_to} (both days inclusive)"},
        "education": EDU_TEXT[edu], "min_education": edu, "selection": selection, "required_documents": docs,
    })
    from datetime import datetime, timedelta
    c = datetime.strptime(closes, "%d/%m/%Y").date()
    dmy = lambda x: x.strftime("%d/%m/%Y")
    n["dates"].update({"application_closes": f"{closes} (23:00 hrs)",
                       "fee_payment_last_date": f"{dmy(c + timedelta(days=1))} (23:00 hrs)",
                       "correction_window": f"{dmy(c + timedelta(days=3))} – {dmy(c + timedelta(days=4))}"})
    n["important_instructions"] = [s.replace("25/11/2026", closes) for s in n["important_instructions"]]
    if physical:
        n["physical_standards"] = physical
        n["important_instructions"] = n["important_instructions"] + [
            "Candidates must meet the Physical Standards (PST) and pass the Physical Efficiency Test (PET) described in "
            "Section 7; height relaxation applies to ST candidates and hill/North-East areas."]
    return n


GD_PHYSICAL = ["Height: Men 170 cm, Women 157 cm (ST: 162.5 / 150 cm)", "Chest (men): 80 cm + 5 cm expansion",
               "PET: Men 5 km in 24 minutes; Women 1.6 km in 8.5 minutes", "Not open to PwBD candidates"]
CBT = "Computer Based Examination (100 marks, 60 minutes; Reasoning, General Awareness, Quantitative Aptitude, English)"
NOTICES = [
    notice("adrb-mts-demo-2026", "MTS", "Multi-Tasking Staff Examination (Demo), 2026", "Multi-Tasking Staff",
           "Level 1 (Rs. 18,000–56,900)", 2400, "10th", 18, 25, "20/11/2026", [CBT, "Document Verification"]),
    notice("adrb-constable-demo-2026", "CONST", "Constable (General Duty) Examination (Demo), 2026", "Constable (GD)",
           "Level 3 (Rs. 21,700–69,100)", 3000, "10th", 18, 23, "30/11/2026",
           [CBT, "Physical Standard Test (PST) and Physical Efficiency Test (PET)", "Medical Examination",
            "Document Verification"], physical=GD_PHYSICAL),
    notice("adrb-ldc-demo-2026", "LDC", "Lower Division Clerk & Data Entry Operator Examination (Demo), 2026",
           "Lower Division Clerk / Data Entry Operator", "Level 2–4 (Rs. 19,900–81,100)", 1800, "12th", 18, 27,
           "22/11/2026", [CBT, "Typing Test: 35 words per minute in English or 30 in Hindi", "Document Verification"]),
    notice("adrb-tech-demo-2026", "JT", "Junior Technician Examination (Demo), 2026", "Junior Technician (Civil/Mech/Elec)",
           "Level 6 (Rs. 35,400–1,12,400)", 900, "diploma", 18, 30, "05/12/2026",
           ["Computer Based Examination (General Intelligence, General Awareness, Engineering discipline paper)",
            "Document Verification"]),
    notice("adrb-aso-demo-2026", "ASO", "Assistant Section Officer Examination (Demo), 2026", "Assistant Section Officer",
           "Level 7 (Rs. 44,900–1,42,400)", 600, "graduate", 20, 30, "28/11/2026",
           [CBT, "Tier-II: Descriptive paper and Computer Proficiency Test", "Document Verification"]),
    notice("adrb-senior-asst-demo-2026", "SA", "Senior Assistant (Lateral Entry) Examination (Demo), 2026",
           "Senior Assistant", "Level 6 (Rs. 35,400–1,12,400)", 300, "graduate", 25, 40, "10/12/2026",
           [CBT, "Interview / Personality Test", "Document Verification"],
           extra_docs=[("Experience certificate (if any)", "Only candidates claiming experience", "Interview weightage")]),
    notice("adrb-research-demo-2026", "RO", "Research Officer Examination (Demo), 2026", "Research Officer",
           "Level 10 (Rs. 56,100–1,77,500)", 150, "postgraduate", 21, 35, "15/12/2026",
           ["Written Examination (subject paper, 200 marks)", "Interview (50 marks)", "Document Verification"]),
]

if __name__ == "__main__":
    os.makedirs("notices", exist_ok=True)
    cgle = json.loads(json.dumps(bn.N))
    cgle.update({"id": "adrb-cgle-demo-2026", "min_education": "graduate"})
    for n in [cgle] + NOTICES:
        bn.N = n
        bn.build_pdf(f"notices/{n['id']}.pdf")
        with open(f"notices/{n['id']}.json", "w", encoding="utf-8") as f:
            json.dump({**n, "disclaimer": bn.DISCLAIMER}, f, ensure_ascii=False, indent=2)
        print(f"{n['id']:28} {n['age']['min']}-{n['age']['max']}  {n['min_education']:12} {n['total_vacancies']:>5} posts")
