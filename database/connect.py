import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

try:
    connection = mysql.connector.connect(host='127.0.0.1',
                                         port='3308',
                                         database='testapp',
                                         user='root',
                                         password='helloworld',
                                         auth_plugin='mysql_native_password')

    mySql_insert_query = """INSERT INTO reference_nucleotide(Chromosome, Position, ID, Reference)
                                    VALUES (18, 47348, 'rs126', 'C');"""

    mySql_insert_query2 = """INSERT INTO variant(Position, Alternate, RFP, AlternateAlleleFrequency, VariantType, AlleleType)
                                    VALUES (47348, 'CT', 0.9573, 0.00067423, 'mixed', 'ins');"""

    cursor = connection.cursor()
    cursor.execute(mySql_insert_query2)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into gene_info table")
    cursor.close()

except mysql.connector.Error as error:
    print("Failed to insert record into gene_info table {}".format(error))

"""
mycursor = mydb.cursor()

sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = ("David", "California")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record(s) inserted.")
"""