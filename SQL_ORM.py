import sqlite3
import pickle
import table_viewer
    # https://docs.python.org/2/library/sqlite3.html
    # https://www.youtube.com/watch?v=U7nfe4adDw8


__author__ = 'OphirH'

DB_PATH = 'data.db'
orders = 'orders'
customers = 'customers'
menu = 'menu'

def pickle_data(rows, columns):
    
    return pickle.dumps((pickle.dumps(rows), pickle.dumps(columns)))


class Order():
    def __init__(self, items: list[str], id: int, payment_method: str) -> None:
        self.items = items
        self.id = id
        self.total = 0  # To be determined according to DB
        self.payment_method = payment_method
        self.order_id = None  # To be determined according to DB

    def __str__(self) -> str:
        return f"OrderID: {self.order_id}, Items: {self.items}, Customer: {self.id}, Total: {self.total}, Payment Method: {self.payment_method}"
    

class Customer():
    def __init__(self, first_name: str, surname: str, phone_num: str, email: str) -> None:
        self.customer_id = None  # To be determined according to DB
        self.first_name = first_name
        self.surname = surname
        self.phone_num = phone_num
        self.email = email

    def __str__(self) -> str:
        return f"Customer ID: {self.customer_id}, Name: {self.first_name, self.surname}, Phone Number: {self.phone_num}"


