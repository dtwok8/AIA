"""
Objekt Pictures a k nemu prislusne a potrebne metody jako zapsani objektu do souboru nebo naopak export objektu ze souboru.

@author: Katerina Kratochvilova
"""
import subprocess
p = subprocess.call("python load_data.py", shell = True)

if p != 0:
    print "Pri zpracovavani souboru load_data.py doslo k chybe."
    exit(1)
    
p = subprocess.call("python count_distance_jec.py", shell = True)

if p != 0:
    print "Pri zpracovavani souboru count_distance_jec.py doslo k chybe."
    exit(1)
    

subprocess.call("python count_result.py", shell = True)

if p != 0:
    print "Pri zpracovavani souboru count_result.py doslo k chybe."
    exit(1)


#import os
#
#os.system("python load_data.py")
#os.system("python count_distance_jec.py")
#os.system("python count_result.py")