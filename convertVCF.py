import vcf
vcf_reader = vcf.Reader(open('data/chr18_onlyintro.vcf', 'r'))
for record in vcf_reader:
    print(record.alleles) #both alleles: ['A', G]
    print(record.INFO['rf_tp_probability'])
    print(record.INFO['variant_type'])
    print(record.INFO['allele_type'])
    print(record.POS,
          record.REF,
          record.ALT,
          record.INFO['AF']
          )


