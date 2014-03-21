#---------------------------------------------------------------------------------------------------
# Title: Portage Community Schools Automated AD Import from IC Export
# Description: Script will read an exported CSV from IC, separate the users by school, 
# compile a batch script for each school of DSADD USER commands to add users to AD, as well 
# as generate a log for each school that updates itself with new users upon execution of the script
# Written by: Ed Karwacki, Technology Specialist, Portage Community Schools
# Date: 2/24/2014
#---------------------------------------------------------------------------------------------------

import array, csv, time, datetime


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

class C:
    # check what school the user is in and place them in the correct OU
    def checkSchool(self, mySchool, myGrade):
        s=','
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
    # check what school the user is in and place them in the correct security group
    def checkSecurityGroup(self, mySchool):
        s=', no security'
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
    # check what school the user is in and give them the correct path to their home drive
    def checkHomeDrive(self, mySchool, myGrade, myUsername):
        s=', no homedrive'
        if mySchool == 'Rusch Elementary':
            s= '\\\\rusch-dc01.portage.k12.wi.us\\homeDir-Rusch\\Students\\'+myUsername
        elif mySchool == 'John Muir Elementary':
            s= '\\\\muir-dc01.portage.k12.wi.us\\homeDir\\'+myUsername
        elif mySchool == "Wayne E. Bartels Middle School":
            s= '\\\\bms-dc01.portage.k12.wi.us\\homeDir\\Students\\'+myGrade+'\\'+myUsername
        elif mySchool == 'Portage High School':
            s= '\\\\phs-fs.portage.k12.wi.us\\homeDir-PHS\\Students\\'+myGrade+'\\'+myUsername
        elif mySchool == 'Portage Academy':
            s= '\\\\rusch-dc01.portage.k12.wi.us\\homeDir-Rusch\\Students\\'+myUsername
        return s
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

    def checkODgroup(self, mySchool):
        if mySchool == 'Lewiston Elementary':
            return "1026"
        else:
            return "1027"

    def checkODhome(self, mySchool):
        if mySchool == 'Lewiston Elementary':
            return "/Network/Servers/lew.portage.k12.wi.us/Shared Items/student3_docs/"
        else:
            return "/Network/Servers/end.portage.k12.wi.us/Shared Items/endstudent/"
# define vars
users=[]
c=C()

