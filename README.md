# ADSync
Active Directory account auto import from Infinite Campus export


Python script that reads in a csv file of new students and/or staff enrolled that day, converts the data for each user into a class,
and uses a variety of methods and static variables to create batch and powershell scripts that add users to appropriate OU's in Active Directory, 
set a randomly generated password, log into a Google Doc and store the username and password for IT use, put users in correct security groups, 
set all other user account attributes, create a powershell script to create user homedrives with approrpriate permissions on a file server, and
create a log file with timestamp that records each days new additions.  This was automated using task schedulers, first to schedule the 
CSV export from our Student Information System to a local drive, then the python script was scheduled to use the new csv and process the 
appropriate scripts, then the scripts were scheduled to run soon after and add our new users.

