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


# class User(object):
#     def __init__(self, user_name, user_password, first_Name, last_Name, adress, phone, email, accountID, isAdmin):
#         self.user_name = user_name
#         self.user_password = user_password
#         self.first_Name = first_Name
#         self.last_Name = last_Name
#         self.adress = adress
#         self.email = email
#         self.phone = phone
#         self.account_ID = accountID
#         self.isAdmin = isAdmin

#     def new_pass(self, newPassword):
#         self.user_password = newPassword

#     def change_manager_status(self):
#         self.is_manager = not self.is_manager

#     def __str__(self):
#         return ("user:" + self.user_name + ":" + self.user_password + ":" + self.first_Name + ":" +
#                 self.last_Name + ":" + self.adress + ":" + self.phone + ":" + self.email + ":" +
#                 str(self.account_ID) + ":" + str(self.isAdmin))

# class Account(object):
#     def __init__(self, id, balance, manager):
#         self.id = id
#         self.balance = balance
#         self.manager = manager
#         self.credit_cards = []


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

    def get_order_by_name(self, firstname, surname):

        self.open_DB()

        # find customer(s) id (could be more than one customer with the same name)
        id_query = f"SELECT id FROM {customers} WHERE first_name = '{firstname}' AND surname = '{surname}';"
        self.current.execute(id_query)
        id_lst = [i[0] for i in self.current.fetchall()]

        rows = []

        for id in id_lst:
            
            order_query = f"SELECT * FROM {orders} WHERE id = {id}"
            self.current.execute(order_query)
            row = self.current.fetchone()
            rows.append(row)
        
        columns = [description[0] for description in self.current.description]

        table_viewer.data_to_html(rows, columns, orders)

        self.close_DB()

        # return res


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


    def update_account(self,account):
        pass



    def delete_user(self,username):
        pass

    def delete_account(self,accountID):
        pass


# def main_test():
#     user1= User("Yos","12345","yossi","zahav","kefar saba","123123123","1111",1,'11')

#     db= UserAccountORM()
#     db.delete_user(user1.user_name)
#     users= db.get_users()
#     for u in users :
#         print u

# if __name__ == "__main__":
#     main_test()













# class UserAccountORM():
#     def __init__(self):
#         self.conn = None  # will store the DB connection
#         self.cursor = None   # will store the DB connection cursor
        
#     def open_DB(self):
#         """
#         will open DB file and put value in:
#         self.conn (need DB file name)
#         and self.cursor
#         """
#         self.conn = sqlite3.connect('UserAccount.db')
#         self.current = self.conn.cursor()
        
#     def close_DB(self):
#         self.conn.close()

#     def commit(self):
#         self.conn.commit()

#     # All read SQL
#     def GetUser(self, username):
#         self.open_DB()

#         usr = None
#         # sql= "SELECT ................ "
#         res = self.current.execute(sql)

#         self.close_DB()
#         return usr
    
#     def GetAccounts(self):
#         pass
    
#     def GetUsers(self):
#         self.open_DB()
#         usrs = []

#         self.close_DB()

#         return usrs

#     def get_user_balance(self, username):
#         self.open_DB()

#         sql = "SELECT a.Balance FROM Accounts a, Users b WHERE a.Accountid=b.Accountid and b.Username='" + username + "'"
#         res = self.current.execute(sql)
#         for ans in res:
#             balance = ans[0]
#         self.close_DB()
#         return balance

#     # __________________________________________________________________________________________________________________
#     # ______end of read start write ____________________________________________________________________________________
#     # __________________________________________________________________________________________________________________
#     # __________________________________________________________________________________________________________________

#     # All write SQL
#     def withdraw_by_username(self, amount, username):
#         """
#         return true for success and false if failed
#         """
#         pass
        
#     def deposit_by_username(self, amount, username):
#         pass

#     def insert_new_user(self, username, password, firstname, lastname, address, phone, email, acid):
#         pass

#     # def insert_new_account(self, username, password, firstname, lastname, address, phone, email):
#     def insert_new_account(self, user):
#         self.open_DB()
#         sql = "SELECT MAX(Accountid) FROM Accounts"
#         res = self.current.execute(sql)
#         for ans in res:
#             accountID = ans[0] + 1
#         sql = ("INSERT INTO Users (Username, Password, Fname, Lname, Adress, Phone, Email, Accountid, Isadmin) "
#                "VALUES('" + user.user_name + "','" + user.user_password + "','" + user.first_
