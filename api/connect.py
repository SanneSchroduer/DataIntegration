import mysql.connector

from mysql.connector import Error
from mysql.connector import errorcode


def connect_to_mysql(result):

    records = []
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                             port='3306',
                                             database='dnaVariants',
                                             user='root',
                                             password='helloworld')


        cursor = connection.cursor(buffered=True, dictionary=True)
        for variant in result:
            select_id = """SELECT r.chromosome, r.position, r.reference, v.alternate
                        FROM referenceNucleotide r
                        INNER JOIN variant v
                        ON r.id = v.id
                        WHERE chromosome = %s
                        AND position = %s
                        AND reference = %s
                        AND v.alternateAlleleFrequency < 0.1"""
            condition_select_id = [variant[0], variant[1], variant[2]]
            cursor.execute(select_id, (condition_select_id))
            record = cursor.fetchone()
            connection.commit()

            if record is not None:
                records.append(record)

        cursor.close()
        return records

    except mysql.connector.Error as error:
        print("Error {}".format(error))

