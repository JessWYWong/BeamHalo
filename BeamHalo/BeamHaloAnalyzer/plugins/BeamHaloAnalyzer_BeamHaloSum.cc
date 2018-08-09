#include "BeamHalo/BeamHaloAnalyzer/interface/BeamHaloAnalyzer_BeamHaloSum.h"
#include "DataFormats/HcalDetId/interface/HcalDetId.h"
#include "DataFormats/METReco/interface/BeamHaloSummary.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include <iostream>

using namespace reco;
using namespace edm;

BeamHaloAnalyzer_BeamHaloSum::BeamHaloAnalyzer_BeamHaloSum(const edm::ParameterSet& iConfig) :
  inputTag (consumes<BeamHaloSummary > (iConfig.getUntrackedParameter<edm::InputTag>("source"))),
  prefix   (iConfig.getUntrackedParameter<std::string>  ("Prefix")),
  suffix   (iConfig.getUntrackedParameter<std::string>  ("Suffix"))
{  
  produces <std::vector<int> > (prefix + "GlobaliPhiSuspects"  + suffix );
  produces <std::vector<int> > (prefix + "HcaliPhiSuspects"    + suffix );
  produces <std::vector<char>> (prefix + "HcalHaloReport"        + suffix );
  produces <std::vector<char>> (prefix + "GlobalHaloReport"       + suffix );
  
}

void BeamHaloAnalyzer_BeamHaloSum::
produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

  std::unique_ptr<std::vector<int> > GlobaliPhiSuspects ( new std::vector<int> () );
  std::unique_ptr<std::vector<int> > HcaliPhiSuspects   ( new std::vector<int> () );
  std::unique_ptr<std::vector<char>> HcalHaloReport     ( new std::vector<char> () );
  std::unique_ptr<std::vector<char>> GlobalHaloReport   ( new std::vector<char> () );
  
  //edm::EDGetTokenT<BeamHaloSummary > IT_BeamHaloSummary = consumes<BeamHaloSummary > (inputTag);
  edm::Handle<BeamHaloSummary> TheBeamHaloSummary;
  iEvent.getByToken(inputTag, TheBeamHaloSummary);
  //bool gotReport = iEvent.getByLabel(inputTag, report);  

  if (TheBeamHaloSummary.isValid()){
    const BeamHaloSummary TheSummary = (*TheBeamHaloSummary.product() ); 
    if (TheSummary.GlobalTightHaloId ()) {
      (*GlobaliPhiSuspects)=TheSummary.GetGlobaliPhiSuspects();
      (*GlobalHaloReport)=TheSummary.GetGlobalHaloReport();
    }
    if (TheSummary.HcalTightHaloId ()) {
      (*HcaliPhiSuspects)=TheSummary.GetHcaliPhiSuspects();
      (*HcalHaloReport)=TheSummary.GetHcalHaloReport();
    }
  } 
  else { 
    std::cout << "Could not find BeamHaloSummary with tag: "  << std::endl;
    return;
  }
  
  iEvent.put ( move( GlobaliPhiSuspects ), prefix + "GlobaliPhiSuspects"  + suffix );
  iEvent.put ( move( HcaliPhiSuspects   ), prefix + "HcaliPhiSuspects"    + suffix );
  iEvent.put ( move( HcalHaloReport     ), prefix + "HcalHaloReport"      + suffix );
  iEvent.put ( move( GlobalHaloReport   ), prefix + "GlobalHaloReport"    + suffix );

}
