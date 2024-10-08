__author__ = 'OphirH'

import socket
import SQL_ORM
import protocol
import queue, threading, time, random
from tcp_by_size import send_with_size, recv_by_size
DEBUG = True
exit_all = False

def handle_client(sock, tid, db):
    global exit_all
    
    print(f"New Client num {tid}")
    
    while not exit_all:
        try:
            data = recv_by_size(sock)
            if data == "":
                print(f"Error: Seems Client DC")
                break
    
            to_send = do_action(data.decode(), db)

            send_with_size(sock, to_send)

        except socket.error as err:
            if err.errno == 10054:
                # 'Connection reset by peer'
                print(f"Error {err.errno} Client is Gone. {str(sock)} reset by peer.")
                break
            else:
                print(f"{err.errno} General Sock Error Client {str(sock)} disconnected")
                break

        except Exception as err:
            print(f"General Error: {err.message}")
            break
    sock.close()

def do_action(data, db):
    """
    Check what client asks and fill to send with the answer
    """
    to_send = "Not Set Yet"
    action = data[:6]
    data = data[7:]
    fields = data.split('~')

    if DEBUG:
        print(f"Got client request {action} -- {str(fields)}")

    if action == protocol.CREATE_ORDER_REQUEST:
        order = SQL_ORM.Order(fields[0].split(','), fields[1], fields[2])
        if db.create_order(order):
            to_send = protocol.create_server_response("create order", "succeed")
        else:
            to_send = protocol.create_server_response("create order", "failed")

    elif action == protocol.INSERT_CUSTOMER_REQUEST:
        customer = SQL_ORM.Customer(fields[0], fields[1], fields[2], fields[3])
        if db.insert_customer(customer):
            to_send = protocol.create_server_response("insert customer", "succeed")
        else:
            to_send = protocol.create_server_response("insert customer", "failed")

    elif action == protocol.GET_ORDERS_REQUEST:
        data = db.get_all_orders()
        to_send = protocol.create_server_response("get orders", data)

    elif action == protocol.GET_ORDER_REQUEST:
        
        if len(fields) == 2:  # get order by name
            data = db.get_order_by_name(fields[0], fields[1])
            to_send = protocol.create_server_response("get order", data)
        else:  # get order by order ID
            data = db.get_order_by_id(fields[0])
            to_send = protocol.create_server_response("get order", data)

    elif action == protocol.GET_MENU_REQUEST:
        data = db.get_menu()
        to_send = protocol.create_server_response("get menu", data)

    elif action == protocol.INSERT_TO_MENU_REQUEST:
        data = db.add_to_menu(fields[0])
        to_send = protocol.create_server_response("menu add", data)

    elif action == protocol.GET_EXP_ORDERS_REQUEST:
        data = db.get_pricey_orders()
        to_send = protocol.create_server_response("pricey orders", data)

    else:
        print(f"Got unknown action from client {action}")
        to_send = "ERR___R|001|" + "unknown action"

    return to_send

def q_manager(q, tid):
    global exit_all
    
    print(f"manager start: {tid}")
    while not exit_all:
        item = q.get()
        print(f"manager got something: {item}")
        # do some work with it(item)

        q.task_done()
        time.sleep(0.3)
    print("Manager say Bye")

def main():
    global exit_all
    
    exit_all = False
    db = SQL_ORM.OrdersCustomersORM()
    
    s = socket.socket()
    
    q = queue.Queue()

    q.put("Hi for start")
    
    manager = threading.Thread(target=q_manager, args=(q, 0))
    
    s.bind(("0.0.0.0", 33445))

    s.listen(4)
    print("after listen")

    threads = []
    i = 1
    while True:
        cli_s, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(cli_s, i, db))
        t.start()
        i += 1
        threads.append(t)

    exit_all = True
    for t in threads:
        t.join()
    manager.join()
    
    s.close()

main()
