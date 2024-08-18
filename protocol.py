CREATE_ORDER_REQUEST = 'CREORD'
CREATE_ORDER_RESPONSE = 'CREORDR'
INSERT_CUSTOMER_REQUEST = 'INSCUS'
INSERT_CUSTOMER_RESPONSE = 'INSCUSR'
GET_ORDER_REQUEST = 'GETORD'
GET_ORDER_RESPONSE = 'GETORDR'

def create_client_request(request_type, *argv):

    if request_type == 'create order':
        return f"{CREATE_ORDER_REQUEST}~{'~'.join(argv)}"
    
    if request_type == 'insert customer':
        return f"{INSERT_CUSTOMER_REQUEST}~{'~'.join(argv)}"
    
    if request_type == 'get order':
        return f"{GET_ORDER_REQUEST}~{'~'.join(argv)}"


def create_server_response(request_type, *argv):
    
    if request_type == 'create order':
        return f"{CREATE_ORDER_RESPONSE}~{argv[0]}"  # succeed or failed

    if request_type == 'insert customer':
        return f"{INSERT_CUSTOMER_RESPONSE}~{argv[0]}"
    
    if request_type == 'get order':
        return f"{GET_ORDER_RESPONSE.encode()}~{argv[0]}"