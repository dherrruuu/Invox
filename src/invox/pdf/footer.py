"""
Footer Section
"""

from reportlab.platypus import (
    Table,
    TableStyle,
    Paragraph,
)

from reportlab.lib import colors


def build_footer(styles):

    table = Table(

        [

            [

                Paragraph(
                    "<b>Customer Signature</b>",
                    styles["normal"],
                ),

                Paragraph(
                    "<b>For BALAJI WOOD DECOR</b>",
                    styles["normal"],
                ),

            ],

            [

                Paragraph(
                    "",
                    styles["normal"],
                ),

                Paragraph(
                    "Authorized Signature",
                    styles["normal"],
                ),

            ],

        ],

        colWidths=[270,270],

    )

    table.setStyle(

        TableStyle(

            [

                ("GRID",(0,0),(-1,-1),1,colors.black),

                ("VALIGN",(0,0),(-1,-1),"TOP"),

                ("LEFTPADDING",(0,0),(-1,-1),10),

                ("RIGHTPADDING",(0,0),(-1,-1),10),

                ("TOPPADDING",(0,0),(-1,-1),18),

                ("BOTTOMPADDING",(0,0),(-1,-1),18),

                ("ALIGN",(1,0),(1,-1),"CENTER"),

            ]

        )

    )

    return table