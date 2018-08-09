from ROOT import *
import CMS_lumi, tdrstyle
from optparse import OptionParser
from time import sleep


def cms_hist_format(hist,histname,draw_method):
  # Set plot style
  tdrstyle.setTDRStyle()
  CMS_lumi.lumi_7TeV = " "
  CMS_lumi.lumi_8TeV = " "
  CMS_lumi.writeExtraText = 1
  CMS_lumi.extraText = "Preliminary"
  W = 800
  H = 600
  iPos = 0
  iPeriod = 4
  if( iPos==0 ): CMS_lumi.relPosX = 0.1  
  gROOT.SetBatch(True)
  canvas = TCanvas("c_"+histname,"c_"+histname,50,50,W,H)
  gStyle.SetOptStat()
  canvas.SetFillColor(0)
  canvas.SetBorderMode(0)
  canvas.SetFrameFillStyle(0)
  canvas.SetFrameBorderMode(0)
  canvas.SetTickx(0)
  canvas.SetTicky(0)  
  hist.Draw(draw_method)
  #draw the lumi text on the canvas
  CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
  canvas.cd()
  canvas.Update()
  canvas.RedrawAxis()
  frame = canvas.GetFrame()
  frame.Draw()
  canvas.Modified()
  canvas.Update()
  canvas.Print(histname+".pdf","pdf")
  gROOT.Reset()

def all_done():
  print "All plots exported."


if __name__== "__main__":
  parser = OptionParser()
  parser.add_option("--file", dest="fPath", help="fpath")
  (options, args) = parser.parse_args()
  fPath   = options.fPath
  print "input file: "+fPath
  
  f=TFile(fPath,"READ")
  
  keys=f.GetListOfKeys()
  
  for k in keys:
    name=k.GetName()
    hist=f.Get(name)
    if isinstance(hist, TH1F):
      draw_method=""
    elif isinstance(hist, TH2F):
      draw_method="COLZ"
    cms_hist_format(hist,name,draw_method)
    hist.Delete()
  
  sleep(0.5)
  
  all_done()
  
  f.Close()
  
  
  raw_input("Press Enter to end")
