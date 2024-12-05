d="PCC"
folder="./Data/cc/"$d

destination="./Data/cc/All_day_stack_"$d

mkdir -p $destination

for i in `seq 1 13`; do for j in `seq $((i + 1)) 14`; do mkdir -p $destination"/"$i"_"$j; done; done


for sacfile in $folder/*.sac
do
	echo $sacfile
	fol=`echo $sacfile | awk -F"/" '{print $NF}' | awk -F"_" '{print $2"_"$3}'`
 	echo "cp "$sacfile" "$destination"/"$fol | sh

#break
done


for pair_folder in $destination/*
do
	p=`echo $pair_folder | awk -F"/" '{print $NF}'`
(
	cd $pair_folder
	echo "ls -1 *.sac > filelist.txt" | sh
	echo "ts_pws filelist.txt rm unbiased osac="$p | sh
	echo "rm filelist.txt" | sh
)
done 


