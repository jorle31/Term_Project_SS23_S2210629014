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
db.c.execute("INSERT INTO prompts (message, type) VALUES ('Please identify 2 keywords for the company Microsoft.', 'keyword')")
db.c.execute("INSERT INTO prompts (message, type) VALUES ('Please identify potential risks for the company {company} from the content of the news article: {news}.', 'analysis')")
db.c.execute("INSERT INTO prompts (message, type) VALUES ('Please rate the relevancy of news: {news} for the company: {company}.', 'relevancy')")

# Create the table ...

# Commit the changes and close the database connection
db.conn.commit()
db.close()