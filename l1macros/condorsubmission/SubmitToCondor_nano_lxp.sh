#!/bin/bash
if [ -d $1 ]
then 
    echo "Folder exists, exiting"
else 
    mkdir $1
    mkdir /eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/atjaiswa/condoroutput/$1
    mkdir $1/log
    mkdir $1/err
    mkdir $1/out
    cp scriptcondor_performances_nano_template_lxp.sub $1/scriptcondor.sub
    cp scriptcondor_performances_nano_lxp.sh $1/.
    cd $1
    sed -ie "s#OUTPUTDIR#$1#g" scriptcondor.sub
    sed -ie "s#CHANNEL#$2#g" scriptcondor.sub
    sed -ie "s#FILENAMES#$3#g" scriptcondor.sub
    sed -ie "s#GOLDENJSON#$4#g" scriptcondor.sub
    
    condor_submit scriptcondor.sub 
fi
