import vcf
vcf_reader = vcf.Reader(open('/home/sanne/Desktop/chr18_onlyintro.vcf', 'r'))
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

##  DATABASE
# downloaden mysql server docker image
#       docker pull mysql/mysql-server:tag
#       naam  van de image is "mysql/mysql-server:tag"
#       tag zorgt ervoor dat de latest tag gebruikt wordt

# starten van een msql server instance (container)
#       docker run --name=mysql1 -d mysql/mysql-server:tag
#       --name geeft de naam aan je container
#       -d zorgt ervoor dat de container op de achtergrond blijft runnen

# controleren of container runt
#       docker ps
# connecten aan de mysql server vanuit de container
#       docker exec -it mysql1 mysql -uroot -p



# mysql database maken in een eigen Docker container
# mysql connector aanmaken, met een insert de data opslaan in een database