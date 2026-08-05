import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from invox.repositories.customer_repository import CustomerRepository


customer_repo = CustomerRepository()


print("ALL CUSTOMERS")
print("----------------")

customers = customer_repo.get_all()

for customer in customers:
    print(customer)


print("\nSEARCH TEST")
print("----------------")

result = customer_repo.search("Dheeraj")

print(result)