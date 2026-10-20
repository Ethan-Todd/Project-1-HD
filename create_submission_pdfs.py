"""Create the two Project 1 submission PDFs from the preserved project records."""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
RESEARCH_PDF = ROOT / "Research-Evolution.pdf"
VALIDATION_PDF = ROOT / "Validation-and-AI-Use.pdf"

NAVY = colors.HexColor("#19375F")
BLUE = colors.HexColor("#D9E7F5")
LIGHT = colors.HexColor("#F3F6F9")
RED = colors.HexColor("#9C2F2F")
GREEN = colors.HexColor("#1E6B43")
GRAY = colors.HexColor("#4B5563")


def register_fonts():
    font_dir = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("Arial", str(font_dir / "Arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(font_dir / "Arial Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Italic", str(font_dir / "Arial Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Unicode", str(font_dir / "Arial Unicode.ttf")))


register_fonts()


styles = getSampleStyleSheet()
TITLE = ParagraphStyle(
    "TitleCustom", parent=styles["Title"], fontName="Arial-Bold", fontSize=21,
    leading=24, textColor=NAVY, alignment=TA_LEFT, spaceAfter=10,
)
SUBTITLE = ParagraphStyle(
    "SubtitleCustom", parent=styles["Normal"], fontName="Arial", fontSize=10,
    leading=14, textColor=GRAY, spaceAfter=12,
)
H1 = ParagraphStyle(
    "H1Custom", parent=styles["Heading1"], fontName="Arial-Bold", fontSize=15,
    leading=18, textColor=NAVY, spaceBefore=9, spaceAfter=6,
)
H2 = ParagraphStyle(
    "H2Custom", parent=styles["Heading2"], fontName="Arial-Bold", fontSize=11.5,
    leading=14, textColor=NAVY, spaceBefore=7, spaceAfter=4,
)
BODY = ParagraphStyle(
    "BodyCustom", parent=styles["BodyText"], fontName="Arial", fontSize=9.1,
    leading=12.2, spaceAfter=5,
)
SMALL = ParagraphStyle(
    "SmallCustom", parent=BODY, fontSize=7.7, leading=10, textColor=GRAY,
)
RAW = ParagraphStyle(
    "RawEdition", parent=BODY, fontName="Arial-Unicode", fontSize=7.15,
    leading=9.2, leftIndent=2, rightIndent=2, spaceAfter=1.8,
)
BULLET = ParagraphStyle(
    "BulletCustom", parent=BODY, leftIndent=13, firstLineIndent=-7, bulletIndent=5,
    spaceAfter=3,
)
CALLOUT = ParagraphStyle(
    "Callout", parent=BODY, backColor=colors.HexColor("#FFF4D6"), borderColor=colors.HexColor("#D9A300"),
    borderWidth=0.7, borderPadding=7, spaceBefore=4, spaceAfter=8,
)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
    canvas.line(0.65 * inch, 0.48 * inch, 7.85 * inch, 0.48 * inch)
    canvas.setFont("Arial", 7)
    canvas.setFillColor(GRAY)
    canvas.drawString(0.65 * inch, 0.31 * inch, "FIN 439 - Home Depot Project 1")
    canvas.drawRightString(7.85 * inch, 0.31 * inch, f"Page {doc.page}")
    canvas.restoreState()


def make_doc(path, title):
    doc = BaseDocTemplate(
        str(path), pagesize=letter, title=title, author="Ethan Todd",
        leftMargin=0.65 * inch, rightMargin=0.65 * inch,
        topMargin=0.62 * inch, bottomMargin=0.62 * inch,
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates(PageTemplate(id="all", frames=[frame], onPage=footer))
    return doc


def p(text, style=BODY):
    return Paragraph(text, style)


def bullet(text):
    return Paragraph("- " + text, BULLET)


def table(data, widths, header=True, font_size=7.5):
    cooked = []
    for row_index, row in enumerate(data):
        row_style = SMALL
        if header and row_index == 0:
            row_style = ParagraphStyle("TableHeader", parent=SMALL, fontName="Arial-Bold", textColor=colors.white)
        cooked.append([Paragraph(str(cell), row_style) for cell in row])
    t = Table(cooked, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        commands.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    for r in range(1 if header else 0, len(data)):
        if r % 2 == 0:
            commands.append(("BACKGROUND", (0, r), (-1, r), LIGHT))
    t.setStyle(TableStyle(commands))
    return t


def add_cover(story, title, subtitle, status):
    story.extend([
        Spacer(1, 0.35 * inch),
        p(title, TITLE),
        p(subtitle, SUBTITLE),
        Spacer(1, 0.08 * inch),
        p(status, CALLOUT),
        table([
            ["Target", "The Home Depot, Inc. (NYSE: HD)"],
            ["Decision user", "Buy-side investment committee; no current position"],
            ["Valuation date", "September 1, 2026"],
            ["Currency / share basis", "USD millions; estimated valuation-date diluted shares"],
            ["Current decision", "WATCH / DEFER"],
            ["Model version checked", "Repository commit 0a4c113215fdda3efdf075926de03e919e7e89e4"],
        ], [1.45 * inch, 5.55 * inch], header=False),
        Spacer(1, 0.15 * inch),
        p("Educational AI finance class work; not professional financial advice.", SMALL),
        PageBreak(),
    ])


def build_research():
    story = []
    add_cover(
        story,
        "Research Evolution",
        "Preserved Edition A, separate provenance qualification, final Edition B, and A-to-B evidence",
        "Edition A is reproduced without rewriting. Its content continuity is established, but its status as the official supervised/Brightspace baseline remains unverified because no receipt or contemporaneous Git record was found.",
    )

    story.extend([
        p("Edition A provenance qualification", H1),
        p("This qualification is separate from Edition A and does not alter its wording.", BODY),
        table([
            ["Evidence", "Finding"],
            ["Earliest available file", "/Users/ethantodd/Documents/Codex/2026-09-01/h/outputs/home-depot-project-1-edition-a.md; filesystem birth/modified metadata September 1, 2026, 13:59:31 EDT"],
            ["Preserved copy", "edition_a_unchanged.md; first Git appearance in commit 46e3d779... on October 19, 2026"],
            ["Content identity", "Both are 8,309 bytes and SHA-256 f9027194f5be2e63490d467483c4eac3010b1feb5cacefe6257fbc253fdf3478; cmp/diff show byte identity"],
            ["What this proves", "A matching file existed at the earliest available location and the repository copy has not changed since preservation"],
            ["What this does not prove", "Original supervised authorship, Brightspace submission order, receipt time, or instructor acceptance"],
        ], [1.55 * inch, 5.45 * inch]),
        p("The file itself retains blank receipt, synthetic-bridge, and partner-question fields. No retrospective completion is inserted. Correct status: unchanged since the earliest available copy and Git preservation; official Edition A originality/submission remains unverified.", CALLOUT),
        PageBreak(),
        p("Preserved Edition A - verbatim text", H1),
        p("The lines below reproduce edition_a_unchanged.md without rewriting. Markdown markers and placeholders are intentionally retained.", SMALL),
    ])

    edition_a = (ROOT / "edition_a_unchanged.md").read_text(encoding="utf-8")
    for line in edition_a.splitlines():
        if line == "":
            story.append(Spacer(1, 3.5))
        else:
            story.append(Paragraph(escape(line), RAW))

    story.extend([
        PageBreak(),
        p("Edition B - final research evolution", H1),
        p("Current decision", H2),
        p("<b>Watch/defer Home Depot as of September 1, 2026.</b> The evidence-backed operating DCF range is <b>$220.99-$253.91 per diluted share</b>, below the <b>$319.77</b> close. The base FCFF/WACC DCF is <b>$234.00</b>. Separate peer references are <b>$240.00</b> from GAAP P/E and <b>$217.21</b> from EV/EBITDA. The methods are not mechanically averaged."),
        p("The recommendation is conditional rather than a certain overvaluation claim because WACC, exact dilution, excess cash, operating-lease treatment, and peer/price evidence remain provisional or limited. The $177.82-$330.03 WACC-growth grid is a boundary test, not the operating recommendation range."),
        p("Consequential evidence developed after Edition A", H2),
        bullet("Reconstructed reported FY2025 from the Form 10-K before forecast adjustments and kept proposed normalizations separate."),
        bullet("Built linked five-year income statement, balance sheet, cash flow, and signed FCFF schedules with balance-sheet and cash-tie checks."),
        bullet("Reconciled commercial paper, Note 5 debt, finance leases, operating leases, cash, and diluted shares in the enterprise-to-equity bridge."),
        bullet("Calculated a provisional 8.1984% WACC from dated Treasury/ERP facts and disclosed beta and marginal debt/tax proxies."),
        bullet("Ran causal downside/base/upside operating cases, WACC-growth sensitivity, reverse DCF, P/E, and EV/EBITDA comparisons."),
        bullet("Qualified Tractor Supply rather than treating it as a close peer after checking its SEC product-category evidence."),
        bullet("Accepted Jack Schlueter's October 13, 2026 challenge that a 76.57% terminal-value share is the largest valuation concentration; the locked test supports the concern."),
        p("A-to-B evidence", H2),
        table([
            ["Changed item", "Edition A", "Edition B", "Driver and evidence"],
            ["Intended user", "Individual long-term investor", "Assigned buy-side committee with no position", "Project 1 role instruction"],
            ["Recommendation", "Watch/defer because valuation was incomplete", "No material change: watch/defer because market exceeds operating range and both peer references", "Three operating cases, dated market price, two unaveraged peer methods"],
            ["Data", "FY2025 10-K; market/WACC unknown", "10-K, Aug. 2026 10-Q/release, Sep. 1 Treasury/ERP/price evidence", "Source and consistency audits; unresolved items remain labelled"],
            ["Model", "Planned DCF and bridge", "Linked statements, signed FCFF, WACC DCF and explicit bridge", "Benchmark, reconciliation, articulation, bridge and boundary tests"],
            ["Assumptions", "Forecast and WACC not established", "8.1984% provisional WACC; 2.5% terminal growth; causal cases", "Sourced facts plus disclosed forecast judgments/proxies"],
            ["Risk", "Organic demand, margins, acquisitions, debt", "Risks quantified; terminal concentration, dilution, cash, WACC and lease limits added", "76.57% terminal share; sensitivity; source audit"],
            ["AI output", "No completed checked example", "TSCO peer suggestion qualified", "SEC Q2 product mix; 11_ai_output_check.md"],
            ["Partner challenge", "Placeholder remains", "Jack Schlueter terminal-value challenge accepted", "Student recollection plus model/locked-test reconciliation; no independent transcript"],
        ], [1.1 * inch, 1.55 * inch, 1.8 * inch, 2.55 * inch]),
        p("What changed from Edition A to Edition B, and why?", H2),
        p("The recommendation did not materially change, but its evidentiary basis did. Edition A deferred because valuation evidence was missing. Edition B defers because a tested $220.99-$253.91 operating range and both separate comparable references remain below the $319.77 market price. The model also shows that the conclusion is sensitive to unresolved WACC inputs and a terminal value representing 76.57% of base enterprise value."),
        p("Conditions and evidence that would change the decision", H2),
        p("Initiate only if a refreshed valuation based on sourced results and a resolved WACC shows sufficient upside to the then-current price, with the margin of safety set by the committee. Move toward do-not-initiate if demand and margin evidence meets or exceeds the downside deterioration, acquisition integration weakens, or a material accounting/bridge validation fails. Monitor comparable sales and transactions, big-ticket demand, gross margin, SG&A leverage, acquisition contribution, capex, inventory days, and WACC inputs."),
        p("AI assistance disclosure", H2),
        p("Codex (GPT-5 surface; no finer version exposed) assisted with source organization, model implementation, validation, drafting, consistency checks, and PDF assembly after the Edition A boundary. The student supplied the locked prediction and partner recollection, selected the decision, and remains responsible for every assumption and conclusion. The checked material AI output is the Tractor Supply peer suggestion, which was qualified using independent SEC evidence."),
        p("Outstanding evidence", H2),
        bullet("Official Edition A Brightspace receipt or other contemporaneous submission evidence."),
        bullet("Independent timestamp/transcript for the recalled partner challenge, if required."),
        bullet("Exchange-quality September 1 price capture and frozen capture of the dated ERP statement."),
        bullet("Resolved beta, marginal debt cost/tax, exact dilution, excess cash, and operating-lease rollforward."),
        bullet("Recorded cold run, videos, corrected transcripts, final access checks, and frozen manifest fields."),
    ])
    make_doc(RESEARCH_PDF, "Home Depot Project 1 Research Evolution").build(story)


def build_validation():
    story = []
    add_cover(
        story,
        "Validation and AI Use",
        "Known-answer benchmark, accounting and valuation checks, locked prediction, AI-output check, partner challenge, and reproducibility record",
        "This is the frozen-format validation artifact assembled from current records. Incomplete evidence remains explicitly incomplete; most importantly, the assignment-required recorded fresh-environment run has not been supplied.",
    )

    story.extend([
        p("Decision, version, and evidence boundary", H1),
        table([
            ["Field", "Record"],
            ["Decision", "Watch/defer; do not initiate at the September 1, 2026 close of $319.77"],
            ["Operating DCF range", "$220.99-$253.91 per diluted share; base $234.00"],
            ["Comparable references", "$240.00 P/E; $217.21 EV/EBITDA; not averaged with DCF"],
            ["Valuation boundary", "September 1, 2026; evidence public by that date"],
            ["Model basis", "USD millions; estimated valuation-date diluted shares; FCFF/WACC"],
            ["Code commit checked", "0a4c113215fdda3efdf075926de03e919e7e89e4"],
            ["Official memo", "Project_1_Decision_Memo_HD.pdf; SHA-256 226c54e570b6a3e816b59157043c352cea8422502f0de3ac5c19af50aa1956d7"],
        ], [1.55 * inch, 5.45 * inch]),
        p("Published training-case benchmark", H1),
        p("Source: course-materials/lessons/week-03/starter/dcf_case.csv and dcf_expected_output.csv. Convention: USD millions, year-end FCFF, five explicit years, Gordon terminal value at Year 5."),
        table([
            ["Output", "Actual", "Expected", "Result"],
            ["FCFF Years 1-5", "108.000000; 114.480000; 120.204000; 125.012160; 128.762525", "Same", "PASS"],
            ["PV explicit FCFF", "448.440817", "448.440817", "PASS"],
            ["Terminal value at Year 5", "1,894.648579", "1,894.648579", "PASS"],
            ["PV terminal value", "1,176.427703", "1,176.427703", "PASS"],
            ["Enterprise value", "1,624.868520", "1,624.868520", "PASS"],
            ["Common equity value", "1,374.868520", "1,374.868520", "PASS"],
            ["Value per diluted share", "27.497370", "27.497370", "PASS"],
            ["Terminal-value share", "0.724014", "0.724014", "PASS"],
        ], [2.2 * inch, 2.15 * inch, 1.55 * inch, 1.1 * inch]),
        p("Overall: PASS. Evidence: benchmark_validation.py and 14_training_benchmark_output.txt.", BODY),
        p("Accounting, valuation, and failure checks", H1),
        table([
            ["Claim / failure mode", "Test", "Result", "Evidence"],
            ["Reported FY2025 base", "Individual income-statement and balance-sheet component sums; CFO + CFI + CFF and cash rollforward", "PASS; all gaps 0", "home_depot_fcff_model.py; 02_implementation_results.md"],
            ["Forecast articulation", "Balance-sheet gap and cash-flow-to-cash gap in every year/case", "PASS; all gaps 0", "Model; 05_part3_visible_output.txt"],
            ["Signed FCFF", "Synthetic -$100m first-year FCFF must reduce EV rather than be floored", "PASS", "Core validation output"],
            ["Debt bridge", "$1,000m more debt must reduce equity value $1,000m; finance leases included once", "PASS", "Model; 03_valuation_basis.md"],
            ["DCF direction", "Value falls as WACC rises and rises as terminal growth rises", "PASS", "Part 3 sensitivity"],
            ["Terminal boundary", "Reject terminal growth greater than or equal to WACC and exit unsuccessfully", "PASS", "Core/Part 3 boundary test"],
            ["Case determinism", "Restore/rerun base after scenarios", "PASS", "part3_analysis.py"],
            ["WACC implementation", "Calculated WACC must equal BASE_INPUTS['wacc']", "PASS; 8.1984%", "home_depot_fcff_model.py"],
        ], [2.0 * inch, 2.7 * inch, 0.8 * inch, 1.5 * inch]),
        PageBreak(),
        p("Highest-risk claim and failure test", H1),
        p("The highest-risk valuation claim is the terminal-value dependence: 76.57% of base enterprise value occurs after 2030. The engine refuses g >= WACC rather than producing an invalid Gordon value. The separate locked changed-input test also measures the economic impact of reducing terminal growth. Both tests pass; neither resolves whether 2.5% is the correct economic assumption."),
        p("Locked Changed-Input Record", H1),
        p("Pre-run record - preserved before execution", H2),
        table([
            ["Field", "Record"],
            ["Recorded at", "October 19, 2026, 18:18:31 EDT"],
            ["Precommit", "46e3d779148b70b78a9ea9bde56ff9a9c7674c03; committed 18:18:48 EDT"],
            ["Input", "Terminal growth: 2.5% to 1.5% per year (-1.0 percentage point)"],
            ["Held fixed", "Five-year operating assumptions/FCFF, WACC, excess cash, debt, diluted shares, and discount timing"],
            ["Original student prediction", "I expect value per share to fall a little like around 3%."],
        ], [1.55 * inch, 5.45 * inch]),
        p("Actual result and decision effect", H2),
        table([
            ["Measure", "Base", "Changed", "Change"],
            ["Value per diluted share", "$234.00", "$199.38", "-$34.62 / -14.80%"],
            ["Enterprise value", "$286,819.6m", "$252,209.8m", "-$34,609.8m"],
            ["Terminal-value share", "76.57%", "73.36%", "-3.22 points"],
        ], [2.1 * inch, 1.55 * inch, 1.55 * inch, 1.8 * inch]),
        p("The predicted direction was correct, but the decline was about 11.80 percentage points larger than the approximate 3% prediction. The watch/defer action did not change because both values remain below $319.77. The mismatch increases the priority of terminal-growth and WACC research. The initial failed command used the wrong relative virtual-environment path; the rerun corrected the execution path without changing the model or input."),
        p("Checked AI output", H1),
        table([
            ["Field", "Record"],
            ["Tool/model surface", "Codex, GPT-5; no finer model version exposed"],
            ["Interaction date", "October 19, 2026"],
            ["Material AI output", "Tractor Supply carried forward as a potential Home Depot comparable"],
            ["Independent evidence", "Tractor Supply Q2 FY2026 10-Q, Note 8 product-category table: 31% livestock/equine/agriculture; 23% seasonal/recreation; 23% companion animal; 15% truck/tool/hardware; 8% clothing/gift/decor"],
            ["Source", "https://www.sec.gov/Archives/edgar/data/916365/000091636526000059/tsco-20260627.htm"],
            ["Disposition", "Qualified, not accepted as a close peer"],
            ["Decision effect", "Peer median remains a fragile reference; no mechanical average; watch/defer unchanged"],
        ], [1.55 * inch, 5.45 * inch]),
        p("This example checks peer classification only. It is not a check of the market-price source or the entire comparable valuation. The debt correction is documented as model work elsewhere, but is not relabelled as the recorded AI-output example."),
        PageBreak(),
        p("Credited partner feedback", H1),
        table([
            ["Field", "Record"],
            ["Partner/date", "Jack Schlueter; October 13, 2026"],
            ["Student-reported challenge", "The biggest valuation risk was the 76.57% terminal-value share; recorded as a paraphrase, not a verbatim transcript"],
            ["Student response", "His point is correct that the valuation leans heavily on the terminal value (76.57%). Your own test supports it, because you predicted a drop of about 3% and got 14.80%."],
            ["Independent check", "76.57% terminal share and -14.80% locked-test result match the model/record"],
            ["Disposition/effect", "Accepted; recommendation unchanged; terminal growth and WACC elevated as research priorities"],
        ], [1.55 * inch, 5.45 * inch]),
        p("Provenance qualification: this interaction is documented from the student's recollection. No independent timestamp or transcript was supplied, and Edition A is not edited retroactively."),
        p("Reproducibility and cold-run record", H1),
        table([
            ["Item", "Status"],
            ["Repository", "https://github.com/Ethan-Todd/Project-1-HD"],
            ["Environment", "Standard-library model; requirements.txt declares no project packages"],
            ["Unrecorded clean clone", "A clean clone of published commit 192d040... contained required files; benchmark, core model, and Part 3 all exited 0; later reviewed model scripts retain the same content hashes"],
            ["Benchmark", "Twelve PASS results; Overall PASS"],
            ["Core model", "Historical, balance, cash, signed-FCFF, debt, monotonicity, bridge and lease checks PASS"],
            ["Part 3", "All cases balance; sensitivity, deterministic rerun, debt, boundary and negative-FCFF checks PASS"],
            ["Required recorded run", "INCOMPLETE - no actual recording or recording URL supplied"],
            ["Submission placement", "UNVERIFIED - checklist has no fourth-video row; Video 2 requires reproducibility/high-risk validation but does not explicitly place the full run there"],
        ], [1.65 * inch, 5.35 * inch]),
        p("Exact run sequence", H2),
        p("git clone --branch main --single-branch https://github.com/Ethan-Todd/Project-1-HD.git Project-1-HD<br/>cd Project-1-HD<br/>git rev-parse HEAD<br/>python3 -m venv .venv<br/>./.venv/bin/python -m pip install -r requirements.txt<br/>./.venv/bin/python benchmark_validation.py<br/>./.venv/bin/python home_depot_fcff_model.py<br/>./.venv/bin/python part3_analysis.py<br/>git status --short", SMALL),
        p("AI assistance disclosure", H1),
        p("Codex (GPT-5 surface; no finer version exposed) assisted after the Edition A boundary with source organization, code/model implementation, debugging, validation design and execution, document drafting, repository operations, consistency review, and PDF assembly. The student supplied the human-authored locked prediction and the partner recollection and owns the forecast judgments, peer policy, recommendation, and all submitted claims. AI outputs were not accepted merely because they sounded technical; the recorded TSCO peer suggestion was checked against an SEC filing and qualified."),
        p("Material limitations and missing evidence", H1),
        bullet("Recorded clean end-to-end fresh-environment run and its submission/recording reference."),
        bullet("Videos 1-3, corrected transcripts, durations, timestamp indices, and logged-out access checks."),
        bullet("Verified Edition A Brightspace receipt or contemporaneous submission evidence; matching hashes do not prove originality."),
        bullet("Independent timestamp/transcript for Jack Schlueter's feedback, if required."),
        bullet("Exchange-quality September 1 prices; current amounts are cross-verified using third-party tables."),
        bullet("Frozen capture of the official dated ERP statement and reconciliation of its 4.75% Treasury input with the model's independent 4.79% par-yield convention."),
        bullet("Resolved beta, marginal debt cost/tax, exact award dilution, excess cash, and operating-lease rollforward."),
        bullet("Final repository commit/URL fields, video IDs, and complete logged-out access confirmation."),
        p("Monitoring and reversal", H1),
        p("Monitor comparable sales and transactions, big-ticket/project demand, gross margin, SG&A leverage, acquisition integration/contribution, inventory days, capex, and market-based WACC inputs. Initiate only if a refreshed valuation using sourced results and resolved WACC shows sufficient upside to the then-current price. Move toward do-not-initiate if downside demand/margin pressure is met or exceeded, acquisition integration weakens, or a material accounting/bridge validation fails."),
        p("Primary evidence locations", H1),
        p("04_part3_assumption_challenge_record.md; 05_part3_visible_output.txt; 07_comparable_valuation.md; 08_locked_changed_input_record.md; 11_ai_output_check.md; 13_source_consistency_audit.md; 14_training_benchmark_output.txt; 20_partner_challenge_status.md; 21_edition_a_provenance.md; 22_decision_memo_verification.md; benchmark_validation.py; home_depot_fcff_model.py; part3_analysis.py.", SMALL),
        p("Source and definition notes", H1),
        bullet("Home Depot FY2025 Form 10-K: year ended February 1, 2026; filed March 18, 2026. Q2 FY2026 Form 10-Q: balance sheet August 2, shares August 18, filed August 25, 2026."),
        bullet("Financing debt includes commercial paper, current and noncurrent long-term debt, and finance leases once. Operating leases remain excluded consistently because lease costs remain in operating profit and FCFF."),
        bullet("The 4.79% risk-free rate is the September 1 U.S. Treasury 10-year par yield. The 4.14% ERP is Damodaran's dated implied estimate; beta and marginal debt/tax remain proxies."),
        bullet("September 1 closing prices are cross-verified using third-party historical tables. The lack of an exchange-quality saved archive remains disclosed rather than treated as resolved."),
        p("Cross-artifact consistency", H1),
        p("The official memo, visible output, model scripts, locked record, and these PDFs use the same September 1, 2026 valuation date, $319.77 market price, $220.99-$253.91 operating range, $234.00 base, $240.00 P/E reference, $217.21 EV/EBITDA reference, 8.1984% provisional WACC, 2.5% terminal growth, 76.57% terminal-value share, +6.23-point reverse-DCF shift, and watch/defer recommendation."),
    ])
    make_doc(VALIDATION_PDF, "Home Depot Project 1 Validation and AI Use").build(story)


if __name__ == "__main__":
    build_research()
    build_validation()
    print(RESEARCH_PDF.name)
    print(VALIDATION_PDF.name)
