__author__ = 'OphirH'


import socket
import threading
from tcp_by_size import send_with_size, recv_by_size
import protocol

def menu():
    print(f"1. Create Order\n" +
          f"2. Insert Customer\n" +
          f"3. Get Order(s) by name\n" +
          f"9. exit\n\n>")

    data = input("Enter Num> ")

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
