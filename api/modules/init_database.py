import mysql.connector
import os
from mysql.connector import Error
from mysql.connector import errorcode
import vcf


def main():
    make_tables()
    read_data()

def make_tables():
    """
    This functions checks if the referenceNucleotide table and variant table already exist.
    If not, these tables are created.
    :return:
    """

    try:
        connection = mysql.connector.connect(host='database',
                                             database='dnaVariants',
                                             user='root',
                                             password='helloworld',
                                             auth_plugin='mysql_native_password')
        if connection:
            table_exists = """SELECT table_name
                              FROM information_schema.tables
                              WHERE table_schema = 'dnaVariants'
                              AND table_name LIKE %s"""
            cursor = connection.cursor(prepared=True)
            cursor.execute(table_exists, ('referenceNucleotide',))
            ref_table = cursor.fetchone()

            if ref_table is None:
                create_ref_table = """CREATE TABLE referenceNucleotide (
                                      id int(255) PRIMARY KEY AUTO_INCREMENT,
                                      chromosome varchar(3),
                                      position int(5),
                                      nuclId varchar(255),
                                      reference varchar(255)
                                      );"""
                add_pk = """ALTER TABLE referenceNucleotide ADD INDEX (id);"""
                cursor.execute(create_ref_table)
                cursor.execute(add_pk)

            cursor.execute(table_exists, ('variant',))
            var_table = cursor.fetchone()
            if var_table is None:
                create_var_table = """CREATE TABLE variant (
                                      id int(255),
                                      alternate varchar(255),
                                      rfp float(6),
                                      alternateAlleleFrequency float(10),
                                      nonCancerFrequency float(10)
                                      );"""
                add_fk = """ALTER TABLE variant ADD FOREIGN KEY (id) REFERENCES referenceNucleotide (id);"""
                cursor.execute(create_var_table)
                cursor.execute(add_fk)

    except mysql.connector.Error as error:
        print("Failed to insert record into table: {}".format(error))
    finally:
        if (connection.is_connected()):
            connection.commit()
            connection.close()
            print("MySQL connection is closed")

def read_data():
    """
    This function reads all the files in the vcf_data folder and calls the fill_db function to fill the database with the data.
    """
    try:
        connection = mysql.connector.connect(host='database',
                                             database='dnaVariants',
                                             user='root',
                                             password='helloworld',
                                             auth_plugin='mysql_native_password')
        cursor = connection.cursor(buffered=True)

        reference_ids = []
        vcf_files = []
        for file in os.listdir("../vcf_data"):
            if file.endswith(".vcf"):
                vcf_files.append(os.path.join("../vcf_data", file))

        for file in vcf_files:
            vcf_reader = vcf.Reader(open(file, 'r'))

            for record in vcf_reader:
                chr = record.CHROM
                nuclId = record.ID
                rfp = record.INFO['rf_tp_probability']
                position = record.POS
                reference = record.REF
                alternate = str(record.ALT).strip('[]')
                allele_frequency = record.INFO['AF'][0]


                if 'non_cancer_AF' in record.INFO:
                    non_cancer_frequency = record.INFO['non_cancer_AF'][0]
                else:
                    non_cancer_frequency = None

                # if the nuclId is not stored in the referenceNucleotide table, the reference is inserted
                if nuclId not in reference_ids:
                    reference_ids.append(nuclId)
                    insert_ref = """INSERT INTO referenceNucleotide(Chromosome, Position, NuclID, Reference)
                                  VALUES (%s, %s, %s, %s);"""
                    referenceNucleotide = chr, position, nuclId, reference

                    cursor.execute(insert_ref, referenceNucleotide)
                    print('Inserting reference nucleotide with nuclId:', nuclId)

                # selecting the id of the referenceNucleotide table that corresponds with the current nuclId
                select_ref = """SELECT id from referenceNucleotide WHERE nuclId = %s"""
                cursor.execute(select_ref, (nuclId,))
                corresponding_id_tuple = cursor.fetchone()

                if corresponding_id_tuple is not None:
                    corresponding_id = int(corresponding_id_tuple[0])
                    # inserting the current variant into the variant table with the corresponding id
                    insert_var = """INSERT INTO variant(id, alternate, rfp, alternateAlleleFrequency, nonCancerFrequency)
                                    VALUES (%s, %s, %s, %s, %s);"""
                    variant = corresponding_id, alternate, rfp, allele_frequency, non_cancer_frequency

                    cursor.execute(insert_var, variant)
                    print('Inserting variant nucleotide')


    except mysql.connector.Error as error:
        print("Failed to insert record into table: {}".format(error))
    finally:
        if (connection.is_connected()):
            connection.commit()
            connection.close()
            print("MySQL connection is closed")


main()