#!/bin/python
#encoding=utf-8

import sys
import subprocess
import os
import logging
import ConfigParser

#Vinfo=[]
#for i in sys.argv:
#	Vinfo.append(i)
Vinfo=['','develop']
#print Vinfo
#branch = sys.argv[1]
#branch = "develop"
#if branch == "develop":
#	version = "7.9.4"
#	print "111"
#elif branch == "develop":
#	version = "7.9.5"
#else:
#	print "wrong parameter,Pls confirm!"
#	sys.exit(0) 
iniFileUrl="/root/Builds/develop/VERSION.ini"
wget_cmd = "wget --no-check-certificate https://waf:'joe&june'@build.zyprotect.com/builds/"

download_dir =r"/root/Builds/develop/"
log_filename= download_dir + "logging.txt"
os.chdir(download_dir)
log_format='[%(asctime)s] %(message)s'
logging.basicConfig (format=log_format,datafmt='%Y-%m-%d %H:%M:%S %p',level=logging.DEBUG,filename=log_filename,filemode='w')

def run_cmd2file(cmd):
        fdout=open(log_filename,'a')
        p=subprocess.Popen(cmd,stdout=fdout,stderr=fdout,shell=True)
        if p.poll():
                return
        p.wait()
        #print (p.returncode)
        return

def getVersioninfo():
	wcmd = wget_cmd + Vinfo[1] + '/current/VERSION.txt'
	#print wcmd
	VIni={}
	if len(Vinfo) == 3:
		wcmd = wget_cmd + Vinfo[1] + '/' + Vinfo[2] + '/VERSION.txt'
	print wcmd
	old = r'/root/Builds/develop/VERSION.txt'
	while True:
		try:
			if os.path.exists(old):
				os.remove(old)
	              	run_cmd2file(wcmd)
			if os.path.exists(old):	
				break
        	except OSError,e:
			print e
	
	try:
		p = open(old,"r")
		lines = p.readlines()
		for line in lines:
			llist = line.split("=")
			if len(llist) != 2:
				continue
			else:
				VIni[llist[0]]=llist[1].split("\n")[0]
	except OSError,e:
		print e
	print VIni
	if os.path.exists(iniFileUrl):
		os.remove(iniFileUrl)
	fp=open(iniFileUrl,'w')
	fp.close()
	config = ConfigParser.ConfigParser()
	config.read(iniFileUrl)
	config.add_section("Version_Info")
	config.set("Version_Info","branch",VIni['BRANCH'])
	config.set("Version_Info","version",VIni['WAF_MAJOR']+'.'+VIni['WAF_MINOR']+'.'+VIni['WAF_REVISION'])
	config.set("Version_Info","build",VIni['WAF_BUILD'])
	config.write(open(iniFileUrl,'wb'))
	if Vinfo[1] in ["develop","develop"]:
                conf=ConfigParser.ConfigParser()
                conf.read(iniFileUrl)
                global version
                version = conf.get("Version_Info","version")
                global build
                build=conf.get("Version_Info","build")

def downfilefrombuildserver():
	if Vinfo[1] in ["develop","develop"]:
		conf=ConfigParser.ConfigParser()
		conf.read(iniFileUrl) 
		global version
		version = conf.get("Version_Info","version")	
		global build
		build=conf.get("Version_Info","build")
	else:
		print "wrong parameters, PLs confirm to enter develop/develop! try againe"
		sys.exit(0)	
	
#print "%s %s %s" %(branch,version,build)
#	wget_cmd = "wget --no-check-certificate https://waf:'joe&june'@52.33.151.102/builds/"
	global waf_filename
	waf_filename = "zyWAF-" + version + "-" + build + ".x86_64.rpm"
	global debug_filename
	debug_filename = "zyWAF-debuginfo-" + version +"-"+ build  + ".x86_64.rpm"
	waf_cmd= wget_cmd + Vinfo[1] + "/" + build + "/" + waf_filename
	debug_cmd = wget_cmd + Vinfo[1] + "/" + build + "/" + debug_filename

#print wget_waf_cmd
        logging.info("------------------------------------")
        logging.info("---execute command-------------------")
        #cmd_cddir= "cd " + download_dir
        logging.info(os.chdir(download_dir))
        #logging.info(os.system("rm -rf *.rpm"))
        logging.info(os.getcwd())

        logging.info("------------------------------------")
        logging.info("---execute command-------------------")
        #print wget_waf_cmd
        logging.info(waf_cmd)
        logging.debug(run_cmd2file(waf_cmd))
        logging.info("------------------------------------")
        logging.info("---execute command-------------------")
        logging.info(debug_cmd)
        logging.debug(run_cmd2file(debug_cmd))

def uninstall():
	run_cmd2file("service zywaf stop")
	run_cmd2file("rpm -e zyWAF-debuginfo")
	run_cmd2file("rpm -e zyWAF")
	run_cmd2file("rm -rf /usr/local/waf")

def install():
	run_cmd2file("rpm -i "+ waf_filename)
	run_cmd2file("service zywaf start")
	run_cmd2file("rpm -i "+ debug_filename)
	
if __name__ == "__main__":
	getVersioninfo()
	fobj=open('/root/Builds/develop/current.txt','r')
	current_build=int(fobj.readlines()[0].split('\n')[0])
	fobj.close()
	print build,current_build
	tmplist=[build]
	if int(build) <= int(current_build):
		print "No new build"
	else:
		print "Download new build"
		downfilefrombuildserver()
		fobj=open('/root/Builds/develop/current.txt','w')	
		fobj.writelines(tmplist)
		fobj.close()
#	uninstall()
#	install()
