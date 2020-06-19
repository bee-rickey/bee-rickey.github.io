BEGIN{
	count=1;
	recordId=1;
}
{
	if(NR == 1){
		print "Patient Number,recordId,num cases,State Patient Number,Date Announced,Estimated Onset Date,Age Bracket,Gender,Detected City,Detected District,Detected State,State code,Current Status,Notes,Contracted from which Patient (Suspected),Nationality,Type of transmission,Status Change Date,Source_1,Source_2,Source_3,Backup Notes"
	}
		
	patientId=$1;

	sub("^[0-9]+,", "patientId,recordId,num_cases,", $0);
	if(NR > 2)
	{
		if(prev == $0){
			count++ ;
		}else{
			sub("^patientId", prevPatientId, prev);
			sub("recordId", recordId, prev);
			sub("num_cases", count, prev);
			print prev;
			recordId++;
			count=1;
		}
	}
	{
		prev=$0;
		prevPatientId=patientId;
	}
}
END{
	sub("^patientId", patientId, prev);
	sub("recordId", recordId, prev);
	sub("num_cases", count, prev);
	print prev
}
