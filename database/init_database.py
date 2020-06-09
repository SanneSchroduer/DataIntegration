import mysql.connector
import os
from mysql.connector import Error
from mysql.connector import errorcode
import vcf


def main():
    check_existance()
    read_data()

def check_existance():

    try:
        connection = mysql.connector.connect(host='database',
                                             port='3306',
                                             database='dnaVariants',
                                             user='root',
                                             password='helloworld')

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
                                    id int(255) PRIMARY KEY AUTO_INCREMENT,
                                    alternate varchar(255),             
                                    rfp         float(6),               
                                    alternateAlleleFrequency float(10), 
                                    variantType varchar(11),            
                                    alleleType  varchar(5)              
                                );"""
                add_fk = """ALTER TABLE variant ADD FOREIGN KEY (id) REFERENCES referenceNucleotide (id);"""
                cursor.execute(create_var_table)
                cursor.execute(add_fk)

            connection.commit()

    except mysql.connector.Error as error:
        print("Parameterized query failed {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def read_data():

    vcf_files = []
    for file in os.listdir("../data"):
        if file.endswith(".vcf"):
            vcf_files.append(os.path.join("../data", file))

    for file in vcf_files:
        vcf_reader = vcf.Reader(open(file, 'r'))

        for record in vcf_reader:
            chr = record.CHROM
            id = record.ID
            rfp = (record.INFO['rf_tp_probability'])
            variant_type = (record.INFO['variant_type'])
            allele_type = str((record.INFO['allele_type'])).strip('[]\'')
            position = record.POS
            reference = record.REF
            alternate = str(record.ALT).strip('[]')
            allele_frequency = float(str(record.INFO['AF']).strip('[]'))

            referenceNucleotide = chr, position, id, reference
            variant = alternate, rfp, allele_frequency, variant_type, allele_type

            fill_db(referenceNucleotide, variant)


def fill_db(referenceNucleotide, variant):
    try:
        connection = mysql.connector.connect(host='database',
                                             port='3306',
                                             database='dnaVariants',
                                             user='root',
                                             password='helloworld')

        sql = """INSERT INTO referenceNucleotide(Chromosome, Position, NuclID, Reference)
                               VALUES (%s, %s, %s, %s);"""

        sql2 = """INSERT INTO variant(alternate, rfp, alternateAlleleFrequency, variantType, alleleType)
                                          VALUES (%s, %s, %s, %s, %s);"""

        cursor = connection.cursor()
        cursor.execute(sql, referenceNucleotide)
        cursor.execute(sql2, variant)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into table")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into table: {}".format(error))

main()