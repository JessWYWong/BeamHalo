from ROOT import *
import numpy as np 
from array import array
from functools import reduce
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--run", dest="run", help="run")
#parser.add_option("--E_max", dest="E_max", help="E_max")
parser.add_option("--E_min", dest="E_min", help="E_min")

(options, args) = parser.parse_args()
dataset = str(options.run)
#E_max = float(options.E_max)
E_min = float(options.E_min)

print "data set : "+dataset
#print "E cut at : "+str(int(E_max))+" GeV"
print "E cut at: "+str(int(E_min))+" GeV"
cut="E"+"_ge"+str(int(E_min))

#f = TFile("/eos/user/w/wiwong/HCALPFG/HcalTupleMaker/Output/"+dataset+".root")
f = TFile(dataset+".root")
outputFile=TFile(dataset+"_BeamHalo_plot_cut_"+cut+".root", "RECREATE")
t = f.Get("hcalTupleTree/tree")
Raw="QIE11Digi"
Rec="HBHERecHit"
layer=np.array([1,2,3,4,5,6,7])

#define functions
def fill_pulse(layer, n, Pulse, hist):
  for i in range(len(n)):
    if n[i]==0:
      n[i]=1
  n=np.stack((n,n,n,n,n,n,n,n),axis=1)
  avg_pulse=Pulse/n
  for l in layer: 
    for TS in range(8):
      hist.Fill(l,TS+1,avg_pulse[l-1][TS])

#define lists and arrays
Pulse=np.zeros((7,8))
n=np.zeros(7)
Pulse_ChannelsmallChi=np.zeros((7,8))
n_ChannelsmallChi=np.zeros(7)
Pulse_ChannellargeChi=np.zeros((7,8))
n_ChannellargeChi=np.zeros(7)
Pulse_smallChi=np.zeros((7,8))
n_smallChi=np.zeros(7)
Pulse_largeChi=np.zeros((7,8))
n_largeChi=np.zeros(7)
Raw_dt=[]
Rec_dt=[]
Rec_sumE=[]
Rec_sumDepth=[]
Raw_t=[]
Rec_t=[]
E=[]
Depth=[]

# Define Lists and Histograms
all_hist_list=[]
hist_RecTime=[]
hist_RawTime=[]
hist_RecTime_Eta=[]
hist_RecTime_Phi=[]
hist_RecTime_E=[]
hist_RawTime_Eta=[]
hist_RawTime_Phi=[]
hist_RawTime_E=[]

for i in range(len(layer)):
  hist_RecTime.append(TH1F(dataset+"_"+"hist_RecTime"+"_depth"+str(i+1)+"_"+cut, "M2 Reconstructed Time", 120, -15., 15.))
  hist_RecTime[i].GetXaxis().SetTitle("Time [ns]")
  hist_RecTime[i].GetYaxis().SetTitle("Entries / 0.25 ns")
  hist_RawTime.append(TH1F(dataset+"_"+"hist_RawTime"+"_depth"+str(i+1)+"_"+cut, "TDC Time", 120, 65., 95.))
  hist_RawTime[i].GetXaxis().SetTitle("Time [ns]")
  hist_RecTime[i].GetYaxis().SetTitle("Entries")
  hist_RecTime_Eta.append(TH2F(dataset+"_"+"hist_RecTime_Eta"+"_depth"+str(i+1)+"_"+cut, "M2 Time against IEta", 60, -30., 30., 31, -15.5, 15.5))
  hist_RecTime_Eta[i].GetYaxis().SetTitle("Time [ns]")
  hist_RecTime_Eta[i].GetXaxis().SetTitle("IEta")
  hist_RecTime_Phi.append(TH2F(dataset+"_"+"hist_RecTime_Phi"+"_depth"+str(i+1)+"_"+cut, "M2 Time against IPhi", 74, 0., 74., 31, -15.5, 15.5))
  hist_RecTime_Phi[i].GetYaxis().SetTitle("Time [ns]")
  hist_RecTime_Phi[i].GetXaxis().SetTitle("IPhi")
  hist_RecTime_E.append(TH2F(dataset+"_"+"hist_RecTime_E"+"_depth"+str(i+1)+"_"+cut, "M2 Time against Energy", 51, -0.5, 50.5, 31, -15.5, 15.5))
  hist_RecTime_E[i].GetYaxis().SetTitle("Time [ns]")
  hist_RecTime_E[i].GetXaxis().SetTitle("Energy [fC]")
  hist_RawTime_Eta.append(TH2F(dataset+"_"+"hist_RawTime_Eta"+"_depth"+str(i+1)+"_"+cut, "TDC Time against IEta", 61, -29.5, 30.5, 31, 64.5, 95.5))
  hist_RawTime_Eta[i].GetYaxis().SetTitle("Time [ns]")
  hist_RawTime_Eta[i].GetXaxis().SetTitle("IEta")
  hist_RawTime_Phi.append(TH2F(dataset+"_"+"hist_RawTime_Phi"+"_depth"+str(i+1)+"_"+cut, "TDC Time against IPhi", 75, -0.5, 74.5, 31, 64.5, 95.5))
  hist_RawTime_Phi[i].GetYaxis().SetTitle("Time [ns]")
  hist_RawTime_Phi[i].GetXaxis().SetTitle("IPhi")
  hist_RawTime_E.append(TH2F(dataset+"_"+"hist_RawTime_E"+"_depth"+str(i+1)+"_"+cut, "TDC Time against Pulse Peak", 71, -0.5, 70000.5, 31, 64.5, 95.5))
  hist_RawTime_E[i].GetYaxis().SetTitle("Time [ns]")
  hist_RawTime_E[i].GetXaxis().SetTitle("Energy [fC]")

