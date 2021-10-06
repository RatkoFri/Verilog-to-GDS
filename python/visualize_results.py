import json
import sys
import os
import docker 
import random 
import numpy as np
import matplotlib.pyplot as plt


#read data 
file_name = "./results/syn_log_new.txt"
lines = open(file_name, 'r').readlines()

header = lines[0]
header_list = header.split()
header_names = ['MULT','Delay','Total-Power','Area','PDP']


header_indices = [];
for i in header_names:
    k = header_list.index(i)
    header_indices.append(k)

mults_raw_data = []
for i in range(2,len(lines)):
    tmp_list = lines[i].split()
    for j in range(1,len(tmp_list)):
        tmp_list[j] = float(tmp_list[j])
    mults_raw_data.append(tmp_list)

mults_data = [];
for mult in mults_raw_data:
    mult_filt = [mult[i] for i in header_indices]
    mults_data.append(mult_filt)

#Artificialy generate NMED 
NMED = [];
for i in range(0,len(mults_data)):
    NMED.append(random.randrange(0, 30))

# append NMED to syn results
for i in range(0,len(mults_data)):
    mults_data[i].append(NMED[i]);


# Generate svg

power = []
nmed = []
name = []
for mults in mults_data:
    power.append(mults[-2]*1000);
    nmed.append(mults[-1]);
    name.append(mults[0]);

    
fig, ax = plt.subplots()
ax.scatter(nmed, power)

for i, txt in enumerate(name):
    ax.annotate(txt, (nmed[i], power[i]))
ax.set_ylabel('PDP [pJ]')
ax.set_xlabel('NMED [10^-3]')

plt.savefig('foo.pdf')
plt.savefig('html/foo.svg')

#Generate HTML

html_in = "./html/template.html"
html_doc =  open(html_in, 'r').readlines()  
html_firstPart = html_doc[0:15]
html_thirdPart = html_doc[46:]

# Content part
html_secondPart = [];

#Table
html_secondPart.append("\t<table class=\"table table-hover\">" + "\n");
#Table header 
html_secondPart.append(2*"\t" + "<thead class=\"table-primary\">" + "\n");
html_secondPart.append(3*"\t" + "<tr>" + "\n");
html_secondPart.append(4*"\t" + "<th scope=\"col\">#<//th>" + "\n" );
html_secondPart.append(4*"\t" + "<th scope=\"col\">Multiplier</th>" + "\n");
html_secondPart.append(4*"\t" + "<th scope=\"col\">Delay [ns]</th>" + "\n");
html_secondPart.append(4*"\t" + "<th scope=\"col\">Power [&mu;W]</th>" + "\n");
html_secondPart.append(4*"\t" + "<th scope=\"col\">Area [&mu;m<sup>2</sup>]</th>" + "\n");
html_secondPart.append(4*"\t" + "<th scope=\"col\">PDP [fJ]</th>" + "\n");
#html_secondPart.append(4*"\t" + "<th scope=\"col\">NMED [10<sup>-3</sup>]</th>" + "\n");
html_secondPart.append(3*"\t" + "</tr>" + "\n");
html_secondPart.append(2*"\t" + "</thead>" + "\n");
#Table body 
html_secondPart.append(2*"\t" + "<tbody>" + "\n");
for mults in mults_data:
    html_secondPart.append(3*"\t" + "<tr>" + "\n");
    html_secondPart.append(4*"\t" + "<th scope=\"row\">"+ str(1+mults_data.index(mults))+"</th>" +"\n");
    #Name
    html_secondPart.append(4*"\t" + "<td>"+ mults[0] +"</td>"+"\n");
    #Delay
    html_secondPart.append(4*"\t" + "<td>"+ "{:.2f}".format(mults[1]) +"</td>"+"\n");
    #Power 
    html_secondPart.append(4*"\t" + "<td>"+ "{:.2f}".format(mults[2]*1000) +"</td>"+"\n");
    #Area 
    html_secondPart.append(4*"\t" + "<td>"+ "{:.2f}".format(mults[3]) +"</td>"+"\n");
    #PDP 
    html_secondPart.append(4*"\t" + "<td>"+ "{:.2f}".format(mults[4]*1000) +"</td>"+"\n");
    #NMED 
    #html_secondPart.append(4*"\t" + "<td>"+ "{:.2f}".format(mults[5]) +"</td>"+"\n");
    html_secondPart.append(3*"\t" + "</tr>" + "\n");
html_secondPart.append(2*"\t" + "</tbody>" + "\n");
html_secondPart.append("\t" + "</table>" + "\n");

# Parreto diagram 

#html_secondPart.append("\t" + "</table>" + "\n");

#html_secondPart.append("\t" + "<h1>PDP-NMED Correlation</h1>" + "\n");
#html_secondPart.append("\t" + "<img src=\"foo.svg\">" + "\n");
    

#print(html_secondPart)



html_out = "./html/results.html"
out = open(html_out, 'w')
out.writelines(html_firstPart + html_secondPart + html_thirdPart)
out.close()