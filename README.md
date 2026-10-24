# ApplyEase — Demo Recruitment Notification

> **DEMO ONLY.** The *ApplyEase Demo Recruitment Board (ADRB)* is fictional. This is **not** a Government
> notification and no recruitment is being conducted. Use only dummy data in the linked form.

Test material for the **ApplyEase** multi-agent system (Fetch.ai / ASI Hackathon):

| File | What it is |
|---|---|
| [`notification.pdf`](notification.pdf) | The notice, laid out like a real recruitment advertisement. **Agent 1 reads it with Gemini.** |
| [`notification.json`](notification.json) | The same facts as structured data — ground truth to check what Gemini extracted. |
| [`sample_candidate.json`](sample_candidate.json) | A dummy applicant used in the demo. |
| [`build_notification.py`](build_notification.py) | Regenerates both files from one source (`pip install reportlab`). |

## The demo vacancy

**Combined Graduate Level Examination (Demo), 2026** — Advt. No. `ADRB/CGLE-DEMO/2026/01`

- **Posts:** Junior Assistant (1,250) and Data Entry Supervisor (450) — 1,700 total, category-wise split
- **Apply:** 25/10/2026 → 25/11/2026, only through the [online application form](https://docs.google.com/forms/d/e/1FAIpQLScWbD6ApjwoqGoubmz9i4qrvZNCnt2nNhasSe8kiQ3Feqko7w/viewform)
- **Age:** 18–27 as on 01/01/2027 · OBC +3 · SC/ST +5 · PwBD +10/13/15 · no relaxation for EWS
- **Qualification:** Bachelor's degree in any discipline
- **Documents:** 10, from the Class 10 certificate (the only DOB proof) to the OBC-NCL certificate (central format, issued on or after 01/04/2026)

## How the agents use it

1. **Agent 1 · ApplyEase** (ASI:One) downloads `notification.pdf` and has **Gemini** extract the rules — age limits,
   relaxations, qualification, dates, required documents and the application form's fields.
2. It checks the candidate **against those extracted rules** (the sample candidate, born 14/05/1998, is 28 on the
   cut-off date: over the general limit of 27, **eligible through the OBC +3 relaxation**).
3. It asks for the documents the notice lists, reads uploads with **Gemini Vision**, and audits them.
4. After the candidate reviews and confirms, it instructs **Agent 2 · Form Filler** to fill the Google Form.

Raw links for the agents:

```
https://raw.githubusercontent.com/stdioa9xh/documentpdf/main/notification.pdf
https://raw.githubusercontent.com/stdioa9xh/documentpdf/main/notification.json
```
