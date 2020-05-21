curl --location --request OPTIONS 'https://services5.arcgis.com/h1qecetkQkV9PbPV/arcgis/rest/services/COVID19_Location_Summary/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*' | jsonpp | grep -i "District\"\|Positive\|Death\|Recovered" > mh_portal.data
curl https://api.covid19india.org/csv/latest/district_wise.csv | grep 'Maharashtra' > current_mh.data 

while read line 
do
	key=`echo $line | cut -d: -f1 | sed -e 's/\"//g'`
	value=`echo $line | cut -d: -f2 | sed -e 's/,//g' | sed -e "s/\"//g"`

	case $key in

	"District")
		currentDistrict=`echo $value`

		if [ "$currentDistrict" == "Ahmadnagar" ]
		then
			currentDistrict="Ahmednagar"
		fi

		currentDistrictData=`grep "$currentDistrict" current_mh.data`

		currentPositive=`echo $currentDistrictData | awk -F, '{print $6}'`
		currentRecovered=`echo $currentDistrictData | awk -F, '{print $8}'`
		currentDeaths=`echo $currentDistrictData | awk -F, '{print $9}'`

    ;;
 	"Death")
		deltaDeaths=$(( value - currentDeaths))
    ;;
 	"Positive")
		deltaPositive=$(( value - currentPositive))
    ;;

 	"Recovered")
		deltaRecovered=$(( value - currentRecovered))
		echo "$currentDistrict, $deltaPositive, $deltaRecovered, $deltaDeaths"
		deltaDeath=0
		deltaPositive=0
		deltaRecovered=0
		currentDistrict=0
		currentPositive=0
		currentRecovered=0
		currentDeaths=0
    ;;
esac

done < mh_portal.data
