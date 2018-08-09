#ifndef BeamHaloAnalyzer_HcalUnpackerReport_h
#define BeamHaloAnalyzer_HcalUnpackerReport_h

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

class BeamHaloAnalyzer_HcalUnpackerReport : public edm::EDProducer {
 public:
  explicit BeamHaloAnalyzer_HcalUnpackerReport(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::InputTag   inputTag;
  const std::string     prefix,suffix;
};

#endif
