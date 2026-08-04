from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QGridLayout, QWidget

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Dashboard Title
        title = QLabel("Dashboard")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Grid layout for dashboard cards
        grid_layout = QGridLayout()

        # Total Sales Card
        total_sales_card = self.create_card("Total Sales", "$0.00")
        grid_layout.addWidget(total_sales_card, 0, 0)

        # Pending Payments Card
        pending_payments_card = self.create_card("Pending Payments", "$0.00")
        grid_layout.addWidget(pending_payments_card, 0, 1)

        # Additional cards can be added here

        layout.addLayout(grid_layout)
        self.setLayout(layout)

    def create_card(self, title, value):
        card = QWidget()
        card_layout = QVBoxLayout()
        card_title = QLabel(title)
        card_value = QLabel(value)

        card_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        card_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        card_layout.addWidget(card_title)
        card_layout.addWidget(card_value)
        card.setLayout(card_layout)

        return card

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec())