# coding: utf-8
import os

fnlist = os.listdir(os.getcwd())

project_name = ""
lay_num = 2

for fns in fnlist:
	ext = fns[-3:]
	if ext == "drl":
	 	project_name = fns[:-4]
	if ext == ".g2":
		lay_num += 1
	if ext == ".g3":
		lay_num += 1
	if ext == ".g4":
		lay_num += 1
	if ext == ".g5":
		lay_num += 1

if project_name == "":
	print "Not find *.drl file."
	exit()

if lay_num != 2 and lay_num != 4 and lay_num != 6:
	print "lay number %d error" %(lay_num)
	exit()

if lay_num == 2:
	readme = """
	L1 : %s-F.Cu.gtl
	L2 : %s-B.Cu.gbl
	""" %(project_name, project_name)
elif lay_num == 4:
	readme = """
	L1 : %s-F.Cu.gtl
	L2 : %s-In1.Cu.g2
	L3 : %s-In2.Cu.g3
	L4 : %s-B.Cu.gbl
	""" %(project_name, project_name, project_name, project_name)
else:
	readme = """
	L1 : %s-F.Cu.gtl
	L2 : %s-In1.Cu.g2
	L3 : %s-In2.Cu.g3
	L4 : %s-In3.Cu.g4
	L5 : %s-In4.Cu.g5
	L6 : %s-B.Cu.gbl
	""" %(project_name, project_name, project_name, project_name, project_name, project_name)


# get board thickness
while True:
	th = raw_input("thickness: 1>1.6mm; 2>1.0mm; 3>0.6mm; 4>0.8mm; 5>1.2mm; 6>2.0mm  ")
	if th.isdigit():
		th = int(th)
		if th > 0 and th<=6:
			break

if th == 1:
	readme += "thickness: 1.6mm"
elif th == 2:
	readme += "thickness: 1.0mm"
elif th == 3:
	readme += "thickness: 0.6mm"
elif th == 4:
	readme += "thickness: 0.8mm"
elif th == 5:
	readme += "thickness: 1.2mm"
else:
	readme += "thickness: 2.0mm"

print readme
with open("readme.txt", "w") as f:
	f.write(readme)

zipcmd = "7z a %s.zip *" %(project_name)
os.system(zipcmd)


