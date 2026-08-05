"""
Professional Items Table
"""

from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors


def build_items_table(items, styles):

    headers = [

        Paragraph("<b>SL</b>", styles["table_header"]),
        Paragraph("<b>DESCRIPTION</b>", styles["table_header"]),
        Paragraph("<b>UNIT</b>", styles["table_header"]),
        Paragraph("<b>LENGTH</b>", styles["table_header"]),
        Paragraph("<b>HEIGHT</b>", styles["table_header"]),
        Paragraph("<b>NO'S</b>", styles["table_header"]),
        Paragraph("<b>QTY</b>", styles["table_header"]),
        Paragraph("<b>RATE</b>", styles["table_header"]),
        Paragraph("<b>AMOUNT</b>", styles["table_header"]),
        Paragraph("<b>RMK</b>", styles["table_header"]),

    ]


    table_data = [headers]


    # -------------------------
    # Item Rows
    # -------------------------

    for i, item in enumerate(items, start=1):

        row = [

            Paragraph(
                str(i),
                styles["table_cell"]
            ),

            Paragraph(
                item.get("description", ""),
                styles["table_cell"]
            ),

            Paragraph(
                item.get("unit", ""),
                styles["table_cell"]
            ),

            Paragraph(
                str(item.get("length", "")),
                styles["table_cell"]
            ),

            Paragraph(
                str(item.get("height", "")),
                styles["table_cell"]
            ),

            Paragraph(
                str(item.get("nos", "")),
                styles["table_cell"]
            ),

            Paragraph(
                str(item.get("quantity", "")),
                styles["table_cell"]
            ),

            Paragraph(
                f"{float(item.get('rate',0)):,.2f}",
                styles["table_right"]
            ),

            Paragraph(
                f"{float(item.get('amount',0)):,.2f}",
                styles["table_right"]
            ),

            Paragraph(
                item.get("remarks", ""),
                styles["table_cell"]
            ),

        ]

        table_data.append(row)



    # -------------------------
    # Empty Rows
    # -------------------------

    minimum_rows = 15


    while len(table_data) < minimum_rows + 1:

        table_data.append(

            [

                Paragraph(
                    "",
                    styles["table_cell"]
                )

                for _ in range(10)

            ]

        )



    # -------------------------
    # Table
    # -------------------------

    table = Table(

        table_data,

        repeatRows=1,

        colWidths=[

            22,     # SL

            115,    # DESCRIPTION

            35,     # UNIT

            42,     # LENGTH

            42,     # HEIGHT

            35,     # NOS

            35,     # QTY

            55,     # RATE

            65,     # AMOUNT

            55,     # RMK

        ],

        hAlign="CENTER"

    )



    # -------------------------
    # Styling
    # -------------------------

    table.setStyle(

        TableStyle(

            [

                # Border

                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    0.5,
                    colors.black
                ),

                (
                    "BOX",
                    (0,0),
                    (-1,-1),
                    1,
                    colors.black
                ),



                # Header

                (
                    "BACKGROUND",
                    (0,0),
                    (-1,0),
                    colors.white
                ),

                (
                    "FONTNAME",
                    (0,0),
                    (-1,0),
                    "Helvetica-Bold"
                ),

                (
                    "ALIGN",
                    (0,0),
                    (-1,0),
                    "CENTER"
                ),



                # Body Alignment

                (
                    "ALIGN",
                    (0,1),
                    (0,-1),
                    "CENTER"
                ),

                (
                    "ALIGN",
                    (2,1),
                    (6,-1),
                    "CENTER"
                ),

                (
                    "ALIGN",
                    (7,1),
                    (8,-1),
                    "RIGHT"
                ),



                # Vertical Center

                (
                    "VALIGN",
                    (0,0),
                    (-1,-1),
                    "MIDDLE"
                ),



                # Fixed row height

                (
                    "MINROWHEIGHT",
                    (0,1),
                    (-1,-1),
                    22
                ),



                # Cell padding

                (
                    "LEFTPADDING",
                    (0,0),
                    (-1,-1),
                    4
                ),

                (
                    "RIGHTPADDING",
                    (0,0),
                    (-1,-1),
                    4
                ),

                (
                    "TOPPADDING",
                    (0,0),
                    (-1,-1),
                    4
                ),

                (
                    "BOTTOMPADDING",
                    (0,0),
                    (-1,-1),
                    4
                ),


            ]

        )

    )


    return table