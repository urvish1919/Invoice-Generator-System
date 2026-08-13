import os
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


def generate_pdf(
    company_name,
    customer_name,
    product_name,
    quantity,
    price,
    gst,
    subtotal,
    total,
    invoice_number
):
    # Create invoices folder if it doesn't exist
    if not os.path.exists("invoices"):
        os.makedirs("invoices")

    filename = f"invoices/Invoice_{invoice_number}.pdf"

    c = canvas.Canvas(filename)

    width, height = c._pagesize

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(1 * inch, height - 1 * inch, "INVOICE")

    # Company Details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, height - 1.6 * inch, "Company")

    c.setFont("Helvetica", 12)
    c.drawString(1 * inch, height - 1.9 * inch, company_name)

    # Customer Details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, height - 2.5 * inch, "Customer")

    c.setFont("Helvetica", 12)
    c.drawString(1 * inch, height - 2.8 * inch, customer_name)

    # Product Details
    y = height - 3.6 * inch

    c.setFont("Helvetica-Bold", 13)
    c.drawString(1 * inch, y, "Product Details")

    y -= 0.35 * inch

    c.setFont("Helvetica", 12)

    c.drawString(1 * inch, y, f"Product : {product_name}")
    y -= 0.3 * inch

    c.drawString(1 * inch, y, f"Quantity : {quantity}")
    y -= 0.3 * inch

    c.drawString(1 * inch, y, f"Price : ₹{price:.2f}")
    y -= 0.3 * inch

    c.drawString(1 * inch, y, f"Subtotal : ₹{subtotal:.2f}")
    y -= 0.3 * inch

    c.drawString(1 * inch, y, f"GST ({gst}%) : ₹{subtotal * gst / 100:.2f}")
    y -= 0.3 * inch

    c.setFont("Helvetica-Bold", 13)
    c.drawString(1 * inch, y, f"Grand Total : ₹{total:.2f}")

    # Footer
    c.setFont("Helvetica", 10)
    c.drawString(
        1 * inch,
        0.8 * inch,
        "Thank you for doing business with us!"
    )

    c.save()

    return filename