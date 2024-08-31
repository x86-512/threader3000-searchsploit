#!/usr/bin/python3
# Threader3000 - Multi-threader Port Scanner
# A project by The Mayor modified by x256_64
# v1.0.7
# https://github.com/dievus/threader3000
# Licensed under GNU GPLv3 Standards.  https://www.gnu.org/licenses/gpl-3.0.en.html


import socket
import os
import signal
import time
import threading
import sys
import subprocess
from queue import Queue
from datetime import datetime

# Start Threader3000 with clear terminal
# subprocess.call('clear', shell=True)

# Main Function
def main():
    socket.setdefaulttimeout(0.30)
    print_lock = threading.Lock()
    discovered_ports:list[str] = []
    discovered_services:list[str] = []

# Welcome Banner
    print("-" * 60)
    print("        Threader 3000 - Multi-threaded Port Scanner          ")
    print("                       Version 1.0.7                    ")
    print("                   A project by The Mayor               ")
    print("                      Modified by x86-512               ")
    print("-" * 60)
    time.sleep(1)
    target = input("Enter your target IP address or URL here: ")
    error = ("Invalid Input")
    try:
        t_ip = socket.gethostbyname(target)
    except (UnboundLocalError, socket.gaierror):
        print("\n[-]Invalid format. Please use a correct IP or web address[-]\n")
        sys.exit()
    #Banner
    print("-" * 60)
    print("Scanning target "+ t_ip)
    print("Time started: "+ str(datetime.now()))
    print("-" * 60)
    t1 = datetime.now()


    #Get vsion like nmap
    def portscan(port):

       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       
       try:
          portx = s.connect((t_ip, port))
          with print_lock:
             print("Port {} is open".format(port))
             discovered_ports.append(str(port))
          portx.close()

       except (ConnectionRefusedError, AttributeError, OSError):
          pass

    def threader():
       while True:
          worker = q.get()
          portscan(worker)
          q.task_done()
      
    q = Queue()
     
    #startTime = time.time()
     
    for x in range(200):
       t = threading.Thread(target = threader)
       t.daemon = True
       t.start()

    for worker in range(1, 65536):
       q.put(worker)

    q.join()

    t2 = datetime.now()
    total = t2 - t1
    print("Port scan completed in "+str(total))
    print("-" * 60)
    print("Threader3000 recommends the following Nmap scan:")
    print("*" * 60)
    print("nmap -p{ports} -sV -sC -T4 -Pn -oA {ip} {ip}".format(ports=",".join(discovered_ports), ip=target))
    print("*" * 60)
    nmap = "nmap -p{ports} -sV -sC -T4 -Pn -oA {ip} {ip}".format(ports=",".join(discovered_ports), ip=target)
    t3 = datetime.now()
    total1 = t3 - t1

    #Update nmap scan to pipe version number back into script for searchsploit

#Nmap Integration (in progress)

    def automate():
       choice = '0'
       while choice =='0':
          print("Would you like to run Nmap or quit to terminal?")
          print("-" * 60)
          print("1 = Run suggested Nmap scan")
          print("2 = Run another Threader3000 scan")
          print("3 = Run suggested Nmap scan and use searchsploit") #New option 3 will be nmap and searchsploit
          print("4 = Exit to terminal") #New option 3 will be nmap and searchsploit
          print("-" * 60)
          choice = input("Option Selection: ")
          if choice == "1":
             try:
                print(nmap)
                os.mkdir(target)
                os.chdir(target)
                os.system(nmap)
                #convert = "xsltproc "+target+".xml -o "+target+".html"
                #os.system(convert)
                t3 = datetime.now()
                total1 = t3 - t1
                print("-" * 60)
                print("Combined scan completed in "+str(total1))
                print("Press enter to quit...")
                input()
             except FileExistsError as e:
                print(e)
                exit()
          elif choice =="2":
             main()
          elif choice== "3":
            nmap = "nmap -p{ports} -sV -sC -T4 -Pn -oA {ip} {ip}".format(ports=",".join(discovered_ports), ip=target)
            command = nmap.split(' ')
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
            stdout, stderr = process.communicate()
            #For the output, split by lines, if line has open state, get the service and version
            outputarr = stdout.decode("utf-8").split("\n")
            version_list = []
            for output in outputarr:
                if((open_ind:= output.find('open'))>-1):
                    found_ver = output[open_ind+4:].strip()
                    if found_ver.find(" ")>-1:
                        version_list.append(found_ver[found_ver.find(" "):].strip())
                    else:
                        version_list.append(found_ver)
            vuln_list:list[str] = []
            try:
                for version in version_list:
                    #vuln_command = f"searchsploit {version}".split(" ")
                    vuln_command = ["searchsploit", version.split(" ")[0]]
                    #print(vuln_command)
                    #breakpoint()
                    process = subprocess.Popen(vuln_command, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    vuln_list.append(stdout.decode("utf-8"))
                for ind, vuln in enumerate(vuln_list):
                    print(f"Searching: {version_list[ind]}\n")
                    print(vuln)
            except FileNotFoundError:
                print("Searchsploit is not installed")
          elif choice =="4":
             sys.exit()
          else:
             print("Please make a valid selection")
             automate()
    automate()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        quit()
