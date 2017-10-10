#!/bin/bash

FILES=./../logs/*

for f in $FILES
do
	#echo $f
	name=${f##*/}
	echo ${name%.*}
	python3 line_graph.py ${f} 30 1000 ${name}
done

#print("Usage: python3 line_graph.py <file path> <number of runs> <number of evals> <graph number>")
