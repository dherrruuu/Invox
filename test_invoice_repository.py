import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).parent / "src")
)


from invox.repositories.invoice_repository import InvoiceRepository



repo = InvoiceRepository()



invoice = {

    "invoice_number":"INV-001",

    "customer_id":1,

    "customer_name":"Test Customer",

    "customer_phone":"9999999999",

    "customer_address":"Bangalore",

    "subtotal":10260,

    "gst_percentage":18,

    "gst_amount":1846.80,

    "grand_total":12106.80

}



items=[

{

"sl_no":1,

"description":"Kitchen Cabinet",

"unit":"sft",

"length_input":"9'6\"",

"height_input":"4'6\"",

"length_value":9.5,

"height_value":4.5,

"nos":2,

"qty":85.5,

"rate":120,

"amount":10260,

"remarks":"Marine plywood"

}

]



result = repo.create_invoice(
    invoice,
    items
)



print(result)