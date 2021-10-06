import docker 

import os
import tarfile
import docker

def copy_to(src, dst):
    os.system('docker cp ' + src + " " + dst)


client = docker.from_env()

container = client.containers.run('ratko992/approx_mult_suite', command='/bin/bash',stdin_open=True,detach=True)


container.start()
destination_folder = "flow/"
copy_to("./conf.json",container.name+":OpenROAD-flow/"+destination_folder)
#exit_code, output = container.exec_run(["/bin/sh", "-c", 'source /OpenROAD-flow/setup_env.sh'])
env = ["OPENROAD=/OpenROAD-flow/tools/OpenROAD","PATH=/OpenROAD-flow/tools/build/OpenROAD/src:/OpenROAD-flow/tools/build/TritonRoute:/OpenROAD-flow/tools/build/yosys/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"]

exit_code, output = container.exec_run(["/bin/sh", "-c", 'chmod +x '],workdir="/OpenROAD-flow/flow",environment=env)

print(output)
print(exit_code)

#container.stop()
#container.remove()
