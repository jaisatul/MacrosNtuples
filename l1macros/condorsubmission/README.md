# Recipe for condorsubmission on lxplus
- Login to lxplus
- Do VOMS Proxy:
  ```$ voms-proxy-init --valid 196:00 --voms cms```
- Create a .proxy directory in your home (~)
- SET VOMS Proxy path: Add the following lines to your ~/.bashrc
  ```
  $ export _PROXYPATH=/afs/cern.ch/user/a/atjaiswa/.proxy/x509up_u144583
  $ export X509_USER_PROXY=$_PROXYPATH
  ```
- In your AFS area, Create a CMSSW environment and clone the Nanoworkflow and switch to branch dqmoff
  ```
  	$ mkdir CondorTest
	$ cmsrel CMSSW_14_1_0_pre4
	$ cd CMSSW_14_1_0_pre4/src
	$ cmsenv
	$ git clone git@github.com:jaisatul/MacrosNtuples.git
	$ cd MacroNTuples
	$ git checkout -b dqmoff --track origin/dqmoff
  ```
- Go to condorsubmission directory
  ```
  $ cd l1macros/condorsubmission
  ```
- Prepare a log file for JetMET, EGamma and Muon Datsets. A sample log file is present here MacrosNtuples/l1macros/condorsubmission/templatelogfile.log
- In scriptcondor_performances_nano_template_lxp.sub, replace the AFS area and eos area location
	NOTE: 
		The .log, .out and .err should be written in afs area
		The output of jobs can be wriiten to AFS or EOS area. In this example, EOS is used.
- In scriptcondor_performances_nano_lxp.sh, replace the proxy path and AFS area of workflow
- In SubmitToCondor_nano_lxp.sh, replace the output path of EOS
- Run Command to submit jobs for preparing the prefiring histos
  ```
	sh SubmitToCondor_nano_lxp.sh <DirName> <Channel> ../<logFileName>.log
  ```
	e.g.
  ```
	$ sh SubmitToCondor_nano_lxp.sh jetmet_2024Ev1 DiJet ../jetmet_2024Ev1.log
        $ sh SubmitToCondor_nano_lxp.sh muon_2024Ev1 ZToMuMu ../muon_2024Ev1.log
	$ sh SubmitToCondor_nano_lxp.sh egamma_2024Ev1 ZToEE ../egamma_2024Ev1.log
  ```

- NOTE:
	- For above example log file is present in condorsubmission directory
	- Channel Options: DiJet for JetMET dataset, ZToMuMu for Muon dataset, ZToEE for EGamma dataset
