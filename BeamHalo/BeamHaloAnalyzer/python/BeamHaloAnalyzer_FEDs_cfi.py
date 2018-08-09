import FWCore.ParameterSet.Config as cms

hcalTupleFEDs = cms.EDProducer("BeamHaloAnalyzer_FEDs",
   source = cms.untracked.InputTag("rawDataCollector"),
   Prefix = cms.untracked.string("FED"),
   Suffix = cms.untracked.string(""),
   MinFED = cms.untracked.uint32(0),
   MaxFED = cms.untracked.uint32(1500)
)                               
