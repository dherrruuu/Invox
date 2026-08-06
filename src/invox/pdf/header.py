"""
Invoice Header
"""

from reportlab.platypus import (
    Table,
    TableStyle,
    Paragraph,
)
from reportlab.lib import colors


def build_header(company, styles):
    """
    Professional Invoice Header
    """

    company_name = company.get(
        "company_name",
        "BALAJI WOOD DECOR",
    )

    company_tagline = company.get(
        "company_tagline",
        "Interior | Furniture | Turnkey Works",
    )

    data = [

        [
            Paragraph(
                "Shri Ganeshay Namah",
                styles["center_small"],
            )
        ],

        [
            Paragraph(
                f"<b>{company_name}</b>",
                styles["company"],
            )
        ],

        [
            Paragraph(
                company_tagline,
                styles["center_normal"],
            )
        ],

    ]

    table = Table(

        data,

        colWidths=[540],

        rowHeights=[
            28,
            48,
            30,
        ],

    )

    table.setStyle(

        TableStyle(

            [

                # Outer Border
                ("BOX", (0, 0), (-1, -1), 1.2, colors.black),

                # Horizontal Lines
                ("LINEBELOW", (0, 0), (-1, 0), 1, colors.black),
                ("LINEBELOW", (0, 1), (-1, 1), 1, colors.black),

                # Alignment
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                # Padding
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),

            ]

        )

    )

    return table