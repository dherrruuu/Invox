from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.units import mm

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)



def generate_invoice_pdf(invoice, file_path):

    pdf = SimpleDocTemplate(

        file_path,

        pagesize=A4,

        rightMargin=10*mm,
        leftMargin=10*mm,
        topMargin=10*mm,
        bottomMargin=10*mm

    )


    styles = getSampleStyleSheet()


    elements = []



    # -------------------------
    # Styles
    # -------------------------

    company_style = ParagraphStyle(

        "Company",

        parent=styles["Heading1"],

        alignment=TA_CENTER,

        fontSize=18,

        spaceAfter=10

    )


    center_style = ParagraphStyle(

        "Center",

        parent=styles["Normal"],

        alignment=TA_CENTER

    )


    right_style = ParagraphStyle(

        "Right",

        parent=styles["Normal"],

        alignment=TA_RIGHT

    )



    # -------------------------
    # Company Header
    # -------------------------

    company_name = invoice.get(

        "company_name",

        "BALAJI WOOD DECOR"

    )


    elements.append(

        Paragraph(

            company_name,

            company_style

        )

    )


    elements.append(

        Spacer(1,10)

    )



    # -------------------------
    # Details Section
    # -------------------------

    left_details = []


    if invoice.get("customer_name"):

        left_details.append(

            f"Name : {invoice['customer_name']}"

        )


    if invoice.get("customer_address"):

        left_details.append(

            f"Address : {invoice['customer_address']}"

        )


    if invoice.get("invoice_number"):

        left_details.append(

            f"Invoice No : {invoice['invoice_number']}"

        )


    left_text = "<br/>".join(left_details)



    right_text = (

        f"Company : {company_name}"

        "<br/>"

        f"Date : {invoice.get('invoice_date','')}"

    )



    details_table = Table(

        [

            [

                Paragraph(
                    left_text,
                    styles["Normal"]
                ),

                Paragraph(
                    right_text,
                    styles["Normal"]
                )

            ]

        ],

        colWidths=[90*mm,70*mm]

    )



    elements.append(details_table)



    elements.append(

        Spacer(1,15)

    )



    # -------------------------
    # Subject
    # -------------------------

    if invoice.get("subject"):


        elements.append(

            Paragraph(

                f"Sub : {invoice['subject']}",

                styles["Normal"]

            )

        )


        elements.append(

            Spacer(1,15)

        )



    # -------------------------
    # Items Table
    # -------------------------

    table_data = [

        [

            "SL",

            "DESCRIPTION",

            "UNIT",

            "SIZE",

            "NOS",

            "QTY",

            "RATE",

            "AMOUNT",

            "REMARKS"

        ]

    ]



    for item in invoice.get("items", []):


        size = ""


        if item.get("length_input"):


            size = (

                f"{item.get('length_input')}"

                " x "

                f"{item.get('height_input','')}"

            )



        table_data.append(

            [

                item.get("sl_no",""),

                item.get("description",""),

                item.get("unit",""),

                size,

                item.get("nos",""),

                item.get("qty",""),

                item.get("rate",""),

                item.get("amount",""),

                item.get("remarks","")

            ]

        )



    item_table = Table(

        table_data,

        repeatRows=1,

        colWidths=[10*mm,30*mm,12*mm,25*mm,12*mm,15*mm,15*mm,20*mm,25*mm]

    )



    item_table.setStyle(

        TableStyle(

            [

                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    0.5,

                    colors.black

                ),


                (

                    "BACKGROUND",

                    (0,0),

                    (-1,0),

                    colors.lightgrey

                ),


                (

                    "ALIGN",

                    (0,0),

                    (-1,-1),

                    "CENTER"

                )

            ]

        )

    )


    elements.append(item_table)



    elements.append(

        Spacer(1,20)

    )



    # -------------------------
    # Amount Section
    # -------------------------

    totals = []


    totals.append(

        [

            "Sub Total",

            f"₹ {invoice.get('subtotal',0)}"

        ]

    )


    totals.append(

        [

            f"GST {invoice.get('gst_percentage',18)}%",

            f"₹ {invoice.get('gst_amount',0)}"

        ]

    )


    totals.append(

        [

            "Grand Total",

            f"₹ {invoice.get('grand_total',0)}"

        ]

    )



    if invoice.get("advance_payment"):


        totals.append(

            [

                "Advance",

                f"₹ {invoice['advance_payment']}"

            ]

        )



    if invoice.get("balance_amount"):


        totals.append(

            [

                "Balance",

                f"₹ {invoice['balance_amount']}"

            ]

        )



    total_table = Table(

        totals,

        colWidths=[50*mm,40*mm],

        hAlign="RIGHT"

    )


    total_table.setStyle(

        TableStyle(

            [

                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    0.5,

                    colors.black

                )

            ]

        )

    )


    elements.append(total_table)



    elements.append(

        Spacer(1,30)

    )



    # -------------------------
    # Footer
    # -------------------------

    elements.append(

        Paragraph(

            "Thank You",

            center_style

        )

    )


    elements.append(

        Spacer(1,10)

    )


    elements.append(

        Paragraph(

            company_name,

            company_style

        )

    )



    pdf.build(elements)