import sqlite3

# employee db for testing
conn = sqlite3.connect('employee.db')

c = conn.cursor()

c.execute(
    """
    CREATE TABLE employees(
        first text,
        last text,
        pay integer
    )
    """
)

# commit the transaction
conn.commit()

# close connectoin
conn.close()