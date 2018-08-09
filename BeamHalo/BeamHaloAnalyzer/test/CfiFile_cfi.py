import FWCore.ParameterSet.Config as cms

demo = cms.EDAnalyzer('BeamHaloGenerator'
     ,tracks = cms.untracked.InputTag('ctfWithMaterialTracks')
)
