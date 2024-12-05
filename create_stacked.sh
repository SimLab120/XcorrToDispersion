folder="/media/bharath/c8291c97-69d5-4cc9-a843-78d42720b650/Satopanth_new/Data/cc/Stacked_CC1b"

for pair_folder in $folder/*
do
	p=`echo $pair_folder | awk -F"/" '{print $NF}'`
	echo $p

	for day_folder in $pair_folder/*
	do
(
		cd $day_folder
		d=`echo $day_folder  | awk -F"/" -v p=$p '{print "cc_"p"_"$NF}'`
		echo $d
		if [ ! -f "tl_"$d".sac" ]
		then 
			echo "pwd" | sh
			echo "ls -1 *.sac > filelist.txt" | sh
			echo "ts_pws filelist.txt rm unbiased osac="$d | sh
			echo "rm filelist.txt" | sh
		fi
)
		#break
	done
	#break
done
