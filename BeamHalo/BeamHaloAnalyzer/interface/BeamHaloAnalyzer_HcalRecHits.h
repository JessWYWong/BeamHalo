#ifndef BeamHaloAnalyzer_HcalRecHits_h
#define BeamHaloAnalyzer_HcalRecHits_h

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/EDGetToken.h"

#include "BeamHalo/BeamHaloAnalyzer/interface/BeamHaloAnalyzer_HcalRecHitAlgorithm.h"

template <class RecHitCollection> 
class BeamHaloAnalyzer_HcalRecHits : public edm::EDProducer {
 protected:
  
  const edm::InputTag   m_hcalRecHitsTag;
  edm::EDGetTokenT<RecHitCollection> m_hcalRecHitsToken;

  const std::string     m_prefix;
  const std::string     m_suffix;

  BeamHaloAnalyzer_HcalRecHitAlgorithm algo;
  
  void produce( edm::Event & iEvent, const edm::EventSetup & iSetup) { 
    
    //-----------------------------------------------------
    // Prepare to put things into event
    //-----------------------------------------------------
    
    loadAlgo();
    
    //-----------------------------------------------------
    // edm::Handles
    //-----------------------------------------------------
    
    bool run_algo = true;

    edm::Handle<RecHitCollection> hcalRecHits;
    bool gotHcalRecHits = iEvent.getByToken(m_hcalRecHitsToken, hcalRecHits);
    if (!gotHcalRecHits ) {
      std::cout << "Could not find HCAL RecHits with tag " << m_hcalRecHitsTag << std::endl;
      run_algo = false;
    }
    
    //-----------------------------------------------------
    // edm::ESHandles
    //-----------------------------------------------------
    
    edm::ESHandle<CaloGeometry> geometry;
    iSetup.get<CaloGeometryRecord>().get(geometry);
    
    //-----------------------------------------------------
    // Run the algorithm
    //-----------------------------------------------------
    
    if ( run_algo ) algo.run ( *hcalRecHits, *geometry );
    
    //-----------------------------------------------------
    // Put things into the event
    //-----------------------------------------------------
    
    dumpAlgo(iEvent);
    
  }
  
 public:
  
 BeamHaloAnalyzer_HcalRecHits(const edm::ParameterSet& iConfig) :
  m_hcalRecHitsTag (iConfig.getUntrackedParameter<edm::InputTag>("source")),
    m_hcalRecHitsToken (consumes<RecHitCollection>(iConfig.getUntrackedParameter<edm::InputTag>("source"))),
    m_prefix         (iConfig.getUntrackedParameter<std::string>  ("Prefix")),
    m_suffix         (iConfig.getUntrackedParameter<std::string>  ("Suffix")) {
    produces<std::vector<int>   > ( m_prefix + "IEta"   + m_suffix );
    produces<std::vector<int>   > ( m_prefix + "IPhi"   + m_suffix );
    produces<std::vector<float> > ( m_prefix + "Eta"    + m_suffix );
    produces<std::vector<float> > ( m_prefix + "Phi"    + m_suffix );
    produces<std::vector<int>   > ( m_prefix + "Depth"  + m_suffix );
    produces<std::vector<int>   > ( m_prefix + "RBXid"  + m_suffix );
    produces<std::vector<int>   > ( m_prefix + "HPDid"  + m_suffix );
    produces<std::vector<int>   > ( m_prefix + "Flags"  + m_suffix );
    //produces<std::vector<int>   > ( m_prefix + "Aux"    + m_suffix );
    produces<std::vector<float> > ( m_prefix + "Energy" + m_suffix );
    produces<std::vector<float> > ( m_prefix + "Time"   + m_suffix );
    produces<std::vector<float> > ( m_prefix + "chi2"   + m_suffix );
  }

 protected:

  void loadAlgo(){
    algo.ieta   = std::unique_ptr<std::vector<int  > > ( new std::vector<int  > ());
    algo.iphi   = std::unique_ptr<std::vector<int  > > ( new std::vector<int  > ());
    algo.eta    = std::unique_ptr<std::vector<float> > ( new std::vector<float> ());
    algo.phi    = std::unique_ptr<std::vector<float> > ( new std::vector<float> ());
    algo.depth  = std::unique_ptr<std::vector<int  > > ( new std::vector<int  > ());
    algo.rbxid  = std::unique_ptr<std::vector<int  > > ( new std::vector<int  > ());
    algo.hpdid  = std::unique_ptr<std::vector<int  > > ( new std::vector<int  > ());
    algo.flags  = std::unique_ptr<std::vector<int  > > ( new std::vector<int  > ());
    //algo.aux    = std::unique_ptr<std::vector<int  > > ( new std::vector<int  > ());
    algo.energy = std::unique_ptr<std::vector<float> > ( new std::vector<float> ());
    algo.time   = std::unique_ptr<std::vector<float> > ( new std::vector<float> ());
    algo.chi2   = std::unique_ptr<std::vector<float> > ( new std::vector<float> ());
  }
  
  void dumpAlgo( edm::Event & iEvent ){
    iEvent.put( move(algo.ieta   ), m_prefix + "IEta"   + m_suffix );
    iEvent.put( move(algo.iphi   ), m_prefix + "IPhi"   + m_suffix );
    iEvent.put( move(algo.eta    ), m_prefix + "Eta"    + m_suffix );
    iEvent.put( move(algo.phi    ), m_prefix + "Phi"    + m_suffix );
    iEvent.put( move(algo.depth  ), m_prefix + "Depth"  + m_suffix );
    iEvent.put( move(algo.rbxid  ), m_prefix + "RBXid"  + m_suffix );
    iEvent.put( move(algo.hpdid  ), m_prefix + "HPDid"  + m_suffix );
    iEvent.put( move(algo.flags  ), m_prefix + "Flags"  + m_suffix );
    //iEvent.put( move(algo.aux    ), m_prefix + "Aux"    + m_suffix );
    iEvent.put( move(algo.energy ), m_prefix + "Energy" + m_suffix );
    iEvent.put( move(algo.time   ), m_prefix + "Time"   + m_suffix );
    iEvent.put( move(algo.chi2   ), m_prefix + "chi2"   + m_suffix );
  }
  
  
};

typedef BeamHaloAnalyzer_HcalRecHits<HBHERecHitCollection> BeamHaloAnalyzer_HBHERecHits;
//typedef BeamHaloAnalyzer_HcalRecHits<HORecHitCollection  > BeamHaloAnalyzer_HORecHits;
//typedef BeamHaloAnalyzer_HcalRecHits<HFRecHitCollection  > BeamHaloAnalyzer_HFRecHits;

#endif
