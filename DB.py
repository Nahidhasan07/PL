########
import mysql.connector


class DB:
    def __init__(self):
        pass

    def info(self, name, password):
        email = ''
        password = ''
        con = mysql.connector.connect(host="localhost", user="root", password="1234", database="performance")
        # query
        dbquery = "SELECT * FROM user WHERE email=%s and pass=%s;"
        value = ('nahid@gmail.com', 'nahid')
        # create cursor object
        cursor = con.cursor()
        cursor.execute(dbquery, value)

        # display all records
        table = cursor.fetchall()

        # fetch all columns
        for row in table:
            email = row[0]
            password = row[1]
            if email == name and password == password:
                # print(email, " ", password)
                cursor.close()
                con.close()
                return 1
            else:
                # print("no user")
                cursor.close()
                con.close()
                return 0

# # __name__
# if __name__ == "__main__":
#     db = DB()
#     f=db.info("nahid1@gmail.com", "nahid")
#     print(f)
