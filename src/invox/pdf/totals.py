"""
Totals Section
"""

from reportlab.platypus import (
    Table,
    TableStyle,
    Paragraph,
)

from reportlab.lib import colors


def build_totals(invoice, styles):

    subtotal = float(invoice.get("subtotal", 0))
    gst = float(invoice.get("gst", 0))
    discount = float(invoice.get("discount", 0))
    roundoff = float(invoice.get("roundoff", 0))
    grand_total = float(invoice.get("grand_total", 0))

    amount_words = invoice.get(
        "amount_in_words",
        ""
    )

    bank = invoice.get(
        "bank_details",
        ""
    )

    terms = invoice.get(
        "terms",
        ""
    )

    left = [

        [
            Paragraph(
                "<b>Amount in Words</b>",
                styles["normal"]
            )
        ],

        [
            Paragraph(
                amount_words,
                styles["normal"]
            )
        ],

        [
            Paragraph(
                "<b>Bank Details</b>",
                styles["normal"]
            )
        ],

        [
            Paragraph(
                bank,
                styles["normal"]
            )
        ],

        [
            Paragraph(
                "<b>Terms & Conditions</b>",
                styles["normal"]
            )
        ],

        [
            Paragraph(
                terms,
                styles["normal"]
            )
        ],

    ]

    left_table = Table(
        left,
        colWidths=[350],
    )

    left_table.setStyle(

        TableStyle(

            [

                ("GRID", (0,0), (-1,-1), 0.6, colors.black),

                ("LEFTPADDING",(0,0),(-1,-1),8),

                ("RIGHTPADDING",(0,0),(-1,-1),8),

                ("TOPPADDING",(0,0),(-1,-1),5),

                ("BOTTOMPADDING",(0,0),(-1,-1),5),

            ]

        )

    )

    right = [

        [

            Paragraph("<b>Sub Total</b>",styles["normal"]),

            Paragraph(f"{subtotal:,.2f}",styles["table_right"])

        ],

        [

            Paragraph("<b>GST</b>",styles["normal"]),

            Paragraph(f"{gst:,.2f}",styles["table_right"])

        ],

        [

            Paragraph("<b>Discount</b>",styles["normal"]),

            Paragraph(f"{discount:,.2f}",styles["table_right"])

        ],

        [

            Paragraph("<b>Round Off</b>",styles["normal"]),

            Paragraph(f"{roundoff:,.2f}",styles["table_right"])

        ],

        [

            Paragraph("<b>GRAND TOTAL</b>",styles["normal"]),

            Paragraph(
                f"{grand_total:,.2f}",
                styles["table_right"]
            )

        ],

    ]

    right_table = Table(

        right,

        colWidths=[90,100]

    )

    right_table.setStyle(

        TableStyle(

            [

                ("GRID",(0,0),(-1,-1),0.7,colors.black),

                ("BOX",(0,0),(-1,-1),1.2,colors.black),

                ("BACKGROUND",(0,4),(-1,4),colors.HexColor("#EEEEEE")),

                ("FONTNAME",(0,4),(-1,4),"Helvetica-Bold"),

                ("LEFTPADDING",(0,0),(-1,-1),8),

                ("RIGHTPADDING",(0,0),(-1,-1),8),

                ("TOPPADDING",(0,0),(-1,-1),6),

                ("BOTTOMPADDING",(0,0),(-1,-1),6),

            ]

        )

    )

    table = Table(

        [

            [

                left_table,

                right_table

            ]

        ],

        colWidths=[350,190]

    )

    table.setStyle(

        TableStyle(

            [

                ("VALIGN",(0,0),(-1,-1),"TOP"),

                ("LEFTPADDING",(0,0),(-1,-1),0),

                ("RIGHTPADDING",(0,0),(-1,-1),0),

            ]

        )

    )

    return table