from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

from invox.db.supabase import get_supabase

db = get_supabase()

customer = {
    "customer_code": "CUST002",
    "name": "Dheeraj Sthar",
    "phone": "9876543210",
    "city": "Bengaluru"
}

result = db.table("customers").insert(customer).execute()

print(result.data)

print("\nCustomers:\n")

customers = db.table("customers").select("*").execute()

for c in customers.data:
    print(c)