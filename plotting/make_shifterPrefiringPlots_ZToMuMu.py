# make_mu_plots.py, a program to draw the L1Studies plots obtained from the histograms extracted from NanoAOD
eventselection='Z#rightarrow #mu#mu'
subfolder='/shifterprefiringplots'
channelname='ZToMuMu'

import yaml
import drawplots
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='''Plotter''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("-d", "--dir", dest="dir", help="The directory to read the inputs files from and draw the plots to", type=str, default='./')
    parser.add_argument("-c", "--config", dest="config", help="The YAML config to read from", type=str, default='../config_cards/full_ZToMuMu.yaml')
    parser.add_argument("-l", "--lumi", dest="lumi", help="The integrated luminosity to display in the top right corner of the plot", type=str, default='')

    args = parser.parse_args()
    config = yaml.safe_load(open(args.config, 'r'))

    input_file = args.dir + "/all_ZToMuMu.root"
    if args.lumi != '':
        toplabel="#sqrt{s} = 13.6 TeV, L_{int} = " + args.lumi #+ " fb^{-1}"
    else:
        toplabel="#sqrt{s} = 13.6 TeV"

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
                num = ['L1Mu10_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_eta'],
                den = ['L1Mu10_L1_UnprefireableEvent_FirstBxInTrain_Denominator_eta'],
                xtitle = '#eta^{#mu}(reco)',
                ytitle = 'L1Mu10 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{#mu}(reco) > 20 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname+'_L1Mu_UnprefireableEvent_FirstBxInTrain_PrefiringVsEta',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta (UnprefireableEvent_TriggerRules)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Mu10_L1_UnprefireableEvent_TriggerRules_bxmin1_eta'],
                den = ['L1Mu10_L1_UnprefireableEvent_TriggerRules_Denominator_eta'],
                xtitle = '#eta^{#mu}(reco)',
                ytitle = 'L1Mu10 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{#mu}(reco) > 20 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_L1Mu_UnprefireableEvent_TriggerRules_PrefiringVsEta',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )


            # Prefiring vs RunNb (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Mu10_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_runnb'],
                den = ['L1Mu10_L1_UnprefireableEvent_FirstBxInTrain_Denominator_runnb'],
                xtitle = 'Run number',
                ytitle = 'L1Mu10 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{#mu}(reco) > 20 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname+'_L1Mu_UnprefireableEvent_FirstBxInTrain_PrefiringVsRunNb',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs RunNb (UnprefireableEvent_TriggerRules)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Mu10_L1_UnprefireableEvent_TriggerRules_bxmin1_runnb'],
                den = ['L1Mu10_L1_UnprefireableEvent_TriggerRules_Denominator_runnb'],
                xtitle = 'Run number',
                ytitle = 'L1Mu10 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{#mu}(reco) > 20 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_L1Mu_UnprefireableEvent_TriggerRules_PrefiringVsRunNb',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = False,
                )


            # Prefiring vs Eta Phi (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Mu10_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_etaphi'],
                den = ['L1Mu10_L1_UnprefireableEvent_FirstBxInTrain_Denominator_etaphi'],
                xtitle = '#eta^{#mu}(reco)',
                ytitle = '#phi^{#mu}(reco)',
                ztitle = 'L1Mu10 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{#mu}(reco) > 20 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname+'_L1Mu_UnprefireableEvent_FirstBxInTrain_PrefiringVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta Phi (UnprefireableEvent_TriggerRules)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Mu10_L1_UnprefireableEvent_TriggerRules_bxmin1_etaphi'],
                den = ['L1Mu10_L1_UnprefireableEvent_TriggerRules_Denominator_etaphi'],
                xtitle = '#eta^{#mu}(reco)',
                ytitle = '#phi^{#mu}(reco)',
                ztitle = 'L1Mu10 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{#mu}(reco) > 20 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_L1Mu_UnprefireableEvent_TriggerRules_PrefiringVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 0.1],
                addnumtoden = False,
                )

            # Prefiring vs Eta Pt (UnprefireableEvent_FirstBxInTrain)
            drawplots.makeeff(
                inputFiles_list = [input_file],
                saveplot = True,
                dirname = args.dir + subfolder,
                nvtx_suffix = s,
                num = ['L1Mu10_L1_UnprefireableEvent_FirstBxInTrain_bxmin1_etapt'],
                den = ['L1Mu10_L1_UnprefireableEvent_FirstBxInTrain_Denominator_etapt'],
                xtitle = '#eta^{#mu}(reco)',
                ytitle = 'p_{T}^{jet}(reco)',
                ztitle = 'L1Mu10 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{#mu}(reco) > 20 GeV}{Unpref. events (1st bx in train)}',
                top_label = toplabel,
                plotname = channelname+'_L1Mu_UnprefireableEvent_FirstBxInTrain_PrefiringVsEtaPt',
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
                num = ['L1Mu10_L1_UnprefireableEvent_TriggerRules_bxmin1_etapt'],
                den = ['L1Mu10_L1_UnprefireableEvent_TriggerRules_Denominator_etapt'],
                xtitle = '#eta^{#mu}(reco)',
                ytitle = 'p_{T}^{jet}(reco)',
                ztitle = 'L1Mu10 (BX-1) matching fraction',
                legendlabels = [''],
                extralabel = '#splitline{'+eventselection+', p_{T}^{#mu}(reco) > 20 GeV}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_L1Mu_UnprefireableEvent_TriggerRules_PrefiringVsEtaPt',
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
                xtitle = 'M(#mu_{1}#mu_{2}) (GeV)',
                ytitle = 'Fraction of events passing L1FinalOR in BX-1',
                legendlabels = ['Unpref events (trig. rules)', 'Unpref events (1st bx)'],
                extralabel = '#splitline{'+eventselection+', |#eta(#mu_{1}, #mu_{2})|<1.24}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_mll_unpref_L1FinalORBXmin1_barrelbarrel',
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
                xtitle = 'M(#mu_{1}#mu_{2}) (GeV)',
                ytitle = 'Fraction of events passing L1FinalOR in BX-2',
                legendlabels = ['Unpref events (trig. rules)'],
                extralabel = '#splitline{'+eventselection+', |#eta(#mu_{1}, #mu_{2})|<1.24}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_mll_unpref_L1FinalORBXmin2_barrelbarrel',
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
                xtitle = 'M(#mu_{1}#mu_{2}) (GeV)',
                ytitle = 'Fraction of events passing L1FinalOR in BX-1',
                legendlabels = ['Unpref events (trig. rules)', 'Unpref events (1st bx)'],
                extralabel = '#splitline{'+eventselection+', |#eta(#mu_{1}, #mu_{2})|>1.24}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_mll_unpref_L1FinalORBXmin1_endcapendcap',
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
                xtitle = 'M(#mu_{1}#mu_{2}) (GeV)',
                ytitle = 'Fraction of events passing L1FinalOR in BX-2',
                legendlabels = ['Unpref events (trig. rules)'],
                extralabel = '#splitline{'+eventselection+', |#eta(#mu_{1}, #mu_{2})|>1.24}{Unpref. events (trig. rules)}',
                top_label = toplabel,
                plotname = channelname+'_mll_unpref_L1FinalORBXmin2_endcapendcap',
                axisranges = [50, 3000, 0, 0.1],
                )

def label(qual):
    labels = {
            'AllQual': 'All qual.',
            'Qual8': 'Qual. #geq 8',
            'Qual12': 'Qual. #geq 12',
            }

    if qual in labels:
        return(labels[qual])
    else:
        return('')

if __name__ == '__main__':
    main()
