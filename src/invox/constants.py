from pathlib import Path

APP_NAME = "INVOX"
APP_VERSION = "1.0.0"
APP_TAGLINE = "Billing, quotations, and ERP operations for project-based businesses."

DEFAULT_CURRENCY = "INR"
DEFAULT_TAX_RATE = 18.0
DEFAULT_DISCOUNT_RATE = 0.0
MAX_DOCUMENT_ITEMS = 500

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"

INVOICE_PREFIX = "INV"
QUOTATION_PREFIX = "QUO"

LUXURY_BACKGROUND = "#111111"
LUXURY_PRIMARY = "#D4A373"
LUXURY_SECONDARY = "#FFFFFF"
LUXURY_CARD = "#1E1E1E"
LUXURY_BORDER = "#2F2F2F"
LUXURY_MUTED = "#A9A9A9"

WINDOW_WIDTH = 1520
WINDOW_HEIGHT = 940

PROJECT_ROOT = Path(r"D:/INVOX")
DIRECTORIES = {
	"bills": PROJECT_ROOT / "Bills",
	"quotations": PROJECT_ROOT / "Quotations",
	"customers": PROJECT_ROOT / "Customers",
	"database": PROJECT_ROOT / "Database",
	"backup": PROJECT_ROOT / "Backup",
	"reports": PROJECT_ROOT / "Reports",
	"assets": PROJECT_ROOT / "Assets",
}

ERROR_INVALID_INPUT = "Invalid input provided."
ERROR_CUSTOMER_NOT_FOUND = "Customer not found."
ERROR_PRODUCT_NOT_FOUND = "Product not found."
ERROR_INVOICE_NOT_FOUND = "Invoice not found."
ERROR_QUOTATION_NOT_FOUND = "Quotation not found."
ERROR_USER_NOT_FOUND = "User not found."

SUCCESS_CUSTOMER_ADDED = "Customer added successfully."
SUCCESS_PRODUCT_ADDED = "Product added successfully."
SUCCESS_INVOICE_GENERATED = "Invoice generated successfully."
SUCCESS_QUOTATION_GENERATED = "Quotation generated successfully."

PDF_EXPORT_PATH = DIRECTORIES["bills"]