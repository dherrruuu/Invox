import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from invox.db.manager import db

customers = db.select_all("customers")

print(customers)