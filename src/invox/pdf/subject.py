"""
Subject Section
"""

from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.platypus import Paragraph
from reportlab.lib import colors


def build_subject(subject, styles):

    if not subject:
        subject = ""

    table = Table(
        [
            [
                Paragraph(
                    f"<b>SUBJECT :</b> {subject}",
                    styles["normal"],
                )
            ]
        ],
        colWidths=[540],
    )

    table.setStyle(
        TableStyle(
            [

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("LEFTPADDING", (0, 0), (-1, -1), 8),

                ("RIGHTPADDING", (0, 0), (-1, -1), 8),

                ("TOPPADDING", (0, 0), (-1, -1), 6),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ]
        )
    )

    return table