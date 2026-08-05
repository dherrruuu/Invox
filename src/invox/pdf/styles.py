"""
Shared ReportLab Styles
"""

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


def get_styles():

    base = getSampleStyleSheet()

    styles = {}

    styles["normal"] = ParagraphStyle(
        "normal",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_LEFT,
    )

    styles["bold"] = ParagraphStyle(
        "bold",
        parent=styles["normal"],
        fontName="Helvetica-Bold",
    )

    styles["company"] = ParagraphStyle(
        "company",
        parent=styles["normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        alignment=TA_CENTER,
        leading=22,
    )

    styles["center_normal"] = ParagraphStyle(
        "center_normal",
        parent=styles["normal"],
        alignment=TA_CENTER,
        fontSize=10,
    )

    styles["center_small"] = ParagraphStyle(
        "center_small",
        parent=styles["normal"],
        alignment=TA_CENTER,
        fontSize=9,
    )

    styles["table_header"] = ParagraphStyle(
        "table_header",
        parent=styles["normal"],
        fontName="Helvetica-Bold",
        alignment=TA_CENTER,
        fontSize=8,
    )

    styles["table_cell"] = ParagraphStyle(
        "table_cell",
        parent=styles["normal"],
        fontSize=8,
    )

    styles["table_right"] = ParagraphStyle(
        "table_right",
        parent=styles["table_cell"],
        alignment=TA_RIGHT,
    )

    return styles