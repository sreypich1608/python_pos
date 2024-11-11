from datetime import date
import requests
def conform_tel_bot(cust_name, cust_email, cust_phone, cust_address, cust_message,product):
    bot_token = "7080607954:AAFnN506rxO0GIWV4B8fjkH5yl0jkxFPIts"
    chat_id = "@my_test_first_channel"
    html = (
        "<strong>👌Conform Booking👌</strong>\n"
        "<code>Customer Name: {cust_name}</code>\n"
        "<code>Customer Email: {cust_email}</code>\n"
        "<code>Customer Phone: {cust_phone}</code>\n"
        "<code>Customer Address: {cust_address}</code>\n"
        "<code>Booking Date:📆 {date}</code>\n"
        "------------List of Product--------------\n"
        "<code>No.1: {product_name} {qty}x{price}</code>\n"
        "------------------Note🤓------------------\n"
        "<code>Customer Note: {cust_message}</code>\n"
    ).format(
        cust_name=cust_name,
        cust_email=cust_email,
        cust_phone=cust_phone,
        cust_address=cust_address,
        date=date.today(),
        cust_message=cust_message,
        product_name=product['title'],
        qty=1,
        price=product['price']
    )
    html = requests.utils.quote(html)
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={html}&parse_mode=HTML"
    res = requests.get(url)
