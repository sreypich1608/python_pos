from datetime import date
import requests


def conform_tel_bot(name, email, phone, address):
    bot_token = "7080607954:AAFnN506rxO0GIWV4B8fjkH5yl0jkxFPIts"
    chat_id = "@my_test_first_channel"
    html = (
        "<strong>New Notification</strong>\n"
        "<code>Customer Name: {name}</code>\n"
        "<code>Customer Email: {email}</code>\n"
        "<code>Customer Phone: {phone}</code>\n"
        "<code>Customer Address: {address}</code>\n"
        "<code>📆 {date}</code>\n"

    ).format(
        name=name,
        email=email,
        phone=phone,
        address=address,
        date=date.today(),
    )
    html = requests.utils.quote(html)
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={html}&parse_mode=HTML"
    res = requests.get(url)
