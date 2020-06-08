import csv
# from connect import connect_to_mysql
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode


ALLOWED_EXTENSIONS = {'csv', 'json', 'vcf'}

def is_allowed(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_result(filename):

    output_data = []
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                             port='3306',
                                             database='dnaVariants',
                                             user='root',
                                             password='helloworld')



        filepath = 'inbox/' + filename
        with open(filepath, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                try:
                    cursor = connection.cursor(buffered=True, dictionary=True)

                    select_id = """SELECT r.chromosome, r.position, r.reference, v.alternate
                                FROM referenceNucleotide r
                                INNER JOIN variant v
                                ON r.id = v.id
                                WHERE chromosome = %s
                                AND position = %s
                                AND reference = %s
                                AND v.alternateAlleleFrequency < 0.1"""
                    condition_select_id = [row[0], row[1], row[3]]
                    cursor.execute(select_id, (condition_select_id))
                    record = cursor.fetchone()
                    connection.commit()

                    if record is not None:
                        print(record)
                        output_data.append(row)

                    cursor.close()

                except IndexError:
                    csv_file.close()


    except mysql.connector.Error as error:
        print("Error {}".format(error))

    return output_data, filepath

def filter_malignant(output_data, filename):

    print(output_data)
    out_filename = filename.split('.')[0]+'_malignant.'+filename.split('.')[1]
    out_file = 'static/'+out_filename

    with open(out_file, "w") as csv_file:
        csv_writer = csv.writer(csv_file, dialect = 'excel')
        for row in output_data:
            csv_writer.writerow(row)

    return output_data, out_filename




# filename = 'test.csv'
# input_data, filepath = get_result(filename)
# filter_malignant(input_data, filename)




