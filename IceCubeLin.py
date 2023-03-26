from datetime import datetime 
import subprocess
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
  <li><a href="#LinInfo">Machine Info</a></li>
  <li><a href="#UsrGrpInfo">User and Group Info</a></li>
  <li><a href="#LogInfo">Crash Info</a></li>
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
projfile = "IceCube_"+str(datetime.now())+".html"
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
def addWithExtra(content, tag, extra):
	content = "\n<"+tag+" "+extra+">\n"+content+"\n</"+tag+">"
	f = open(projfile,"a")
	f.write(content)
	f.close()
def addScroll(list):
	list.sort()
	f = open(projfile,"a")
	f.write("\n<div style='height:500px; width:500px; overflow: auto; color:pink;'>\n")
	for item in list:
		f.write("<p>"+item+"</p>")
	f.write("\n</div>")
	f.close()
#Defining Python Command Parsing Function#
def getoutput(cmd):
	temp = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
	output = str(temp.communicate())
#	print(output)
	output = output.split("\n")
#	print(output)
	output = output[0].split('\\n')
#	print(output)
	output[0]=output[0][3:]
#	print(output)
	output=output[0:-1]
#	print(output)
	return output
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

###Memory and Storage###
addWithExtra("Memory CPU and Storage","h1","id='MemWStor'")

#Memory Info#
add("Memory", "h2")
output = getoutput("free -h")
for line in output:
	info=remEmpty(line.split(" "))
	if "Mem" in info[0]:
		add("Total Memory: "+str(info[1]))
		add("Used Memory: "+str(info[2]))
	elif "Swap" in info[0]:
		add("Swap Memory: "+str(info[1]))
		add("Used Swap: "+str(info[2]))

#CPU Info#
add("CPU Info", "h2")
output = getoutput("lscpu")
dashes = "-"
for line in output:
	if "Flags:" in line:
		break;
	elif "Architecture:" in line:
		add(line)
	elif "CPU(s):" in line:
		add(line)
	elif "Vendor ID:" in line:
		add(line)
	elif "Model name:" in line:
		add(dashes+line)
		dashes="--"
	else:
		add(dashes+line)

#Top Processes#
add("Top Running Processes", "h2")
add("Format: Process, Process ID, %CPU, %Memory,Time Ran", "h3")
output = getoutput("top -o %CPU -bin 1")
pasttop = False
for line in output:
	if line == "":
		pasttop = True
	elif pasttop:
		info=remEmpty(line.split(" "))
		if info[0] != "PID":
			add(info[11]+ ", "+info[0]+", "+info[8]+"%, "+info[9]+"%, "+info[10])
	
#Storage#
add("Disks and Partitions", "h2")
output = getoutput("lsblk -lo NAME,TYPE,FSUSED,SIZE,FSTYPE,STATE")
for line in output:
	if "NAME" in line:
		add("Disk Format: Name, Type, Size, If Running","h3")
		add("Partition Format: Name, Type, Used Space, Size, File System","h3")
	if "disk" in line:
		add(line)
	elif "part" in line:
		add("--"+line)
		
###Network Information###
addWithExtra("Network Information", "h1","id='NetInfo'")

#IP and Mac Addresses#
add("IP and MAC Addresses", "h2")
output = getoutput("ip addr")
for line in output:
	if line[1] == ":":
		state = line[line.find("state"):line.find("group")]
		add(line[:line.find("qdisc")]+state)
	elif "inet" in line:
		add("--"+line[:line.find("scope")])
	elif "link/" in line:
		add("--"+line[:line.find("scope")])
		
#DNS Server Addresses#
add("DNS Servers", "h2")
output = getoutput("cat /etc/resolv.conf")
for line in output:
	if "nameserver" in line:
		info = line.split(" ")
		add(info[1])
		tempoutput = getoutput("ping -c 2 "+info[1])
		for templine in tempoutput:
			if "---" in templine:
				add(templine)
			elif "2 packets" in templine:
				add(templine)
				
#Default Gateway#
add("Default Gateway", "h2")
output = getoutput("ip route")
for line in output:
	if "default via" in line:
		info = line.split(" ")
		add(info[2])
		tempoutput = getoutput("ping -c 2 "+info[2])
		for templine in tempoutput:
			if "---" in templine:
				add(templine)
			elif "2 packets" in templine:
				add(templine)
			
###Machine Info###
addWithExtra("Machine Info","h1","id='LinInfo'")

#Hostname#
add("Hostname", "h2")
add(str(getoutput("hostname")[0]))

#Uptime#
add("Uptime", "h2")
add("System "+str(getoutput("uptime -p")[0]))

#Version Information#
add("Version Information","h2")
output = getoutput("cat /etc/os-release")
for line in output:
    	info = line.split("=")
    	if info[0] == "NAME":
    		add(line)
    	elif info[0] == "SUPPORT_URL":
    		add(line)
    	elif info[0] == "VERSION_ID":
    		add(line)
    	elif info[0] == "VERSION":	
    		add(line)
    		
#Shell Info#
add("Shell Info","h2")
add("Preffered Shell: "+str(getoutput("echo $SHELL")[0]))

#Printer Info#
add("Installed Printers","h2")
output = getoutput("lpstat -p")
for line in output:
	add(line)
	
#Run Levels#
add("Runlevel Info","h2")
add("Default Runlevel: " + str(getoutput("systemctl get-default")[0]))
add("Current Runlevel: " + str(getoutput("runlevel")[0]))

#Language and Encoding
add("Language and Encoding","h2")
add("LANG: " + str(getoutput("echo $LANG")[0]))

#Modules#
add("Installed Modules (Hover and Scroll)","h2")
output = getoutput("lsmod")[1:]
tempstr = ''''''
for line in output:
	info = line.split(" ")
	tempstr +=info[0]+"\n"
addScroll(tempstr.split("\n"))

#History#
add("History (Hover and Scroll)","h2")
output = getoutput("cat ~/.bash_history")
tempstr = ''''''
for line in output:
	if "\\x00" not in line:
		tempstr+=line+"\n"
addScroll(tempstr.split("\n"))

#Dimensions#
add("Dimensions","h2")
output = getoutput("xdpyinfo | grep 'dimensions'")
add("Dimensions: "+str(output[0][13:]))

###User and Group Info###
addWithExtra("User and Group Info","h1","id='UsrGrpInfo'")

#Non-System Users#
add("Non-System Users","h2")
output = getoutput("cat /etc/passwd")
for line in output:
	info = line.split(":")
	if int(info[2]) > 999:
		if info[0] != "nobody":
			add(info[0])
			
#Non-System Groups#
add("Non-System Groups","h2")
output = getoutput("cat /etc/group")
for line in output:
	info = line.split(":")
	if int(info[2]) > 999:
		if info[0] != "nogroup" and info[0] != "nobody" :
			add(info[0])	

#Currently Logged In Users
add("Logged In Users","h2")
output = getoutput("who")
for line in output:
	info=remEmpty(line.split(" "))
	add("User: "+info[0]+", Terminal: "+info[1])

###Log Info###
addWithExtra("Crash Info","h1","id='LogInfo'")
#Crash Reports#
add("Crash Reports","h2")
output = getoutput("last | grep -i crash")
for line in output:
	add(line)

###end html###
endhtml()
