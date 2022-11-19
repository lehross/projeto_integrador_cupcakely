from index import get_conn, close_conn

def create_products_table():
    try:
        conn = get_conn()
    except:
        print('Connection Failed!')
        pass
    
    query = '''
                CREATE TABLE Products (
                    Id int NOT NULL AUTO_INCREMENT,
                    Name varchar(50) NOT NULL,
                    Price decimal(4, 2) NOT NULL,
                    PRIMARY KEY (Id)
                )
            '''
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        print('Products Table Created Successfully!')
    
    except:
        print('Failed to create Products table!')

    finally:
        close_conn(conn)


def create_orders_table():
    try:
        conn = get_conn()
    except:
        print('Connection Failed!')
        pass
    
    query = '''
                CREATE TABLE Orders (
                    Id int NOT NULL AUTO_INCREMENT,
                    Name varchar(50) NOT NULL,
                    Email varchar(50) NOT NULL,
                    Phone varchar(12) NOT NULL,
                    Address varchar(100) NOT NULL,
                    Number int NOT NULL,
                    Cpf bigint NOT NULL,
                    Payment tinyint NOT NULL,
                    Delivery tinyint NOT NULL,
                    Total decimal(4, 2) NOT NULL,
                    Items varchar(255) NOT NULL,
                    PRIMARY KEY (Id)
                )
            '''
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        print('Orders Table Created Successfully!')
    
    except:
        print('Failed to create Orders table!')

    finally:
        close_conn(conn)


# create_products_table()
# create_orders_table()
