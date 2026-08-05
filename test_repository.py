import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from invox.repositories.base_repository import BaseRepository


customer_repo = BaseRepository("customers")


customers = customer_repo.get_all()


print("CUSTOMERS")
print("----------------")

for customer in customers:
    print(customer)