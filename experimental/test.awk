BEGIN{
	prev=""
	truthFlag=0;
	resetState=1;
	appendLine=1;
}
{

	if($0 ~ /\[/) {
		district=$0;
		if(resetState == 1)
			state=prev;
	}

	if($0 ~ ".*active.*" || $0 ~ ".*notes.*") {
		combinedLine=state district $0;
	} else{
		combinedLine=combinedLine $0;
		if($0 ~ ".*date.*"){
			print combinedLine;
		}
	}

	if($0 ~ /\]/) {
		district="";
		resetState=0
   	}
    if($0 ~ /\}/){
		if(prev ~ /\]/) {
			state="";
			resetState=1;
		}
	}

}   
{
	prev=$0
}
