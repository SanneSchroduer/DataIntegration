CREATE TABLE referenceNucleotide (
    id int(255) PRIMARY KEY AUTO_INCREMENT,
    chromosome varchar(3),      #Chromosome
    position int(5),            #position on chromosome
    nuclId varchar(255),        #ID code starts with rs
    reference varchar(255)       #only A, T, G or C
);


CREATE TABLE variant (
    id int(255) PRIMARY KEY AUTO_INCREMENT,
    alternate varchar(255),               #only A, T, G or C
    rfp         float(6),               #Random Forest Prediction: probabilities of being a true positive variant
    alternateAlleleFrequency float(10), #Allel frequency in samples
    variantType varchar(11),            #Variant type: snv, i-comndel, multi-indel, or mixed
    alleleType  varchar(5)              #Allele type: snv, ins, del, or mixed
);

ALTER TABLE referenceNucleotide ADD INDEX (id);
ALTER TABLE variant ADD FOREIGN KEY (id) REFERENCES referenceNucleotide (id);
