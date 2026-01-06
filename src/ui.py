import tkinter as tk
from tkinter import filedialog, messagebox
import os
from generate_report import generate_pdf_report

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BASE_DIR, "report")

def select_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")])
    if file_path:
        entry_csv.delete(0, tk.END)
        entry_csv.insert(0, file_path)

def generate_report():
    csv_file = entry_csv.get()
    if not csv_file:
        messagebox.showerror("Error", "Please select a CSV file")
        return

    output_file = os.path.join(REPORT_DIR, "automated_sales_report.pdf")

    try:
        generate_pdf_report(csv_file, output_file)
        messagebox.showinfo(
            "Success",
            f"PDF generated successfully!\n\nLocation:\n{output_file}"
        )
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Automated Report Generator")
root.geometry("520x180")

tk.Label(root, text="Select CSV File").pack(pady=5)
entry_csv = tk.Entry(root, width=60)
entry_csv.pack(pady=5)

tk.Button(root, text="Browse", command=select_file).pack(pady=5)
tk.Button(root, text="Generate PDF Report", command=generate_report).pack(pady=10)

root.mainloop()
