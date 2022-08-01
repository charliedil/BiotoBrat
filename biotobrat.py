import sys
import os
if len(sys.argv)!= 4:
    print("Incorrect amount of arguments. Should be 3 (input dir, output dir, entity)")

input_dir = sys.argv[1]
output_dir = sys.argv[2]
entity = sys.argv[3]

for file in os.listdir(input_dir):
    input_file = open(input_dir+"/"+file, "r")
    input_file_text = input_file.read()
    docs = input_file_text.split("-DOCSTART- X X O")
    print(docs)