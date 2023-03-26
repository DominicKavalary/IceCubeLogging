import subprocess
from datetime import datetime 
##########Defining#########
###Defining Html Needed###
#Html Start#
htmlstart = '''<!DOCTYPE html>
<html lang=en>
<head>
<img src="LOGO.gif" width="250" height="250">
<meta charset="utf-8">
<title>IceCube Logging</title>
<nav>
<ul>
  <li><a href="#MemWStor">Memory and Storage</a></li>
  <li><a href="#NetInfo">Network Information</a></li>
  <li><a href="#WinInfo">Machine Info</a></li>
  <li><a href="#UsrGrpInfo">User and Group Info</a></li>
</ul>
</nav>
<style>
img {
  position: fixed;
  right: 0px;
  top: 0px;
}
nav{
position: fixed;
right:0px;
top:275px;
}
li{
display: block;
padding: 4px;
font-size:25px;
}
a {
color: #7ED5EA;
text-decoration: none;
}
h1 {
color: #265487;
}  
h2{
margin-left:50px;
color:#3778C2;
}
h3{
margin-left:100px;
color:#3778C2;
}
p{
margin-left:100px;
color:#A4E1F0;
}
body {
background-color: #150734;
font-family:Consolas, monaco, monospace;
}
</style>
</head>
<body>
'''
#Html End#
htmlend = '''</body>
</html>
'''
###Getting Current Date/Time For File Name###
date_time = datetime.now()
logdate = date_time.strftime("%x").replace("/",",")
logtime = date = date_time.strftime("%X").replace(":",";")
projfile = "IceCube_" + logdate + "_" + logtime + ".html"
###Defining File Content Functions###
#Defining Html Adding Functions#
def starthtml():
	f = open(projfile,"a")
	for line in htmlstart:
		f.write(line)
	f.close()
def endhtml():
	f = open(projfile,"a")
	for line in htmlend:
		f.write(line)
	f.close()
def add(content, tag = "p"):
	content = "\n<"+tag+">\n"+content+"\n</"+tag+">"
	f = open(projfile,"a")
	f.write(content)
	f.close()
def addList(content, tag = "p"):
	f = open(projfile,"a")
	for line in content:
                line = "\n<"+tag+">\n"+line+"\n</"+tag+">"
                f.write(line)
	f.close()
def addWithExtra(content, tag, extra):
	content = "\n<"+tag+" "+extra+">\n"+content+"\n</"+tag+">"
	f = open(projfile,"a")
	f.write(content)
	f.close()
def addScroll(list):
	f = open(projfile,"a")
	f.write("\n<div style='height:500px; width:600px; overflow: auto;'>\n")
	for item in list:
		f.write("<p>"+item+"</p>")
	f.write("\n</div>")
	f.close()
#Defining Python Command Info Grabber
def getoutput(cmd):
        temp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output,error = temp.communicate()
        output = output.decode("utf-8")
        output = output.splitlines()
        return output
        #Returns list of every line outputed
def remEmpty(list):
	count = 0
	for item in list:
		if item == "":
			count = count +1
	for x in range(count):
		list.remove("")
	return list
##########Main##########
#starthtml#
starthtml()

###Memory and Storage
addWithExtra("Memory CPU and Storage","h1","id='MemWStor'")
#Memory Info#
add("Memory", "h2")
output = getoutput('systeminfo |find "Memory"')
addList(output)
#CPU Info#
add("CPU Info", "h2")
output = remEmpty(getoutput('wmic cpu get currentclockspeed,description, deviceid,manufacturer,maxclockspeed,name,numberofcores,numberoflogicalprocessors,status, threadcount,virtualizationfirmwareenabled'))
output = output[1]
output = output.split("  ")
output = remEmpty(output)
temparr = ['Current Clock Speed: ','Description: ', 'DeviceID: ','Manufacturer: ','Max Clock Speed: ','Name: ','Number Of Cores: ','Number Of Logical Processors: ','Status: ', 'System Name: ', 'Thread Count: ','Virtualization Firmware Enabled: ']
tempnum = 0
for line in output:
        if tempnum <= len(temparr):
                add(temparr[tempnum] + line)
                tempnum=tempnum+1

#Top Processes#


#Storage#
add("Storage Info", "h2")
output = getoutput('wmic logicaldisk get size,freespace,caption, FileSystem')
addList(output)
output = getoutput('wmic diskdrive get model,name,size, description, status')
addList(output)
###Network Information###
addWithExtra("Network Information", "h1","id='NetInfo'")

#IP and Mac Addresses#
add("IP and MAC Addresses", "h2")
add("Summary", "h3")
output = getoutput('wmic nicconfig where "ipenabled=true" get macaddress,ipaddress,defaultipgateway,dnsdomain,description')[1:]
addList(output)
add("Extended", "h3")
output = getoutput('ipconfig /all')
tempstr = ''''''
tracker = 0
for line in output:
        if line == "":
                line = "##############################"
        tempstr += line + "\n"
addScroll(tempstr.split("\n"))

###Machine Info###
addWithExtra("Machine Info","h1","id='WinInfo'")
#Hostname#
add("Hostname and Product Name", "h2")
output = getoutput('hostname')
add("Hostname: " + output[0])
output = getoutput('wmic csproduct get name')
output = remEmpty(output)
add("Product Name: " + output[1])
#Uptime#
add("Uptime", "h2")
output = getoutput('net statistics workstation | find "Statistics since"')
add(output[0])
#OS#
add("OS Info", "h2")
output = getoutput('systeminfo | find "OS"')
addList(output)
#Langauge and Encoding#
#Antivirus#
add("Antivirus Info","h2")
output = getoutput("wmic /namespace:\\\\root\securitycenter2 path antivirusproduct")
addList(output)
#Printer Info#
add("Printers", "h2")
output = getoutput('wmic printer get CapabilityDescriptions, caption, location')[1:]
addList(output)
#Downloaded Applications#
add("Downloaded Applications", "h2")
output = getoutput('wmic product get name')
addScroll(output)
###User and Group Info###
addWithExtra("User Info","h1","id='UsrGrpInfo'")
#Users#
add("Users", "h2")
output = getoutput('wmic USERACCOUNT Get Domain,Name,Sid')
addList(output)
##possibly add tasklist, time, powercfg /batteryreport, 


##end html
endhtml()