hist_avg_Pulse= TH2F(dataset+"_"+"hist_avg_Pulse"+"_"+cut, "TDC Pulse in Each Depth", 7, 0.5, 7.5, 8, 0.5, 8.5)
hist_avg_Pulse.GetYaxis().SetTitle("TS [25ns]")
hist_avg_Pulse.GetXaxis().SetTitle("Depth")
hist_E_Depth= TH2F(dataset+"_"+"hist_E_Depth"+"_"+cut, "Reconstructed Energy Distribution in Depths", 7, 0.5, 7.5, 51, -0.5, 49.5)
hist_E_Depth.GetYaxis().SetTitle("Energy [GeV]")
hist_E_Depth.GetXaxis().SetTitle("Depth")
hist_RecTime_Depth= TH2F(dataset+"_"+"hist_RecTime_Depth"+"_"+cut, "M2 Time Distribution in Depths", 7, 0.5, 7.5, 31, -15.5, 15.5)
hist_RecTime_Depth.GetYaxis().SetTitle("Time [ns]")
hist_RecTime_Depth.GetXaxis().SetTitle("Depth")
hist_RawTime_Depth= TH2F(dataset+"_"+"hist_RawTime_Depth"+"_"+cut, "TDC Time Distribution in Depths", 7, 0.5, 7.5,31, 64.5, 95.5)
hist_RawTime_Depth.GetYaxis().SetTitle("Time [ns]")
hist_RawTime_Depth.GetXaxis().SetTitle("Depth")
hist_Chi2_RecTime= TH2F(dataset+"_"+"hist_Chi2_RecTime"+"_"+cut, "Chi-Squared Distribution against M2 Time", 31, -15.5, 15.5, 21, -0.5, 20.5)
hist_Chi2_RecTime.GetYaxis().SetTitle("Chi-Squared")
hist_Chi2_RecTime.GetXaxis().SetTitle("Time [ns]")
hist_avg_Pulse_ChannelsmallChi= TH2F(dataset+"_"+"hist_avg_Pulse_ChannelsmallChi"+"_"+cut, "TDC Pulse in Each Depth", 7, 0.5, 7.5, 8, 0.5, 8.5)
hist_avg_Pulse_ChannelsmallChi.GetYaxis().SetTitle("TS [25ns]")
hist_avg_Pulse_ChannelsmallChi.GetXaxis().SetTitle("Depth")
hist_avg_Pulse_ChannellargeChi= TH2F(dataset+"_"+"hist_avg_Pulse_ChannellargeChi"+"_"+cut, "TDC Pulse in Each Depth", 7, 0.5, 7.5, 8, 0.5, 8.5)
hist_avg_Pulse_ChannellargeChi.GetYaxis().SetTitle("TS [25ns]")
hist_avg_Pulse_ChannellargeChi.GetXaxis().SetTitle("Depth")
hist_avg_Pulse_smallChi= TH2F(dataset+"_"+"hist_avg_Pulse_smallChi"+"_"+cut, "TDC Pulse in Each Depth", 7, 0.5, 7.5, 8, 0.5, 8.5)
hist_avg_Pulse_smallChi.GetYaxis().SetTitle("TS [25ns]")
hist_avg_Pulse_smallChi.GetXaxis().SetTitle("Depth")
hist_avg_Pulse_largeChi= TH2F(dataset+"_"+"hist_avg_Pulse_largeChi"+"_"+cut, "TDC Pulse in Each Depth", 7, 0.5, 7.5, 8, 0.5, 8.5)
hist_avg_Pulse_largeChi.GetYaxis().SetTitle("TS [25ns]")
hist_avg_Pulse_largeChi.GetXaxis().SetTitle("Depth")

