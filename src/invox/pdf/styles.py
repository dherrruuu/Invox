"""
Professional PDF Styles
"""

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import black


def get_styles():

    sample = getSampleStyleSheet()

    styles = {}

    # -------------------------
    # Normal
    # -------------------------

    styles["normal"] = ParagraphStyle(
        "normal",
        parent=sample["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_LEFT,
        textColor=black,
    )

    # -------------------------
    # Bold
    # -------------------------

    styles["bold"] = ParagraphStyle(
        "bold",
        parent=sample["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        alignment=TA_LEFT,
    )

    # -------------------------
    # Small
    # -------------------------

    styles["small"] = ParagraphStyle(
        "small",
        parent=sample["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        alignment=TA_LEFT,
    )

    # -------------------------
    # Company Name
    # -------------------------

    styles["company"] = ParagraphStyle(
        "company",
        parent=sample["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=2,
    )

    # -------------------------
    # Center Normal
    # -------------------------

    styles["center_normal"] = ParagraphStyle(
        "center_normal",
        parent=sample["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=12,
        alignment=TA_CENTER,
    )

    # -------------------------
    # Center Small
    # -------------------------

    styles["center_small"] = ParagraphStyle(
        "center_small",
        parent=sample["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
    )

    # -------------------------
    # Right
    # -------------------------

    styles["right"] = ParagraphStyle(
        "right",
        parent=sample["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_RIGHT,
    )

    # -------------------------
    # Table Header
    # -------------------------

    styles["table_header"] = ParagraphStyle(
        "table_header",
        parent=sample["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=8,
        alignment=TA_CENTER,
    )

    # -------------------------
    # Table Cell
    # -------------------------

    styles["table_cell"] = ParagraphStyle(
        "table_cell",
        parent=sample["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=8,
        alignment=TA_LEFT,
    )

    # -------------------------
    # Table Right
    # -------------------------

    styles["table_right"] = ParagraphStyle(
        "table_right",
        parent=sample["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=8,
        alignment=TA_RIGHT,
    )

    return styles