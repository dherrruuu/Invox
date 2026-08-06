"""
Professional Totals Section
"""

from reportlab.platypus import Table, TableStyle, Paragraph
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

    data = [

        [

            Paragraph("<b>Amount in Words</b>", styles["normal"]),

            Paragraph("<b>Sub Total</b>", styles["normal"]),

            Paragraph(f"{subtotal:,.2f}", styles["table_right"]),

        ],

        [

            Paragraph(amount_words, styles["small"]),

            Paragraph("<b>GST (18%)</b>", styles["normal"]),

            Paragraph(f"{gst:,.2f}", styles["table_right"]),

        ],

        [

            Paragraph("<b>Bank Details</b>", styles["normal"]),

            Paragraph("<b>Discount</b>", styles["normal"]),

            Paragraph(f"{discount:,.2f}", styles["table_right"]),

        ],

        [

            Paragraph(bank, styles["small"]),

            Paragraph("<b>Round Off</b>", styles["normal"]),

            Paragraph(f"{roundoff:,.2f}", styles["table_right"]),

        ],

        [

            Paragraph("", styles["normal"]),

            Paragraph("<b>GRAND TOTAL</b>", styles["normal"]),

            Paragraph(f"{grand_total:,.2f}", styles["table_right"]),

        ],

    ]

    table = Table(

        data,

        colWidths=[350, 90, 100],

        rowHeights=[24, 34, 24, 34, 28],

    )

    table.setStyle(

        TableStyle(

            [

                # --------------------------
                # Outer Border
                # --------------------------

                ("BOX", (0, 0), (-1, -1), 1.2, colors.black),

                # --------------------------
                # Vertical Lines
                # --------------------------

                ("LINEAFTER", (0, 0), (0, -1), 0.8, colors.black),

                ("LINEAFTER", (1, 0), (1, -1), 0.6, colors.black),

                # --------------------------
                # Right Section Grid
                # --------------------------

                ("LINEBELOW", (1, 0), (2, 0), 0.6, colors.black),

                ("LINEBELOW", (1, 1), (2, 1), 0.6, colors.black),

                ("LINEBELOW", (1, 2), (2, 2), 0.6, colors.black),

                ("LINEBELOW", (1, 3), (2, 3), 0.6, colors.black),

                # --------------------------
                # Grand Total
                # --------------------------

                ("BACKGROUND", (1, 4), (2, 4), colors.HexColor("#F2F2F2")),

                ("FONTNAME", (1, 4), (2, 4), "Helvetica-Bold"),

                ("FONTSIZE", (1, 4), (2, 4), 10),

                # --------------------------
                # Alignment
                # --------------------------

                ("ALIGN", (2, 0), (2, -1), "RIGHT"),

                ("VALIGN", (0, 0), (-1, -1), "TOP"),

                # --------------------------
                # Padding
                # --------------------------

                ("LEFTPADDING", (0, 0), (-1, -1), 8),

                ("RIGHTPADDING", (0, 0), (-1, -1), 8),

                ("TOPPADDING", (0, 0), (-1, -1), 5),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),

            ]

        )

    )

    return table