import sys
import heapq
import operator as o

infile = open(sys.argv[1], 'r')

def get_next_fasta (fileObject):
    '''usage: for header, seq in get_next_fasta(fileObject):
    This is a generator that returns one fasta record's header and
sequence at a time from a multiple fasta file. Return character is removed
from the header. The sequence is returned as one continuous string
with no returns. The returned value is a tuple (header, sequence)
If their is no sequence associated with a header, seq will be an
empty string
Code simplification contributed by Dattatreya Mellacheruvu
01/16/2009, Jeffrey R. de Wet

    '''
    header = ''
    seq = ''
    #The following for loop gets the header of the first fasta
    #record. Skips any leading junk in the file
    for line in fileObject:
        if line.startswith('>'):
            header = line.strip()
            break
    
    for line in fileObject:
        if line.startswith('>'):
            yield header, seq
            header = line.strip()
            seq = ''
        else:
            seq += line.strip()
    #yield the last entry
    if header:
        yield header, seq

def sd(myList, avg):
    tmp = []
    for item in myList:
        tmp.append((item - avg)**2)
    SD = (float(sum(tmp))/len(tmp))**0.5
    return SD
    
def median(s):
    s= sorted(s)
    i = len(s)
    if not i%2:
        return (s[(i/2)-1]+s[i/2])/2.0
    return s[i/2]

totalLen = 0
totalSeqs = 0
longest = 0
tmpcount = 0
shortest = 10000000000000000000000000000
lengthlist = []
longestseq = ''
longestseq_header = ''
seqdict = {}
lendic = {}

for header, seq in get_next_fasta(infile):
    seqdict[header] = seq
    lendic[header] = len(seq)
    length = len(seq)
    #for key, value in list(seqdict.items()):
    #    if key not in [x[0] for x in heapq.nlargest(10, seqdict.iteritems(), o.itemgetter(1))]:
    #        del seqdict[key]
    lengthlist.append(length)
    totalLen += length
    totalSeqs += 1
    if length > longest:
        longest = length
        longestseq = seq
        longestseq_header = header
    if length < shortest:
        shortest = length
    if length >= 4000:
        tmpcount += 1

infile.close()
# top10file = open("top10longestcontigs.fa", 'w')
# #top10 = heapq.nlargest(10, seqdict, key=len)
# #print top10
# 
# for item in [x[0] for x in heapq.nlargest(10, lendic.iteritems(), o.itemgetter(1))]:
#     top10file.write("%s\n%s\n" % (item, seqdict[item]) )
# 
# lengthlist.sort(reverse=True)

avgLen = totalLen/totalSeqs
trimmedAvg = (totalLen-(longest+shortest))/(totalSeqs-2)

print "total contigs:", totalSeqs
print "average length:", avgLen, "bp"
print "trimmed average length:", trimmedAvg, "bp"
print "top 10: ", str(lengthlist[:10])
#print "other avg: ", float(sum(lengthlist))/len(lengthlist)
print "standard deviation: ", sd(lengthlist, avgLen)
print "median: ", median(lengthlist)
print "greater than or equal to 4000: ", tmpcount
print "shortest conting:", shortest, "bp"
print "longest contig:", longest, "bp"
print "total length:", totalLen/1000000.00, "Mb"

#outfile = open("longest_contig.fa", 'w')
#outfile.write("%s\n%s" % (longestseq_header, longestseq) )
#outfile.close()
infile.close()
