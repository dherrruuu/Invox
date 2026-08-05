from decimal import Decimal


def convert_feet_inches(value: str) -> float:
    """
    Convert feet-inch format into decimal feet.

    Examples:
    9'6"  -> 9.5
    4'6"  -> 4.5
    10'   -> 10
    """

    if not value:
        return 0


    value = value.strip()


    feet = 0
    inches = 0


    try:

        # Feet + Inches
        if "'" in value:

            parts = value.split("'")

            feet = float(parts[0])


            if len(parts) > 1:

                inch_part = (
                    parts[1]
                    .replace('"', '')
                    .strip()
                )

                if inch_part:
                    inches = float(inch_part)


        # Only inches
        elif '"' in value:

            inches = float(
                value.replace('"', '')
            )


        return feet + (inches / 12)


    except Exception:

        raise ValueError(
            f"Invalid size format: {value}"
        )



def calculate_qty(
        unit: str,
        length: float = 0,
        height: float = 0,
        nos: float = 1
):

    """
    Calculate quantity based on unit.
    """


    unit = unit.lower()


    if unit == "sft":

        # Square Feet
        return length * height * nos



    elif unit == "rft":

        # Running Feet
        return length * nos



    elif unit == "rmt":

        # Running Meter
        return (length * 0.3048) * nos



    elif unit == "smt":

        # Square Meter
        sqft = length * height * nos

        return sqft * 0.092903



    elif unit == "nos":

        return nos



    else:

        return nos




def calculate_amount(
        qty: float,
        rate: float
):

    return qty * rate




def calculate_totals(
        items,
        gst_percentage=18
):

    """
    items example:

    [
      {
        "qty":85.5,
        "rate":120
      }
    ]

    """


    subtotal = 0


    for item in items:

        subtotal += (
            item["qty"] *
            item["rate"]
        )


    gst_amount = (
        subtotal *
        gst_percentage /
        100
    )


    grand_total = (
        subtotal +
        gst_amount
    )


    return {

        "subtotal": round(subtotal,2),

        "gst_percentage": gst_percentage,

        "gst_amount": round(gst_amount,2),

        "grand_total": round(grand_total,2)

    }