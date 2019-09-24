#!/bin/sh
# Please put this shell script in the directory where there is pyrat.py
# Copyright Xi SONG 23/09/2019
# TODO: How to automatically kill the game and continue
echo -e "Automatically execute the pyrat.py and store the data necessary in data.txt\n"
# Read the controlling file
echo "Please enter the absolute path of your file to be tested"
read fileName
# Read the smallest size of the maze
echo "Enter the inital length of the maze (Default: a square maze)"
read iniLen
# Read the step betwenn each experiement
echo "Enter the step"
read step
# Read the biggest size of the maze
echo "Enter the biggest length"
read maxLen

# Initialize the data.txt
echo "" > data.txt
i=$iniLen
while(( ${i} <= ${iniLen} ))
do
# Here you should replace the path by your own TODO: How to automatically kill the process?
	result=$(python3 /Users/xisung/Desktop/StudyHard/AlgorithmandDiscretMath/PyRat-master/pyrat.py -x $i -y $i -p 1 -md 0 --nodrawing --test 10 --synchronous--rat ${fileName})
	moves=$(echo $result | grep "moves_rat" | cut -f6 -d ":" | cut -f1 -d "\"")
	preptime=$(echo $result | grep "prep_time_rat" | cut -f8 -d ":" | cut -f1 -d "\"")
	turntime=$(echo $result | grep "turn_time_rat" | cut -f14 -d ":"| cut -f1 -d "\"")
	output="Length: ${i}\t Moves: ${moves}\t Prepare time: ${preptime}\t Turn time: ${turntime}\t"
	echo ${output} >> data.txt
	let "i=$i+$step"
done
