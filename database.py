import mysql.connector
import constants

# Connect to MySQL database
conn = mysql.connector.connect(
    host=constants.DB_HOST,
    user=constants.DB_USER,
    password=constants.DB_PASSWORD,
    database=constants.DB_NAME,
    autocommit=True
)


c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS {} (
        Username TEXT NOT NULL,
        Password VARCHAR(100) NOT NULL,
        Email VARCHAR(30) NOT NULL,
        Tema_interes TEXT NOT NULL,
        CHECK (CHAR_LENGTH(Username) > 0),
        CHECK (CHAR_LENGTH(Password) > 0),
        CHECK (CHAR_LENGTH(Email) > 0),
        CHECK (CHAR_LENGTH(Tema_interes) > 0)
    )
'''.format(constants.TBL_NAME))
conn.commit()

# Close the connection
conn.close()
