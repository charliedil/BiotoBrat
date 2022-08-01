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
    input_file.close()
    docs = input_file_text.split("-DOCSTART- X X O")
    print(docs[1])
    filename = 0
    for d in docs:

        counter = 0
        entities = {}
        text = ""
        entity_text = ""
        span = 0
        start_span = span
        lines = d.split("\n\n")
        print(lines)
        for l in lines:
            if l != "" and l!= "** JJ O\nIGNORE NNP O\nLINE NNP O\n** . O":
                tokens = l.split("\n")
                for t in range(len(tokens)):
                    subtokens = tokens[t].split(" ")
                    if subtokens[2].split("-")[0] == "B" and entity_text !="":
                        entities["T" + str(counter)] = [entity_text, start_span, start_span + len(entity_text)]
                        start_span = span
                        entity_text = ""
                        entity_text += subtokens[0]
                        counter+=1
                    if subtokens[2].split("-")[0] == "B" and entity_text =="":
                        entity_text += subtokens[0]
                        start_span = span
                    if subtokens[2].split("-")[0] == "I":
                        entity_text +=" "+subtokens[0]
                    if subtokens[2].split("-")[0] == "O" and entity_text!="":
                        entities["T"+str(counter)] = [entity_text, start_span, start_span+len(entity_text)]
                        start_span = span
                        entity_text = ""
                        counter+=1

                    text+=subtokens[0]
                    span+=len(subtokens[0])
                    if t!=len(tokens)-1:
                        text += " "
                        span+=1
                    else:
                        text+="\n"
                        span+=1
        ann_file = open(output_dir+"/"+str(filename)+".ann", "w")
        for e in entities:
            ann_file.write(e+"\t"+entity+" "+str(entities[e][1])+" "+str(entities[e][2])+"\t"+entities[e][0]+"\n")
        text_file = open(output_dir+"/"+str(filename)+".txt", "w")
        text_file.write(text)
        text_file.close()
        ann_file.close()
        filename+=1

