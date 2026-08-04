from __future__ import annotations

from ..constants import LUXURY_BACKGROUND, LUXURY_BORDER, LUXURY_CARD, LUXURY_MUTED, LUXURY_PRIMARY, LUXURY_SECONDARY


APP_STYLESHEET = f"""
QWidget {{
    background-color: {LUXURY_BACKGROUND};
    color: {LUXURY_SECONDARY};
    font-family: Segoe UI;
    font-size: 10pt;
}}

QMainWindow {{
    background-color: {LUXURY_BACKGROUND};
}}

QFrame#Card, QWidget#Card {{
    background-color: {LUXURY_CARD};
    border: 1px solid {LUXURY_BORDER};
    border-radius: 16px;
}}

QLabel#Muted {{
    color: {LUXURY_MUTED};
}}

QPushButton {{
    background-color: {LUXURY_PRIMARY};
    color: #111111;
    border: none;
    border-radius: 12px;
    padding: 10px 14px;
    font-weight: 600;
}}

QPushButton:hover {{
    background-color: #e0b17a;
}}

QPushButton:pressed {{
    background-color: #c78f53;
}}

QLineEdit, QComboBox, QTextEdit, QSpinBox, QDateEdit {{
    background-color: #191919;
    color: {LUXURY_SECONDARY};
    border: 1px solid {LUXURY_BORDER};
    border-radius: 10px;
    padding: 8px 10px;
}}

QListWidget {{
    background-color: transparent;
    border: none;
}}

QListWidget::item {{
    padding: 14px 16px;
    border-radius: 10px;
    margin-bottom: 4px;
}}

QListWidget::item:selected {{
    background-color: rgba(212, 163, 115, 0.18);
    color: {LUXURY_PRIMARY};
}}

QTableWidget {{
    background-color: {LUXURY_CARD};
    alternate-background-color: #232323;
    gridline-color: {LUXURY_BORDER};
    border: 1px solid {LUXURY_BORDER};
    border-radius: 14px;
}}

QHeaderView::section {{
    background-color: #2b2b2b;
    color: {LUXURY_SECONDARY};
    padding: 8px;
    border: none;
    font-weight: 600;
}}
"""
