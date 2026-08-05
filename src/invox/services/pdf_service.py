"""PDF generation — clean white layout for Balaji Wood Decor."""
from __future__ import annotations

from pathlib import Path

from ..config import APP_CONFIG
from ..utils.formatting import format_currency, format_date


class PDFService:
    def __init__(self, invoice_dir: Path | None = None, quotation_dir: Path | None = None):
        self.invoice_dir = Path(invoice_dir or APP_CONFIG.bills_dir)
        self.quotation_dir = Path(quotation_dir or APP_CONFIG.quotations_dir)
        self.invoice_dir.mkdir(parents=True, exist_ok=True)
        self.quotation_dir.mkdir(parents=True, exist_ok=True)

    # ── helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _safe(v) -> str:
        return str(v or "").strip()

    @staticmethod
    def _money(v) -> str:
        try:
            return f"{float(v):,.2f}"
        except Exception:
            return "0.00"

    # ── main builder ─────────────────────────────────────────────────────────

    def _reportlab_pdf(
        self,
        file_path: Path,
        document_data: dict,
        document_label: str,
    ) -> str:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import (
            HRFlowable,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )

        W, H = A4
        BLACK = colors.black
        GREY = colors.HexColor("#555555")
        LIGHT = colors.HexColor("#EEEEEE")
        WHITE = colors.white

        base = getSampleStyleSheet()

        def style(name, **kw):
            s = ParagraphStyle(name, parent=base["Normal"], **kw)
            return s

        co_style   = style("co",   fontSize=18, fontName="Helvetica-Bold", alignment=TA_CENTER, textColor=BLACK, leading=22)
        co_sub     = style("cosub",fontSize=9,  fontName="Helvetica",      alignment=TA_CENTER, textColor=GREY,  leading=11)
        head_l     = style("hl",   fontSize=9,  fontName="Helvetica",      textColor=BLACK,     leading=13)
        head_r     = style("hr",   fontSize=9,  fontName="Helvetica",      textColor=BLACK,     leading=13, alignment=TA_RIGHT)
        bold9      = style("b9",   fontSize=9,  fontName="Helvetica-Bold", textColor=BLACK,     leading=13)
        small      = style("sm",   fontSize=8,  fontName="Helvetica",      textColor=GREY,      leading=11)
        subj_style = style("subj", fontSize=11, fontName="Helvetica-Bold", textColor=BLACK,     leading=14, alignment=TA_CENTER)
        tot_lbl    = style("tl",   fontSize=9,  fontName="Helvetica",      textColor=BLACK,     leading=13, alignment=TA_RIGHT)
        tot_val    = style("tv",   fontSize=9,  fontName="Helvetica-Bold", textColor=BLACK,     leading=13, alignment=TA_RIGHT)
        grand_lbl  = style("gl",   fontSize=10, fontName="Helvetica-Bold", textColor=BLACK,     leading=14, alignment=TA_RIGHT)
        grand_val  = style("gv",   fontSize=10, fontName="Helvetica-Bold", textColor=BLACK,     leading=14, alignment=TA_RIGHT)
        cell_style = style("ce",   fontSize=8,  fontName="Helvetica",      textColor=BLACK,     leading=11)
        hdr_style  = style("ch",   fontSize=8,  fontName="Helvetica-Bold", textColor=WHITE,     leading=11, alignment=TA_CENTER)
        num_style  = style("cn",   fontSize=8,  fontName="Helvetica",      textColor=BLACK,     leading=11, alignment=TA_RIGHT)

        doc = SimpleDocTemplate(
            str(file_path),
            pagesize=A4,
            rightMargin=14 * mm,
            leftMargin=14 * mm,
            topMargin=14 * mm,
            bottomMargin=14 * mm,
        )

        company_name = self._safe(document_data.get("company_name")) or "Balaji Wood Decor"
        company_addr = self._safe(document_data.get("company_address"))
        company_ph   = self._safe(document_data.get("company_phone"))
        company_gst  = self._safe(document_data.get("company_gst"))

        cust_name    = self._safe(document_data.get("customer_name"))
        cust_addr    = self._safe(document_data.get("customer_address"))
        cust_ph      = self._safe(document_data.get("customer_phone"))
        cust_gst     = self._safe(document_data.get("customer_gst"))

        doc_code     = self._safe(
            document_data.get("document_code")
            or document_data.get("invoice_code")
            or document_data.get("quotation_code")
        )
        doc_date     = format_date(document_data.get("date"))
        items        = document_data.get("items", [])
        subtotal     = float(document_data.get("subtotal", 0) or 0)
        gst_amount   = float(document_data.get("gst_amount", 0) or 0)
        discount     = float(document_data.get("discount_amount", 0) or 0)
        grand_total  = float(document_data.get("grand_total", 0) or 0)
        bank_details = self._safe(document_data.get("bank_details"))
        terms        = self._safe(document_data.get("terms_and_conditions"))

        story = []

        # ── Company header ────────────────────────────────────────────────
        story.append(Paragraph(company_name, co_style))
        co_info_parts = [p for p in [company_addr, company_ph and f"Ph: {company_ph}", company_gst and f"GST: {company_gst}"] if p]
        if co_info_parts:
            story.append(Paragraph("  |  ".join(co_info_parts), co_sub))
        story.append(Spacer(1, 3 * mm))
        story.append(HRFlowable(width="100%", thickness=1, color=BLACK))
        story.append(Spacer(1, 3 * mm))

        # ── Customer (left) + Doc details (right) ────────────────────────
        usable_w = W - 28 * mm
        col_w    = usable_w / 2

        # Build left (customer) lines
        cust_lines = [f"<b>To:</b> {cust_name}" if cust_name else "<b>To:</b>"]
        if cust_addr:
            for ln in cust_addr.split("\n"):
                if ln.strip():
                    cust_lines.append(ln.strip())
        if cust_ph:
            cust_lines.append(f"Ph: {cust_ph}")
        if cust_gst:
            cust_lines.append(f"GST: {cust_gst}")

        # Build right (doc info) lines
        doc_lines = [
            f"<b>{document_label} No:</b>  {doc_code}",
            f"<b>Date:</b>  {doc_date}",
        ]

        left_cell  = "\n".join(f'<para>{l}</para>' for l in cust_lines)
        right_cell = "\n".join(f'<para>{l}</para>' for l in doc_lines)

        header_table = Table(
            [[Paragraph(left_cell,  head_l), Paragraph(right_cell, head_r)]],
            colWidths=[col_w, col_w],
        )
        header_table.setStyle(TableStyle([
            ("VALIGN",  (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING",  (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 4 * mm))

        # ── Subject ──────────────────────────────────────────────────────
        story.append(Paragraph(f"Subject: {document_label}", subj_style))
        story.append(Spacer(1, 3 * mm))

        # ── Items table ──────────────────────────────────────────────────
        # Columns: SL | Description | Length | Height | Nos | Qty | Rate | Amount | Remarks
        col_widths = [
            8  * mm,   # SL
            45 * mm,   # Description
            14 * mm,   # Length
            14 * mm,   # Height
            12 * mm,   # Nos
            14 * mm,   # Qty
            18 * mm,   # Rate
            20 * mm,   # Amount
            None,      # Remarks (fill remaining)
        ]
        # Remaining width for Remarks
        fixed = sum(c for c in col_widths if c is not None)
        col_widths[-1] = usable_w - fixed

        def _hdr(t):
            return Paragraph(t, hdr_style)

        def _cell(t):
            return Paragraph(str(t or ""), cell_style)

        def _num(v, decimals=2):
            try:
                f = float(v or 0)
                return Paragraph(f"{f:,.{decimals}f}", num_style)
            except Exception:
                return Paragraph("", num_style)

        table_data = [[
            _hdr("SL"), _hdr("Description"),
            _hdr("L"), _hdr("H"), _hdr("Nos"), _hdr("Qty"),
            _hdr("Rate"), _hdr("Amount"), _hdr("Remarks"),
        ]]

        for idx, item in enumerate(items, 1):
            length = float(item.get("length", 0) or 0)
            height = float(item.get("height", 0) or 0)
            nos    = float(item.get("nos", item.get("width", 0)) or 0)
            qty    = float(item.get("quantity", 0) or 0)
            rate   = float(item.get("rate", 0) or 0)
            amount = float(item.get("amount", 0) or rate * qty)
            table_data.append([
                Paragraph(str(idx), num_style),
                _cell(item.get("description", "")),
                _num(length) if length else Paragraph("", num_style),
                _num(height) if height else Paragraph("", num_style),
                _num(nos, 0) if nos else Paragraph("", num_style),
                _num(qty),
                _num(rate),
                _num(amount),
                _cell(item.get("remarks", "")),
            ])

        items_tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
        items_tbl.setStyle(TableStyle([
            # Header row
            ("BACKGROUND",   (0, 0), (-1, 0), BLACK),
            ("TEXTCOLOR",    (0, 0), (-1, 0), WHITE),
            # Body alternating
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
            ("TEXTCOLOR",    (0, 1), (-1, -1), BLACK),
            # Grid
            ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
            ("FONTSIZE",     (0, 0), (-1, -1), 8),
            ("LEADING",      (0, 0), (-1, -1), 11),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",   (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 3),
            # Right-align numeric columns
            ("ALIGN", (2, 1), (7, -1), "RIGHT"),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ]))
        story.append(items_tbl)
        story.append(Spacer(1, 4 * mm))

        # ── Totals (bottom-right, aligned under Amount column) ───────────
        tot_w = col_widths[7] + col_widths[6]   # Amount + Rate columns width
        spacer_w = usable_w - tot_w * 2

        def _tot_row(label, value, is_grand=False):
            ls = grand_lbl if is_grand else tot_lbl
            vs = grand_val if is_grand else tot_val
            return [
                Paragraph("", cell_style),
                Paragraph(label, ls),
                Paragraph(self._money(value), vs),
            ]

        totals_data = [
            _tot_row("Subtotal",   subtotal),
            _tot_row("GST",        gst_amount),
        ]
        if discount:
            totals_data.append(_tot_row("Discount", discount))
        totals_data.append(_tot_row("Grand Total", grand_total, is_grand=True))

        totals_tbl = Table(
            totals_data,
            colWidths=[usable_w - tot_w * 2, tot_w, tot_w],
        )
        totals_tbl.setStyle(TableStyle([
            ("LINEABOVE",    (1, len(totals_data) - 1), (2, len(totals_data) - 1), 0.8, BLACK),
            ("TOPPADDING",   (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 3),
            ("LEFTPADDING",  (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(totals_tbl)

        # ── Footer ───────────────────────────────────────────────────────
        if bank_details or terms:
            story.append(Spacer(1, 5 * mm))
            story.append(HRFlowable(width="100%", thickness=0.5, color=GREY))
            story.append(Spacer(1, 2 * mm))
            if bank_details:
                story.append(Paragraph(f"<b>Bank Details:</b> {bank_details}", small))
            if terms:
                story.append(Paragraph(f"<b>Terms &amp; Conditions:</b> {terms}", small))

        doc.build(story)
        return str(file_path)

    def _fallback_pdf(self, file_path: Path, document_data: dict, document_label: str) -> str:
        """Minimal PDF without ReportLab."""
        doc_code = (
            document_data.get("document_code")
            or document_data.get("invoice_code")
            or document_data.get("quotation_code")
            or "DOC"
        )
        lines = [
            document_data.get("company_name", "Balaji Wood Decor"),
            f"{document_label}: {doc_code}",
            f"Date: {format_date(document_data.get('date'))}",
            f"Customer: {document_data.get('customer_name', '')}",
            "",
        ]
        for i, item in enumerate(document_data.get("items", []), 1):
            qty = float(item.get("quantity", 0) or 0)
            rate = float(item.get("rate", 0) or 0)
            lines.append(f"{i}. {item.get('description','')}  Qty:{qty:.2f}  Rate:{rate:.2f}  Amt:{qty*rate:.2f}")
        lines += [
            "",
            f"Subtotal: {self._money(document_data.get('subtotal', 0))}",
            f"GST: {self._money(document_data.get('gst_amount', 0))}",
            f"Grand Total: {self._money(document_data.get('grand_total', 0))}",
        ]
        stream_ops = []
        y = 800
        for ln in lines:
            safe = ln.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            stream_ops.append(f"BT /F1 10 Tf 40 {y} Td ({safe}) Tj ET")
            y -= 14
            if y < 40:
                break
        content = "\n".join(stream_ops).encode("latin-1", "replace")
        objects = [
            b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
            b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream",
        ]
        pdf = bytearray(b"%PDF-1.4\n")
        offsets = [0]
        for n, obj in enumerate(objects, 1):
            offsets.append(len(pdf))
            pdf.extend(f"{n} 0 obj\n".encode())
            pdf.extend(obj)
            pdf.extend(b"\nendobj\n")
        xref = len(pdf)
        pdf.extend(f"xref\n0 {len(objects)+1}\n".encode())
        pdf.extend(b"0000000000 65535 f \n")
        for off in offsets[1:]:
            pdf.extend(f"{off:010d} 00000 n \n".encode())
        pdf.extend(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode())
        file_path.write_bytes(bytes(pdf))
        return str(file_path)

    def _build_document(self, file_path: Path, document_data: dict, document_label: str) -> str:
        try:
            return self._reportlab_pdf(file_path, document_data, document_label)
        except Exception:
            return self._fallback_pdf(file_path, document_data, document_label)

    def generate_invoice_pdf(self, invoice_data):
        code = invoice_data.get("invoice_code") or f"INV-{invoice_data.get('invoice_number')}"
        file_path = self.invoice_dir / f"{code}.pdf"
        payload = dict(invoice_data)
        payload["document_code"] = code
        return self._build_document(file_path, payload, "Invoice")

    def generate_quotation_pdf(self, quotation_data):
        code = quotation_data.get("quotation_code") or f"QUO-{quotation_data.get('quotation_number')}"
        file_path = self.quotation_dir / f"{code}.pdf"
        payload = dict(quotation_data)
        payload["document_code"] = code
        return self._build_document(file_path, payload, "Quotation")
