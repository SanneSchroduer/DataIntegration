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

    mySql_insert_query = """SELECT * FROM referenceNucleotide"""

    cursor = connection.cursor()
    cursor.execute(mySql_insert_query)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into gene_info table")
    cursor.close()

except mysql.connector.Error as error:
    print("Failed to insert record into gene_info table {}".format(error))