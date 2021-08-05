on lxplus : 

export SINGULARITY_CACHEDIR="/tmp/$(whoami)/singularity"
singularity shell -B /afs -B /eos docker://clelange/hepdata_lib bash


Then navigate to the dir with your root files. 
1D likelihood scans need to be made into txt files. 
The script t-something.py will read the canvases saved from the scans and make txt files. 
Be careful of the order of your graphs in the canvas. 

 


The function makegraph n in read.py will make the the tables for those. 
See examples for 2D hists - easy direct root -> yaml table 

To run the creator of the files : 
python read.py 
