import FWCore.ParameterSet.Config as cms

hcalTupleBeamHaloSummary = cms.EDProducer("BeamHaloAnalyzer_BeamHaloSum",
  source  = cms.untracked.InputTag("BeamHaloSummary"),
  Prefix  = cms.untracked.string("BeamHaloSum"),
  Suffix  = cms.untracked.string(""),
)
