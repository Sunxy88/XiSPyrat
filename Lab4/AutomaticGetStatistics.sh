#!/bin/sh
# Please put this shell script in the directory where there is pyrat.py
# Copyright Xi SONG 23/09/2019
echo -e "Automatically execute the pyrat.py and store the data necessary in data.txt\n"
# Read the controlling file
echo "Please enter the absolute path of your file to be tested"
read fileName
# Read the smallest size of the maze
echo "Enter the size of the maze (Default: a square maze and Attention: an odd number please)"
read iniLen

echo "Enter the initial pieces of the cheeses"
read iniPiece

echo "Enter the step"
read step

echo "Enter the biggest number of cheese"
read maxCheese

# Initialize the data.txt
echo "" > data.txt
i=$iniPiece

while [[ ${i} -le ${maxCheese} ]]
do
# Here you should replace the path by your own
	echo "Iteration ${i}"
	result=$(python3 /Users/xisung/Desktop/StudyHard/AlgorithmandDiscretMath/PyRat-master/pyrat.py -x ${iniLen} -y ${iniLen} -p ${i} --nodrawing --test 10 --synchronous --rat ${fileName})
	moves=$(echo $result | grep "moves_rat" | cut -f6 -d ":" | cut -f1 -d "\"")
	preptime=$(echo $result | grep "prep_time_rat" | cut -f8 -d ":" | cut -f1 -d "\"")
	turntime=$(echo $result | grep "turn_time_rat" | cut -f14 -d ":"| cut -f1 -d "\"")
	output="Length: ${i}\t Moves: ${moves}\t Prepare time: ${preptime}\t Turn time: ${turntime}\t"
	echo ${output} >> data.txt
	let "i=i+step"
	echo ${i}
done

echo "Script is done, the data.txt is in the same directory as pyrat.py"
