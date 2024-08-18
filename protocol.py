CREATE_ORDER_REQUEST = 'CREORD'
CREATE_ORDER_RESPONSE = 'CREORDR'
INSERT_CUSTOMER_REQUEST = 'INSCUS'
INSERT_CUSTOMER_RESPONSE = 'INSCUSR'
GET_ORDERS_REQUEST = 'GETODS'
GET_ORDERS_RESPONSE = 'GETODSR'
GET_ORDER_REQUEST = 'GETORD'
GET_ORDER_RESPONSE = 'GETORDR'
GET_MENU_REQUEST = 'GETMEN'
GET_MENU_RESPONSE = 'GETMENR'
GET_EXP_ORDERS_REQUEST = 'GETEXP'
GET_EXP_ORDERS_RESPONSE = 'GETEXPR'


def create_client_request(request_type, *argv):

    if request_type == 'create order':
        return f"{CREATE_ORDER_REQUEST}~{'~'.join(argv)}"
    
    if request_type == 'insert customer':
        return f"{INSERT_CUSTOMER_REQUEST}~{'~'.join(argv)}"
    
    if request_type == 'get orders':
        return f"{GET_ORDERS_REQUEST}"

    if request_type == 'get order':
        return f"{GET_ORDER_REQUEST}~{'~'.join(argv)}"
    
    if request_type == 'get menu':
        return f"{GET_MENU_REQUEST}"
    
    if request_type == 'pricey orders':
        return f"{GET_EXP_ORDERS_REQUEST}"


def create_server_response(request_type, *argv):
    
    if request_type == 'create order':
        return f"{CREATE_ORDER_RESPONSE}~{argv[0]}"  # succeed or failed

    if request_type == 'insert customer':
        return f"{INSERT_CUSTOMER_RESPONSE}~{argv[0]}"
    
    if request_type == 'get orders':
        return f"{GET_ORDERS_RESPONSE}".encode() + b'~' + argv[0]

    if request_type == 'get order':
        return f"{GET_ORDER_RESPONSE}".encode() + b'~' + argv[0]
    
    if request_type == 'get menu':
        return f"{GET_MENU_RESPONSE}".encode() + b'~' + argv[0]
    
    if request_type == 'pricey orders':
        return f"{GET_EXP_ORDERS_RESPONSE}".encode() + b'~' + argv[0]