from __future__ import annotations

from pathlib import Path

from ..config import APP_CONFIG
from ..constants import LUXURY_BACKGROUND, LUXURY_CARD, LUXURY_PRIMARY, LUXURY_SECONDARY
from ..utils.formatting import format_currency, format_date


class PDFService:
    def __init__(self, invoice_dir: Path | None = None, quotation_dir: Path | None = None):
        self.invoice_dir = Path(invoice_dir or APP_CONFIG.bills_dir)
        self.quotation_dir = Path(quotation_dir or APP_CONFIG.quotations_dir)
        self.invoice_dir.mkdir(parents=True, exist_ok=True)
        self.quotation_dir.mkdir(parents=True, exist_ok=True)

    def _fallback_pdf(self, file_path: Path, title: str, document_data: dict, document_label: str) -> str:
        company = document_data.get("company", {})
        customer = document_data.get("customer", {})
        items = document_data.get("items", [])
        lines = [
            company.get("company_name", "INVOX"),
            company.get("address", ""),
            f"{document_label}: {document_data.get('document_code') or document_data.get('invoice_code') or document_data.get('quotation_code')}",
            f"Date: {format_date(document_data.get('date'))}",
            f"Customer: {customer.get('name', '')}",
            f"Address: {customer.get('address', '')}",
            "",
        ]
        for index, item in enumerate(items, start=1):
            lines.append(
                f"{index}. {item.get('description', '')} | {item.get('size') or item.get('unit') or ''} | Qty {float(item.get('quantity', 0)):.2f} | {format_currency(item.get('rate', 0))} | {format_currency(item.get('amount', float(item.get('quantity', 0)) * float(item.get('rate', 0))))}"
            )
        lines.extend([
            "",
            f"Subtotal: {format_currency(document_data.get('subtotal', 0))}",
            f"GST: {format_currency(document_data.get('gst_amount', 0))}",
            f"Discount: {format_currency(document_data.get('discount_amount', 0))}",
            f"Grand Total: {format_currency(document_data.get('grand_total', 0))}",
            f"Bank Details: {company.get('bank_details', '')}",
            f"Terms: {company.get('terms_and_conditions', '')}",
        ])

        def _pdf_text_line(text: str) -> str:
            text = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            return f"BT /F1 10 Tf 50 760 Td ({text}) Tj ET"

        stream_lines = ["BT /F1 16 Tf 50 800 Td (INVOX) Tj ET"]
        y = 770
        for line in lines:
            stream_lines.append(f"BT /F1 10 Tf 50 {y} Td ({line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')}) Tj ET")
            y -= 16
            if y < 50:
                break
        content = "\n".join(stream_lines).encode("latin-1", "replace")

        objects = []
        objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
        objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
        objects.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>")
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        objects.append(b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream")

        pdf = bytearray(b"%PDF-1.4\n")
        offsets = [0]
        for index, obj in enumerate(objects, start=1):
            offsets.append(len(pdf))
            pdf.extend(f"{index} 0 obj\n".encode("ascii"))
            pdf.extend(obj)
            pdf.extend(b"\nendobj\n")
        xref_offset = len(pdf)
        pdf.extend(f"xref\n0 {len(objects)+1}\n".encode("ascii"))
        pdf.extend(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
        pdf.extend(b"trailer\n")
        pdf.extend(f"<< /Size {len(objects)+1} /Root 1 0 R >>\n".encode("ascii"))
        pdf.extend(b"startxref\n")
        pdf.extend(f"{xref_offset}\n".encode("ascii"))
        pdf.extend(b"%%EOF")
        file_path.write_bytes(pdf)
        return str(file_path)

    def _reportlab_pdf(self, file_path: Path, title: str, document_data: dict, document_label: str) -> str:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="INVOXTitle", parent=styles["Title"], textColor=colors.HexColor(LUXURY_PRIMARY), fontSize=20, leading=24))
        styles.add(ParagraphStyle(name="INVOXBody", parent=styles["BodyText"], textColor=colors.white, fontSize=9, leading=12))
        styles.add(ParagraphStyle(name="INVOXSmall", parent=styles["BodyText"], textColor=colors.HexColor("#CCCCCC"), fontSize=8, leading=10))

        doc = SimpleDocTemplate(
            str(file_path),
            pagesize=A4,
            rightMargin=14 * mm,
            leftMargin=14 * mm,
            topMargin=16 * mm,
            bottomMargin=14 * mm,
        )

        company = document_data.get("company", {})
        customer = document_data.get("customer", {})
        items = document_data.get("items", [])

        story = []
        story.append(Paragraph(company.get("company_name", "INVOX"), styles["INVOXTitle"]))
        story.append(Paragraph(company.get("address", ""), styles["INVOXSmall"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"{document_label}: {document_data.get('document_code') or document_data.get('invoice_code') or document_data.get('quotation_code')}", styles["INVOXBody"]))
        story.append(Paragraph(f"Date: {format_date(document_data.get('date'))}", styles["INVOXBody"]))
        story.append(Paragraph(f"Customer: {customer.get('name', '')}", styles["INVOXBody"]))
        story.append(Paragraph(f"Address: {customer.get('address', '')}", styles["INVOXBody"]))
        story.append(Spacer(1, 10))

        table_data = [["SL", "Description", "Size/Unit", "Qty", "Rate", "Amount"]]
        for index, item in enumerate(items, start=1):
            table_data.append([
                str(index),
                item.get("description", ""),
                item.get("size") or item.get("unit") or "",
                f"{float(item.get('quantity', 0)):.2f}",
                format_currency(item.get("rate", 0)),
                format_currency(item.get("amount", float(item.get("quantity", 0)) * float(item.get("rate", 0)))),
            ])

        table = Table(table_data, repeatRows=1, colWidths=[12 * mm, 70 * mm, 28 * mm, 20 * mm, 25 * mm, 25 * mm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(LUXURY_PRIMARY)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor(LUXURY_CARD)),
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#3A3A3A")),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("LEADING", (0, 0), (-1, -1), 10),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#1A1A1A"), colors.HexColor("#202020")]),
        ]))
        story.append(table)
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"Subtotal: {format_currency(document_data.get('subtotal', 0))}", styles["INVOXBody"]))
        story.append(Paragraph(f"GST: {format_currency(document_data.get('gst_amount', 0))}", styles["INVOXBody"]))
        story.append(Paragraph(f"Discount: {format_currency(document_data.get('discount_amount', 0))}", styles["INVOXBody"]))
        story.append(Paragraph(f"Grand Total: {format_currency(document_data.get('grand_total', 0))}", styles["INVOXBody"]))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Bank Details: {company.get('bank_details', '')}", styles["INVOXSmall"]))
        story.append(Paragraph(f"Terms: {company.get('terms_and_conditions', '')}", styles["INVOXSmall"]))

        def _page_background(canvas, doc):
            canvas.saveState()
            canvas.setFillColor(colors.HexColor(LUXURY_BACKGROUND))
            canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1, stroke=0)
            canvas.setFillColor(colors.HexColor(LUXURY_PRIMARY))
            canvas.rect(0, doc.pagesize[1] - 18, doc.pagesize[0], 18, fill=1, stroke=0)
            canvas.restoreState()

        doc.build(story, onFirstPage=_page_background, onLaterPages=_page_background)
        return str(file_path)

    def _build_document(self, file_path: Path, title: str, document_data: dict, document_label: str) -> str:
        try:
            return self._reportlab_pdf(file_path, title, document_data, document_label)
        except Exception:
            return self._fallback_pdf(file_path, title, document_data, document_label)

    def generate_invoice_pdf(self, invoice_data):
        invoice_code = invoice_data.get("invoice_code") or f"INV-{invoice_data.get('invoice_number')}"
        file_path = self.invoice_dir / f"{invoice_code}.pdf"
        payload = dict(invoice_data)
        payload["document_code"] = invoice_code
        return self._build_document(file_path, "Invoice", payload, "Invoice")

    def generate_quotation_pdf(self, quotation_data):
        quotation_code = quotation_data.get("quotation_code") or f"QUO-{quotation_data.get('quotation_number')}"
        file_path = self.quotation_dir / f"{quotation_code}.pdf"
        payload = dict(quotation_data)
        payload["document_code"] = quotation_code
        return self._build_document(file_path, "Quotation", payload, "Quotation")