import csv

ALLOWED_EXTENSIONS = {'csv', 'json', 'vcf'}

filename = '/home/sanne/Desktop/test.csv'

def is_allowed(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_result(filename):

    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            chrom = row[0]
            pos = row[1]
            id = row[3]
            ref = row[4]
            alt = row[5]
            prob = row[10]
    #logic for comparing the input data against the database
    #parsing the input file; extracting the chromosome, the postition, the nucleotide and the variant.
    #possibly the probability score
    return filename

get_result(filename)