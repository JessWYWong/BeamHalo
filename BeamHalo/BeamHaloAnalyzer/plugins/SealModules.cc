#include "FWCore/PluginManager/interface/ModuleDef.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "BeamHalo/BeamHaloAnalyzer/interface/BeamHaloAnalyzer_Tree.h"
#include "BeamHalo/BeamHaloAnalyzer/interface/BeamHaloAnalyzer_Event.h"
#include "BeamHalo/BeamHaloAnalyzer/interface/BeamHaloAnalyzer_FEDs.h"
#include "BeamHalo/BeamHaloAnalyzer/interface/BeamHaloAnalyzer_HcalDigis.h"
#include "BeamHalo/BeamHaloAnalyzer/interface/BeamHaloAnalyzer_QIE11Digis.h"
#include "BeamHalo/BeamHaloAnalyzer/interface/BeamHaloAnalyzer_HcalRecHits.h"
#include "BeamHalo/BeamHaloAnalyzer/interface/BeamHaloAnalyzer_HcalPhase1RecHits.h"
#include "BeamHalo/BeamHaloAnalyzer/interface/BeamHaloAnalyzer_HcalUnpackerReport.h"
#include "BeamHalo/BeamHaloAnalyzer/interface/BeamHaloAnalyzer_BeamHaloSum.h"

DEFINE_FWK_MODULE(BeamHaloAnalyzer_Tree);
DEFINE_FWK_MODULE(BeamHaloAnalyzer_Event);
DEFINE_FWK_MODULE(BeamHaloAnalyzer_FEDs);
DEFINE_FWK_MODULE(BeamHaloAnalyzer_HBHEDigis);
//DEFINE_FWK_MODULE(HcalTupleMaker_HODigis);
//DEFINE_FWK_MODULE(HcalTupleMaker_HFDigis);
DEFINE_FWK_MODULE(BeamHaloAnalyzer_QIE11Digis);
DEFINE_FWK_MODULE(BeamHaloAnalyzer_HBHERecHits);
//DEFINE_FWK_MODULE(HcalTupleMaker_HORecHits);
//DEFINE_FWK_MODULE(HcalTupleMaker_HFRecHits);
//DEFINE_FWK_MODULE(HcalTupleMaker_HFPhase1RecHits);
DEFINE_FWK_MODULE(BeamHaloAnalyzer_HcalUnpackerReport);
DEFINE_FWK_MODULE(BeamHaloAnalyzer_BeamHaloSum);
