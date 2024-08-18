__author__ = 'OphirH'

import socket
import threading
from tcp_by_size import send_with_size, recv_by_size
import protocol
import pickle
import table_viewer

orders = 'orders'
customers = 'customers'

def handle_response(response):

    code = response[:7]

    if type(code) != str:
        code = code.decode()

    data = response[8:]
    try:
        fields = data.split('~')
    except:
        fields = data.split(b'~')

    if code == protocol.GET_ORDER_RESPONSE or code == protocol.GET_ORDERS_RESPONSE:
        data = pickle.loads(fields[0])
        table_viewer.data_to_html(pickle.loads(data[0]), pickle.loads(data[1]), orders)

    elif code == protocol.GET_MENU_RESPONSE:
        data = pickle.loads(fields[0])
        table_viewer.data_to_html(pickle.loads(data[0]), pickle.loads(data[1]), 'menu')

    elif code == protocol.GET_EXP_ORDERS_RESPONSE:
        data = pickle.loads(fields[0])
        table_viewer.data_to_html(pickle.loads(data[0]), pickle.loads(data[1]), 'Highets total-cost orders')

def menu():
    print(f"1. Create Order\n" +
          f"2. Insert Customer\n" +
          f"3. Get Order(s) by name\n" +
          f"4. Get Order(s) by order ID\n"
          f"5. Get all orders\n"
          f"6. Get menu\n"
          f"7. Get top 5 orders by total price\n"
          f"9. exit\n\n>")

    data = input("Enter Num > ")

    if data == "9":
        return "q"
    
    elif data == "1":
        items = input("Enter items (seperate with comma e.g. banana,apple,pear) > ")
        customer_id = input("Enter customer ID > ")
        payment_method = input("Enter payment method (card, cash...) > ")
        return protocol.create_client_request('create order', items, customer_id, payment_method)
    
    elif data == "2":
        first_name = input("Customer's first name > ")
        surname = input("Customer's surname > ")
        phone = input("Customer's phone number > ")
        email = input("Customer's email address > ")
        return protocol.create_client_request("insert customer", first_name, surname, phone, email)
    
    elif data == "3":
        first_name = input("Enter customer's first name > ")
        surname = input("Enter customer's surname > ")
        return protocol.create_client_request("get order", first_name, surname)
    
    elif data == "4":
        order_id = input("Enter order ID > ")
        return protocol.create_client_request("get order", order_id)
    
    elif data == "5":
        return protocol.create_client_request("get orders")
    
    elif data == "6":
        return protocol.create_client_request("get menu")
    
    elif data == "7":
        return protocol.create_client_request("pricey orders")
    
    else:
        return "RULIVE"

cli_s = socket.socket()
cli_s.connect(("127.0.0.1", 33445))

while True:
    data = menu()

    if data == "q":
        break
    send_with_size(cli_s, data)

    data = recv_by_size(cli_s)
    if data == "":
        print("seems server DC")
        break
    print(f"Got>> {data}")
    handle_response(data)
