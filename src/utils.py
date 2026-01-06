import pandas as pd

def calculate_sales(data):
    total_sales = (data['Quantity'] * data['Price']).sum()
    sales_summary = data.groupby('Product').agg({
        'Quantity': 'sum',
        'Price': lambda x: (x * data.loc[x.index, 'Quantity']).sum()
    }).rename(columns={'Price': 'Total Sales ($)'})
    return total_sales, sales_summary
