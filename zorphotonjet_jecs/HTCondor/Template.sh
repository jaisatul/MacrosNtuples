#!/bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh  # CMS default software environment
cd swpath                                    # swpath to be set from the SubmitToHTCondor.sh script
eval `scramv1 runtime -sh`                   # this is the cmsenv
cd subpath                                   # submission path to be set from the SubmitToHTCondor.sh script

# $1 input file to be set from Template.sub
# $2 output file to be set from Template.sub
# "channel" to be set from the SubmitToHTCondor.sh script
python3 ../../analysis.py --max_events -1 -i $1 -o $2 -c channel
