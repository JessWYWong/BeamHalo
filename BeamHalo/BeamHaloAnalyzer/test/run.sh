#!/bin/sh
#import valid proxy
export X509_USER_PROXY=/afs/cern.ch/user/u/username/x509up_u94005 #number after u depnds on the output of voms-proxy-info -all and copied to home directory from /tmp/

#The build architecture of CMSSW version
export SCRAM_ARCH=slc6_amd64_gcc700

cd /afs/cern.ch/user/w/wiwong/work/HCALPFG/BeamHalo/CMSSW_10_2_1/src

# This is equivalent to doing "cmsenv"
eval `scramv1 runtime -sh`

cd /afs/cern.ch/user/w/wiwong/work/HCALPFG/BeamHalo/CMSSW_10_2_1/src/BeamHalo/BeamHaloAnalyzer/test

eval cmsRun ConfFile_cfg.py
