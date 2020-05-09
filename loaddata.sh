/usr/local/mysql-8.0.20-macos10.15-x86_64/bin/mysql  -s -u root -p'root1234' --local-infile=1 << EOF > data/groupby.csv
use covid19;
SET GLOBAL local_infile=1;
#truncate rawdata3;
#load data local infile 'data/rawdata3.csv' into table rawdata3 fields terminated by "," lines terminated by "\n" ;


delete from rawdata_unified where \`sheet version\` = 'v3';

insert into covid19.\`rawdata_unified\` (\`Date Announced\`,  \`Age Bracket\`, \`Gender\`, \`Detected City\`,
  \`Detected District\`,
  \`Detected State\`,
  \`State code\`,
  \`Current Status\`,
  \`Contracted from which Patient (Suspected)\`,
  \`Source_1\`,
  \`Source_2\`,
  \`Source_3\`,
  \`Num cases\`, \`sheet version\`) select \`Date Announced\`,  \`Age Bracket\`, \`Gender\`,
  \`Detected City\`,
  \`Detected District\`,
  \`Detected State\`,
  \`State code\`,
  \`Current Status\`,
  \`Contracted from which Patient (Suspected)\`,
  \`Source_1\`,
  \`Source_2\`,
  \`Source_3\`, \`Num cases\`, 'v3' from covid19.\`rawdata3\` ;


select sum(\`num cases\`), \`detected district\`, \`detected state\` 
from rawdata_unified 
where \`current status\` = 'Hospitalized' 
group by \`detected district\`, \`detected state\`
order by \`detected state\`;

EOF

sed -i.orig 's/	/,/g' data/groupby.csv 
