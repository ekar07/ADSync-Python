#---------------------------------------------------------------------------------------------------
# Title: Portage Community Schools Automated AD Import from IC Export
# Description: Script will read an exported CSV from IC, separate the users by school, 
# compile a batch script for each school of DSADD USER commands to add users to AD, as well 
# as generate a log for each school that updates itself with new users upon execution of the script
# Written by: Ed Karwacki, Technology Specialist, Portage Community Schools
# Date: 2/24/2014
#---------------------------------------------------------------------------------------------------

import array, csv, time, datetime#, gdata.spreadsheet.service

# Generic class to assign all user account information
class user(object):
    def __init__(self, lastname, firstname, grade, school, stuid, username, password, startdate):
        self.lastname=lastname
        self.firstname=firstname
        self.grade=grade
        self.school=school
        self.username=username
        self.password=password
        self.stuid=stuid
        self.startdate =startdate

# Generic class to assign all faculty user account information
class staff(object):
    def __init__(self, school, username, password, firstname, lastname, gender, staffnumber, startdate, title):
        self.school = school
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.staffnumber = staffnumber
        self.startdate = startdate
        self.title = title

# Generic class used to access methods
class C:

# check what school the student user is in and place them in the correct OU
    def checkSchool(self, mySchool, myGrade):
        if mySchool == 'Rusch Elementary':
            s= ',OU=R-Student,OU=RUSCH'
        elif mySchool == 'John Muir Elementary':
            s= ',OU='+myGrade+',OU=Student,ou=Muir'
        elif mySchool == "Woodridge Elementary": 
            s=',Woodridge'
        elif mySchool == "Wayne E. Bartels Middle School":
            s= ',OU=Student,OU=BMS'
        elif mySchool == 'Portage High School':
            s= ',OU='+myGrade+',OU=PHS'
        elif mySchool == 'Portage Academy':
            s= ',OU=R-Student,OU=RUSCH'
        return s
# check what school the faculty user is in and place them in the correct OU
    def checkFacultySchool(self, mySchool):
        if mySchool == 'Rusch Elementary':
            s= ',OU=R-Faculty,OU=RUSCH'
        elif mySchool == 'John Muir Elementary':
            s= ',OU=Faculty,OU=Muir'
        elif mySchool == "Woodridge Elementary": 
            s=',OU=Faculty,OU=PHS'
        elif mySchool == "Wayne E. Bartels Middle School":
            s= ',OU=Faculty,OU=BMS'
        elif mySchool == 'Portage High School':
            s= ',OU=Faculty,OU=PHS'
        elif mySchool == 'Portage Academy':
            s= ',OU=R-Faculty,OU=RUSCH'
        return s
# check what school the student is in and place them in the correct security group
    def checkSecurityGroup(self, mySchool):
        if mySchool == 'Rusch Elementary':
            s= '-memberof CN=Rusch-Stud-No-Sync,OU=RUSCH,DC=portage,DC=k12,DC=wi,DC=us '
        elif mySchool == 'John Muir Elementary':
            s= '-memberof CN=Stud-Group-for-Muir-WGM,OU=Muir,DC=portage,DC=k12,DC=wi,DC=us '
        elif mySchool == "Woodridge Elementary":
            s=',Woodridge'
        elif mySchool == "Wayne E. Bartels Middle School":
            s= '-memberof CN=Stud-Group-for-BMS-WGM,OU=BMS,DC=portage,DC=k12,DC=wi,DC=us '
        elif mySchool == 'Portage High School':
            s= '-memberof CN=HS-Stud-No-Sync,OU=PHS,DC=portage,DC=k12,DC=wi,DC=us '
        elif mySchool == 'Portage Academy':
            s= '-memberof CN=Rusch-Stud-No-Sync,OU=RUSCH,DC=portage,DC=k12,DC=wi,DC=us '
        return s
