home="Data/cc/All_day_stack_PCC"

destination1="Data/cc/All_day_stack_PCC_tl/"
destination2="Data/cc/All_day_stack_PCC_ts_pws/"
#for i in $home/*
#do
#	for j in $i/*
#	do
#		echo "mv "$j"/tl*.sac" $destination1 | sh 
#		echo "mv "$j"/ts_pws*.sac" $destination2 | sh
#	done
#done

for i in $home/*
do
	echo "mv "$i"/tl*.sac" $destination1 | sh 
	echo "mv "$i"/ts_pws*.sac" $destination2 | sh
done

