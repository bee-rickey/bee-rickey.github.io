#curl "https://docs.google.com/spreadsheets/d/e/2PACX-1vQW1sf6ptHC1I4vLmEI6kddb_2C1T3x4062y7NFn8s_G0rq0_c7RvtHcRDpohA8hkNQxIFRy6H4OIdJ/pub?gid=1857317333&single=true&output=csv"  | grep -v "^," > data/siva.csv
#curl https://api.covid19india.org/csv/latest/district_wise.csv > data/districtwise.csv
#curl https://api.covid19india.org/csv/latest/raw_data1.csv > data/rawdata1.csv
#curl https://api.covid19india.org/csv/latest/raw_data2.csv > data/rawdata2.csv
#curl https://api.covid19india.org/csv/latest/raw_data3.csv > data/rawdata3.csv

>data/matching.txt
>data/notMatching.txt
>notMatching.html
>data/notfound.txt
>data/notMatching.txt.tmp
>data/notMatching.tmp

prevState="gloglog"
districtCount=1
var=0

while read line
do
	district=`echo $line | awk -F, '{print $2}'`
	state=`echo $line | awk -F, '{print $1}'`
	echo "0" > data/.found
	if [ "$prevState" != "$state" ]
	then
		echo "<h2> $state </h2>" >> data/notMatching.tmp
		prevState=`echo $state`
	fi

    if [ -z "${district}" ]
	then
		continue;
	fi

	grep -i "$state" data/districtwise.csv | while read -r matched; do 
		if [ -n "${district}" ]
		then
			districtNameFromDistrictWise=`echo $matched | awk -F, '{print $5}'`
			if [ "$districtNameFromDistrictWise" == "$district" ]
			then
				echo "1" > data/.found
				confirmedCountFromDistrictWise=`echo $matched | awk -F, '{print $6}'`
				confirmedCountFromSiva=`echo $line | awk -F, '{print $5}'`

                if [ $confirmedCountFromDistrictWise != $confirmedCountFromSiva ]
				then
					
					districtString="<a href=\"#$district\"> $district count does not match $confirmedCountFromSiva:$confirmedCountFromDistrictWise    ";
					echo "$district count does not match $confirmedCountFromSiva:$confirmedCountFromDistrictWise" >> data/notMatching.txt.tmp

					echo "<h2 id=\"$district\">$district</h2>" >> data/notMatching.txt

					> data/.notMatching.txt
					grep -i "$district" data/rawdata1.csv >> data/.notMatching.txt
					countForVersion=`wc -l < data/.notMatching.txt | bc`
	   				echo "<h3>RAW DATA V1 : Total Count: $countForVersion </h3>:<br>" >> data/notMatching.txt
					cat data/.notMatching.txt >> data/notMatching.txt
					districtString="$districtString V1: $countForVersion,";
						

					> data/.notMatching.txt
					grep -i "$district" data/rawdata2.csv >> data/.notMatching.txt
					countForVersion=`wc -l < data/.notMatching.txt | bc`
	   				echo "<h3>RAW DATA V2 : Total Count: $countForVersion </h3>:<br>" >> data/notMatching.txt
					cat data/.notMatching.txt >> data/notMatching.txt
					districtString="$districtString V2: $countForVersion";

   					echo "<h3>RAW DATA V3</h3><br>" >> data/notMatching.txt
   					grep -i "$district" data/rawdata3.csv >> data/notMatching.txt

					districtString="$districtString </a><br>";
					echo $districtString >> data/notMatching.tmp

				else
					echo "$district count does not match $confirmedCountFromSiva:$confirmedCountFromDistrictWise" >> data/matching.txt
				fi
			break;
			fi
		fi
	done

	districtFound=`cat data/.found`
	if (( $districtFound == 0 ))
	then
		message="$district Not found in districtwise.csv." 
		grep $district data/rawdata1.csv > /dev/null 2>&1 
		if (( $? == 0 ))
		then
			message="$message Present in raw_data1.csv"
		fi

		grep $district data/rawdata2.csv > /dev/null 2>&1 
		if (( $? == 0 ))
		then
			message="$message Present in raw_data2.csv"
		fi

		echo $message >> data/notfound.txt
	fi


done < data/siva.csv

districtCount=`grep "count does not match" data/notMatching.tmp | wc -l`

echo "<html> " >> notMatching.html
echo "	<body> " >> notMatching.html
echo "<h2> Number of districts having mismatches in count: $districtCount </h2> <br>" >> notMatching.html
cat data/notMatching.tmp >> notMatching.html
sed 's/$/ <br>/' data/notMatching.txt >> notMatching.html
echo "	</body> " >> notMatching.html
echo "</html> " >> notMatching.html
