# Verilog-to-GDS    
Automated flow for synthesizing approximate multipliers in NanGate 45nm technology.

## Description 
To-Do

## Code organisation 

- html/ -> Web pages for visualizing the synthesis results
- log/ -> synthesis log files
- OR_config/ -> Configuration and intermediate files for OpenROAD synthesis
- python/ -> Python scripts for running the tool
- results/ -> Synthesis results presented as s table in txt file 
- source/ -> Verilog description of approximate multipliers which user needs to provide. 
- conf.json -> JSON file for configuring the tool

## Set-up 

1. Install docker
   - ``` sudo apt update```
   - ``` sudo apt upgrade ```
   - ``` sudo apt install docker.io ```
   - ``` sudo systemctl enable --now docker ```
   - ``` sudo groupadd docker ```
   - ``` sudo usermod -aG docker $USER ```
   - ``` newgrp docker ```
2. Install python libraries  
   - ``` pip install docker ```
   - ``` pip install numpy ```
   - ``` pip install matplotlib ```
3. Pull the docker image 
   - ``` docker pull ratko992/approx_mult_suite:latest ```

## Usage 

1. Copy Verilog files to folder src/
   -  The top module needs to have three signals: two input signals which represent operands and one output signal which represents the product. Input signals should be denoted with *x* and *y* while the output should be marked as *p*. For example:
    ```verilog
        module mult_approx(
            input [15:0] x,
            input [15:0] y,
            output [31:0] p
        );
    ```
        N.B. The filename and top module should share the same name. Currently, the tool does not support generic parameters. 
   - Modify conf.json
   - Run synthesis. This will produce syn_log_new.txt file in folder results/. 
    ```sh
        python3 python/configSynthesis.py
    ```
   - Visualize the results. This will produce web page results.html in folder html/ 

## Conf.json file 

## Constraints