"""
Invoice Header
"""

from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.platypus import Paragraph
from reportlab.lib import colors


def build_header(company, styles):

    company_name = company.get(
        "company_name",
        "BALAJI WOOD DECOR"
    )

    company_tagline = company.get(
        "company_tagline",
        "Interior | Furniture | Turnkey Works"
    )

    company_address = company.get(
        "company_address",
        ""
    )

    company_phone = company.get(
        "company_phone",
        ""
    )

    company_gstin = company.get(
        "company_gstin",
        ""
    )

    address_line = " | ".join(
        [
            value
            for value in [
                company_address,
                company_phone,
                f"GSTIN : {company_gstin}" if company_gstin else ""
            ]
            if value
        ]
    )

    data = [

        [
            Paragraph(
                "Shri Ganeshay Namah",
                styles["center_small"]
            )
        ],

        [
            Paragraph(
                f"<b>{company_name}</b>",
                styles["company"]
            )
        ],

        [
            Paragraph(
                company_tagline,
                styles["center_normal"]
            )
        ],

        [
            Paragraph(
                address_line,
                styles["center_small"]
            )
        ],

    ]

    table = Table(
        data,
        colWidths=[540],
    )

    table.setStyle(
        TableStyle(
            [

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),

                ("TOPPADDING", (0, 0), (-1, -1), 5),

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ]
        )
    )

    return table