"""
Customer / Invoice Details Section
"""

from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.platypus import Paragraph
from reportlab.lib import colors


def build_customer_section(customer, invoice, styles):

    left = [

        Paragraph("<b>FROM / BILL TO</b>", styles["normal"]),

        Paragraph(
            f"<b>Name :</b> {customer.get('name','')}",
            styles["normal"]
        ),

        Paragraph(
            f"<b>Address :</b> {customer.get('address','')}",
            styles["normal"]
        ),

        Paragraph(
            f"<b>Phone :</b> {customer.get('phone','')}",
            styles["normal"]
        ),

    ]

    right = [

        Paragraph(
            f"<b>Date :</b> {invoice.get('date','')}",
            styles["normal"]
        ),

        Paragraph(
            f"<b>Invoice No :</b> {invoice.get('invoice_no','')}",
            styles["normal"]
        ),

        Paragraph(
            f"<b>GSTIN :</b> {invoice.get('gstin','')}",
            styles["normal"]
        ),

        Paragraph(
            f"<b>Place :</b> {invoice.get('place','')}",
            styles["normal"]
        ),

        Paragraph(
            f"<b>Payment :</b> {invoice.get('payment','')}",
            styles["normal"]
        ),

    ]

    table = Table(

        [

            [

                left,

                right

            ]

        ],

        colWidths=[270,270]

    )

    table.setStyle(

        TableStyle(

            [

                ("GRID",(0,0),(-1,-1),1,colors.black),

                ("VALIGN",(0,0),(-1,-1),"TOP"),

                ("LEFTPADDING",(0,0),(-1,-1),8),

                ("RIGHTPADDING",(0,0),(-1,-1),8),

                ("TOPPADDING",(0,0),(-1,-1),8),

                ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ]

        )

    )

    return table