# check what school the student is in and place them in the correct security group
    def checkFacultySecurityGroup(self, mySchool):
        if mySchool == 'Rusch Elementary':
            s= '-memberof CN=Rusch-Fac-No-Sync,OU=RUSCH,DC=portage,DC=k12,DC=wi,DC=us '
        elif mySchool == 'John Muir Elementary':
            s= '-memberof CN=FAC-NO-SYNC-MUIR,OU=Muir,DC=portage,DC=k12,DC=wi,DC=us '
        elif mySchool == "Woodridge Elementary":
            s= '-memberof CN=Wood-Fac-No-Sync,OU=PHS,DC=portage,DC=k12,DC=wi,DC=us '
        elif mySchool == "Wayne E. Bartels Middle School":
            s= '-memberof CN=FAC-NO-SYNC,OU=BMS,DC=portage,DC=k12,DC=wi,DC=us '
        elif mySchool == 'Portage High School':
            s= '-memberof CN=HS-Fac-No-Sync,OU=PHS,DC=portage,DC=k12,DC=wi,DC=us '
        elif mySchool == 'Portage Academy':
            s= '-memberof CN=Rusch-Fac-No-Sync,OU=RUSCH,DC=portage,DC=k12,DC=wi,DC=us '
        return s
# check what school the user is in and give them the correct path to their home drive
    def checkHomeDrive(self, mySchool, myGrade, myUsername):
        if mySchool == 'Rusch Elementary':
            s= '\\\\rusch-dc01.portage.k12.wi.us\\homeDir-Rusch\\Students\\'+myUsername
        elif mySchool == 'John Muir Elementary':
            s= '\\\\muir-dc01.portage.k12.wi.us\\homeDir\\Students\\'+myUsername
        elif mySchool == "Wayne E. Bartels Middle School":
            s= '\\\\bms-dc01.portage.k12.wi.us\\homeDir\\Students\\'+myGrade+'\\'+myUsername
        elif mySchool == 'Portage High School':
            s= '\\\\phs-fs.portage.k12.wi.us\\homeDir-PHS\\Students\\'+myGrade+'\\'+myUsername
        elif mySchool == 'Portage Academy':
            s= '\\\\rusch-dc01.portage.k12.wi.us\\homeDir-Rusch\\Students\\'+myUsername
        return s
# check what school the user is in and give them the correct path to their home drive
    def checkFacultyHomeDrive(self, mySchool, myUsername):
        if mySchool == 'Rusch Elementary':
            s= '\\\\rusch-dc01.portage.k12.wi.us\\homeDir-Rusch\\Faculty\\'+myUsername
        elif mySchool == 'John Muir Elementary':
            s= '\\\\muir-dc01.portage.k12.wi.us\\homeDir\\Faculty\\'+myUsername
        elif mySchool == "Wayne E. Bartels Middle School":
            s= '\\\\bms-dc01.portage.k12.wi.us\\homeDir\\Faculty\\'+myUsername
        elif mySchool == 'Portage High School':
            s= '\\\\phs-fs.portage.k12.wi.us\\homeDir-PHS\\Faculty\\'+myUsername
        elif mySchool == 'Woodridge Elementary':
            s= '\\\\phs-fs.portage.k12.wi.us\\homeDir-PHS\\Faculty\\'+myUsername
        elif mySchool == 'Portage Academy':
            s= '\\\\rusch-dc01.portage.k12.wi.us\\homeDir-Rusch\\Faculty\\'+myUsername
        return s

# check what school the user is in and assign the google docs spreadsheet key for that school
    def checkGdocs(self, mySchool):
        if mySchool == 'Rusch Elementary':
            s= '0Ah0X0hy_gOmEdHMwQlVFOVgzUFlxelk1a2hrNWdlYkE'
        elif mySchool == 'John Muir Elementary':
            s= '0Ah0X0hy_gOmEdDllWTBNOVE1N1Q2M2poUXFoclhxZ3c'
        elif mySchool == "Wayne E. Bartels Middle School":
            s= '0Ah0X0hy_gOmEdEdVSVhzT0UtMDU5TThPNlk4RzJHcGc'
        elif mySchool == 'Portage High School':
            s= '0Ah0X0hy_gOmEdDlhNmlLck1OaFBEQWhibXlVVS1sRWc'
        elif mySchool == 'Portage Academy':
            s= '0Ah0X0hy_gOmEdDlhNmlLck1OaFBEQWhibXlVVS1sRWc'
        return s
