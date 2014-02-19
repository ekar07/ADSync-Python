import array, csv

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




users=[]
c=C()

with open('adtest.csv', 'rU') as f:
    reader = csv.reader(f)
    for row in reader:
        this_instance=user(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        users.append(this_instance)

hs = open('HS_ADimport.bat', 'w+')
ms = open('MS_ADimport.bat', 'w+')
m = open('Muir_ADimport.bat', 'w+')
r = open('Rusch_ADimport.bat', 'w+')
e = open('Endeavor_ODimport.bat', 'w+')
l = open('Lewiston_ODimport.bat', 'w+')
w = open('Woodridge_ADimport.bat', 'w+')
paa = open('PAA_ADimport.bat', 'w+')

for x in range(1,len(users)):
    if users[x].school == 'Portage High School':
        f = hs
    elif users[x].school == 'Wayne E. Bartels Middle School':
        f = ms
    elif users[x].school == 'John Muir Elementary':
        f = m
    elif users[x].school == 'Rusch Elementary':
        f = r
    elif users[x].school == 'Portage Acadmey':
        f = r
    elif users[x].school == 'Lewiston Elementary':
        f = l
    elif users[x].school == 'Endeavor Elementary':
        f = e
    elif users[x].school == 'Portage Academy':
        f = paa
 
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
    f.write(users[x].grade)
    f.write('\n')
f.close()

