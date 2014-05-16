New-Item -itemType directory -Path \\phs-fs.portage.k12.wi.us\homeDir-PHS\Students\2016\TESTPHS
$acl = Get-Acl \\phs-fs.portage.k12.wi.us\homeDir-PHS\Students\2016\TESTPHS
$permission = "PORTAGE\TESTPHS","FullControl","ContainerInherit, ObjectInherit","None","Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
$acl.SetAccessRule($accessRule)
$acl | Set-Acl \\phs-fs.portage.k12.wi.us\homeDir-PHS\Students\2016\TESTPHS

New-Item -itemType directory -Path \\bms-dc01.portage.k12.wi.us\homeDir\Students\2018\TESTBMS
$acl = Get-Acl \\bms-dc01.portage.k12.wi.us\homeDir\Students\2018\TESTBMS
$permission = "PORTAGE\TESTBMS","FullControl","ContainerInherit, ObjectInherit","None","Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
$acl.SetAccessRule($accessRule)
$acl | Set-Acl \\bms-dc01.portage.k12.wi.us\homeDir\Students\2018\TESTBMS

New-Item -itemType directory -Path \\rusch-dc01.portage.k12.wi.us\homeDir-Rusch\Students\TESTRUSCH
$acl = Get-Acl \\rusch-dc01.portage.k12.wi.us\homeDir-Rusch\Students\TESTRUSCH
$permission = "PORTAGE\TESTRUSCH","FullControl","ContainerInherit, ObjectInherit","None","Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
$acl.SetAccessRule($accessRule)
$acl | Set-Acl \\rusch-dc01.portage.k12.wi.us\homeDir-Rusch\Students\TESTRUSCH

New-Item -itemType directory -Path \\muir-dc01.portage.k12.wi.us\homeDir\Students\TESTMUIR
$acl = Get-Acl \\muir-dc01.portage.k12.wi.us\homeDir\Students\TESTMUIR
$permission = "PORTAGE\TESTMUIR","FullControl","ContainerInherit, ObjectInherit","None","Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
$acl.SetAccessRule($accessRule)
$acl | Set-Acl \\muir-dc01.portage.k12.wi.us\homeDir\Students\TESTMUIR

New-Item -itemType directory -Path \\muir-dc01.portage.k12.wi.us\homeDir\Faculty\FACTESTMUIR
$acl = Get-Acl \\muir-dc01.portage.k12.wi.us\homeDir\Faculty\FACTESTMUIR
$permission = "PORTAGE\FACTESTMUIR","FullControl","ContainerInherit, ObjectInherit","None","Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
$acl.SetAccessRule($accessRule)
$acl | Set-Acl \\muir-dc01.portage.k12.wi.us\homeDir\Faculty\FACTESTMUIR

New-Item -itemType directory -Path \\rusch-dc01.portage.k12.wi.us\homeDir-Rusch\Faculty\FACTESTRUSCH
$acl = Get-Acl \\rusch-dc01.portage.k12.wi.us\homeDir-Rusch\Faculty\FACTESTRUSCH
$permission = "PORTAGE\FACTESTRUSCH","FullControl","ContainerInherit, ObjectInherit","None","Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
$acl.SetAccessRule($accessRule)
$acl | Set-Acl \\rusch-dc01.portage.k12.wi.us\homeDir-Rusch\Faculty\FACTESTRUSCH

New-Item -itemType directory -Path \\phs-fs.portage.k12.wi.us\homeDir-PHS\Faculty\FACTTESTPHS
$acl = Get-Acl \\phs-fs.portage.k12.wi.us\homeDir-PHS\Faculty\FACTTESTPHS
$permission = "PORTAGE\FACTTESTPHS","FullControl","ContainerInherit, ObjectInherit","None","Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
$acl.SetAccessRule($accessRule)
$acl | Set-Acl \\phs-fs.portage.k12.wi.us\homeDir-PHS\Faculty\FACTTESTPHS

