import sqlite3
import constants

conn = sqlite3.connect(constants.URL_DB) 
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS %s 
          ([Username] TEXT NOT NULL CHECK (length(Username)>0), [Password] VARCHAR(12) NOT NULL CHECK (length(Password)>0) , 
          [Email] VARCHAR(30) NOT NULL CHECK (length(email)>0), [Tema_interes] TEXT NOT NULL CHECK (length(Tema_interes)>0))
          ''' %constants.TBL_NAME)          
conn.commit()