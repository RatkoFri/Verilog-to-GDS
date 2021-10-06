import json
import sys
import os
import docker 

def copy_to(src, dst):
    os.system('docker cp ' + src + " " + dst)
# Parse json file

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


with open('./conf.json') as json_file:
    
    client = docker.from_env()
    container = client.containers.run('ratko992/approx_mult_suite',stdin_open=True,detach=True)

    data = json.load(json_file)

    # ----------------------------------
    # bitlength and source files

    bitlength =  int(data['synthesis']['bitlength']);
    if(bitlength & (bitlength-1) ):
        raise Exception("The bitlength needs to be power of two")

    replace_line("OR_config/mult_top.v", 4, "\tinput ["+ str(bitlength-1)+ ":0] x,\n")
    replace_line("OR_config/mult_top.v", 6, "\tinput ["+ str(bitlength-1)+ ":0] y,\n")
    replace_line("OR_config/mult_top.v", 8, "\toutput reg ["+ str(2*bitlength-1)+ ":0] p\n")
    replace_line("OR_config/mult_top.v", 11, "\treg ["+ str(bitlength-1)+ ":0] X_vec;\n")
    replace_line("OR_config/mult_top.v", 12, "\treg ["+ str(bitlength-1)+ ":0] Y_vec;\n")
    replace_line("OR_config/mult_top.v", 17, "\twire ["+ str(2*bitlength-1)+ ":0] P_vec;\n")

    # Copy file mult_top.v to /OpenROAD-flow/flow/designs/src/mult_approx
    destination_folder = "flow/designs/src/mult_approx/"
    copy_to("OR_config/mult_top.v",container.name+":OpenROAD-flow/"+destination_folder)
    designs = os.listdir(data['synthesis']['design_folder'])

    str_designs = "";
    for i in designs:
        str_designs = str_designs + "\"" + i[:-2] + "\""+ " ";
    
    replace_line("OR_config/OpenROAD.sh", 5, "arr_mult=(" + str_designs+")\n")

    # Copy OpenRoad.sh to /OpenROAD-flow/flow
    destination_folder = "flow/"
    copy_to("OR_config/OpenROAD.sh",container.name+":OpenROAD-flow/"+destination_folder+"OpenROAD_syn.sh")
    
    # Copy Verilog files to OpenROAD-flow/flow/mults_src

    destination_folder = "flow/mults_src/"
    for i in designs:
        copy_to("source/"+i,container.name+":OpenROAD-flow/"+destination_folder)

    # ----------------------------------
    # platform and dia area

    replace_line("OR_config/config.mk", 2, "export PLATFORM    = " + data['synthesis']['ORparams']['PLATFORM'] + "\n")

    width =  float(data['synthesis']['ORparams']['DIE_AREA']);
    replace_line("OR_config/config.mk", 9, "export DIE_AREA    = 0 0 " + str(width) + " " + str(width) + "\n")
    replace_line("OR_config/config.mk", 10, "export CORE_AREA   = 10.07 11.2 " + str(width-52*0.19) + " " + str(width-7*1.4) + "\n")
    

    # clock and loaf 
    clk = float(data['synthesis']['ORparams']['CLOCK'])
    tmp = "create_clock [get_ports clk] -period " + str(clk)+"  -waveform {0 " + str(clk/2)+"}\n"

    replace_line("OR_config/constraint.sdc", 1, tmp)
    replace_line("OR_config/constraint.sdc", 2, "set_load "+ data['synthesis']['ORparams']['CLOAD'] + " [get_ports p]")

    # copy config.mk and constraint.sdc to /OpenROAD-flow/flow/designs/nangate45/mult_approx
    destination_folder = "flow/designs/nangate45/mult_approx/"
    copy_to("OR_config/config.mk",container.name+":OpenROAD-flow/"+destination_folder)
    copy_to("OR_config/constraint.sdc",container.name+":OpenROAD-flow/"+destination_folder)

    # Run the flow
    env = ["OPENROAD=/OpenROAD-flow/tools/OpenROAD","PATH=/OpenROAD-flow/tools/build/OpenROAD/src:/OpenROAD-flow/tools/build/TritonRoute:/OpenROAD-flow/tools/build/yosys/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"]

    exit_code, output = container.exec_run(["/bin/sh", "-c", 'chmod +x ./OpenROAD_syn.sh'],workdir="/OpenROAD-flow/flow",environment=env)
    exit_code, output = container.exec_run(["/bin/sh", "-c", './OpenROAD_syn.sh'],workdir="/OpenROAD-flow/flow",environment=env)

    # logging
    file1 = open("log/logs.txt","w") 
    file1.writelines(output.decode('utf-8')) 
    file1.close() #to change file access modes 
    
    # results
    destination_folder = "flow/syn_log_new.txt"
    copy_to(container.name+":OpenROAD-flow/"+destination_folder,"./results/")

    #stop and remove containers
    container.stop()
    container.remove()
