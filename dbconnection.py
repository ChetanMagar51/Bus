import pymysql

def get_db_connection():
    myconn = pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="bus_project"
    )
    return myconn