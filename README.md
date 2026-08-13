# Invoice Generator System 🧾

**🔗 Live Demo:** [invoice-generator-system.streamlit.app](https://invoice-generator-system.streamlit.app)

A simple, self-contained web app for creating and managing invoices, built with **Streamlit** and **ReportLab**. Users can sign up, log in, generate professional PDF invoices with automatic GST calculation, and view their invoice history — all from a clean browser-based interface.

## Features

- **User Authentication** — sign up and log in with a username/email and password
- **Invoice Creation** — enter company, customer, and product details; quantity, price, and GST % are calculated automatically
- **Automatic Calculations** — live subtotal, GST amount, and total as you fill in the form
- **PDF Generation** — generates a clean, professional invoice PDF (built with ReportLab) that's instantly downloadable
- **Invoice History** — view all previously generated invoices in a sortable table

## Tech Stack

- **Frontend + Backend:** [Streamlit](https://streamlit.io/) (Python) — single-file web app, no separate frontend/backend split needed
- **PDF Generation:** [ReportLab](https://www.reportlab.com/)
- **Data Storage:** Simple flat text files (`users.txt`, `invoices.txt`) — lightweight, no database setup required

## Project Structure

```
Invoice-Generator-System/
├── app.py              # Main application (entry point) — login, signup, invoice creation, history
├── auth.py             # Standalone auth module (not currently used by app.py)
├── invoice.py          # Standalone invoice/billing module (not currently used by app.py)
├── pdf_generator.py    # Standalone PDF module (not currently used by app.py)
├── users.py, utils.py  # Reserved for future use
├── requirements.txt    # Python dependencies
└── invoices/           # Generated invoice PDFs (not tracked in git)
```

> **Note:** `app.py` is fully self-contained — it includes its own authentication, PDF generation, and data handling, and is the only file currently used to run the app. The other modules are early scaffolding kept for future refactoring.

## Running Locally

**1. Clone the repository**
```bash
git clone https://github.com/urvish1919/Invoice-Generator-System.git
cd Invoice-Generator-System
```

**2. Create a virtual environment and install dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

## How It Works

1. **Sign up** with a username/email and password (stored in `users.txt`).
2. **Log in** with those credentials.
3. Fill in company name, customer name, product details, quantity, price, and GST %.
4. Click **Generate Invoice** — the app calculates the subtotal, GST amount, and total, saves a record to `invoices.txt`, and generates a downloadable PDF invoice.
5. View all past invoices under **Invoice History**.

## Security Notes

- User passwords are currently stored as plain text in `users.txt` for simplicity. In a production deployment, passwords should be hashed (e.g. with `bcrypt`) before storage.
- `users.txt` and `invoices.txt` are excluded from version control via `.gitignore`, since they contain user-entered data.

## Roadmap

- [ ] Hash passwords instead of storing them in plain text
- [ ] Migrate from flat text files to a proper database (SQLite/PostgreSQL)
- [ ] Add invoice editing/deletion
- [ ] Support multiple companies per user
- [ ] Add company logo upload to the PDF

## Disclaimer

This project is for educational and portfolio purposes. It uses simple file-based storage and is not intended for production use handling real financial or personal data without further security hardening.
