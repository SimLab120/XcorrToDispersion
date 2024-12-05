for f in Data/cc/Stacked_PCC/*
do 
	for j in $f/*
	do 
		for k in ${j}/*sacpcc
		do
			x=`echo $k | awk -F".sacpcc" '{print $1".sac"}'`
			mv $k $x
		done
		#break
	done
	#break
done
