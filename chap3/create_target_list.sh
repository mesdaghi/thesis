for file in ./DAT/*.dat; do
	if [ "${file:8:1}" == "r" ]; 
	then 
		echo ${file:6:5} >> target2.list
	else	
		name=${file:6:4}
		chain='A'		 
		echo $name$chain >> target2.list
	fi

#do printf '%s\n' "${f%.dat}" # > target2.list
done;
