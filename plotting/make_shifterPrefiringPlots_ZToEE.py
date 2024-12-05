# make_ZToEE_plots.py, a program to draw the L1Studies plots obtained from the histograms extracted from NanoAOD
eventselection='Z#rightarrow ee'
subfolder='/shifterprefiringplots'
channelname='ZToEE'

import yaml
import drawplots
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='''Plotter''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("-d", "--dir", dest="dir", help="The directory to read the inputs files from and draw the plots to", type=str, default='./')
    parser.add_argument("-c", "--config", dest="config", help="The YAML config to read from", type=str, default='../config_cards/full_ZToEE.yaml')
    parser.add_argument("-l", "--lumi", dest="lumi", help="The integrated luminosity to display in the top right corner of the plot", type=str, default='')
    parser.add_argument("-e", "--era", dest="era", help="Label to mark the era", type=str, default='')

    args = parser.parse_args()
    config = yaml.safe_load(open(args.config, 'r'))

    input_file = args.dir + "/all_ZToEE_" +  args.era + ".root"
    # if args.lumi != '':
    #     toplabel="#sqrt{s} = 13.6 TeV, L_{int} = " + args.lumi #+ " fb^{-1}"
    # else:
    #     toplabel="#sqrt{s} = 13.6 TeV"
    toplabel= "#sqrt{s} = 13.6 TeV, " +  args.lumi
    suffixes = ['']
    if config['PU_plots']['make_histos']:
        bins = config['PU_plots']['nvtx_bins']
        suffixes += ['_nvtx{}to{}'.format(bins[i], bins[i+1]) for i in range(len(bins) - 1)]

    
    for s in suffixes:

        if config['Prefiring']:

            # Prefiring vs Eta (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_eta'],
                den = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_Denominator_eta'],
                xtitle = '#eta^{e}(reco)',
                ytitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}(e)>25 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname + '_L1EG_UnprefireableEvent_FirstBxInTrain_PrefiringVsEta',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta (UnprefireableEvent_TriggerRules)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_TriggerRules_bxmin1_eta'],
                den = ['L1EG20_L1_UnprefireableEvent_TriggerRules_Denominator_eta'],
                xtitle = '#eta^{e}(reco)',
                ytitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}(e)>25 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname + '_L1EG_UnprefireableEvent_TriggerRules_PrefiringVsEta',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )


            # Prefiring vs Runnb (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_runnb'],
                den = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_Denominator_runnb'],
                xtitle = 'Run number',
                ytitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}(e)>25 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname + '_L1EG_UnprefireableEvent_FirstBxInTrain_PrefiringVsRunnb',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Runnb (UnprefireableEvent_TriggerRules)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_TriggerRules_bxmin1_runnb'],
                den = ['L1EG20_L1_UnprefireableEvent_TriggerRules_Denominator_runnb'],
                xtitle = 'Run number',
                ytitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}(e)>25 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname + '_L1EG_UnprefireableEvent_TriggerRules_PrefiringVsRunnb',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )


            # Prefiring vs Eta Phi (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_etaphi'],
                den = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_Denominator_etaphi'],
                xtitle = '#eta^{e}(reco)',
                ytitle = '#phi^{e}(reco)',
                ztitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}(e)>25 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname + '_L1EG_UnprefireableEvent_FirstBxInTrain_PrefiringVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta Phi (UnprefireableEvent_TriggerRules)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_TriggerRules_bxmin1_etaphi'],
                den = ['L1EG20_L1_UnprefireableEvent_TriggerRules_Denominator_etaphi'],
                xtitle = '#eta^{e}(reco)',
                ytitle = '#phi^{e}(reco)',
                ztitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}(e)>25 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname + '_L1EG_UnprefireableEvent_TriggerRules_PrefiringVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta Pt (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_etapt'],
                den = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_Denominator_etapt'],
                xtitle = '#eta^{e}(reco)',
                ytitle = 'p_{T}^{e}(reco)',
                ztitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}(e)>25 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname + '_L1EG_UnprefireableEvent_FirstBxInTrain_PrefiringVsEtaPt',
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
                num = ['L1EG20_L1_UnprefireableEvent_TriggerRules_bxmin1_etapt'],
                den = ['L1EG20_L1_UnprefireableEvent_TriggerRules_Denominator_etapt'],
                xtitle = '#eta^{e}(reco)',
                ytitle = 'p_{T}^{e}(reco)',
                ztitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}(e)>25 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname + '_L1EG_UnprefireableEvent_TriggerRules_PrefiringVsEtaPt',
                axisranges = [-5, 5, 50, 4000, 0, 0.1],
                addnumtoden = False,
                setlogy = True,
                )


            # Prefiring vs M(ll)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['mll_unpref_trigrules_L1FinalORBXmin1_barrelbarrel', 'mll_unpref_1stbx_L1FinalORBXmin1_barrelbarrel'],
                den = ['mll_unpref_trigrules_barrelbarrel', 'mll_unpref_1stbx_barrelbarrel'],
                xtitle = 'M(e_{1}e_{2}) (GeV)',
                ytitle = 'Fraction of events passing L1FinalOR in BX-1',
                legendlabels = ['Unpref events (trig. rules)', 'Unpref events (1st bx)'],
                extralabel = '#splitline{'+eventselection+', |#eta(e_{1}, e_{2})|<1.479}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname + '_mll_unpref_L1FinalORBXmin1_barrelbarrel',
                axisranges = [50, 3000, 0, 0.1],
                )

            # Prefiring vs M(ll)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['mll_unpref_trigrules_L1FinalORBXmin2_barrelbarrel'],
                den = ['mll_unpref_trigrules_barrelbarrel'],
                xtitle = 'M(e_{1}e_{2}) (GeV)',
                ytitle = 'Fraction of events passing L1FinalOR in BX-2',
                legendlabels = ['Unpref events (trig. rules)'],
                extralabel = '#splitline{'+eventselection+', |#eta(e_{1}, e_{2})|<1.479}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname + '_mll_unpref_L1FinalORBXmin2_barrelbarrel',
                axisranges = [50, 3000, 0, 0.1],
                )

            # Prefiring vs M(ll)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['mll_unpref_trigrules_L1FinalORBXmin1_endcapendcap', 'mll_unpref_1stbx_L1FinalORBXmin1_endcapendcap'],
                den = ['mll_unpref_trigrules_endcapendcap', 'mll_unpref_1stbx_endcapendcap'],
                xtitle = 'M(e_{1}e_{2}) (GeV)',
                ytitle = 'Fraction of events passing L1FinalOR in BX-1',
                legendlabels = ['Unpref events (trig. rules)', 'Unpref events (1st bx)'],
                extralabel = '#splitline{'+eventselection+', |#eta(e_{1}, e_{2})|>1.479}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname + '_mll_unpref_L1FinalORBXmin1_endcapendcap',
                axisranges = [50, 3000, 0, 0.1],
                )

            # Prefiring vs M(ll)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['mll_unpref_trigrules_L1FinalORBXmin2_endcapendcap'],
                den = ['mll_unpref_trigrules_endcapendcap'],
                xtitle = 'M(e_{1}e_{2}) (GeV)',
                ytitle = 'Fraction of events passing L1FinalOR in BX-2',
                legendlabels = ['Unpref events (trig. rules)'],
                extralabel = '#splitline{'+eventselection+', |#eta(e_{1}, e_{2})|>1.479}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname + '_mll_unpref_L1FinalORBXmin2_endcapendcap',
                axisranges = [50, 3000, 0, 0.1],
                )


            # Prefiring vs Eta (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_eta_fwd'],
                den = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_Denominator_eta_fwd'],
                xtitle = '#eta^{e}(reco)',
                ytitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}(e)>25 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname + '_L1EG_UnprefireableEvent_FirstBxInTrain_PrefiringVsEta_Fwd',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta (UnprefireableEvent_TriggerRules)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_TriggerRules_bxmin1_eta_fwd'],
                den = ['L1EG20_L1_UnprefireableEvent_TriggerRules_Denominator_eta_fwd'],
                xtitle = '#eta^{e}(reco)',
                ytitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}(e)>25 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname + '_L1EG_UnprefireableEvent_TriggerRules_PrefiringVsEta_Fwd',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta Phi (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_etaphi_fwd'],
                den = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_Denominator_etaphi_fwd'],
                xtitle = '#eta^{e}(reco)',
                ytitle = '#phi^{e}(reco)',
                ztitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}(e)>25 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname + '_L1EG_UnprefireableEvent_FirstBxInTrain_PrefiringVsEtaPhi_Fwd',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta Phi (UnprefireableEvent_TriggerRules)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_TriggerRules_bxmin1_etaphi_fwd'],
                den = ['L1EG20_L1_UnprefireableEvent_TriggerRules_Denominator_etaphi_fwd'],
                xtitle = '#eta^{e}(reco)',
                ytitle = '#phi^{e}(reco)',
                ztitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}(e)>25 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname + '_L1EG_UnprefireableEvent_TriggerRules_PrefiringVsEtaPhi_Fwd',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 0.1],
                addnumtoden = False,
                )


            # Prefiring vs Eta Pt (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_etapt_fwd'],
                den = ['L1EG20_L1_UnprefireableEvent_FirstBxInTrain_Denominator_etapt_fwd'],
                xtitle = '#eta^{e}(reco)',
                ytitle = 'p_{T}^{e}(reco)',
                ztitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}(e)>25 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname + '_L1EG_UnprefireableEvent_FirstBxInTrain_PrefiringVsEtaPt_Fwd',
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
                num = ['L1EG20_L1_UnprefireableEvent_TriggerRules_bxmin1_etapt_fwd'],
                den = ['L1EG20_L1_UnprefireableEvent_TriggerRules_Denominator_etapt_fwd'],
                xtitle = '#eta^{e}(reco)',
                ytitle = 'p_{T}^{e}(reco)',
                ztitle = 'L1EG20 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}(e)>25 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname + '_L1EG_UnprefireableEvent_TriggerRules_PrefiringVsEtaPt_Fwd',
                axisranges = [-5, 5, 50, 4000, 0, 0.1],
                addnumtoden = False,
                setlogy = True,
                )


def label(iso):
    labels = {
            'EGNonIso': 'Non iso',
            'EGLooseIso': 'Loose iso',
            'EGTightIso': 'Tight iso',
            }

    if iso in labels:
        return(labels[iso])
    else:
        return('')

if __name__ == '__main__':
    main()