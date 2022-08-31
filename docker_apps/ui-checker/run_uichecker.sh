#!/bin/bash

# !!IMPORTANT!!
# The rules .dl file should have this line at the top of the file: #include "/home/ui-checker/rules/input.dl" 

# ARGUMENTS
#$1 = apk file
#$2 = rules file file (.dl file)

## uncomment line below if you wish to re-run script
# docker rm -f ui-checker

echo starting ui-checker container
docker run --name ui-checker -td triplejays/ui-checker:1.2

echo copying files into ui-checker
docker cp $1 ui-checker:/home/ui-checker/
docker cp $2 ui-checker:/home/ui-checker/

echo running ui-checker ...
docker exec ui-checker ./uicheck $1 $2

echo saving output to current dir
docker cp ui-checker:/home/ui-checker/output_markii/ . 

echo results saved to output_markii
