"""
biotobrat.py - a converter made to convert HUNER dataset files into Brat format. Produces txt files and ann files


Running instructions
---------------------

Note this was specifically made for user with the HUNER dataset and may not work as intended with different datasets
Specifically this assumes that there is only one entity class in the files - which you have to specify as an arg

Input
Input directory of files to convert, output directory for txt and ann files to go to, the entity class

Output:
Files will be written to the output directory

Example run:
python biotobrat.py in out gene

files in this case would be outputted to out

Charlie Dil
python3.8
"""

import sys
import os
if len(sys.argv)!= 4: # error handling
    print("Incorrect amount of arguments. Should be 3 (input dir, output dir, entity)")

input_dir = sys.argv[1]  # collect command line args
output_dir = sys.argv[2]
entity = sys.argv[3]

for file in os.listdir(input_dir):  # go through each file in the input directory
    input_file = open(input_dir+"/"+file, "r") # open it
    input_file_text = input_file.read() # read it
    input_file.close() # we close our files in this house!
    docs = input_file_text.split("-DOCSTART- X X O") # use the docstart tags to split the file into "documents"
    print(docs[1])
    filename = 0
    for d in docs: # iterate through the docs

        counter = 0
        entities = {}
        text = ""  #for the full text
        entity_text = ""  #for the entities we may encounter
        span = 0  # ongoing span, we'll increment this as we parse the document
        start_span = span # used to hold the entity starting span
        lines = d.split("\n\n") # lines in the document
        print(lines)
        for l in lines:
            if l != "" and l!= "** JJ O\nIGNORE NNP O\nLINE NNP O\n** . O": #we ignore the ignore lines and blanks
                tokens = l.split("\n") # get the tokens in the lines
                for t in range(len(tokens)):
                    subtokens = tokens[t].split(" ")  # get the subtokens (text, POS, entity)
                    if subtokens[2].split("-")[0] == "B" and entity_text !="": # added this in case of sequential entities
                        entities["T" + str(counter)] = [entity_text, start_span, start_span + len(entity_text)] # adding previous entity to dictionary
                        start_span = span  # set start span for new entity
                        entity_text = "" # reset entity text
                        entity_text += subtokens[0] # add text to entity text
                        counter+=1 # increment counter
                    if subtokens[2].split("-")[0] == "B" and entity_text =="": # if not a sequential entity, less work needs to be done
                        entity_text += subtokens[0] # just append text
                        start_span = span # set start span
                    if subtokens[2].split("-")[0] == "I": # Intermediate token
                        entity_text +=" "+subtokens[0] # append space AND text
                    if subtokens[2].split("-")[0] == "O" and entity_text!="": # if we hit "O" but were working on an entity, we need to append that entity
                        entities["T"+str(counter)] = [entity_text, start_span, start_span+len(entity_text)]
                        start_span = span # resetting all variables (except counter)
                        entity_text = ""
                        counter+=1

                    text+=subtokens[0] # add to text for text file
                    span+=len(subtokens[0]) # increment span
                    if t!=len(tokens)-1: #if it's not the last token
                        text += " " # add a space
                        span+=1 # increment span
                    else:
                        text+="\n" # add a new line
                        span+=1 # increment span

        ## write entities to ann file
        ann_file = open(output_dir+"/"+str(filename)+".ann", "w")
        for e in entities:
            ann_file.write(e+"\t"+entity+" "+str(entities[e][1])+" "+str(entities[e][2])+"\t"+entities[e][0]+"\n")

        ## write text to text file
        text_file = open(output_dir+"/"+str(filename)+".txt", "w")
        text_file.write(text)
        ##close our files!
        text_file.close()
        ann_file.close()

        ##incrememnt filename so our files have unique names
        filename+=1

