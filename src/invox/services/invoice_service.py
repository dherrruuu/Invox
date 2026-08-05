from typing import Dict, Any, List

from invox.repositories.invoice_repository import InvoiceRepository
from invox.utils.calculator import (
    convert_feet_inches,
    calculate_qty,
    calculate_amount,
    calculate_totals,
)


class InvoiceService:

    def __init__(self):
        self.invoice_repository = InvoiceRepository()

    # ------------------------------------
    # Create complete invoice
    # ------------------------------------

    def create_invoice(
        self, 
        invoice_data: Dict[str, Any], 
        items: List[Dict[str, Any]]
    ) -> Any:
        processed_items: List[Dict[str, Any]] = []

        # Process every invoice row
        for index, item in enumerate(items, start=1):
            length_value = convert_feet_inches(item.get("length_input"))
            height_value = convert_feet_inches(item.get("height_input"))
            nos = item.get("nos", 1)
            rate = item.get("rate", 0)

            qty = calculate_qty(
                item.get("unit"),
                length_value,
                height_value,
                nos,
            )

            amount = calculate_amount(qty, rate)

            processed_items.append({
                "sl_no": index,
                "description": item.get("description"),
                "unit": item.get("unit"),
                "length_input": item.get("length_input"),
                "height_input": item.get("height_input"),
                "length_value": length_value,
                "height_value": height_value,
                "nos": nos,
                "qty": qty,
                "rate": rate,
                "amount": amount,
                "remarks": item.get("remarks"),
            })

        # Calculate invoice totals
        gst_percentage = invoice_data.get("gst_percentage", 18)
        totals = calculate_totals(processed_items, gst_percentage)
        invoice_data.update(totals)

        # Advance payment and balance calculation
        advance = invoice_data.get("advance_payment", 0)
        balance = invoice_data.get("grand_total", 0) - advance
        invoice_data["balance_amount"] = round(balance, 2)

        # Save everything
        return self.invoice_repository.create_invoice(
            invoice_data, 
            processed_items
        )