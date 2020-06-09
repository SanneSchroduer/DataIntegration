
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import vcf


def main():
    read_data()


def read_data():
    vcf_reader = vcf.Reader(open('data/chr18.vcf', 'r'))

    for record in vcf_reader:
        print(record.alleles)
        chr = record.CHROM
        id = record.ID
        rfp = (record.INFO['rf_tp_probability'])
        variant_type = (record.INFO['variant_type'])
        allele_type = str((record.INFO['allele_type'])).strip('[]\'')
        position = record.POS
        reference = record.REF
        alternate = str(record.ALT).strip('[]')
        allele_frequency1 = str(record.INFO['AF']).strip('[]')
        allele_frequency = float(allele_frequency1)

        referenceNucleotide = chr, position, id, reference
        variant = alternate, rfp, allele_frequency, variant_type, allele_type

        fill_db(referenceNucleotide, variant)


def fill_db(referenceNucleotide, variant):
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            port='3308',
                                            database='dnaVariance',
                                            user='root',
                                            password='helloworld',
                                            auth_plugin='mysql_native_password')

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