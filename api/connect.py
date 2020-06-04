import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

try:
    connection = mysql.connector.connect(host='database',
                                         port='3306',
                                         database='dnaVariants',
                                         user='root',
                                         password='helloworld',
                                         auth_plugin='mysql_native_password')
    print(connection)
    mySql_insert_query = """SELECT * FROM referenceNucleotide"""

    cursor = connection.cursor()
    cursor.execute(mySql_insert_query)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into gene_info table")
    cursor.close()

except mysql.connector.Error as error:
    print("Failed to insert record into table {}".format(error))

''' 
mysql:
    build: mysql-server
    environment:
      MYSQL_DATABASE: test
      MYSQL_ROOT_PASSWORD: root
      MYSQL_ROOT_HOST: 0.0.0.0
      MYSQL_USER: testing
      MYSQL_PASSWORD: testing
    ports:
      - "3306:3306"
      
return mysql.connector.connect(user='testing', host='mysql', port='3306', password='testing', database='test')
'''