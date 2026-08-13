import os

INVOICE_FILE = "invoices.txt"


def initialize_invoice_file():
    """Create invoices.txt if it doesn't exist."""
    if not os.path.exists(INVOICE_FILE):
        with open(INVOICE_FILE, "w") as file:
            pass


def calculate_bill(quantity, price, gst):
    """
    Calculates subtotal, GST amount and total.
    """

    subtotal = quantity * price
    gst_amount = subtotal * gst / 100
    total = subtotal + gst_amount

    return subtotal, gst_amount, total


def get_invoice_number():
    """
    Returns the next invoice number.
    """

    initialize_invoice_file()

    with open(INVOICE_FILE, "r") as file:
        invoices = file.readlines()

    return len(invoices) + 1


def save_invoice(
    company_name,
    customer_name,
    product_name,
    quantity,
    price,
    gst,
    subtotal,
    gst_amount,
    total
):
    """
    Save invoice details into invoices.txt
    """

    initialize_invoice_file()

    invoice_number = get_invoice_number()

    with open(INVOICE_FILE, "a") as file:
        file.write(
            f"{invoice_number},"
            f"{company_name},"
            f"{customer_name},"
            f"{product_name},"
            f"{quantity},"
            f"{price},"
            f"{gst},"
            f"{subtotal},"
            f"{gst_amount},"
            f"{total}\n"
        )

    return invoice_number