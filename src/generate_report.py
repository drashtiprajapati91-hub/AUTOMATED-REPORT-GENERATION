import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime

def generate_pdf_report(csv_file, output_file):
    # Ensure output folder exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = pd.read_csv(csv_file)

    total_sales = (data['Quantity'] * data['Price']).sum()
    total_quantity = data['Quantity'].sum()
    sales_summary = data.groupby('Product').agg({
        'Quantity': 'sum',
        'Price': lambda x: (x * data.loc[x.index, 'Quantity']).sum()
    }).rename(columns={'Price': 'Total Sales ($)'})

    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, 'Automated Sales Report', ln=True, align='C')
            self.ln(5)
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, f'Page {self.page_no()}', align='C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Summary:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"- Total Sales: ${total_sales}", ln=True)
    pdf.cell(0, 8, f"- Total Quantity Sold: {total_quantity}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(60, 10, "Product", 1)
    pdf.cell(40, 10, "Quantity", 1)
    pdf.cell(50, 10, "Total Sales ($)", 1)
    pdf.ln()
    pdf.set_font("Arial", '', 12)
    for idx, row in sales_summary.iterrows():
        pdf.cell(60, 10, str(idx), 1)
        pdf.cell(40, 10, str(row['Quantity']), 1)
        pdf.cell(50, 10, str(row['Total Sales ($)']), 1)
        pdf.ln()

    pdf.output(output_file)
