"""
Professional Invoice Builder
"""

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

from reportlab.platypus import (
    SimpleDocTemplate,
    Spacer,
)

from .styles import get_styles
from .header import build_header
from .customer import build_customer_section
from .subject import build_subject
from .items_table import build_items_table
from .totals import build_totals
from .footer import build_footer


class InvoiceBuilder:

    def __init__(self):

        self.styles = get_styles()

    def build(
        self,
        file_path,
        company,
        customer,
        invoice,
        items,
    ):

        file_path = Path(file_path)

        doc = SimpleDocTemplate(

            str(file_path),

            pagesize=A4,

            leftMargin=12 * mm,

            rightMargin=12 * mm,

            topMargin=12 * mm,

            bottomMargin=12 * mm,

        )

        story = []

        # --------------------------------------------------
        # HEADER
        # --------------------------------------------------

        story.append(

            build_header(
                company,
                self.styles,
            )

        )

        story.append(

            Spacer(
                1,
                5,
            )

        )

        # --------------------------------------------------
        # CUSTOMER
        # --------------------------------------------------

        story.append(

            build_customer_section(

                customer,

                invoice,

                self.styles,

            )

        )

        story.append(

            Spacer(
                1,
                5,
            )

        )

        # --------------------------------------------------
        # SUBJECT
        # --------------------------------------------------

        story.append(

            build_subject(

                invoice.get(
                    "subject",
                    "",
                ),

                self.styles,

            )

        )

        story.append(

            Spacer(
                1,
                5,
            )

        )

        # --------------------------------------------------
        # ITEMS
        # --------------------------------------------------

        story.append(

            build_items_table(

                items,

                self.styles,

            )

        )

        story.append(

            Spacer(
                1,
                5,
            )

        )

        # --------------------------------------------------
        # TOTALS
        # --------------------------------------------------

        story.append(

            build_totals(

                invoice,

                self.styles,

            )

        )

        story.append(

            Spacer(
                1,
                5,
            )

        )

        # --------------------------------------------------
        # FOOTER
        # --------------------------------------------------

        story.append(

            build_footer(

                self.styles,

            )

        )

        # --------------------------------------------------

        doc.build(story)

        return str(file_path)