import sys
import sqlite3

con = sqlite3.connect('/home/kiverson/keggGenes')
c = con.cursor()

ko2gene = open(sys.argv[1], 'r')
ko2mod = open(sys.argv[2], 'r')
mod2des = open(sys.argv[3], 'r')

for line in ko2gene:
    line = line.strip()
    line = line.split("\t")
    ko = str(line[0])
    for gene in line[1:]:
        t = (gene.strip(), ko.strip())
        c.execute("INSERT INTO ko2gene VALUES (?,?)", t)

con.commit()

for line in ko2mod:
    line = line.strip()
    line = line.split("\t")
    mod = str(line[0])
    for ko in line[1:]:
        t = (ko.strip(), mod.strip())
        c.execute("INSERT INTO ko2module VALUES (?,?)", t)

con.commit()

for line in mod2des:
    line = line.strip()
    line = line.split("\t")
    mod = str(line[0])
    for des in line[1:]:
        t = (mod.strip(), des.strip())
        c.execute("INSERT INTO module2des VALUES (?,?)", t)

con.commit()
c.close()
