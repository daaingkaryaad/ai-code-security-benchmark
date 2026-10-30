def lookup(connection, name):
    sql = "SELECT id FROM customers WHERE name = '" + name + "'"
    return connection.execute(sql).fetchall()
