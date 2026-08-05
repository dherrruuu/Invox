import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).parent / "src")
)


from invox.utils.calculator import *


length = convert_feet_inches("9'6\"")

height = convert_feet_inches("4'6\"")


print("Length:", length)

print("Height:", height)



qty = calculate_qty(
    "sft",
    length,
    height,
    2
)


print("Qty:", qty)



amount = calculate_amount(
    qty,
    120
)


print("Amount:", amount)



print(
    calculate_totals(
        [
            {
                "qty":qty,
                "rate":120
            }
        ]
    )
)