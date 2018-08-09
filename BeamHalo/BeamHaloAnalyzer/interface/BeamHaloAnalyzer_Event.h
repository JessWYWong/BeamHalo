#ifndef BeamHaloAnalyzer_Event_h
#define BeamHaloAnalyzer_Event_h

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

class BeamHaloAnalyzer_Event : public edm::EDProducer {
 public:
  explicit BeamHaloAnalyzer_Event(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );

};

#endif
