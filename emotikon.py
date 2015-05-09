#!/usr/bin/env python3
#	Käsurealt argumentide lugemine
import argparse
#	Standardsisendi lugemine
import sys
import os
import datetime
#	CSV library
import csv
#	Regex library[()]*
import re

# SED - https://www.gnu.org/software/sed/manual/html_node/Regular-Expressions.html
# Python - https://docs.python.org/3/library/re.html
# Abiks : http://www.pythonregex.com/

# Kasutame mustrifailides .tsv formaati, kuna  kontrollitavates mustrites ei ole /t sümbolit. Kasutame Python'i .csv failide lugemiseks mõeldud moodulit.
# https://docs.python.org/3/library/csv.html
# Failist loetakse mustreid järjekorras, mis failis on toodud
# Funktsioon mustrite lugemiseks failist
def readPairsFromTSV(input_dir, Dict=False):
	with open (input_dir,newline='') as tsvfile:
		if(Dict):
			pairs = {}
		else:
			pairs = []

		tsvReader  = csv.reader(tsvfile,delimiter='\t',quotechar='"')
		for row in tsvReader:
			try:
				if(Dict):
					pairs[row[1]] = row[0]
				else:
					row[0]	= re.compile(row[0])
					row[1]	= row[1]
					pairs.append(row)
			except re.error:
				print(re.error)
			except:
				return pairs
		return pairs
# Parameetrite sättimine ja lugemine käsurealt
def getParams():
	parser = argparse.ArgumentParser()
	# Käsurealt antavad argumendid 	
	## Sisendfaili nimi 
	parser.add_argument('-i','--input')
	## Töötluse tüüp, näiteks foorum, uudisgrupp, kommentaar
	parser.add_argument('-t','--type')
	## Väljundfaili nimi
	parser.add_argument('-o','--output')
	options = parser.parse_args();
	return options


working_dir = os.getcwd()
def main():
	# Loeme käsurea argumendid
	options = getParams()

	# Käsurea input väärtuse kontroll.
	# Kui käsurealt parameetrit ei tulnud, kuulatakse standardsisendit
	if(options.input != None):
		f_input = open(options.input, 'r')
	else:
		f_input = sys.stdin
	
	# Käsurea output väärtuse kontroll.
	# Kui käsurealt failinime ei tulnud, kirjutatakse standardväljundisse
	f_output = False
	if(options.output != None):
		f_output = open(options.output, 'w')
	
	# Erinevate sisenditüüpide ja nende argumentide tuvastamine
	inputTypes = readPairsFromTSV(working_dir + "//inputTypes.tsv",True)
	# Vaikimisi töödeldakse iga rida sisendis
	processAll = True
	lineMarker = ".*"
	# Käsurealt tüübi kontroll - kui ei tulnud, töötle kõiki
	if(options.type in inputTypes):
		# Märgend, mis peab olema rea alguses, kust emotikone tuvastada soovitakse
		lineMarker = re.compile(inputTypes[options.type])
		processAll = False

	# Mustrifailide avamine
	arPatterns	= readPairsFromTSV(working_dir + '//uusmeedia//activePatterns.tsv')
	
	# Lühendatud mustrid, work in progress
	#arPatterns	= readPairsFromTSV('//home//ando//Desktop//emoticon//uusmeedia//andopatterns.tsv')

	for row in f_input:
		#	Kontrollib, kas rida algab rea alguse märgendiga
		#	Mustrid rakendatakse järjestikku pärast eelmise mustri töö lõppu.
		if (processAll or lineMarker.match(row) != None):
			for pair in arPatterns:
				row = pair[0].sub(pair[1],row, count=0)
		if (f_output == False):
			print(row, end='')
		else:
			f_output.write(row)
	if (f_output != False):
		f_output.close()

def test():

	global working_dir
	f_inputdirs = os.listdir(working_dir + "/sisend/foorumid")
	
	# Käsurea output väärtuse kontroll.
	# Kui käsurealt failinime ei tulnud, kirjutatakse standardväljundisse
	# outf = os.getcwd() + "/testid/test " + str(datetime.datetime.now())
	# f_output = open(outf, 'w')

	processAll = True
	lineMarker = ".*"
	
	# Mustrifailide avamine
	arPatterns	= readPairsFromTSV(working_dir ++ '//uusmeedia//activePatterns.tsv')
	
	# Lühendatud mustrid, work in progress
	#arPatterns	= readPairsFromTSV('//home//ando//Desktop//emoticon//uusmeedia//andopatterns.tsv')
	
	# Väljundkausta loomine
	currentTestTime = str(datetime.datetime.now())
	os.mkdir(working_dir + "/testid/" + currentTestTime)

	for f_inputdir in f_inputdirs:
		f_input = open(working_dir + "/sisend/foorumid/" + f_inputdir + "/emotikon_enne")
		
		# Väljundkausta loomine
		f_outputdir = working_dir + "/testid/" + currentTestTime + "/" + f_inputdir
		os.mkdir(f_outputdir)
		
		# Ava väljundfail
		f_output = open(f_outputdir + "/emotikon_prst.txt", 'w')
		
		for row in f_input:
			#	Kontrollib, kas rida algab rea alguse märgendiga
			#	Mustrid rakendatakse järjestikku pärast eelmise mustri töö lõppu.
			if (processAll or lineMarker.match(row) != None):
				for pair in arPatterns:
					row = pair[0].sub(pair[1],row, count=0)
					
			f_output.write(row)
			
		f_output.close()
	


# Kui testitakse, siis siin määrata lipu asend!
Test = False
# Test = True
if (Test):
	test()
else:
	main()