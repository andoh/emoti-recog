#!/usr/bin/env python3
#	Käsurealt lugemine
import argparse
#	CSV library
import csv
#	Regex library[()]*
import re

# UNIX i ja Python 3.4 REGEX on erinevad, proovime BA töös esialgu saada nad samale kujule
# sed - https://www.gnu.org/software/sed/manual/html_node/Regular-Expressions.html
# python - https://docs.python.org/3/library/re.html
# abiks : http://www.pythonregex.com/

# Make the '.' special character match any character at all, including a newline; without this flag, '.' will match anything except a newline.
# re.DOTALL

# Käsurealt argumentidega käivitamisel kommenteeri alumised 2 rida välja.
# f_input	= open ('//home//ando//Desktop//loputoo//trunk//ando_proovib_1//foorumid//Arvutid_valiidne.xml_tmp//emotikon_enne','r')
# f_output= open ('//home//ando//Desktop//loputoo//trunk//ando_proovib_1//foorumid//Arvutid_valiidne.xml_tmp//emotikon_prst_ando','w')

#	Kasutame .tsv formaati, kuna rea kontrollitavates mustrites ei ole /t sümbolit. Kasutame Python'i .csv failide lugemiseks mõeldud osa.
#	https://docs.python.org/3/library/csv.html

# f_input = open('//home//ando//Desktop//loputoo//trunk//puhtam_xml_ando//foorumid/Arvutid_valiidne.xml','r')
# Failist loetakse mustreid järjekorras, mis failis on toodud
# Märgend, mis peab olema rea alguses, kust
# emotikone tuvastama hakatakse
lineMarker = re.compile("<tuvasta_keel>.*")


# Funktsioon mustrite lugemiseks failist
def readPatternsFromTSV(input_dir):
	with open (input_dir,newline='') as tsvfile:

		patternPairs = []
		tsvReader  = csv.reader(tsvfile,delimiter='\t',quotechar='"')
		for row in tsvReader:
			try:
				row[0]	= re.compile(row[0])
				row[1]	= row[1]
				patternPairs.append(row)
			except re.error:
				print(re.error)
			except:
				return patternPairs
		return patternPairs


def main():
	
	# Käsurealt antud parameetri tuvastamine
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--input'),

	options = parser.parse_args();
	f_input = open(options.input, 'r')
	
	output = ''
	for row in f_input:

	#	Kontrollib, kas rida algab rea alguse märgendiga üldse
	#	Esmalt loeb failist mustrid massiivi, 
	#	seejärel rakendab ükshaaval pärast eelmise mustri töö lõppu.
	#	Kui ei alga soovitud sümboliga, siis kirjutab rea kohe ära

	#	Kirjuta subn-iks üle
	
		if (lineMarker.match(row) != None):
			alteredRow	= row

			arPatterns	= readPatternsFromTSV('//home//ando//Desktop//emoticon//Patterns//patterns.tsv')
			for pair in arPatterns:
				alteredRow = pair[0].sub(pair[1],alteredRow, count=0)

			#	Asenda tühikud vahepeal 
			alteredRow = re.sub(' +',' ', alteredRow)
			arPatterns	= []
			arPatterns	= readPatternsFromTSV('//home//ando//Desktop//emoticon//Patterns//patterns.1.tsv')

#			for pair in arPatterns:
#				alteredRow = pair[0].sub(pair[1],alteredRow, count=0)
			
			output += alteredRow
		else:
			output += row
	print(output)

main()