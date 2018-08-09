import FWCore.ParameterSet.Config as cms

hcalTupleTree = cms.EDAnalyzer("BeamHaloAnalyzer_Tree",
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_hcalTupleEvent_*_*',
        'keep *_hcalTupleFEDs_*_*',
        'keep *_hcalTupleHBHEDigis_*_*',
        'keep *_hcalTupleQIE11Digis_*_*',
        'keep *_hcalTupleHBHERecHits_*_*',
        'keep *_hcalTupleHBHERecHitsMethod0_*_*',
        'keep *_hcalTupleUnpackReport_*_*',
        'keep *_hcalTupleBeamHaloSummary_*_*'
    )
)

