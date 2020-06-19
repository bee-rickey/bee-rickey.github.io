curl https://api.covid19india.org/csv/latest/district_wise.csv | grep "Uttar Pradesh" > up.csv
while read line 
do
	confirmed=`echo $line | cut -d"," -f2`
	recovered=`echo $line | cut -d"," -f3`
	deaths=`echo $line | cut -d"," -f4`
	city=`echo $line | cut -d"," -f1`

	matched=`grep "$city" up.csv`

	confirmedYesterday=`echo $matched | cut -d"," -f6`
	recoveredYesterday=`echo $matched | cut -d"," -f8`
	deathsYesterday=`echo $matched | cut -d"," -f9`

	deltaconfirmed=$(( confirmed - confirmedYesterday ))
	deltarecovered=$(( recovered - recoveredYesterday ))
	deltadeaths=$(( deaths - deathsYesterday ))

	echo "$city, $deltaconfirmed, $deltarecovered, $deltadeaths"

done < today.txt
