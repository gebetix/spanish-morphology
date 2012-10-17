#!/bin/sh

learn() {
	echo "\n====== Building ======\n"
	rm -Rf temporary.*
	cp spanish.foma temporary.spanish.foma
	echo "\n\nsave stack spanish.bin\nexit" >> temporary.spanish.foma
	./foma/foma -l temporary.spanish.foma

	echo "\n====== Running ======\n"
	cat data/spanish.txt.learn | awk '{print $1}' | ./foma/flookup spanish.bin > temporary.prediction.raw.result
	echo 'Created file temporary.prediction.raw.result'
	cat temporary.prediction.raw.result | grep -o "^[^\+]*\+.." | uniq > temporary.prediction.result
	echo 'Created file temporary.prediction.result'
	cat temporary.prediction.result | awk 'BEGIN{m=1;str=""}{if(m==1){w=$1;m=0}if($1==w){str=str"\t"$2}else{print w""str;w=$1;str="\t"$2}}END{if(length(str)>0){print w""str}}'> temporary.final.result
	echo 'Created file temporary.final.result'

	echo "\n====== Results ======\n"
	python py/evaluate.py data/spanish.txt.learn temporary.final.result	
}

control() {
	echo "\n====== Building ======\n"
	rm -Rf temporary.*
	cp spanish.foma temporary.spanish.foma
	echo "\n\nsave stack spanish.bin\nexit" >> temporary.spanish.foma
	./foma/foma -l temporary.spanish.foma

	echo "\n====== Running ======\n"
	cat data/spanish.txt.test.clean | ./foma/flookup spanish.bin > temporary.prediction.raw.result
	echo 'Created file temporary.prediction.raw.result'
	cat temporary.prediction.raw.result | grep -o "^[^\+]*\+.." | uniq > temporary.prediction.result
	echo 'Created file temporary.prediction.result'
	cat temporary.prediction.result | awk 'BEGIN{m=1;str=""}{if(m==1){w=$1;m=0}if($1==w){str=str"\t"$2}else{print w""str;w=$1;str="\t"$2}}END{if(length(str)>0){print w""str}}'> temporary.final.result
	echo 'Created file temporary.final.result'
	iconv -f utf-8 -t ISO8859-1 temporary.final.result > temporary.final.result.latin1
	echo 'Created file temporary.final.result.latin1, send this file!!'
}

#learn
control