#hist_RawTime_IEta= TH1F(dataset+"_"+"hist_RawTime_IEta"+"_"+cut, "TDC Time of Beam Halo in HE against IEta", 32, -30.5, 30.5)
outputFile.cd()
for i,event in enumerate(t):
  Raw_FC=np.array(getattr(t,Raw+"FC"))
  Raw_Time=np.array(getattr(t,Raw+"TimeTDC"))  # ns
  max_FC=np.amax(Raw_FC, axis=1)
  Raw_ID epth=np.array(getattr(t,Raw+"Depth"))
  Raw_IEta=np.array(getattr(t,Raw+"IEta"))
  Raw_IPhi=np.array(getattr(t,Raw+"IPhi"))
  Rec_E=np.array(getattr(t,Rec+"Energy"))
  Rec_Time=np.array(getattr(t,Rec+"Time"))
  Rec_IDepth=np.array(getattr(t,Rec+"Depth"))
  Rec_IEta=np.array(getattr(t,Rec+"IEta"))
  Rec_IPhi=np.array(getattr(t,Rec+"IPhi"))  
  Rec_Chi2=np.array(getattr(t,Rec+"chi2"))
 
  Raw_DetID=reduce(np.core.defchararray.add,(Raw_IDepth.astype(str),"_",Raw_IPhi.astype(str),"_",Raw_IEta.astype(str)))
  Rec_DetID=reduce(np.core.defchararray.add,(Rec_IDepth.astype(str),"_",Rec_IPhi.astype(str),"_",Rec_IEta.astype(str)))
  
  Raw_etaphi=reduce(np.core.defchararray.add,(Raw_IEta.astype(str),"_",Raw_IPhi.astype(str)))
  Rec_etaphi=reduce(np.core.defchararray.add,(Rec_IEta.astype(str),"_",Rec_IPhi.astype(str)))
  
  match_mask=np.isin(Rec_DetID,Raw_DetID)
  Rec_E=Rec_E[match_mask]
  Rec_Time=Rec_Time[match_mask]
  Rec_IDepth=Rec_IDepth[match_mask]
  Rec_IEta=Rec_IEta[match_mask]
  Rec_IPhi=Rec_IPhi[match_mask]
  Rec_Chi2=Rec_Chi2[match_mask]
  Rec_etaphi=Rec_etaphi[match_mask]
  Rec_DetID=Rec_DetID[match_mask]

  E_max_cut=np.where(Rec_E<E_max)[0]
  E_min_cut=np.where(Rec_E>=E_min)[0]
  Rec_index=np.intersect1d(E_max_cut,E_min_cut)
  passed_phi=np.unique(Rec_IPhi[Rec_index])
  
  for j,phi in enumerate(passed_phi):
    hist_RawTime_IEta= TH1F(dataset+"_"+"hist_RawTime_IEta"+"_"+cut+"_Evt"+str(j), "TDC Time of Beam Halo in HE against IEta", 32, -30.5, 30.5)
    is_small_Chi = False
    is_large_Chi = False
    Raw_channel=np.where(Raw_IPhi==phi)[0]
    Rec_channel=np.where(Rec_IPhi==phi)[0]
    # Raw_zero=np.where(Raw_IDepth[Raw_channel]==1)[0]
    # Rec_zero=np.where(Rec_IDepth[Rec_channel]==1)[0]
    # if len(Raw_zero)!=1 or len(Rec_zero)!=1:
    #   print "Layer 1 not found in "+eta_phi
    #   continue
    # Raw_zero_time=Raw_Time[Raw_channel[Raw_zero[0]]]
    # Rec_zero_time=Rec_Time[Rec_channel[Rec_zero[0]]]
    Raw_zero_time=0
    Rec_zero_time=0
    if len(Raw_channel) != len(Rec_channel):
      print "matching error"
      break
    if (Rec_Chi2[Rec_channel]<=5.).all():
      is_small_Chi = True
    if (Rec_Chi2[Rec_channel]>5.).all():
      is_large_Chi = True
    #if not (np.diff(Rec_E[Rec_channel])<np.average(Rec_E[Rec_channel])*0.2).all():
    #  continue
    for k in range(len(Raw_channel)):
      hist_RawTime_IEta.Fill(Raw_IEta[Raw_channel[k]],Raw_Time[Raw_channel[k]])
      Rec_l=Rec_IDepth[Rec_channel[k]]-1
      Raw_l=Raw_IDepth[Raw_channel[k]]-1
      hist_RecTime[Rec_l].Fill(Rec_Time[Rec_channel[k]]-Rec_zero_time) 
      hist_RawTime[Raw_l].Fill(Raw_Time[Raw_channel[k]]-Raw_zero_time) 
      hist_RecTime_Eta[Rec_l].Fill(Rec_IEta[Rec_channel[k]],Rec_Time[Rec_channel[k]]-Rec_zero_time)
      hist_RecTime_Phi[Rec_l].Fill(Rec_IPhi[Rec_channel[k]],Rec_Time[Rec_channel[k]]-Rec_zero_time)
      hist_RecTime_E[Rec_l].Fill(Rec_E[Rec_channel[k]],Rec_Time[Rec_channel[k]]-Rec_zero_time)
      hist_RawTime_Eta[Raw_l].Fill(Raw_IEta[Raw_channel[k]],Raw_Time[Raw_channel[k]]-Raw_zero_time)
      hist_RawTime_Phi[Raw_l].Fill(Raw_IPhi[Raw_channel[k]],Raw_Time[Raw_channel[k]]-Raw_zero_time)
      hist_RawTime_E[Raw_l].Fill(max_FC[Raw_channel[k]],Raw_Time[Raw_channel[k]]-Raw_zero_time)
      hist_E_Depth.Fill(Rec_l+1,Rec_E[Rec_channel[k]])
      hist_RecTime_Depth.Fill(Rec_l+1,Rec_Time[Rec_channel[k]]-Rec_zero_time)
      hist_RawTime_Depth.Fill(Raw_l+1,Raw_Time[Raw_channel[k]]-Raw_zero_time)
      hist_Chi2_RecTime.Fill(Rec_Time[Rec_channel[k]]-Rec_zero_time,Rec_Chi2[Rec_channel[k]])
      Pulse[Raw_l]+=Raw_FC[Raw_channel[k]]
      n[Raw_l]+=1
      if is_small_Chi:
        Pulse_ChannelsmallChi[Raw_l]+=Raw_FC[Raw_channel[k]]
        n_ChannelsmallChi[Raw_l]+=1
      if is_large_Chi:
        Pulse_ChannellargeChi[Raw_l]+=Raw_FC[Raw_channel[k]]
        n_ChannellargeChi[Raw_l]+=1
      if Rec_Chi2[Rec_channel[k]] >5 :
        Pulse_largeChi[Raw_l]+=Raw_FC[Raw_channel[k]]
        n_largeChi[Raw_l]+=1
      else:
        Pulse_smallChi[Raw_l]+=Raw_FC[Raw_channel[k]]
        n_smallChi[Raw_l]+=1
    hist_RawTime_IEta.Write()
  print "Complete event "+str(i)

