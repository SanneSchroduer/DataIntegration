import csv

import mysql.connector
import vcf

ALLOWED_EXTENSIONS = {'csv', 'vcf'}

def is_allowed(filename):
    """
    This function can be used to check if the extension of the chosen input file is allowed.

    :param filename: the name of the input file (string)
    :return: True or False
    """
    return '.' in filename and \
           filename.rsplit('.')[1].lower() in ALLOWED_EXTENSIONS


def get_db_result(filename):
    """
    This function reads the input file and compares the data per row to the corresponding information in the database.
    A connection with the database is made and per row (in other words: per variant) a SQL query is executed using the chromosome,
    the position of the variant, the reference nucleotide and the alternative nucleotide.
    When the variant has a alternative frequency less than 1%,
    and a non cancer frequency of 0% the row is saved into the output_data variable.

    :param filename: name of the chosen input file (string)
    :return:
    - output data: list of the rows in the input file with variants <1% (list)
    - filepath: path to the output file (string)
    """


    if filename.split('.')[1] == 'csv':
        output_data, unknown_variants = parse_csv(filename)
    # elif filename.split('.')[1] == 'vcf':
        # output_data = parse_vcf(filename)
        # unfortunately this does not work yet due to decode errors

    return output_data, unknown_variants

def parse_csv(filename):
    output_data = []
    unknown_variants = []
    try:
        connection = mysql.connector.connect(host='database',
                                             port='3306',
                                             database='dnaVariants',
                                             user='root',
                                             password='helloworld')

        filepath = '../inbox/' + filename
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
                                AND alternate = %s
                                AND v.alternateAlleleFrequency < 0.01
                                OR v.nonCancerFrequency = 0
                                AND chromosome = %s
                                AND position = %s
                                AND reference = %s
                                AND alternate = %s"""
                    chr = row[0]
                    position = row[1]
                    reference = row[3]
                    alternate = row[4]
                    condition_select_id = [chr, position, reference, alternate,chr, position, reference, alternate]
                    cursor.execute(select_id, (condition_select_id))
                    record = cursor.fetchone()
                    connection.commit()

                    if record is not None:
                        output_data.append(row)
                    elif record is None:
                        select_id = """SELECT r.chromosome, r.position, r.reference, v.alternate
                                FROM referenceNucleotide r
                                INNER JOIN variant v
                                ON r.id = v.id
                                WHERE chromosome = %s
                                AND position = %s
                                AND reference = %s
                                AND alternate = %s"""
                        condition_select_id = [chr, position, reference, alternate]
                        cursor.execute(select_id, (condition_select_id))
                        reference = cursor.fetchone()
                        connection.commit()

                        if reference is None:
                            unknown_variants.append(row)

                    cursor.close()

                except IndexError:
                    csv_file.close()

    except mysql.connector.Error as error:
        print("Error {}".format(error))

    return output_data, unknown_variants

def parse_vcf(filename):
    output_data = []
    unknown_variants = []
    try:
        connection = mysql.connector.connect(host='database',
                                             port='3306',
                                             database='dnaVariants',
                                             user='root',
                                             password='helloworld')

        filepath = '../inbox/' + filename
        vcf_reader = vcf.Reader(open(filepath, 'r'))

        for record in vcf_reader:
            if record.CHROM:

                cursor = connection.cursor(buffered=True, dictionary=True)

                select_id = """SELECT r.chromosome, r.position, r.reference, v.alternate
                            FROM referenceNucleotide r
                            INNER JOIN variant v
                            ON r.id = v.id
                            WHERE chromosome = %s
                            AND position = %s
                            AND reference = %s
                            AND alternate = %s
                            AND v.alternateAlleleFrequency < 0.01
                            OR v.nonCancerFrequency = 0"""

                chr = record.CHROM
                position = record.POS
                reference = record.REF
                alternate = str(record.ALT).strip('[]')
                condition_select_id = [chr, position, reference, alternate]
                cursor.execute(select_id, (condition_select_id))
                record = cursor.fetchone()
                connection.commit()

                if record is not None:
                    output_data.append(record)
                elif record is None:
                    select_id = """"SELECT r.chromosome, r.position, r.reference, v.alternate
                            FROM referenceNucleotide r
                            INNER JOIN variant v
                            ON r.id = v.id
                            WHERE chromosome = %s
                            AND position = %s
                            AND reference = %s
                            AND alternate = %s"""
                    condition_select_id = [chr, position, reference, alternate]
                    cursor.execute(select_id, (condition_select_id))
                    reference = cursor.fetchone()
                    connection.commit()

                    if reference is None:
                        unknown_variants.append(row)

                cursor.close()

    except mysql.connector.Error as error:
        print("Error {}".format(error))
    finally:
        if (connection.is_connected()):
            connection.commit()
            connection.close()
            print("MySQL connection is closed")

    return output_data, unknown_variants

def write_output(output_data, unknown_variants, filename):
    """
    This function writes the variants with less than 1% alternative frequency and 0% non cancer frequency in
    the non output_data list to an output file.
    :param output_data: list of the rows in the input file with variants <1% (list)
    :param filename: the filename of the input file (string)
    :return:
    - out_filename: the name of the file in which the malignant variants are saved
    """

    out_file_hits = '../static/'+filename.split('.')[0]+'_malignant.'+filename.split('.')[1]


    with open(out_file_hits, "w") as csv_file:
        csv_writer = csv.writer(csv_file, dialect = 'excel')
        for row in output_data:
            csv_writer.writerow(row)

    out_file_unknown = '../static/'+filename.split('.')[0] + '_unknown.' + filename.split('.')[1]

    with open(out_file_unknown, "w") as csv_file:
        csv_writer = csv.writer(csv_file, dialect='excel')
        for row in unknown_variants:
            csv_writer.writerow(row)

    return out_file_hits, out_file_unknown
