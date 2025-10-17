import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfMerger
from datetime import datetime
import os


print("=== CUSTOMER SEGMENTATION ===")

# Load customer data
customer_data = pd.read_csv("customers.csv")
print("Customer Data Loaded Successfully!\n")
print(customer_data.head())


X = customer_data[["Total Amount Spent", "Total Items Purchased", "Average Purchase Value"]]

# Apply K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
customer_data["Cluster"] = kmeans.fit_predict(X)

print("\nCustomer Clustering Completed. Cluster Centers:")
print(kmeans.cluster_centers_)

# Visualize clusters
plt.figure(figsize=(8, 5))
plt.scatter(customer_data["Total Amount Spent"], customer_data["Total Items Purchased"],
            c=customer_data["Cluster"], cmap='viridis', s=100)
plt.title("Customer Segments Based on Spending and Purchase Frequency")
plt.xlabel("Total Amount Spent")
plt.ylabel("Total Items Purchased")
plt.grid(True)
plt.show()

# Save clustered data
customer_data.to_csv("customer_segments.csv", index=False)
print("\nClustered customer data saved to 'customer_segments.csv'\n")



print("=== INVOICE GENERATION ===")

# Load order data
orders = pd.read_csv("orders.csv")
print("Order Data Loaded Successfully!\n")
print(orders.head())

# Create directory for invoices
if not os.path.exists("invoices"):
    os.makedirs("invoices")

# Generate PDF invoices for each order
for _, order in orders.iterrows():
    order_id = str(order["Order ID"])
    customer_name = order["Customer Name"]
    product_name = order["Product Name"]
    quantity = order["Quantity"]
    unit_price = order["Unit Price"]
    total_amount = quantity * unit_price
    date = datetime.now().strftime("%Y-%m-%d")

    filename = f"invoices/{order_id}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "INVOICE")

    c.setFont("Helvetica", 12)
    c.drawString(50, 700, f"Invoice Number: {order_id}")
    c.drawString(50, 680, f"Date of Purchase: {date}")
    c.drawString(50, 660, f"Customer Name: {customer_name}")
    c.drawString(50, 640, f"Product Name: {product_name}")
    c.drawString(50, 620, f"Quantity: {quantity}")
    c.drawString(50, 600, f"Unit Price: ₹{unit_price}")
    c.drawString(50, 580, f"Total Amount: ₹{total_amount:.2f}")

    c.showPage()
    c.save()
    print(f"Invoice generated for Order ID {order_id}")

# Merge all invoices into one PDF
merger = PdfMerger()
for file in sorted(os.listdir("invoices")):
    if file.endswith(".pdf"):
        merger.append(os.path.join("invoices", file))

merged_filename = "All_Invoices.pdf"
merger.write(merged_filename)
merger.close()

print(f"\nAll invoices merged into '{merged_filename}' successfully!")
