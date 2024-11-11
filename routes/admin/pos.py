from app import app, render_template, request
import requests
from flask import jsonify
from datetime import datetime
from sqlalchemy import create_engine, text
from routes.admin import myproduct
from fpdf import FPDF

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos")
connection = engine.connect()


@app.get('/admin/pos')
def pos():
    return render_template('pos/sale_screen_1.html')

@app.get('/admin/get-by-category')
def getBycategory():
    category_id = request.args.get('category_id')
    filter_product = myproduct.getProductByCategoryId(category_id)
    return filter_product


@app.post('/invoice')
def create_invoice():
    data = request.get_json()
    discount = float(data.get('discount'))
    tax = float(data.get('tax'))
    payment = float(data.get('payment', 0))
    change = float(data.get('change', 0))
    items = data.get('items')

    # Step 1: Calculate total for the invoice
    total = sum(float(item['price']) * int(item['qty']) for item in items)
    mytax = sum(tax * (float(item['price']) * int(item['qty'])) for item in items)
    mydiscount = (discount / 100) * total
    grand_total = total + mytax - mydiscount

    try:
        # Step 2: Insert into the invoice table and get the generated invoice_id
        insert_invoice_query = text("""
            INSERT INTO invoice (date, total, discount, tax, grand_total, pay, `change`)
            VALUES (:date, :total, :discount, :tax, :grand_total, :pay, :change)
        """)
        result = connection.execute(insert_invoice_query, {
            'date': datetime.now(),
            'total': total,
            'discount': discount,
            'tax': tax,
            'grand_total': grand_total,
            'pay': payment,
            'change': change
        })
        invoice_id = result.lastrowid  # Capture the generated invoice_id

        # Step 3: Insert items into invoicedetail, using the invoice_id for each item
        for item in items:
            print(f"Inserting item {item['product_id']} with quantity {item['qty']} for invoice {invoice_id}")  # Debug log
            insert_detail_query = text("""
                INSERT INTO invoicedetail (invoice_id, product_id, quantity, unit_price, total_price)
                VALUES (:invoice_id, :product_id, :quantity, :unit_price, :total_price)
            """)
            connection.execute(insert_detail_query, {
                'invoice_id': invoice_id,  # Use the invoice's ID as the reference
                'product_id': item['product_id'],
                'quantity': int(item['qty']),
                'unit_price': float(item['price']),
                'total_price': float(item['price']) * int(item['qty'])
            })

            # Step 4: Update product quantity in the product table
            print(f"Updating product {item['product_id']} quantity")  # Debug log
            update_product_query = text("""
                UPDATE product SET qty = qty - :quantity WHERE id = :product_id
            """)
            connection.execute(update_product_query, {
                'quantity': int(item['qty']),
                'product_id': item['product_id']
            })

        connection.commit()  # Commit the transaction
        return jsonify({'success': True, 'invoice_id': invoice_id}), 201

    except Exception as e:
        print("Error during transaction:", e)
        connection.rollback()  # Rollback in case of error
        return jsonify({'success': False, 'error': str(e)}), 500


@app.get('/invoice/print/<int:invoice_id>')
def print_invoice(invoice_id):
    try:
        # Query for the invoice details using the invoice's id
        invoice_query = text("SELECT * FROM invoice WHERE id = :invoice_id")
        invoice = connection.execute(invoice_query, {'invoice_id': invoice_id}).fetchone()

        if not invoice:
            return jsonify({'success': False, 'error': 'Invoice not found'}), 404

        # Query for all items in invoicedetail associated with the specified invoice_id
        items_query = text("""
            SELECT p.name, d.quantity, d.unit_price, d.total_price
            FROM invoicedetail d
            JOIN product p ON d.product_id = p.id
            WHERE d.invoice_id = :invoice_id
        """)
        items = connection.execute(items_query, {'invoice_id': invoice_id}).fetchall()

        # Render the template for printing
        return render_template('pos/invoice_print.html', invoice=invoice, items=items)

    except Exception as e:
        print("Error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500
