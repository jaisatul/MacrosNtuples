eventselection='dijet'
subfolder='/shifterprefiringplots'
channelname='DiJet'

import yaml
import drawplots
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='''Plotter''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-d", "--dir", dest="dir", help="The directory to read the inputs files from and draw the plots to", type=str, default='./')
    parser.add_argument("-c", "--config", dest="config", help="The YAML config to read from", type=str, default='../config_cards/full_DiJet.yaml')
    parser.add_argument("-l", "--lumi", dest="lumi", help="The integrated luminosity to display in the top right corner of the plot", type=str, default='')
    parser.add_argument("-e", "--era", dest="era", help="Label to mark the era", type=str, default='')

    args = parser.parse_args()
    config = yaml.safe_load(open(args.config, 'r'))

    input_file = args.dir + "/all_DiJet_" +  args.era + ".root"
    # if args.lumi != '':
    #     toplabel="#sqrt{s} = 13.6 TeV, L_{int} = " + args.lumi #+ " fb^{-1}"
    # else:
    #     toplabel="#sqrt{s} = 13.6 TeV"
    # toplabel= "#sqrt{s} = 13.6 TeV, " +  args.lumi
    toplabel= "JetMET, " +  args.lumi
    suffixes = ['']
    if config['PU_plots']['make_histos']:
        bins = config['PU_plots']['nvtx_bins']
        suffixes += ['_nvtx{}to{}'.format(bins[i], bins[i+1]) for i in range(len(bins) - 1)]

    
    for s in suffixes:

        if config['Prefiring']:

            # Prefiring vs Eta (All events) 
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Jet30_AllEvents_bxmin1_eta_jet500'],
                den = ['L1Jet30_AllEvents_Denominator_eta_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = 'L1Jet30 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{All events}',
                top_label = toplabel,
                plotname = channelname+'_L1Jet_AllEvents_PrefiringVsEta',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Jet30_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_eta_jet500'],
                den = ['L1Jet30_L1_UnprefireableEvent_FirstBxInTrain_Denominator_eta_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = 'L1Jet30 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname+'_L1Jet_UnprefireableEvent_FirstBxInTrain_PrefiringVsEta',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta (UnprefireableEvent_TriggerRules)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Jet30_L1_UnprefireableEvent_TriggerRules_bxmin1_eta_jet500'],
                den = ['L1Jet30_L1_UnprefireableEvent_TriggerRules_Denominator_eta_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = 'L1Jet30 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_L1Jet_UnprefireableEvent_TriggerRules_PrefiringVsEta',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )


            # Prefiring vs Runnb (All events) 
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Jet30_AllEvents_bxmin1_runnb_jet500'],
                den = ['L1Jet30_AllEvents_Denominator_runnb_jet500'],
                xtitle = 'Run number',
                ytitle = 'L1Jet30 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{All events}',
                top_label = toplabel,
                plotname = channelname+'_L1Jet_AllEvents_PrefiringVsRunNb',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Runnb (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Jet30_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_runnb_jet500'],
                den = ['L1Jet30_L1_UnprefireableEvent_FirstBxInTrain_Denominator_runnb_jet500'],
                xtitle = 'Run number',
                ytitle = 'L1Jet30 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname+'_L1Jet_UnprefireableEvent_FirstBxInTrain_PrefiringVsRunNb',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Runnb (UnprefireableEvent_TriggerRules)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Jet30_L1_UnprefireableEvent_TriggerRules_bxmin1_runnb_jet500'],
                den = ['L1Jet30_L1_UnprefireableEvent_TriggerRules_Denominator_runnb_jet500'],
                xtitle = 'Run number',
                ytitle = 'L1Jet30 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_L1Jet_UnprefireableEvent_TriggerRules_PrefiringVsRunNb',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )


            # Prefiring vs Eta Phi (All events)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Jet30_AllEvents_bxmin1_etaphi_jet500'],
                den = ['L1Jet30_AllEvents_Denominator_etaphi_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = '#phi^{jet}(reco)',
                ztitle = 'L1Jet30 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{All events}',
                top_label = toplabel,
                plotname = channelname+'_L1Jet_AllEvents_PrefiringVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta Phi (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Jet30_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_etaphi_jet500'],
                den = ['L1Jet30_L1_UnprefireableEvent_FirstBxInTrain_Denominator_etaphi_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = '#phi^{jet}(reco)',
                ztitle = 'L1Jet30 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname+'_L1Jet_UnprefireableEvent_FirstBxInTrain_PrefiringVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta Phi (UnprefireableEvent_TriggerRules)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Jet30_L1_UnprefireableEvent_TriggerRules_bxmin1_etaphi_jet500'],
                den = ['L1Jet30_L1_UnprefireableEvent_TriggerRules_Denominator_etaphi_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = '#phi^{jet}(reco)',
                ztitle = 'L1Jet30 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_L1Jet_UnprefireableEvent_TriggerRules_PrefiringVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 0.1],
                addnumtoden = False,
                )


            # Prefiring vs Eta Pt (All events)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Jet30_AllEvents_bxmin1_etapt_jet500'],
                den = ['L1Jet30_AllEvents_Denominator_etapt_jet500'],
                xtitle = '#eta(jet)',
                ytitle = 'p_{T}(jet) [GeV]',
                # xtitle = '#eta^{jet}(reco)',
                # ytitle = 'p_{T}^{jet}(reco)',
                ztitle = 'L1Jet30 matched in BX-1',
                # ztitle = 'L1Jet30 (BX-1) matching fraction',

                legendlabels = [''],
                extralabel = 'DiJet',
                # extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{All events}',
                top_label = toplabel,
                plotname = channelname+'_L1Jet_AllEvents_PrefiringVsEtaPt',
                axisranges = [-5, 5, 500, 4000, 0, 0.1],
                addnumtoden = False,
                setlogy = True,
                )

            # Prefiring vs Eta Pt (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Jet30_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_etapt_jet500'],
                den = ['L1Jet30_L1_UnprefireableEvent_FirstBxInTrain_Denominator_etapt_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = 'p_{T}^{jet}(reco)',
                ztitle = 'L1Jet30 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname+'_L1Jet_UnprefireableEvent_FirstBxInTrain_PrefiringVsEtaPt',
                axisranges = [-5, 5, 500, 4000, 0, 0.1],
                addnumtoden = False,
                setlogy = True,
                )

            # Prefiring vs Eta Pt (UnprefireableEvent_TriggerRules)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Jet30_L1_UnprefireableEvent_TriggerRules_bxmin1_etapt_jet500'],
                den = ['L1Jet30_L1_UnprefireableEvent_TriggerRules_Denominator_etapt_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = 'p_{T}^{jet}(reco)',
                ztitle = 'L1Jet30 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_L1Jet_UnprefireableEvent_TriggerRules_PrefiringVsEtaPt',
                axisranges = [-5, 5, 500, 4000, 0, 0.1],
                addnumtoden = False,
                setlogy = True,
                )

            
            
            ##############Now looking at EG prefiring. Question: can it happen that a very high pt jet leaks some ECAL energy in BX-1?
            # Prefiring vs Eta (All events) 
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_AllEvents_bxmin1_eta_jet500'],
                den = ['L1EG20_AllEvents_Denominator_eta_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{All events}',
                top_label = toplabel,
                plotname = channelname+'_L1EG_AllEvents_PrefiringVsEta',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_eta_jet500'],
                den = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_Denominator_eta_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname+'_L1EG_UnprefireableEvent_FirstBxInTrain_PrefiringVsEta',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta (UnprefireableEvent_TriggerRules)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_TriggerRules_bxmin1_eta_jet500'],
                den = ['L1EG20_L1_UnprefireableEvent_TriggerRules_Denominator_eta_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_L1EG_UnprefireableEvent_TriggerRules_PrefiringVsEta',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )


            # Prefiring vs Eta Phi (All events)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_AllEvents_bxmin1_etaphi_jet500'],
                den = ['L1EG20_AllEvents_Denominator_etaphi_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = '#phi^{jet}(reco)',
                ztitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{All events}',
                top_label = toplabel,
                plotname = channelname+'_L1EG_AllEvents_PrefiringVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta Phi (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_etaphi_jet500'],
                den = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_Denominator_etaphi_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = '#phi^{jet}(reco)',
                ztitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname+'_L1EG_UnprefireableEvent_FirstBxInTrain_PrefiringVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta Phi (UnprefireableEvent_TriggerRules)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_TriggerRules_bxmin1_etaphi_jet500'],
                den = ['L1EG20_L1_UnprefireableEvent_TriggerRules_Denominator_etaphi_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = '#phi^{jet}(reco)',
                ztitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_L1EG_UnprefireableEvent_TriggerRules_PrefiringVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 0.1],
                addnumtoden = False,
                )


            # Prefiring vs Eta Pt (All events)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_AllEvents_bxmin1_etapt_jet500'],
                den = ['L1EG20_AllEvents_Denominator_etapt_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = 'p_{T}^{jet}(reco)',
                ztitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{All events}',
                top_label = toplabel,
                plotname = channelname+'_L1EG_AllEvents_PrefiringVsEtaPt',
                axisranges = [-5, 5, 50, 4000, 0, 0.1],
                addnumtoden = False,
                setlogy = True,
                )

            # Prefiring vs Eta Pt (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_etapt_jet500'],
                den = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_Denominator_etapt_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = 'p_{T}^{jet}(reco)',
                ztitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname+'_L1EG_UnprefireableEvent_FirstBxInTrain_PrefiringVsEtaPt',
                axisranges = [-5, 5, 50, 4000, 0, 0.1],
                addnumtoden = False,
                setlogy = True,
                )

            # Prefiring vs Eta Pt (UnprefireableEvent_TriggerRules)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_TriggerRules_bxmin1_etapt_jet500'],
                den = ['L1EG20_L1_UnprefireableEvent_TriggerRules_Denominator_etapt_jet500'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = 'p_{T}^{jet}(reco)',
                ztitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{jet} > 500 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_L1EG_UnprefireableEvent_TriggerRules_PrefiringVsEtaPt',
                axisranges = [-5, 5, 50, 4000, 0, 0.1],
                addnumtoden = False,
                setlogy = True,
                )


            # Prefiring vs Mjj
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['mjj_unpref_trigrules_L1FinalORBXmin1_barrelbarrel', 'mjj_unpref_1stbx_L1FinalORBXmin1_barrelbarrel'],
                den = ['mjj_unpref_trigrules_barrelbarrel', 'mjj_unpref_1stbx_barrelbarrel'],
                xtitle = 'M(j_{1}j_{2}) (GeV)',
                ytitle = 'Fraction of events passing L1FinalOR in BX-1',
                legendlabels = ['Unpref events (trig. rules)', 'Unpref events (1st bx)'],
                extralabel = '#splitline{'+eventselection+', |#eta(j_{1}, j_{2})|<1.3}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_mjj_unpref_L1FinalORBXmin1_barrelbarrel',
                axisranges = [1000, 6000, 0, 0.5],
                )

            # Prefiring vs Mjj
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['mjj_unpref_trigrules_L1FinalORBXmin2_barrelbarrel'],
                den = ['mjj_unpref_trigrules_barrelbarrel'],
                xtitle = 'M(j_{1}j_{2}) (GeV)',
                ytitle = 'Fraction of events passing L1FinalOR in BX-2',
                legendlabels = ['Unpref events (trig. rules)'],
                extralabel = '#splitline{'+eventselection+', |#eta(j_{1}, j_{2})|<1.3}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_mjj_unpref_L1FinalORBXmin2_barrelbarrel',
                axisranges = [1000, 6000, 0, 0.5],
                )

            # Prefiring vs Mjj
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['mjj_unpref_trigrules_L1FinalORBXmin1_endcapendcap', 'mjj_unpref_1stbx_L1FinalORBXmin1_endcapendcap'],
                den = ['mjj_unpref_trigrules_endcapendcap', 'mjj_unpref_1stbx_endcapendcap'],
                xtitle = 'M(j_{1}j_{2}) (GeV)',
                ytitle = 'Fraction of events passing L1FinalOR in BX-1',
                legendlabels = ['Unpref events (trig. rules)', 'Unpref events (1st bx)'],
                extralabel = '#splitline{'+eventselection+', |#eta(j_{1}, j_{2})|>1.3}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_mjj_unpref_L1FinalORBXmin1_endcapendcap',
                axisranges = [1000, 6000, 0, 0.5],
                )

            # Prefiring vs Mjj
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['mjj_unpref_trigrules_L1FinalORBXmin2_endcapendcap'],
                den = ['mjj_unpref_trigrules_endcapendcap'],
                xtitle = 'M(j_{1}j_{2}) (GeV)',
                ytitle = 'Fraction of events passing L1FinalOR in BX-2',
                legendlabels = ['Unpref events (trig. rules)'],
                extralabel = '#splitline{'+eventselection+', |#eta(j_{1}, j_{2})|>1.3}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_mjj_unpref_L1FinalORBXmin2_endcapendcap',
                axisranges = [1000, 6000, 0, 0.5],
                )


            

if __name__ == '__main__':
    main()





    


