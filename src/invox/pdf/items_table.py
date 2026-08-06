"""
Professional Items Table
"""

from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm


def build_items_table(items, styles):
    """
    Professional invoice items table.
    Fits inside page margins automatically.
    """

    # Printable width
    page_width = A4[0]
    usable_width = page_width - (24 * mm)   # 12mm left + 12mm right margins

    # -------------------------------------------------------
# Fixed column widths (points)
# Total = 540
# -------------------------------------------------------

    col_widths = [

        22,     # SL

        145,    # DESCRIPTION

        40,     # UNIT

        45,     # LENGTH

        45,     # HEIGHT

        32,     # NOS

        40,     # QTY

        55,     # RATE

        65,     # AMOUNT

        51,     # REMARKS

    ]

    # -------------------------------
    # Header
    # -------------------------------

    headers = [

        Paragraph("<b>SL</b>", styles["table_header"]),

        Paragraph("<b>DESCRIPTION</b>", styles["table_header"]),

        Paragraph("<b>UNIT</b>", styles["table_header"]),

        Paragraph("<b>LENGTH</b>", styles["table_header"]),

        Paragraph("<b>HEIGHT</b>", styles["table_header"]),

        Paragraph("<b>NOS</b>", styles["table_header"]),

        Paragraph("<b>QTY</b>", styles["table_header"]),

        Paragraph("<b>RATE</b>", styles["table_header"]),

        Paragraph("<b>AMOUNT</b>", styles["table_header"]),

        Paragraph("<b>REMARKS</b>", styles["table_header"]),

    ]

    data = [headers]

    # -------------------------------
    # Rows
    # -------------------------------

    for index, item in enumerate(items, start=1):

        data.append(

            [

                Paragraph(str(index), styles["table_right"]),

                Paragraph(
                    str(item.get("description", "")),
                    styles["table_cell"],
                ),

                Paragraph(
                    str(item.get("unit", "")),
                    styles["table_cell"],
                ),

                Paragraph(
                    str(item.get("length", "")),
                    styles["table_right"],
                ),

                Paragraph(
                    str(item.get("height", "")),
                    styles["table_right"],
                ),

                Paragraph(
                    str(item.get("nos", "")),
                    styles["table_right"],
                ),

                Paragraph(
                    str(item.get("quantity", "")),
                    styles["table_right"],
                ),

                Paragraph(
                    f'{float(item.get("rate", 0)):,.2f}',
                    styles["table_right"],
                ),

                Paragraph(
                    f'{float(item.get("amount", 0)):,.2f}',
                    styles["table_right"],
                ),

                Paragraph(
                    str(item.get("remarks", "")),
                    styles["table_cell"],
                ),

            ]

        )

    # ---------------------------------
    # Keep table height even if few rows
    # ---------------------------------

    minimum_rows = 18

    while len(data) < minimum_rows:

        data.append(

            [

                Paragraph("", styles["table_cell"]),

                Paragraph("", styles["table_cell"]),

                Paragraph("", styles["table_cell"]),

                Paragraph("", styles["table_cell"]),

                Paragraph("", styles["table_cell"]),

                Paragraph("", styles["table_cell"]),

                Paragraph("", styles["table_cell"]),

                Paragraph("", styles["table_cell"]),

                Paragraph("", styles["table_cell"]),

                Paragraph("", styles["table_cell"]),

            ]

        )

    table = Table(

        data,

        colWidths=col_widths,

        repeatRows=1,

    )

    table.setStyle(

        TableStyle(

            [

                # Header
                ("BACKGROUND", (0, 0), (-1, 0), colors.white),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("ALIGN", (0, 0), (-1, 0), "CENTER"),

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                # Outer border
                ("BOX", (0, 0), (-1, -1), 1.3, colors.black),

                # Grid
                ("GRID", (0, 0), (-1, -1), 0.6, colors.black),

                # Row height
                ("TOPPADDING", (0, 0), (-1, -1), 5),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),

                ("LEFTPADDING", (0, 0), (-1, -1), 4),

                ("RIGHTPADDING", (0, 0), (-1, -1), 4),

                # Description left
                ("ALIGN", (1, 1), (1, -1), "LEFT"),

                # Numeric columns
                ("ALIGN", (3, 1), (8, -1), "RIGHT"),

                # Remarks
                ("ALIGN", (9, 1), (9, -1), "LEFT"),

            ]

        )

    )

    return table