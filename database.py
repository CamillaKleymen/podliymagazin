import sqlite3

#conection to db
connection = sqlite3.connect('shop.db', check_same_thread=False)
# conn with python
sql = connection.cursor()
#tablecreation
sql.execute('CREATE TABLE IF NOT EXISTS users ('
            'id INTEGER, '
            'name TEXT, '
            'number TEXT, '
            'location TEXT'
            ');')
#creation table of products

sql.execute('CREATE TABLE IF NOT EXISTS products ('
            'pr_id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'pr_name TEXT, '
            'pr_count INTEGER,'
            'pr_description TEXT, '
            'pr_price REAL, '
            'pr_photo TEXT'
            ');')
#creation busket
sql.execute('CREATE TABLE IF NOT EXISTS cart ('
              'id INTEGER, '
              # 'user_id INTEGER,'
              'user_pr_name TEXT,'
              'user_pr_count INTEGER,'
              'total REAL'
              ');')

##method of user
##check of user

def check_user(id):
    check = sql.execute('SELECT * FROM users WHERE id=?;', (id,))
    if check.fetchone():
        return True
    else:
        return False

#registr
def register(id, name, number, location):
    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (id, name, number, location))
    connection.commit()

## method for products
#side of user
# show of products



def get_pr():
    return sql.execute('SELECT pr_id, pr_name, pr_count FROM products;').fetchall()

#info about exact product

def get_exact_pr(pr_id):
    return sql.execute('SELECT pr_name, pr_description, pr_count, pr_price, pr_photo ' 
                       'FROM products WHERE pt_id = ?', (pr_id,)).fetchone()
#method of addition in busket
def add_pr_to_cart(user_id, user_pr, user_pr_count, total):
    sql.execute('INSERT INTO users VALUES(?,?,?,?);', (user_id, user_pr, user_pr_count, total))
    connection.commit()

#side of admin
#add of product


def add_pr(pr_name, pr_description, pr_count, pr_price, pr_photo):
    sql.execute('INSERT INTO products(pr_name, pr_description, pr_count, pr_price, pr_photo) '
                'VALUES(?,?,?,?,?);', (pr_name, pr_description, pr_count, pr_price, pr_photo))
    #fix edition
    connection.commit()


#delete product

def del_pr(pr_id):
    sql.execute('DELETE FROM products WHERE pr_id=?;', (pr_id,))
    connection.commit()

# edit of products count
def change_pr_count(pr_id, new_count):
    current_count=sql.execute('SELECT pr_count FROM products WHERE pr_id=?;', (pr_id,)).fetchone()
    #updated_count = current_count[0] + new_count
    #if new_count > 0:
    sql.execute('UPDATE products SET pr_counts=? WHERE pr_id=?;',
                (current_count[0] + new_count, pr_id))
    # else:
    #     return 'Enter only plusable count'
#fix editions
    connection.commit()
#check products

def pr_check():
    pr_check = sql.execute('SELECT * FROM products;')
    if pr_check.fetchone():
        return True
    else:
        return False

# methods for cart
# cart
def show_cart(user_id):
    cart_check = sql.execute('SELECT*FROM cart WHERE user_id = ?;', (user_id,)).fetchone()
    if cart_check.fetchone():
        return cart_check.fetchone()
    else:
        return False


#busket clear
def clear_cart(user_id):
    sql.execute('DELETE FROM cart WHERE id = ?;', (user_id,))
    connection.commit()

def make_order(user_id):
    pr_name = sql.execute('SELECT user_pr_name FROM cart WHERE id = ?;', (user_id,)).fetchone()
    user_pr_count = sql.execute('SELECT user_pr_count FROM cart WHERE id = ?', (user_id, )).fetchone()
    current_count = sql.execute('SELECT pr_count FROM products WHERE pr_name = ?',
                                (pr_name[0],)).fetchone()
    sql.execute('UPDATE products SET pr_count = ? WHERE pr_name = ?;',
                (current_count[0]-user_pr_count[0], pr_name[0]))

    info = sql.execute ('SELECT * FROM cart WHERE id = ?;',(user_id,)).fetchone()
    address = sql.execute('SELECT location FROM users WHERE id = ?;', (user_id,)).fetchone()

    connection.commit()
    return info, address
