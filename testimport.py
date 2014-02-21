import array, csv, time, datetime

class user(object):
    def __init__(self, lastname, firstname, grade, school, username, password, stuid):
        self.lastname=lastname
        self.firstname=firstname
        self.grade=grade
        self.school=school
        self.username=username
        self.password=password
        self.stuid=stuid

class C:
    def checkSchool(self, mySchool, myGrade):
        s=', no school'
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
    def checkHomeDrive(self, mySchool, myGrade, myUsername):
        s=', no homedrive'
        if mySchool == 'Rusch Elementary':
            s= '-hmdir \\\\rusch-dc01.portage.k12.wi.us\\homeDir-Rusch\\Students\\'+myUsername
        elif mySchool == 'John Muir Elementary':
            s= '-hmdir \\\\muir-dc01.portage.k12.wi.us\\homeDir\\'+myUsername
        elif mySchool == "Wayne E. Bartels Middle School":
            s= '-hmdir \\\\bms-dc01.portage.k12.wi.us\\homeDir\\Students\\'+myGrade+'\\'+myUsername
        elif mySchool == 'Portage High School':
            s= '-hmdir \\\\phs-fs.portage.k12.wi.us\\homeDir-PHS\\Students\\'+myGrade+'\\'+myUsername
        elif mySchool == 'Portage Academy':
            s= '-hmdir \\\\rusch-dc01.portage.k12.wi.us\\homeDir-Rusch\\Students\\'+myUsername
        return s

    def gradYear(self, myGrade):
        myGrade = int(myGrade)
        d = datetime.date.today()
        if d.month == 01 or d.month == 02 or d.month == 03 or d.month == 04 or d.month == 05:
            gradyear = d.year + (12 - myGrade)
        else:
            gradyear = d.year + (13 - myGrade)
        gradyear = str(gradyear)
        return gradyear

users=[]
c=C()

with open('adtest.csv', 'rU') as f:
    reader = csv.reader(f)
    for row in reader:
        this_instance=user(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        users.append(this_instance)

hs = open('Batches/HS_ADimport.bat', 'w+')
ms = open('Batches/MS_ADimport.bat', 'w+')
m = open('Batches/Muir_ADimport.bat', 'w+')
r = open('Batches/Rusch_ADimport.bat', 'w+')
e = open('Batches/Endeavor_ODimport.bat', 'w+')
l = open('Batches/Lewiston_ODimport.bat', 'w+')
w = open('Batches/Woodridge_ADimport.bat', 'w+')
paa = open('Batches/PAA_ADimport.bat', 'w+')

lhs = open('Logs/HS_AD_Log.txt', 'a+')
lms = open('Logs/MS_AD_log.txt', 'a+')
lm = open('Logs/Muir_AD_log.txt', 'a+')
lr = open('Logs/Rusch_AD_log.txt', 'a+')
le = open('Logs/Endeavor_OD_log.txt', 'a+')
ll = open('Logs/Lewiston_OD_log.txt', 'a+')
lw = open('Logs/Woodridge_AD_log.txt', 'a+')
lpaa = open('Logs/PAA_AD_log.txt', 'a+')

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

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

for x in range(1,len(users)):
    if users[x].school == 'Portage High School':
        f = hs
        log = lhs
    elif users[x].school == 'Wayne E. Bartels Middle School':
        f = ms
        log = lms
    elif users[x].school == 'John Muir Elementary':
        f = m
        log = lm
    elif users[x].school == 'Rusch Elementary':
        f = r
        log = lr
    elif users[x].school == 'Portage Acadmey':
        f = paa
        log = lpaa
    elif users[x].school == 'Lewiston Elementary':
        f = l
        log = ll
    elif users[x].school == 'Endeavor Elementary':
        f = e
        log = le



    
    f.write('dsadd user \"CN=')
    f.write(users[x].username)
    f.write(c.checkSchool(users[x].school, users[x].grade)) 
    f.write(',DC=portage,DC=k12,DC=wi,DC=us\"')
    f.write(' -fn ')
    f.write(users[x].firstname)
    f.write(' -ln ')
    f.write(users[x].lastname)
    f.write(' -pwd ')
    f.write(users[x].password)
    f.write(' -email ')
    f.write(users[x].username)
    f.write('@portage.k12.wi.us ')
    f.write('-disabled no -canchpwd no -pwdneverexpires yes ')
    f.write(c.checkSecurityGroup(users[x].school))
    f.write(c.checkHomeDrive(users[x].school, users[x].grade, users[x].username))
    f.write(' -hmdrv h:')
    f.write(' -desc ')
    f.write(c.gradYear(users[x].grade))
    f.write('\n')
    log.write(users[x].firstname)
    log.write(' ')
    log.write(users[x].lastname)
    log.write(' ')
    log.write(users[x].grade)
    log.write('\n')
f.close()
log.close()


