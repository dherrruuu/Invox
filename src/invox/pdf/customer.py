"""
Customer / Invoice Details Section
"""

from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors


def build_customer_section(customer, invoice, styles):

    from_section = [

        Paragraph("<b>FROM</b>", styles["normal"]),

        Paragraph("<b>Balaji Wood Decor</b>", styles["normal"]),

        Paragraph("17, Bangalore", styles["small"]),

        Paragraph("GSTIN : XXXXXXXX", styles["small"]),

    ]

    bill_to = [

        Paragraph("<b>BILL TO</b>", styles["normal"]),

        Paragraph(
            f"<b>{customer.get('name','')}</b>",
            styles["normal"]
        ),

        Paragraph(
            customer.get("address",""),
            styles["small"]
        ),

        Paragraph(
            f"Phone : {customer.get('phone','')}",
            styles["small"]
        ),

        Paragraph(
            f"GSTIN : {customer.get('gstin','')}",
            styles["small"]
        ),

    ]

    invoice_details = [

        Paragraph("<b>INVOICE DETAILS</b>", styles["normal"]),

        Paragraph(
            f"<b>Date :</b> {invoice.get('date','')}",
            styles["small"]
        ),

        Paragraph(
            f"<b>Invoice No :</b> {invoice.get('invoice_no','')}",
            styles["small"]
        ),

        Paragraph(
            f"<b>Place :</b> {invoice.get('place','')}",
            styles["small"]
        ),

        Paragraph(
            f"<b>Payment :</b> {invoice.get('payment','')}",
            styles["small"]
        ),

    ]

    table = Table(

        [[

            from_section,

            bill_to,

            invoice_details

        ]],

        colWidths=[170, 170, 200]

    )

    table.setStyle(

        TableStyle(

            [

                ("BOX", (0, 0), (-1, -1), 1.2, colors.black),

                ("LINEAFTER", (0, 0), (0, -1), 0.8, colors.black),

                ("LINEAFTER", (1, 0), (1, -1), 0.8, colors.black),

                ("VALIGN", (0, 0), (-1, -1), "TOP"),

                ("LEFTPADDING", (0, 0), (-1, -1), 8),

                ("RIGHTPADDING", (0, 0), (-1, -1), 8),

                ("TOPPADDING", (0, 0), (-1, -1), 8),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

            ]

        )

    )

    return table