import csv

ALLOWED_EXTENSIONS = {'csv', 'json', 'vcf'}

filename = '/home/sanne/Desktop/test.csv'

def is_allowed(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_result(filename):
    result = []
    pos_list = []
    filepath = 'inbox/'+filename
    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            try:
                chrom = row[0]
                pos = row[1]
                id = row[2]
                ref = row[3]
                alt = row[4]
                prob = row[10].split('=')[1]

                if pos in pos_list:
                    print(pos)
                pos_list.append(pos)
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


'''
filename get_variants.py 
e.g. chr18 get_variants.py

get_variants.py: 
- draait lokaal
- leest input file in
- stuurt request naar API (draait vanuit een docker container op 127.0.0.1:5000) met filenaam van input file
- schrijft alle malign variants naar output file in directory van 

output: chr18_malign
'''
#
# for x in files:
#     request(127.0.0.1:500, 'chr18')


