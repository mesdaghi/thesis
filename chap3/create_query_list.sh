for file in ./DAT_pdb/*.dat; do
	if [ "${file:8:1}" == "r" ]; 
	then 
		echo ${file:6:5} >> query.list
	else	
		name=${file:6:4}
		chain='A'		 
		echo $name$chain >> query.list
	fi

#do printf '%s\n' "${f%.dat}" # > target2.list
done;