fill_pulse(layer, n, Pulse, hist_avg_Pulse)
fill_pulse(layer, n_ChannellargeChi, Pulse_ChannellargeChi, hist_avg_Pulse_ChannellargeChi)
fill_pulse(layer, n_ChannelsmallChi, Pulse_ChannelsmallChi, hist_avg_Pulse_ChannelsmallChi)
fill_pulse(layer, n_largeChi, Pulse_largeChi, hist_avg_Pulse_largeChi)
fill_pulse(layer, n_smallChi, Pulse_smallChi, hist_avg_Pulse_smallChi)

for l in layer: 
  all_hist_list.append(hist_RecTime[l-1])
  all_hist_list.append(hist_RawTime[l-1])
  all_hist_list.append(hist_RecTime_Eta[l-1])
  all_hist_list.append(hist_RecTime_Phi[l-1])
  all_hist_list.append(hist_RecTime_E[l-1])
  all_hist_list.append(hist_RawTime_Eta[l-1])
  all_hist_list.append(hist_RawTime_Phi[l-1])
  all_hist_list.append(hist_RawTime_E[l-1])

all_hist_list.append(hist_E_Depth)
all_hist_list.append(hist_RecTime_Depth)
all_hist_list.append(hist_RawTime_Depth)
all_hist_list.append(hist_Chi2_RecTime)
all_hist_list.append(hist_avg_Pulse)
all_hist_list.append(hist_avg_Pulse_ChannellargeChi)
all_hist_list.append(hist_avg_Pulse_ChannelsmallChi)
all_hist_list.append(hist_avg_Pulse_largeChi)
all_hist_list.append(hist_avg_Pulse_smallChi)

#outputFile.cd()

for hist in all_hist_list:
  hist.Write()

outputFile.Close()

