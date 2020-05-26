import csv

ALLOWED_EXTENSIONS = {'csv', 'json', 'vcf'}

filename = '/home/sanne/Desktop/test.csv'

def is_allowed(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_result(filename):
    result = []
    filepath = 'inbox/'+filename
    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            try:
                print(row)
                chrom = row[0]
                pos = row[1]
                id = row[2]
                ref = row[3]
                alt = row[4]
                prob = row[10].split('=')[1]
                variant = [chrom, pos, id, ref, alt, prob]
                result.append(variant)
            except IndexError:
                pass
    #logic for comparing the input data against the database
    #parsing the input file; extracting the chromosome, the postition, the nucleotide and the variant.
    #possibly the probability score

    return result

# filename = 'test.csv'
# get_result(filename)