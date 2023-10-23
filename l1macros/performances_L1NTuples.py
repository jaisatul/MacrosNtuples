from datetime import datetime
import ROOT
import json
import os
import sys
import argparse

#Get absolute location of code package
topDir = os.getcwd().split('MacrosNtuples')[0]+'MacrosNtuples/'

sys.path.insert(0, topDir+'helpers')
from helper_L1Ntuples import *

ROOT.gInterpreter.Declare('#include "'+topDir+'helper/Helper.h"')
def main():
    parser = argparse.ArgumentParser(
        description='''L1 performance studies (turnons, scale/resolution/...)                                                                                                                                
        Based on L1 ntuples
        ''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--max_events", dest="max_events", help="Maximum number of events to analyze. Default=-1 i.e. run on all events.", type=int, default=-1)
    parser.add_argument("--print_events", dest="print_events", help="Print out every Nth event analyzed. Default=100000 i.e. print every 100k-th.", type=int, default=100000)
    parser.add_argument("-i", "--input", dest="inputFile", help="Input file", type=str, default='')
    parser.add_argument("-o", "--output", dest="outputFile", help="Output file", type=str, default='')
    parser.add_argument("-c", "--channel", dest="channel", help=
                        '''Set channel and analysis:
                        -PhotonJet: For L1 jet studies with events trigger with a SinglePhoton trigger
                        -MuonJet: For L1 jet studies with events trigger with a SingleMuon trigger
                        -ZToMuMu: For L1 muon studies with Z->mumu
                        -ZToEE: For L1 EG studies with Z->ee''',
                        type=str, default='PhotonJet')
    args = parser.parse_args()
    inputFile = ROOT.TFile.Open(args.inputFile)
    tree = inputFile.Get('l1EventTree/L1EventTree')
    tree_Upgrade = inputFile.Get('l1UpgradeEmuTree/L1UpgradeTree')
    tree_uGT  = inputFile.Get('l1uGTTree/L1uGTTree')
    tree_Reco = inputFile.Get('l1RecoTree/RecoTree')
    tree_RecoJet = inputFile.Get('l1JetRecoTree/JetRecoTree')
    tree_RecoMuon = inputFile.Get('l1MuonRecoTree/Muon2RecoTree')
    tree_RecoElectron = inputFile.Get('l1ElectronRecoTree/ElectronRecoTree')
    tree.AddFriend(tree_Upgrade)
    tree.AddFriend(tree_uGT)
    tree.AddFriend(tree_Reco)
    tree.AddFriend(tree_RecoMuon)
    tree.AddFriend(tree_RecoJet)
    

    #tree = ROOT.TTree(ROOT.TFile(inputFile,'open').Get('l1UpgradeTree/L1UpgradeTree'))
    print(type(tree))
    df = ROOT.RDataFrame(tree)
    #df = ROOT.RDataFrame('l1UpgradeTree/L1UpgradeTree', inputFile)
    nEvents = df.Count().GetValue()
    print('There are {} events'.format(nEvents))
    
    max_events = min(nEvents, args.max_events) if args.max_events >=0 else nEvents
    df = df.Range(0, max_events)
    df = df.Filter('if(tdfentry_ %'+str(args.print_events)+' == 0) {cout << "Event is  " << tdfentry_ << endl;cout << Event.nPV<<endl;  } return true;')

    out = ROOT.TFile(args.outputFile, "recreate")
    
    #df = df.Filter("L1uGT.m_algoDecisionFinal[460]","zb") #bit 459 for L1_ZeroBias (standard ZB), bit 460 for L1_ZeroBias_copy (for Ephemeral ZB)
    df = df.Filter("L1uGT.m_algoDecisionInitial[460]","zb")
    h = df.Histo1D(ROOT.RDF.TH1DModel('h_evtbx', '', 4000, 0, 4000), 'Event.bx')


    
    df = MuonJet_MuonSelection(df)
    df = CleanJets(df)
    
    df, histos_jets = AnalyzeCleanJets(df, 100, 50)
    
    #df, histos_sum = EtSum(df)
    
    df_report = df.Report()

    for i in histos_jets:
        histos_jets[i].GetValue().Write()

    #for i in histos_sum:
    #    histos_sum[i].GetValue().Write()


    h.Write()

    df_report.Print()

if __name__ == '__main__':
    main()


