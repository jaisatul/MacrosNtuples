from datetime import datetime
import ROOT
import json
import os
import sys
import argparse



#In case you want to load an helper for C++ functions
ROOT.gInterpreter.Declare('#include "../helpers/Helper.h"')
ROOT.gInterpreter.Declare('#include "../helpers/Helper_InvariantMass.h"')
#Importing stuff from other python files
sys.path.insert(0, '../helpers')

from helper import * 


def main():
    ###Arguments 
    parser = argparse.ArgumentParser(
        description='''L1 performance studies (turnons, scale/resolution/...)
        Based on ntuples produced from MINIAOD with a code adapted from:
        https://github.com/lathomas/JetMETStudies/blob/master/JMEAnalyzer/python/JMEanalysis.py''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--max_events", dest="max_events", help="Maximum number of events to analyze. Default=-1 i.e. run on all events.", type=int, default=-1)
    parser.add_argument("-i", "--input", dest="inputFile", help="Input file", type=str, default='')
    parser.add_argument("-o", "--output", dest="outputFile", help="Output file", type=str, default='')
    parser.add_argument("-c", "--channel", dest="channel", help=
                        '''Set channel and analysis:
                        -PhotonJet: For L1 jet studies with events triggered with a SinglePhoton trigger
                        -DiJet: For L1 jet studies with events triggered with a SingleJet trigger
                        -MuonJet: For L1 jet studies with events triggered with a SingleMuon trigger
                        -ZToMuMu: For L1 muon studies with Z->mumu
                        -ZToEE: For L1 EG studies with Z->ee''', 
                        type=str, default='PhotonJet')
    parser.add_argument("--plot_nvtx", dest="plot_nvtx", help="Whether to save additional plots in bins of nvtx. Boolean, default = False", type=bool, default=False)
    parser.add_argument("--nvtx_bins", dest="nvtx_bins", help="Edges of the nvtx bins to use if plotNvtx is set to True. Default=[10, 20, 30, 40, 50, 60]", nargs='+', type=int, default=[10, 20, 30, 40, 50, 60])
    args = parser.parse_args() 

    
    ###Define the RDataFrame from the input tree
    inputFile = args.inputFile
    if inputFile == '':
        if args.channel == 'PhotonJet':
            inputFile = '/user/lathomas/Public/L1Studies/PhotonJet.root'
        elif args.channel == 'DiJet':
            inputFile = '/user/lathomas/Public/L1Studies/DiJet.root'
        elif args.channel == 'MuonJet':
            inputFile = '/user/lathomas/Public/L1Studies/MuJet.root'
        elif args.channel == 'ZToMuMu':
            inputFile = '/user/lathomas/Public/L1Studies/ZToMuMu.root'
        elif args.channel == 'ZToEE':
            inputFile = '/user/lathomas/Public/L1Studies/ZToEE.root'

    ### Create filters and suffix, if needed, to later run on bins of nvtx

    filter_list = ["true"]
    suffix_list = [""]

    # bins of nvtx
    if args.plot_nvtx == True:
        filter_list += ["_n_PV>{}&&_n_PV<{}".format(low, high) for (low, high) \
                in zip(args.nvtx_bins[:-1],args.nvtx_bins[1:])]
        suffix_list += ["_nvtx{}to{}".format(low, high) for (low, high) \
                in zip(args.nvtx_bins[:-1],args.nvtx_bins[1:])]

    ###

    df = ROOT.RDataFrame('ntuplizer/tree', inputFile)    
    nEvents = df.Count().GetValue()

    if nEvents == 0:
        df = ROOT.RDataFrame('jmeanalyzer/tree', inputFile)
        nEvents = df.Count().GetValue()

    nEvents = df.Count().GetValue()
    if nEvents == 0:
        print('There are no events, exiting...')
        exit()
    
    print('There are {} events'.format(nEvents))
    
    #Max events to run on 
    max_events = min(nEvents, args.max_events) if args.max_events >=0 else nEvents
    df = df.Range(0, max_events)
    #Next line to monitor event loop progress
    df = df.Filter('if(tdfentry_ %100000 == 0) {cout << "Event is  " << tdfentry_ << endl;} return true;')

    #Apply MET filters
    df = df.Filter('Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_goodVertices&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_BadPFMuonFilter&&Flag_BadPFMuonDzFilter')

    # binning for run number
    set_runnb_bins(df)
    
    if args.outputFile == '':
        args.outputFile = 'output_'+args.channel+'.root'
    out = ROOT.TFile(args.outputFile, "recreate")
    ####The sequence of filters/column definition starts here
    
    if args.channel not in ['PhotonJet','MuonJet','ZToMuMu','ZToEE']:
        print("Channel {} does not exist".format(args.channel))
        return 

    # add nvtx histo
    nvtx_histo = df.Histo1D(ROOT.RDF.TH1DModel("h_nvtx" , "Number of reco vertices;N_{vtx};Events"  ,    100, 0., 100.), "_n_PV")
    nvtx_histo.GetValue().Write()
        
    if args.channel == 'PhotonJet':
        df = SinglePhotonSelection(df) 
        
        df = CleanJets(df)
        
        # make copies of df for each bin of nvtx (+1 copy of the original)
        df_list = [df.Filter(nvtx_cut) for nvtx_cut in filter_list]

        all_histos_jets = {}
        all_histos_balance = {}
        all_histos_hf = {}

        # run for each bin of nvtx:
        for i, df_element in enumerate(df_list):
            df_element, histos_jets = AnalyzeCleanJets(df_element, 200, 100, suffix = suffix_list[i])
            df_element = PtBalanceSelection(df_element)
            df_element, histos_balance = AnalyzePtBalance(df_element, suffix = suffix_list[i])
            #df_report = df_element.Report()
            df_element, histos_hf = HFNoiseStudy(df_element, suffix = suffix_list[i])

            for key, val in histos_jets.items():
                all_histos_jets[key] = val

            for key, val in histos_balance.items():
                all_histos_balance[key] = val

            for key, val in histos_hf.items():
                all_histos_hf[key] = val

            #df_report.Print()

        for i in all_histos_jets:
            all_histos_jets[i].GetValue().Write()
            
        for i in all_histos_balance:
            all_histos_balance[i].GetValue().Write()
            
        for i in all_histos_hf:
            all_histos_hf[i].GetValue().Write()

#        df, histos_jets = AnalyzeCleanJets(df, 200, 100) 
#        
#        df = PtBalanceSelection(df)
#        
#        df, histos_balance = AnalyzePtBalance(df)
#        
        df_report = df.Report()
#        
#        df, histos_hf = HFNoiseStudy(df)
#
#        #Selection is over. Now do some plotting
#
#        for i in histos_jets:
#            histos_jets[i].GetValue().Write()
#
#        for i in histos_balance:
#            histos_balance[i].GetValue().Write()
#            
#        for i in histos_hf:
#            histos_hf[i].GetValue().Write()
        df_report.Print()
        
        
    if args.channel == 'MuonJet':
        df = MuonJet_MuonSelection(df) 
        
        df = CleanJets(df)
        
        # make copies of df for each bin of nvtx (+1 copy of the original)
        df_list = [df.Filter(nvtx_cut) for nvtx_cut in filter_list]

        all_histos_jets = {}
        all_histos_sum = {}
        all_histos_hf = {}

        for i, df_element in enumerate(df_list):
            df_element, histos_jets = AnalyzeCleanJets(df_element, 100, 50, suffix = suffix_list[i]) 
            df_element, histos_sum = EtSum(df_element, suffix = suffix_list[i])
            df_element, histos_hf = HFNoiseStudy(df_element, suffix = suffix_list[i])

            for key, val in histos_jets.items():
                all_histos_jets[key] = val

            for key, val in histos_sum.items():
                all_histos_sum[key] = val

            for key, val in histos_hf.items():
                all_histos_hf[key] = val

        for i in all_histos_jets:
            all_histos_jets[i].GetValue().Write()
            
        for i in all_histos_sum:
            all_histos_sum[i].GetValue().Write()

        for i in all_histos_hf:
            all_histos_hf[i].GetValue().Write()
            
#        df, histos_jets = AnalyzeCleanJets(df, 100, 50) 
#        
#        df, histos_sum = EtSum(df)
#        
#        df_report = df.Report()
#        
#        df, histos_hf = HFNoiseStudy(df)
#
#        #Selection is over. Now do some plotting
#        
#        for i in histos_jets:
#            histos_jets[i].GetValue().Write()
#            
#        for i in histos_sum:
#            histos_sum[i].GetValue().Write()
#            
#        for i in histos_hf:
#            histos_hf[i].GetValue().Write()
#                
#        df_report.Print()

    if args.channel == 'ZToEE':
        df = ZEE_EleSelection(df)

        # make copies of df for each bin of nvtx (+1 copy of the original)
        df_list = [df.Filter(nvtx_cut) for nvtx_cut in filter_list]
        all_histos = {}

        for i, df_element in enumerate(df_list):
            df_element, histos = ZEE_Plots(df_element, suffix = suffix_list[i])

            for key, val in histos.items():
                all_histos[key] = val
        
        for i in all_histos:
            all_histos[i].GetValue().Write()

#        df, histos = ZEE_Plots(df)
#        
#        for i in histos:
#            histos[i].GetValue().Write()

    if args.channel == 'ZToMuMu':
        df = ZMuMu_MuSelection(df)

        # make copies of df for each bin of nvtx (+1 copy of the original)
        df_list = [df.Filter(nvtx_cut) for nvtx_cut in filter_list]
        all_histos = {}

        for i, df_element in enumerate(df_list):
            df_element, histos = ZMuMu_Plots(df_element, suffix = suffix_list[i])

            for key, val in histos.items():
                all_histos[key] = val

        for i in all_histos:
            all_histos[i].GetValue().Write()

#        df, histos = ZMuMu_Plots(df)
#
#        for i in histos:
#            histos[i].GetValue().Write()


if __name__ == '__main__':
    main()
