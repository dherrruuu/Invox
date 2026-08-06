from num2words import num2words


def amount_to_words(amount: float) -> str:
    """
    Convert amount to Indian currency words.
    Example:
    12106.80 ->
    Rupees Twelve Thousand One Hundred Six and Eighty Paise Only
    """

    amount = round(float(amount), 2)

    rupees = int(amount)
    paise = int(round((amount - rupees) * 100))

    words = num2words(
        rupees,
        lang="en_IN",
    ).title()

    if paise > 0:
        paise_words = num2words(
            paise,
            lang="en_IN",
        ).title()

        return (
            f"Rupees {words} "
            f"And {paise_words} Paise Only"
        )

    return f"Rupees {words} Only"