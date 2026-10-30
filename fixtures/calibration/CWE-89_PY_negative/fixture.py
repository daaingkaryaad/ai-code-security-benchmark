def lookup(connection, name):
    return connection.execute("SELECT id FROM customers WHERE name = ?", (name,)).fetchall()
