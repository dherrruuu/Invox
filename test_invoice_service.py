import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).parent / "src")
)


from invox.services.invoice_service import InvoiceService



service = InvoiceService()



invoice = {

    "invoice_number":"INV-0024",

    "company_name":"BALAJI WOOD DECOR",

    "customer_id":1,

    "customer_name":"ABC Apartment",

    "customer_phone":"9876543210",

    "customer_address":"Bangalore",


    "subject":
    "Final Carpentry Bill executed at ABC Apartment",


    "gst_percentage":18,


    "advance_payment":10000,


    "terms_conditions":
    """
    1. Payment as per agreement.
    2. Changes after approval will be charged extra.
    """
}



items=[

{

"description":"Kitchen Cabinet",

"unit":"sft",

"length_input":"9'6\"",

"height_input":"4'6\"",

"nos":2,

"rate":120,

"remarks":"BWP plywood"

},

{

"description":"Drawer",

"unit":"nos",

"nos":5,

"rate":500,

"remarks":"Soft close"

}

]



result = service.create_invoice(

    invoice,

    items

)



print(result)