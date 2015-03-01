#!/usr/bin/python

#
# Count code lines (no comments, no blank lines)
# Version 2.0: Works on c, python, or text files
# Version 1.0: Works on c code, /* */ or //
#
# Dean Blevins
# Mar 2015
#

#import pdb		#Debugger

import argparse		#argv
import sys		#For program exits

codeversion =	2.0
codelines =	0
index =		0
j =		0
SawCode =	False
InCComment =	False
InCppComment =	False
TestSlash =	False
TestStar =	False
TotalLines =	0
rawlines =	0

#####
##### FUNCTION: process_c_source()
#####

def process_c_source( fp, verbose, Verbose ):
	"Process a c language source file"

	codelines =	0   
	j =		0
	SawCode =	False
	InCComment =	False
	InCppComment =	False
	TestSlash =	False
	TestStar =	False
	rawlines =	0   

	# Read each line
	for codeline in fp:

		rawlines += 1

		for j in range(0, len(codeline)):

			c = codeline[j]

			if c == ' ':
				TestSlash = False
			elif c == '\t':
				TestSlash = False
			elif c == '\r':
				TestSlash = False
				
			elif c == '/':
				if TestSlash:
					InCppComment = True
					TestSlash = False  #Reset Cpp comment marker
				elif TestStar:
					TestStar = False
					TestSlash = False
					SawCode = False
					InCppComment = False
					InCComment = False
				else:
					TestSlash = True

			elif c == '*':
				if TestSlash:
					InCComment = True
					if SawCode: #Saw code earlier in the line?
						codelines = codelines +1
					SawCode = False
					InCppComment = False
					TestSlash = False
					TestStar = False
				else:
					TestStar = True

			elif c == '\n':
				if SawCode:
					codelines = codelines +1
					InCppComment = False
					SawCode = False
                                                
				if InCppComment:
					InCppComment = False
					SawCode = False
					TestSlash = False

				#Very Verbose
				if Verbose:
					print "%d : %d : %s" % (rawlines, codelines, codeline[0:len(codeline)-1])

			else:

				#Read a code char, reset comment marker
				TestSlash = False
				TestStar = False
				
				if InCComment or InCppComment:
					DoNothing = True  # Bogus line for pass through

				else:
					SawCode = True
	return( codelines )

#####
##### END FUNCTION: process_c_source()
#####

#####
##### MAIN
#####

codeversion =	2.0 
codelines =	0   
index =		0
TotalLines =	0   

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="verbose output", action="store_true")
parser.add_argument("-V", "--Verbose", help="more verbose output", action="store_true")
parser.add_argument("-t", "--totals", help="totals all files", action="store_true")
parser.add_argument("--version", help="version info", action="store_true")
parser.add_argument("files", help="source file(s)...", nargs=argparse.REMAINDER)
args = parser.parse_args()

#pdb.set_trace()	#Turn on debugger

# If just looking at program version, show it and exit
if args.version:
	print sys.argv[0], codeversion
	sys.exit(0)

# Process each file

for index in range(0, len(args.files)):

	with open(args.files[index], 'r') as fp:

		# What kind of file is it?
		if args.files[index].endswith(".c") or args.files[index].endswith(".h"):

			if args.verbose or args.Verbose:
				print "c source: ", args.files[index]

			codelines = process_c_source( fp, args.verbose, args.Verbose )

		print "%d %s" % (codelines, args.files[index])

		TotalLines += codelines
		codelines = 0

		fp.close()

if args.totals:
	print "Total: ", TotalLines