class OrdersCustomersORM():
    def __init__(self):
        self.conn = None  # will store the DB connection
        self.cursor = None   # will store the DB connection cursor
        
    def open_DB(self):
        """
        will open DB file and put value in:
        self.conn (need DB file name)
        and self.cursor
        """
        self.conn = sqlite3.connect(DB_PATH)
        self.current = self.conn.cursor()
        
    def close_DB(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    # All read SQL

    def get_all_orders(self):

        self.open_DB()

        sql_query = f"SELECT * FROM {orders}"
        self.current.execute(sql_query)
        res = self.current.fetchall()
        columns = [description[0] for description in self.current.description]
        data = pickle_data(res, columns)

        self.close_DB()
        return data

    def get_order_by_name(self, firstname, surname):

        self.open_DB()

        # find customer(s) id (could be more than one customer with the same name)
        id_query = f"SELECT id FROM {customers} WHERE first_name = '{firstname}' AND surname = '{surname}';"
        self.current.execute(id_query)
        id_lst = [i[0] for i in self.current.fetchall()]

        rows = []

        for id in id_lst:
            
            order_query = f"SELECT * FROM {orders} WHERE customer_id = {id};"
            self.current.execute(order_query)
            res = self.current.fetchall()
            if res != None:
                for row in res:
                    rows.append(row)
        
        columns = [description[0] for description in self.current.description]

        data = pickle_data(rows, columns)

        self.close_DB()
        return data
    
    def get_order_by_id(self, order_id):
        
        self.open_DB()

        print(f"Before: {order_id}")

        if "or" in order_id:
            order_id = order_id[:order_id.index("or")]

        print(f"After: {order_id}")

        sql_query = f"SELECT * FROM {orders} WHERE id = {order_id};"
        self.current.execute(sql_query)
        res = self.current.fetchall()
        columns = [description[0] for description in self.current.description]

        data = pickle.dumps((pickle.dumps(res), pickle.dumps(columns)))
        self.close_DB()
        return data
    
    def get_menu(self):

        self.open_DB()

        sql_query = f"SELECT * FROM {menu}"
        self.current.execute(sql_query)
        res = self.current.fetchall()
        columns = [description[0] for description in self.current.description]
        # data = pickle.dumps((pickle.dumps(res), pickle.dumps(columns)))
        data = pickle_data(res, columns)

        self.close_DB()
        return data
    
    def get_pricey_orders(self):
        """get 5 Orders with heighest total cost."""

        self.open_DB()

        sql_query = f"SELECT * FROM orders ORDER BY total DESC LIMIT 5;"
        self.current.execute(sql_query)
        res = self.current.fetchall()
        columns = [description[0] for description in self.current.description]
        # data = pickle.dumps((pickle.dumps(res), pickle.dumps(columns)))
        data = pickle_data(res, columns)

        self.close_DB()
        return data
    
    def get_id_by_phone(self, phone_num):

        self.open_DB()

        sql_query = f"SELECT phone_num, id FROM customers WHERE phone_num = '{phone_num}'"
        self.current.execute(sql_query)
        res = self.current.fetchall()
        columns = [description[0] for description in self.current.description]
        data = pickle_data(res, columns)

        self.close_DB()
        return data


    def GetUser(self, username):
        self.open_DB()

        usr = None
        # sql= "SELECT ................ "
        res = self.current.execute(sql)

        self.close_DB()
        return usr
    
    def GetAccounts(self):
        pass
    
    def GetUsers(self):
        self.open_DB()
        usrs = []

        self.close_DB()

        return usrs

    def get_user_balance(self, username):
        self.open_DB()

        sql = "SELECT a.Balance FROM Accounts a, Users b WHERE a.Accountid=b.Accountid and b.Username='" + username + "'"
        res = self.current.execute(sql)
        for ans in res:
            balance = ans[0]
        self.close_DB()
        return balance

    # __________________________________________________________________________________________________________________
    # ______end of read start write ____________________________________________________________________________________
    # __________________________________________________________________________________________________________________
    # __________________________________________________________________________________________________________________

    # All write SQL

    def create_order(self, order: Order):
        
        self.open_DB()

        # deterine order ID
        self.current.execute("SELECT max(id) FROM orders;")
        try:
            id = self.current.fetchone()[0] + 1
        except:
            id = 1

        # determine order total price
        try:
            for item in order.items:
                price_query = f"SELECT price FROM {menu} WHERE item = '{item}';"
                self.current.execute(price_query)
                order.total += self.current.fetchone()[0]

            sql_query = f"INSERT INTO {orders} (id, items, customer_id, total, payment_method) VALUES ({id}, '{', '.join(order.items)}', {order.id}, {order.total}, '{order.payment_method}');"
            self.current.execute(sql_query)
            self.commit()
            

        except:
            self.close_DB()
            return False

        self.close_DB()
        return True
    
    def insert_customer(self, customer: Customer):

        self.open_DB()

        self.current.execute("SELECT max(id) FROM customers;")
        try:
            id = self.current.fetchall()[0][0] + 1
        except:
            self.close_DB()
            id = 1
        
        try:
            sql_query = f"INSERT INTO {customers} (id, first_name, surname, phone_num, email) VALUES ({id}, '{customer.first_name}', '{customer.surname}', '{customer.phone_num}', '{customer.email}');"
            self.current.execute(sql_query)
            self.commit()
        except:
            self.close_DB()
            return False
        self.close_DB()
        return True
    

    def add_to_menu(self, items:str):

        self.open_DB()

        for itemPrice in items.split(','):
            item_name, price = itemPrice.split(':')
            sql_query = f"INSERT INTO {menu} (item, price) VALUES ('{item_name}', {price});"
            self.current.execute(sql_query)
            self.commit()

        # res = self.current.fetchall()
        # columns = [description[0] for description in self.current.description]
        # data = pickle.dumps((pickle.dumps(res), pickle.dumps(columns)))
        
        data = self.get_menu()

        self.close_DB()
        return data
    
    def edit_item_price(self, item, new_price):

        self.open_DB()

        sql_query = f"UPDATE menu SET price={new_price} WHERE item = '{item}'"
        self.current.execute(sql_query)
        self.commit()
        data = self.get_menu()

        self.close_DB()
        return data



    def withdraw_by_username(self, amount, username):
        """
        return true for success and false if failed
        """
        pass
        
    def deposit_by_username(self, amount, username):
        pass

    def insert_new_user(self, username, password, firstname, lastname, address, phone, email, acid):
        pass

    # def insert_new_account(self, username, password, firstname, lastname, address, phone, email):
    def insert_new_account(self, user):
        self.open_DB()
        sql = "SELECT MAX(Accountid) FROM Accounts"
        res = self.current.execute(sql)
        for ans in res:
            accountID = ans[0] + 1
        sql="INSERT INTO Accounts (Accountid,Balance,Manager) VALUES("+str(accountID)+",0,'"+user.username+"')"
        res=self.current.execute(sql)
        self.commit()
        self.close_DB()
        print(res)
        return "Ok"


    def update_user(self,user):
        self.open_DB()



        self.close_DB()
        return True