# insert a row in the specific schools google password sheet
    def insertRow(self, lname, fname, myGrade, mySchool, myUsername, myPassword):
        dict = {}
        spreadsheet_key = c.checkGdocs(mySchool)
        worksheet_id = 'od6'
        spr_client = gdata.spreadsheet.service.SpreadsheetsService()
        spr_client.email = email
        spr_client.password = password
        spr_client.source = 'Example Spreadsheet Writing Application'
        spr_client.ProgrammaticLogin()

        if mySchool == 'Rusch Elementary':
            dict['LastName'] = users[x].lastname
            dict['FirstName'] = users[x].firstname
            dict['Grade'] = users[x].grade
            dict['Username'] = users[x].username
            dict['Password /part lunch pin'] = users[x].password
        elif mySchool == 'John Muir Elementary':
            dict['LastName'] = users[x].lastname
            dict['FirstName'] = users[x].firstname
            dict['Password'] = users[x].password
            dict['Login Username'] = users[x].username
            dict['Grade'] = users[x].grade
        elif mySchool == "Wayne E. Bartels Middle School":
            dict['LastName'] = users[x].lastname
            dict['FirstName'] = users[x].firstname
            dict['Password'] = users[x].password
            dict['Login Username'] = users[x].username
            dict['Grade'] = users[x].grade
        elif mySchool == 'Portage High School':
            dict['LastName'] = users[x].lastname
            dict['FirstName'] = users[x].firstname
            dict['Password'] = users[x].password
            dict['Username'] = users[x].username
            dict['Class year'] = users[x].grade
        elif mySchool == 'Portage Academy':
            dict['LastName'] = users[x].lastname
            dict['FirstName'] = users[x].firstname
            dict['Password'] = users[x].password
            dict['Username'] = users[x].username
            dict['Class year'] = users[x].grade
        spr_client.InsertRow(dict, spreadsheet_key, worksheet_id)

# check the user's grade and return what year they graduate
    def gradYear(self, myGrade):
        if myGrade == 'KG' or myGrade == 'K4':
            myGrade = '0'
        myGrade = int(myGrade)
        d = datetime.date.today()
        y = int(d.year)
        m = int(d.month)
        g = int(myGrade)
        if m == 1 or m == 2 or m == 3 or m == 4 or m == 5:
            gy = y + (12 - myGrade)
        else:
            gy = y + (13 - myGrade)

        gy = str(gy)
        return gy
# check the users's school and assign the appropriate OD group value
    def checkODgroup(self, mySchool):
        if mySchool == 'Lewiston Elementary':
            return "1026"
        else:
            return "1027"
# check the user's school and assign the appropriate home directory location
    def checkODhome(self, mySchool):
        if mySchool == 'Lewiston Elementary':
            return "/Network/Servers/lew.portage.k12.wi.us/Shared Items/student3_docs/"
        else:
            return "/Network/Servers/end.portage.k12.wi.us/Shared Items/endstudent/"
            # define vars
users=[]
faculty=[]
c=C()
email = 'pcstechdrive@portage.k12.wi.us'
password = '3o1Collins'
# open batch script files to write to
bat=open('..\Batches\ADimport.bat', 'w+')
# open log files to write to
masterlog=open('..\Logs\MASTER_LOG.txt', 'a+')
# open homedrive creation batches
hd=open('..\Batches\homedrive.ps1', 'w+')
# initalize logs with current timestamp
ts=time.time()
st=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
masterlog.write('---------------- ')
masterlog.write(st)
masterlog.write(' ----------------\n')
masterlog.write('       --- STUDENTS ---       \n')


