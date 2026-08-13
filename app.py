import streamlit as st
import os
from datetime import datetime
from io import BytesIO
 
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
 
USERS_FILE = "users.txt"
INVOICES_FILE = "invoices.txt"
 
# ---------------------------------------------------------------------------
# 5. DATA STORAGE MODULE
# ---------------------------------------------------------------------------
 
def ensure_files_exist():
    """Create the storage files if they don't already exist."""
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()
    if not os.path.exists(INVOICES_FILE):
        open(INVOICES_FILE, "w").close()
 
 
def load_users():
    """Read users.txt into a dict {username: password}."""
    users = {}
    with open(USERS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            username, password = line.split(",", 1)
            users[username] = password
    return users
 
 
def save_user(username, password):
    """Append a new user to users.txt."""
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{password}\n")
 
 
def save_invoice_record(data: dict):
    """Append an invoice record to invoices.txt (one line, comma separated)."""
    line = (
        f"{data['timestamp']},{data['company']},{data['customer']},"
        f"{data['product']},{data['qty']},{data['price']},"
        f"{data['gst_percent']},{data['total']}\n"
    )
    with open(INVOICES_FILE, "a") as f:
        f.write(line)
 
 
def load_invoices():
    """Read all invoice records for the history view."""
    records = []
    with open(INVOICES_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) == 8:
                records.append(parts)
    return records
 
 
# ---------------------------------------------------------------------------
# 4. PDF GENERATOR MODULE
# ---------------------------------------------------------------------------
 
def generate_invoice_pdf(company, customer, product, qty, price, gst_percent,
                          subtotal, gst_amount, total, invoice_no):
    """Builds a professional invoice PDF in memory and returns the bytes."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                             topMargin=25 * mm, bottomMargin=20 * mm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Heading1"], fontSize=20, spaceAfter=6
    )
    normal = styles["Normal"]
 
    elements = []
    elements.append(Paragraph(company, title_style))
    elements.append(Paragraph("INVOICE", styles["Heading2"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f"Invoice No: {invoice_no}", normal))
    elements.append(Paragraph(f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}", normal))
    elements.append(Paragraph(f"Billed To: {customer}", normal))
    elements.append(Spacer(1, 14))
 
    table_data = [
        ["Product", "Quantity", "Price (Rs.)", "Amount (Rs.)"],
        [product, str(qty), f"{price:.2f}", f"{subtotal:.2f}"],
    ]
    table = Table(table_data, colWidths=[180, 90, 100, 110])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E4053")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 16))
 
    summary_data = [
        ["Subtotal", f"Rs. {subtotal:.2f}"],
        [f"GST ({gst_percent}%)", f"Rs. {gst_amount:.2f}"],
        ["Total Amount", f"Rs. {total:.2f}"],
    ]
    summary_table = Table(summary_data, colWidths=[380, 100])
    summary_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("FONTNAME", (0, 2), (-1, 2), "Helvetica-Bold"),
        ("LINEABOVE", (0, 2), (-1, 2), 1, colors.black),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("Thank you for your business!", normal))
 
    doc.build(elements)
    buffer.seek(0)
    return buffer
 
 
# ---------------------------------------------------------------------------
# 1 & 2. LOGIN / SIGNUP MODULE
# ---------------------------------------------------------------------------
 
def login_signup_screen():
    st.title("🧾 Invoice Generator System")
    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])
 
    with tab_login:
        st.subheader("User Login")
        username = st.text_input("Username / Email", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", use_container_width=True):
            users = load_users()
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
 
    with tab_signup:
        st.subheader("New User Registration")
        new_username = st.text_input("Choose a Username / Email", key="signup_user")
        new_password = st.text_input("Choose a Password", type="password", key="signup_pass")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
        if st.button("Sign Up", use_container_width=True):
            users = load_users()
            if not new_username or not new_password:
                st.error("Username and password cannot be empty.")
            elif new_username in users:
                st.error("Username already exists. Please choose another.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                save_user(new_username, new_password)
                st.success("Signup successful! Please login now.")
 
 
# ---------------------------------------------------------------------------
# 3. INVOICE MODULE (main app after login)
# ---------------------------------------------------------------------------
 
def invoice_screen():
    st.sidebar.write(f"👤 Logged in as **{st.session_state.username}**")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
 
    page = st.sidebar.radio("Navigate", ["Create Invoice", "Invoice History"])
 
    if page == "Create Invoice":
        st.title("🧾 Create New Invoice")
 
        st.subheader("Company Details")
        company = st.text_input("Company Name", value="My Company Pvt. Ltd.")
 
        st.subheader("Customer Details")
        customer = st.text_input("Customer Name")
 
        st.subheader("Product Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            product = st.text_input("Product Name")
        with col2:
            qty = st.number_input("Quantity", min_value=1, value=1, step=1)
        with col3:
            price = st.number_input("Price per Unit (Rs.)", min_value=0.0, value=0.0, step=1.0)
 
        gst_percent = st.selectbox("GST %", [0, 5, 12, 18, 28], index=3)
 
        subtotal = qty * price
        gst_amount = subtotal * gst_percent / 100
        total = subtotal + gst_amount
 
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Subtotal", f"Rs. {subtotal:.2f}")
        c2.metric(f"GST ({gst_percent}%)", f"Rs. {gst_amount:.2f}")
        c3.metric("Total Amount", f"Rs. {total:.2f}")
 
        if st.button("Generate Invoice", type="primary", use_container_width=True):
            if not customer or not product or price <= 0:
                st.error("Please fill in Customer Name, Product, and a valid Price.")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                record = {
                    "timestamp": timestamp,
                    "company": company,
                    "customer": customer,
                    "product": product,
                    "qty": qty,
                    "price": price,
                    "gst_percent": gst_percent,
                    "total": round(total, 2),
                }
                save_invoice_record(record)
 
                invoice_no = "INV-" + datetime.now().strftime("%Y%m%d%H%M%S")
                pdf_buffer = generate_invoice_pdf(
                    company, customer, product, qty, price, gst_percent,
                    subtotal, gst_amount, total, invoice_no
                )
 
                st.success("Invoice generated and saved successfully!")
                st.download_button(
                    label="⬇️ Download Invoice PDF",
                    data=pdf_buffer,
                    file_name=f"{invoice_no}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
 
    else:  # Invoice History
        st.title("📜 Invoice History")
        records = load_invoices()
        if not records:
            st.info("No invoices generated yet.")
        else:
            headers = ["Date/Time", "Company", "Customer", "Product",
                       "Qty", "Price", "GST %", "Total"]
            st.dataframe(
                [dict(zip(headers, r)) for r in reversed(records)],
                use_container_width=True,
            )
 
 
# ---------------------------------------------------------------------------
# MAIN APP ENTRY POINT
# ---------------------------------------------------------------------------
 
def main():
    st.set_page_config(page_title="Invoice Generator", page_icon="🧾", layout="centered")
    ensure_files_exist()
 
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
 
    if st.session_state.logged_in:
        invoice_screen()
    else:
        login_signup_screen()
 
 
if __name__ == "__main__":
    main()