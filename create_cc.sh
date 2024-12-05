sac_data_folder="Data/min_wise/"

(
cd $sac_data_folder

for i in `seq 1 1 14`
do
txt_name="rec_"$i".txt"
echo "ls rec_"$i"_*.sac>"$txt_name |sh 
done

for f1 in `ls -1 rec_*.txt`
do
	i=`ls -1 rec_*.txt | grep -n $f1 | awk -F":" '{print $1+1}'`
	for f2 in `ls -1 rec_*.txt | tail -n +$i`
	do
		echo $f1 $f2
		PCC_fullpair_1b_cuda $f1 $f2 tl1=-59 tl2=59 cc1b isac osac clip v=2
		break
	done
	break
done

)
