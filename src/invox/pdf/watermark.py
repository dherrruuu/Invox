"""
Watermark
"""

from reportlab.lib.colors import Color


def draw_watermark(canvas, doc):

    canvas.saveState()

    canvas.setFont(
        "Helvetica-Bold",
        90
    )

    # Very light grey
    canvas.setFillColor(
        Color(
            0.90,
            0.90,
            0.90,
            alpha=0.18
        )
    )

    canvas.translate(
        300,
        420
    )

    canvas.rotate(
        45
    )

    canvas.drawCentredString(
        0,
        0,
        "BWD"
    )

    canvas.restoreState()