# read IC export 
with open('AD Extract.csv', 'rU') as f:
    reader = csv.reader(f)
    for row in reader:
        this_instance=user(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        users.append(this_instance)

# open batch script files to write to
hs=open('Batches/Import_Scripts/HS_ADimport.bat', 'w+')
ms=open('Batches/Import_Scripts/MS_ADimport.bat', 'w+')
m=open('Batches/Import_Scripts/Muir_ADimport.bat', 'w+')
r=open('Batches/Import_Scripts/Rusch_ADimport.bat', 'w+')
e=open('Batches/Import_Scripts/Endeavor_ODimport.sh', 'w+')
l=open('Batches/Import_Scripts/Lewiston_ODimport.sh', 'w+')
w=open('Batches/Import_Scripts/Woodridge_ADimport.bat', 'w+')
paa=open('Batches/Import_Scripts/PAA_ADimport.bat', 'w+')

# open log files to write to
lhs=open('Logs/HS_AD_Log.txt', 'a+')
lms=open('Logs/MS_AD_log.txt', 'a+')
lm=open('Logs/Muir_AD_log.txt', 'a+')
lr=open('Logs/Rusch_AD_log.txt', 'a+')
le=open('Logs/Endeavor_OD_log.txt', 'a+')
ll=open('Logs/Lewiston_OD_log.txt', 'a+')
lw=open('Logs/Woodridge_AD_log.txt', 'a+')
lpaa=open('Logs/PAA_AD_log.txt', 'a+')

hdhs=open('Batches/H_Drives/H_HS_ADimport.bat', 'w+')
hdms=open('Batches/H_Drives/H_MS_ADimport.bat', 'w+')
hdm=open('Batches/H_Drives/H_Muir_ADimport.bat', 'w+')
hdr=open('Batches/H_Drives/H_Rusch_ADimport.bat', 'w+')
hdw=open('Batches/H_Drives/H_Woodridge_ADimport.bat', 'w+')
hdpaa=open('Batches/H_Drives/H_PAA_ADimport.bat', 'w+')

# initalize logs with current timestamp
ts=time.time()
st=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

lhs.write('---------------- ')
lhs.write(st)
lhs.write(' ----------------\n')

lms.write('---------------- ')
lms.write(st)
lms.write(' ----------------\n')

lm.write('---------------- ')
lm.write(st)
lm.write(' ----------------\n')

lr.write('---------------- ')
lr.write(st)
lr.write(' ----------------\n')

le.write('---------------- ')
le.write(st)
le.write(' ----------------\n')

ll.write('---------------- ')
ll.write(st)
ll.write(' ----------------\n')

lw.write('----------------' )
lw.write(st)
lw.write(' ----------------\n')

lpaa.write('---------------- ')
lpaa.write(st)
lpaa.write(' ----------------\n')

test=open('test.txt', 'a+')

# determine what school the user is in and assign the appropriate log and batch script
for x in range(1,len(users)):
    if users[x].school == 'Lewiston Elementary' or users[x].school == 'Endeavor Elementary' or users[x].school == 'Rusch Elementary' or users[x].school == 'John Muir Elementary' or users[x].school == 'Wayne E. Bartels Middle School' or users[x].school == 'Portage High School' or users[x].school == 'Portage Academy':
        test.write(users[x].school+'\n')

        if users[x].school == 'Portage High School':
            f=hs
            log=lhs
            hd=hdhs
        elif users[x].school == 'Wayne E. Bartels Middle School':
            f=ms
            log=lms
            hd=hdms
        elif users[x].school == 'John Muir Elementary':
            f=m
            log=lm
            hd=hdm
        elif users[x].school == 'Rusch Elementary':
            f=r
            log=lr
            hd=hdr
        elif users[x].school == 'Portage Academy':
            f=paa
            log=lpaa
            hd=hdpaa
        elif users[x].school == 'Lewiston Elementary':
            f=l
            log=ll
        elif users[x].school == 'Endeavor Elementary':
            f=e
            log=le


# write the line in the batch script
        gy = c.gradYear(users[x].grade)
        if users[x].school != 'Lewiston Elementary' and users[x].school != 'Endeavor Elementary' and users[x].grade != 'KG' and users[x].grade != 'K4' and users[x].grade != '1' and users[x].grade != '2':
            f.write('dsadd user \"CN=')
            f.write(users[x].firstname+' '+users[x].lastname)
            f.write(c.checkSchool(users[x].school, gy)) 
            f.write(',DC=portage,DC=k12,DC=wi,DC=us\"')
            f.write(' -fn ')
            f.write(users[x].firstname)
            f.write(' -ln ')
            f.write(users[x].lastname)
            f.write(' -samid ')
            f.write(users[x].username)
            f.write(' -display ')
            f.write('\"'+users[x].firstname+' '+users[x].lastname+'\"')
            f.write(' -pwd ')
            f.write(users[x].password)
            f.write(' -email ')
            f.write(users[x].username)
            f.write('@portage.k12.wi.us ')
            f.write(' -upn ')
            f.write(users[x].username)
            f.write('@portage.k12.wi.us ')
            f.write('-disabled no -canchpwd no -pwdneverexpires yes ')
            f.write(c.checkSecurityGroup(users[x].school))
            f.write('-hmdir ')
            f.write(c.checkHomeDrive(users[x].school, gy, users[x].username))
            f.write(' -hmdrv h:')
            f.write(' -desc \"')
            f.write(gy)
            f.write(' '+users[x].startdate)
            f.write('\"\n')
            hd.write('mkdir ')
            hd.write(c.checkHomeDrive(users[x].school,gy,users[x].username))
            hd.write('\n')
        elif users[x].school == 'Lewiston Elementary' or users[x].school == 'Endeavor Elementary':
            f.write('. /etc/rc.common\n')
            f.write('dscl . create /Users/'+users[x].username+'\n')
            f.write('dscl . create /Users/'+users[x].username+' RealName \"' + users[x].firstname +' '+users[x].lastname+'\"\n')
            f.write('dscl . passwd /Users/'+users[x].username+' '+users[x].password+'\n')
            f.write('dscl . create /Users/'+users[x].username+' UniqueID 1'+users[x].stuid+'\n')
            f.write('dscl . create /Users/'+users[x].username+' PrimaryGroupID '+c.checkODgroup(users[x].school)+'\n')
            f.write('dscl . create /Users/'+users[x].username+' UserShell /bin/bash\n')
            f.write('dscl . create /Users/'+users[x].username+' NFSHomeDirectory ' + c.checkODhome(users[x].school) + users[x].username+'\n')
            f.write('\n')




# write the line in the log
        log.write(users[x].firstname)
        log.write(' ')
        log.write(users[x].lastname)
        log.write(' - ')
        log.write(gy)
        log.write('\n')
# close the batch scripts and logs    
    hd.close()
    f.close()
    log.close()


