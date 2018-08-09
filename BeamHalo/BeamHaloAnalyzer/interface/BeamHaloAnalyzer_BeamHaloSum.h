#ifndef BeamHaloAnalyzer_BeamHaloSum_h
#define BeamHaloAnalyzer_BeamHaloSum_h

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/METReco/interface/BeamHaloSummary.h"

class BeamHaloAnalyzer_BeamHaloSum : public edm::EDProducer {
 public:
  explicit BeamHaloAnalyzer_BeamHaloSum(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::EDGetTokenT<reco::BeamHaloSummary >  inputTag;
  const std::string     prefix,suffix;
};

#endif
