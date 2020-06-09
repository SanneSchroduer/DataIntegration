import mysql.connector
import os
from mysql.connector import Error
from mysql.connector import errorcode
import vcf


def main():
    read_data()

def read_data():

    vcf_files = []
    for file in os.listdir("../vcf_data"):
        if file.endswith(".vcf"):
            vcf_files.append(os.path.join("../vcf_data", file))

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