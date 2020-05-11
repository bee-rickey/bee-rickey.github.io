/usr/local/mysql-8.0.20-macos10.15-x86_64/bin/mysql -u root -p'root1234' --local-infile=1 << EOF 
use covid19;
SET GLOBAL local_infile=1;
truncate rawdata;
truncate rawdata_unified;

load data local infile 'data/rawdata.csv' into table rawdata fields terminated by "," ENCLOSED BY '"' lines terminated by "\n" ;


insert into covid19.\`rawdata_unified\` (\`Date Announced\`,  \`Age Bracket\`, \`Gender\`, \`Detected City\`,
  \`Detected District\`,
  \`Detected State\`,
  \`State code\`,
  \`current status\`,
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
  \`Source_3\`, \`num cases\`, 'v1v2' from covid19.\`rawdata\` ;

update rawdata_unified set \`current status\` = 'Hospitalized';
update rawdata_unified set \`num cases\` = 1 where \`num cases\` = 0;


EOF
