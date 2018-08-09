import FWCore.ParameterSet.Config as cms
from RecoMET.METProducers.CSCHaloData_cfi import *
from RecoMET.METProducers.EcalHaloData_cfi import *
from RecoMET.METProducers.HcalHaloData_cfi import *
from RecoMET.METProducers.GlobalHaloData_cfi import *
from RecoMET.METProducers.BeamHaloSummary_cfi import*
from RecoMET.METFilters.metFilters_cff import globalSuperTightHalo2016Filter

#------------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------------
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

#------------------------------------------------------------------------------------
# Options
#------------------------------------------------------------------------------------
options = VarParsing.VarParsing()

options.register('skipEvents',
                 0, # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Number of events to skip")

options.register('processEvents',
                 -1, # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Number of events to process")

#options.register('inputFiles',
#                 "file:/eos/cms/store/data/Run2018B/JetHT/RAW/v1/000/318/828/00000/*.root",
#                 VarParsing.VarParsing.multiplicity.list,
#                 VarParsing.VarParsing.varType.string,
#                 "Input files")
data="MET"
run_no="320673"
options.register('inputFiles',
                 data+"_files.txt", # customized value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Input file")

options.register('outputFile',
                 "/eos/user/w/wiwong/HCALPFG/HcalTupleMaker/Output/BeamHalo_"+data+"_"+run_no+".root", # customized value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Output file")

options.parseArguments()

print " "
print "Using options:"
print " skipEvents    =", options.skipEvents
print " processEvents =", options.processEvents
print " inputFiles    =", options.inputFiles
print " outputFile    =", options.outputFile
print " "



from Configuration.StandardSequences.Eras import eras
process = cms.Process('PFG',eras.Run2_2018)

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = '101X_dataRun2_HLT_v7' #'100X_dataRun2_HLT_v3' #'101X_dataRun2_v8' #'101X_dataRun2_HLT_frozen_v6' # '101X_dataRun2_HLT_v7'

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1)
#process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')

#process.load('RecoMET.METFilters.CSCTightHalo2015Filter_cfi')
#process.CSCTightHalo2015Filter.taggingMode = cms.bool(True)
process.load("RecoMET.METProducers.CSCHaloData_cfi")
process.load("RecoMET.METProducers.EcalHaloData_cfi")
process.load("RecoMET.METProducers.HcalHaloData_cfi")
process.load("RecoMET.METProducers.GlobalHaloData_cfi")
process.load("RecoMET.METProducers.BeamHaloSummary_cfi")
process.load("RecoMET.METFilters.globalSuperTightHalo2016Filter_cfi")
process.globalSuperTightHalo2016Filter.taggingMode = cms.bool(True)
process.load('Configuration.EventContent.EventContent_cff')
process.load("EventFilter.HcalRawToDigi.HcalRawToDigi_cfi")
process.load("BeamHalo.BeamHaloAnalyzer.BeamHaloAnalyzer_hcalLocalReco_cff")
#process.load("BeamHalo.BeamHaloAnalyzer.BeamHaloAnalyzer_Event_cfi")
#process.load("BeamHalo.BeamHaloAnalyzer.BeamHaloAnalyzer_QIE11Digis_cfi")
#process.load("BeamHalo.BeamHaloAnalyzer.BeamHaloAnalyzer_hcalTupleHBHERecHits_cfi")
#process.load("BeamHalo.BeamHaloAnalyzer.BeamHaloAnalyzer_hcalTupleTree_cfi")
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load("BeamHalo.BeamHaloAnalyzer.BeamHaloAnalyzer_cfi") # loads all modules
process.hcalTupleHBHEDigis.DoEnergyReco = False

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


readFiles     = cms.untracked.vstring()
with open( options.inputFiles) as inputtextFile:
  for line in inputtextFile:
    f = "file:"+str(line)
    #print f
    readFiles.extend([f])

process.source = cms.Source(
    "PoolSource",
    fileNames = readFiles
)
#process.source = cms.Source("PoolSource",
#    # replace 'myfile.root' with the source file you want to use
#    fileNames = cms.untracked.vstring(
##        'root://cmsxrootd.fnal.gov//store/data/Run2018A/MET/MINIAOD/PromptReco-v1/000/316/238/00000/A8202F7B-D658-E811-8328-FA163EADB477.root '
#        'file:/eos/cms/store/data/Run2018D/MET/RAW-RECO/HighMET-PromptReco-v2/000/320/838/00000/08379DF3-199A-E811-80F0-FA163E50A814.root'
##        'file:/eos/cms/store/data/Run2018A/IsolatedBunch/RAW/v1/000/315/357/00000/EA3647DE-244B-E811-AAC3-02163E015D6B.root'
#    )
#)

process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(options.outputFile)
    )

#process.muonReco = cms.Sequence(process.muonsFromCosmics)

process.BeamHaloId = cms.Sequence(CSCHaloData*EcalHaloData*HcalHaloData*GlobalHaloData*BeamHaloSummary*process.hcalTupleBeamHaloSummary)
process.tuple_step = cms.Sequence(process.hcalTupleEvent*process.hcalTupleHBHEDigis*process.hcalTupleQIE11Digis*process.hcalTupleHBHERecHits*process.hcalTupleTree)

#process.demo = cms.EDAnalyzer('BeamHaloGenerator'
#     , tracks = cms.untracked.InputTag('ctfWithMaterialTracks')
#)


process.p = cms.Path(process.BeamHaloId*process.globalSuperTightHalo2016Filter*process.hcalDigis*process.hbheprereco*process.tuple_step)