# read student IC export 
with open('..\AD Extract.csv', 'rU') as f:
    reader = csv.reader(f)
    for row in reader:
        this_instance=user(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
        users.append(this_instance)
# determine what school the user is in and assign the appropriate log and batch script
for x in range(1,len(users)):
    if users[x].school == 'Lewiston Elementary' or users[x].school == 'Endeavor Elementary' or users[x].school == 'Rusch Elementary' or users[x].school == 'John Muir Elementary' or users[x].school == 'Wayne E. Bartels Middle School' or users[x].school == 'Portage High School' or users[x].school == 'Portage Academy':
# write the line in the batch script
        gy = c.gradYear(users[x].grade)
        if users[x].school != 'Lewiston Elementary' and users[x].school != 'Endeavor Elementary' and users[x].grade != 'KG' and users[x].grade != 'K4' and users[x].grade != '1' and users[x].grade != '2':
            bat.write('dsadd user \"CN=')
            bat.write(users[x].firstname+' '+users[x].lastname)
            bat.write(c.checkSchool(users[x].school, gy)) 
            bat.write(',DC=portage,DC=k12,DC=wi,DC=us\"')
            bat.write(' -fn ')
            bat.write(users[x].firstname)
            bat.write(' -ln ')
            bat.write(users[x].lastname)
            bat.write(' -samid ')
            bat.write(users[x].username)
            bat.write(' -display ')
            bat.write('\"'+users[x].firstname+' '+users[x].lastname+'\"')
            bat.write(' -pwd ')
            bat.write(users[x].password)
            bat.write(' -email ')
            bat.write(users[x].username)
            bat.write('@portage.k12.wi.us ')
            bat.write(' -upn ')
            bat.write(users[x].username)
            bat.write('@portage.k12.wi.us ')
            bat.write('-disabled no -canchpwd no -pwdneverexpires yes ')
            bat.write(c.checkSecurityGroup(users[x].school))
            bat.write('-hmdir ')
            bat.write(c.checkHomeDrive(users[x].school, gy, users[x].username))
            bat.write(' -hmdrv h:')
            bat.write(' -desc \"')
            bat.write(gy)
            bat.write(' '+users[x].startdate)
            bat.write('\"\n\n')
            hd.write('New-Item -itemType directory -Path ')
            hd.write(c.checkHomeDrive(users[x].school,gy,users[x].username))
            hd.write('\n$acl = Get-Acl ')
            hd.write(c.checkHomeDrive(users[x].school,gy,users[x].username))
            hd.write('\n$permission = \"PORTAGE\\'+users[x].username+'\",\"FullControl\",\"ContainerInherit, ObjectInherit\",\"None\",\"Allow\"\n')
            hd.write('$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission\n')
            hd.write('$acl.SetAccessRule($accessRule)\n')
            hd.write('$acl | Set-Acl ')
            hd.write(c.checkHomeDrive(users[x].school,gy,users[x].username))
            hd.write('\n\n')
        elif users[x].school == 'Lewiston Elementary' or users[x].school == 'Endeavor Elementary':
            bat.write('. /etc/rc.common\n')
            bat.write('dscl . create /Users/'+users[x].username+'\n')
            bat.write('dscl . create /Users/'+users[x].username+' RealName \"' + users[x].firstname +' '+users[x].lastname+'\"\n')
            bat.write('dscl . passwd /Users/'+users[x].username+' '+users[x].password+'\n')
            bat.write('dscl . create /Users/'+users[x].username+' UniqueID 1'+users[x].stuid+'\n')
            bat.write('dscl . create /Users/'+users[x].username+' PrimaryGroupID '+c.checkODgroup(users[x].school)+'\n')
            bat.write('dscl . create /Users/'+users[x].username+' UserShell /bin/bash\n')
            bat.write('dscl . create /Users/'+users[x].username+' NFSHomeDirectory ' + c.checkODhome(users[x].school) + users[x].username+'\n')
            bat.write('\n\n')

        #write the line in the master log
        masterlog.write(users[x].firstname)
        masterlog.write(' ')
        masterlog.write(users[x].lastname)
        masterlog.write(' - ')
        masterlog.write(users[x].school)
        masterlog.write(' - ')
        masterlog.write(gy)
        masterlog.write('\n')
'''
        #Open the Google Doc password spreadsheet
        spreadsheet_key = c.checkGdocs(users[x].school)

        worksheet_id = 'od6'
        #Login to the spreadsheet
        spr_client = gdata.spreadsheet.service.SpreadsheetsService()
        spr_client.email = email
        spr_client.password = password
        spr_client.source = 'Example Spreadsheet Writing Application'
        spr_client.ProgrammaticLogin()
        # Prepare the dictionary to write
        dict = {}
        dict['lastname'] = users[x].lastname
        dict['firstname'] = users[x].firstname
        dict['grade'] = users[x].grade
        dict['username'] = users[x].username
        dict['password'] = users[x].password
        #Insert the row into the spreadsheet
        entry = spr_client.InsertRow(dict, spreadsheet_key, worksheet_id)
        if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
            print "Insert row succeeded."
        else:
            print "Insert row failed."
'''        

#Prep Master Log for Faculty accounts
masterlog.write('       --- FACULTY ---       \n')
# process faculty accounts
with open('..\Faculty.csv', 'rU') as f:
    reader = csv.reader(f)
    for row in reader:
        this_instance=staff(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        faculty.append(this_instance)
for x in range(1,len(faculty)):
    if faculty[x].title != 'Summer School Teacher':
        if faculty[x].school != 'Lewiston Elementary' and faculty[x].school != 'Endeavor Elementary':
            bat.write('dsadd user \"CN=')
            bat.write(faculty[x].firstname+' '+faculty[x].lastname)
            bat.write(c.checkFacultySchool(faculty[x].school)) 
            bat.write(',DC=portage,DC=k12,DC=wi,DC=us\"')
            bat.write(' -fn ')
            bat.write(faculty[x].firstname)
            bat.write(' -ln ')
            bat.write(faculty[x].lastname)
            bat.write(' -samid ')
            bat.write(faculty[x].username)
            bat.write(' -display ')
            bat.write('\"'+faculty[x].firstname+' '+faculty[x].lastname+'\"')
            bat.write(' -pwd ')
            bat.write(faculty[x].password)
            bat.write(' -email ')
            bat.write(faculty[x].username)
            bat.write('@portage.k12.wi.us ')
            bat.write(' -upn ')
            bat.write(faculty[x].username)
            bat.write('@portage.k12.wi.us ')
            bat.write('-disabled no -canchpwd no -pwdneverexpires yes ')
            bat.write(c.checkFacultySecurityGroup(faculty[x].school))
            bat.write('-hmdir ')
            bat.write(c.checkFacultyHomeDrive(faculty[x].school, faculty[x].username))
            bat.write(' -hmdrv h:')
            bat.write(' -desc \"')
            bat.write(faculty[x].title)
            bat.write(' '+faculty[x].startdate)
            bat.write('\"\n\n')
            hd.write('New-Item -itemType directory -Path ')
            hd.write(c.checkFacultyHomeDrive(faculty[x].school, faculty[x].username))
            hd.write('\n$acl = Get-Acl ')
            hd.write(c.checkFacultyHomeDrive(faculty[x].school, faculty[x].username))
            hd.write('\n$permission = \"PORTAGE\\'+faculty[x].username+'\",\"FullControl\",\"ContainerInherit, ObjectInherit\",\"None\",\"Allow\"\n')
            hd.write('$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission\n')
            hd.write('$acl.SetAccessRule($accessRule)\n')
            hd.write('$acl | Set-Acl ')
            hd.write(c.checkFacultyHomeDrive(faculty[x].school, faculty[x].username))
            hd.write('\n\n')
        elif faculty[x].school == 'Lewiston Elementary' or faculty[x].school == 'Endeavor Elementary':
            bat.write('. /etc/rc.common\n')
            bat.write('dscl . create /Users/'+faculty[x].username+'\n')
            bat.write('dscl . create /Users/'+users[x].username+' RealName \"' + users[x].firstname +' '+users[x].lastname+'\"\n')
            bat.write('dscl . passwd /Users/'+users[x].username+' '+users[x].password+'\n')
            bat.write('dscl . create /Users/'+users[x].username+' UniqueID 1'+users[x].stuid+'\n')
            bat.write('dscl . create /Users/'+users[x].username+' PrimaryGroupID '+c.checkODgroup(users[x].school)+'\n')
            bat.write('dscl . create /Users/'+users[x].username+' UserShell /bin/bash\n')
            bat.write('dscl . create /Users/'+users[x].username+' NFSHomeDirectory ' + c.checkODhome(users[x].school) + users[x].username+'\n')
            bat.write('\n')

# close the batch scripts and logs  
hd.close()
f.close()
masterlog.close() 