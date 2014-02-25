. /etc/rc.common
dscl . create /Users/TESTEND1
dscl . create /Users/TESTEND1 RealName "END TEST"
dscl . passwd /Users/TESTEND1 ufq17ayz!
dscl . create /Users/TESTEND1 UniqueID 115208
dscl . create /Users/TESTEND1 PrimaryGroupID 1027
dscl . create /Users/TESTEND1 UserShell /bin/bash
dscl . create /Users/TESTEND1 NFSHomeDirectory /Network/Servers/end.portage.k12.wi.us/Shared Items/endstudent/TESTEND1

. /etc/rc.common
dscl . create /Users/TESTEND2
dscl . create /Users/TESTEND2 RealName "END 2 TEST"
dscl . passwd /Users/TESTEND2 5067asdf
dscl . create /Users/TESTEND2 UniqueID 113873
dscl . create /Users/TESTEND2 PrimaryGroupID 1027
dscl . create /Users/TESTEND2 UserShell /bin/bash
dscl . create /Users/TESTEND2 NFSHomeDirectory /Network/Servers/end.portage.k12.wi.us/Shared Items/endstudent/TESTEND2

