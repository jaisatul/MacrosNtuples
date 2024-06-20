#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export X509_USER_PROXY=/afs/cern.ch/user/a/atjaiswa/.proxy/x509up_u144583
cd /afs/cern.ch/user/a/atjaiswa/L1TDQMCondorSetUp/CMSSW_13_0_3/src/
eval `scramv1 runtime -sh`
cd /afs/cern.ch/user/a/atjaiswa/L1TDQMCondorSetUp/CMSSW_13_0_3/src/MacrosNtuples/l1macros


if [ -z "$4" ]
then
    python3 performances_nano.py --max_events -1 -i $1 -o $2 -c $3
else
    python3 performances_nano.py --max_events -1 -i $1 -o $2 -c $3 -g $4
fi

