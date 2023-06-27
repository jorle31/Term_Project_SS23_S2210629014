"""
File that contains functionality for creating and populating the database.
"""

from database_connector import DatabaseConnector

# Instantiate the DatabaseConnector class
db = DatabaseConnector('risk.db')

# Open the database connection
db.open()

# Drop the tables if they exists
db.c.execute("DROP TABLE IF EXISTS prompts")

# Create prompts tables
columns = [
    ('message', 'TEXT'),
    ('type', 'VARCHAR(50)'),
    ('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'),
    ('created_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
]
# Create the table prompts
db.create_table('prompts', columns)

# Commit the changes and close the database connection
db.conn.commit()
db.close()