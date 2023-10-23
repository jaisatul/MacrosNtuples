# make_ZToEE_plots.py, a program to draw the L1Studies plots obtained from the histograms extracted from NanoAOD

muselection='#geq 1 tight #mu (p_{{T}} > 25 GeV), pass HLT_IsoMu24'

import os
import yaml
import drawplots
import argparse

#Get absolute location of code packaage
topDir = os.getcwd().split('MacrosNtuples')[0]+'MacrosNtuples/'

def main():
    parser = argparse.ArgumentParser(
        description='''Plotter''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("-d", "--dir", dest="dir", help="The directory to read the inputs files from and draw the plots to", type=str, default='.')
    parser.add_argument("-i", "--input", dest="inputFile", help="Input file", type=str, default='all_PhotonJet.root')
    parser.add_argument("-c", "--config", dest="config", help="The YAML config to read from", type=str, default=topDir+'config_cards/full_PhotonJet.yaml')
    parser.add_argument("-l", "--lumi", dest="lumi", help="The integrated luminosity to display in the top right corner of the plot", type=str, default='')

    args = parser.parse_args()
    config = yaml.safe_load(open(args.config, 'r'))

    input_file = args.dir+'/'+args.inputFile
    if args.lumi != '':
        toplabel="#sqrt{s} = 13.6 TeV, L_{int} = " + args.lumi #+ " fb^{-1}"
    else:
        toplabel="#sqrt{s} = 13.6 TeV"

    # Some keyword arguments common to all figures:
    common_kwargs = {
            'inputFiles_list': [input_file],
            'saveplot': True,
            'dirname': args.dir+'/plotsL1Run3',
            'top_label': toplabel,
            }
    if not os.path.exists(args.dir+'/plotsL1Run3'):
        os.makedirs(args.dir+'/plotsL1Run3')

    suffixes = ['']
    if config['PU_plots']['make_histos']:
        bins = config['PU_plots']['nvtx_bins']
        suffixes += ['_nvtx{}to{}'.format(bins[i], bins[i+1]) for i in range(len(bins) - 1)]

    # NVTX distribution:
    drawplots.makedist(
            h1d = ['h_nvtx'],
            xtitle = 'N_{vtx}',
            ytitle = 'Events',
            plotname = 'L1Jet_FromEGamma_nvtx',
            **common_kwargs,
            )

    for s in suffixes:

        if config['TurnOns']:

            regions = [r for r in config['Regions']]
            eta_ranges = ["eta{}to{}".format(region[0], region[1]).replace(".","p") for region in config['Regions'].values()]
            eta_labels = ['{} #leq | #eta^{{e}}(reco)| < {}'.format(region[0], region[1]) for region in config['Regions'].values()]

            # Efficiency vs pT
            # comparison between eta regions
            for thr in [40., 180.]:
                drawplots.makeeff(
                    nvtx_suffix = s,
                    den = ['h_Jet_plots_{}'.format(eta_range) for eta_range in eta_ranges],
                    num = ['h_Jet_plots_{}_l1thrgeq{}'.format(eta_range, thr).replace(".", "p") for eta_range in eta_ranges],
                    xtitle = 'p_{T}^{jet}(reco) (GeV)',
                    ytitle = 'Efficiency',
                    legendlabels = eta_labels,
                    #axisranges = [0, 500],
                    extralabel = "#splitline{{#geq 1 tight #mu (p_{{T}} > 25 GeV), pass HLT_IsoMu24, p_{{T}}^{{jet}} > 30 GeV}}{{p_{{T}}^{{L1 jet}} #geq {} GeV}}".format(thr), 
                    setlogx = True,
                    plotname = 'L1Jet{}_FromEGamma_TurnOn_EtaComparison'.format(thr).replace(".", "p") ,
                    **common_kwargs,
                    )

                drawplots.makeeff(
                    nvtx_suffix = s,
                    den = ['h_Jet_plots_{}'.format(eta_range) for eta_range in eta_ranges],
                    num = ['h_Jet_plots_{}_l1thrgeq{}'.format(eta_range, thr).replace(".", "p") for eta_range in eta_ranges],
                    xtitle = 'p_{T}^{jet}(reco) (GeV)',
                    ytitle = 'Efficiency',
                    legendlabels = eta_labels,
                    axisranges = [0, 300],
                    extralabel = "#splitline{{#geq 1 tight #mu (p_{{T}} > 25 GeV), pass HLT_IsoMu24, p_{{T}}^{{jet}} > 30 GeV}}{{p_{{T}}^{{L1 jet}} #geq {} GeV}}".format(thr), 
                    #setlogx = True,
                    plotname = 'L1Jet{}_FromEGamma_TurnOn_EtaComparison_Zoom'.format(thr).replace(".", "p") ,
                    **common_kwargs,
                    )

        for r in config['Regions']:
            region = config['Regions'][r]
            eta_range = "eta{}to{}".format(region[0], region[1]).replace(".","p")
            eta_label = '{{{} #leq | #eta^{{e}}(reco)| < {}}}'.format(region[0], region[1])

            if config['Efficiency']:

                # Efficiency vs Run Number
                drawplots.makeeff(
                    nvtx_suffix = s,
                    den = ['h_PlateauEffVsRunNb_Denominator_Jet_plots_{}'.format(eta_range)],
                    num = ['h_PlateauEffVsRunNb_Numerator_Jet_plots_{}'.format(eta_range)],
                    xtitle = 'run number',
                    ytitle = 'Efficiency',
                    legendlabels = [],
                    extralabel = "#splitline{{#geq 1 tight #mu (p_{{T}} > 25 GeV), pass HLT_IsoMu24, p_{{T}}^{{jet}} > 30 GeV}}{}".format(eta_label),
                    plotname = "L1Jet_FromEGamma_EffVsRunNb_{}".format(r),
                    **common_kwargs,
                    )

            if config['TurnOns']:
                
                # Efficiency vs pT
                # all eta ranges and all qualities
                drawplots.makeeff(
                    nvtx_suffix = s,
                    den = ['h_Jet_plots_{}'.format(eta_range)],
                    num = ['h_Jet_plots_{}_l1thrgeq{}'.format(eta_range, thr).replace(".", "p") for thr in  config['Thresholds']],
                    xtitle = 'p_{T}^{jet}(reco) (GeV)',
                    ytitle = 'Efficiency',
                    legendlabels = ['p_{{T}}^{{L1 jet}} #geq {} GeV'.format(thr) for thr in config['Thresholds']],
                    #axisranges = [0, 500],
                    extralabel = "#splitline{{#geq 1 tight #mu (p_{{T}} > 25 GeV), pass HLT_IsoMu24, p_{{T}}^{{jet}} > 30 GeV}}{}".format(eta_label), 
                    setlogx = True,
                    plotname = 'L1Jet_FromEGamma_TurnOn_{}'.format(r) ,
                    **common_kwargs,
                    )

                # same thing, zoom on the 0 - 50 GeV region in pT
                drawplots.makeeff(
                    nvtx_suffix = s,
                    den = ['h_Jet_plots_{}'.format(eta_range)],
                    num = ['h_Jet_plots_{}_l1thrgeq{}'.format(eta_range, thr).replace(".", "p") for thr in  config['Thresholds']],
                    xtitle = 'p_{T}^{jet}(reco) (GeV)',
                    ytitle = 'Efficiency',
                    legendlabels = ['p_{{T}}^{{L1 jet}} #geq {} GeV'.format(thr) for thr in config['Thresholds']],
                    axisranges = [0, 300],
                    extralabel = "#splitline{{#geq 1 tight #mu (p_{{T}} > 25 GeV), pass HLT_IsoMu24, p_{{T}}^{{jet}} > 30 GeV}}{}".format(eta_label), 
                    #setlogx = True,
                    plotname = 'L1Jet_FromEGamma_TurnOn_{}_Zoom'.format(r) ,
                    **common_kwargs,
                    )

                # Comparisons between bins of PU:
                if config['PU_plots']['make_histos'] and s == '':
                    bins = config['PU_plots']['nvtx_bins']
                    for thr in config['PU_plots']['draw_thresholds']:
                        drawplots.makeeff(
                            den = ['h_Jet_plots_{}{}'.format(eta_range, suf) for suf in suffixes[1:]],
                            num = ['h_Jet_plots_{}_l1thrgeq{}{}'.format(eta_range, thr, suf).replace(".", "p") for suf in suffixes[1:]],
                            xtitle = 'p_{T}^{jet}(reco) (GeV)',
                            ytitle = 'Efficiency',
                            legendlabels = ['{} #leq nvtx < {}'.format(bins[i], bins[i+1]) for i in range(len(bins)-1)],
                            #axisranges = [3, 300],
                            extralabel = "#splitline{{#geq 1 tight #mu (p_{{T}} > 25 GeV), pass HLT_IsoMu24, p_{{T}}^{{jet}} > 30 GeV}}{}".format(eta_label), 
                            setlogx = True,
                            plotname = 'L1Jet{}_FromEGamma_TurnOn_{}_vsPU'.format(thr, r),
                            **common_kwargs,
                            )

        if config['Efficiency']:
            # Efficiency vs Eta Phi
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['h_L1Jet100vsEtaPhi_Numerator'],
                den = ['h_L1Jet100vsEtaPhi_EtaRestricted'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = '#phi^{jet}(reco)',
                ztitle = 'L1Jet50 efficiency',
                legendlabels = [''],
                extralabel = '#splitline{#geq 1 tight #mu (p_{T} > 25 GeV), pass HLT_IsoMu24}{p_{T}^{jet} > 30 GeV}',
                plotname = 'L1Jet_FromEGamma_EffVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 1.1],
                **common_kwargs,
                )

        if config['Prefiring']:

            # Postfiring vs Eta Phi
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['L1Jet100to150_bxplus1_etaphi'],
                den = ['L1Jet100to150_bx0_etaphi'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = '#phi^{jet}(reco)',
                ztitle = 'bx+1 / (bx0 or bx+1)',
                legendlabels = [''],
                extralabel = '#splitline{#geq 1 tight #mu (p_{T} > 25 GeV), pass HLT_IsoMu24}{p_{T}^{jet} > 30 GeV}',
                plotname = 'L1Jet_FromEGamma_PostfiringVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 1.1],
                addnumtoden = True,
                **common_kwargs,
                )

            # Prefiring vs Eta Phi
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['L1Jet100to150_bxmin1_etaphi'],
                den = ['L1Jet100to150_bx0_etaphi'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = '#phi^{jet}(reco)',
                ztitle = 'bx-1 / (bx0 or bx-1)',
                legendlabels = [''],
                extralabel = '#splitline{#geq 1 tight #mu (p_{T} > 25 GeV), pass HLT_IsoMu24}{p_{T}^{jet} > 30 GeV}',
                plotname = 'L1Jet_FromEGamma_PrefiringVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 1.1],
                addnumtoden = True,
                **common_kwargs,
                )

            # Postfiring vs Eta 
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['L1Jet100to150_bxplus1_eta'],
                den = ['L1Jet100to150_bx0_eta'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = 'bx+1 / (bx0 or bx+1)',
                legendlabels = [''],
                extralabel = '#splitline{#geq 1 tight #mu (p_{T} > 25 GeV), pass HLT_IsoMu24}{p_{T}^{jet} > 30 GeV}',
                plotname = 'L1Jet_FromEGamma_PostfiringVsEta',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = True,
                **common_kwargs,
                )

            # Prefiring vs Eta 
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['L1Jet100to150_bxmin1_eta'],
                den = ['L1Jet100to150_bx0_eta'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = 'bx-1 / (bx0 or bx-1)',
                legendlabels = [''],
                extralabel = '#splitline{#geq 1 tight #mu (p_{T} > 25 GeV), pass HLT_IsoMu24}{p_{T}^{jet} > 30 GeV}',
                plotname = 'L1Jet_FromEGamma_PrefiringVsEta',
                axisranges = [-5, 5, 0, 0.1],
                addnumtoden = True,
                **common_kwargs,
                )
        

        regions = config['Regions'].values()
        eta_ranges = ["eta{}to{}".format(region[0], region[1]).replace(".","p") for region in regions]
        eta_labels = ['{} #leq | #eta| < {}'.format(region[0], region[1]) for region in regions]

        if config['Response']:
            # Resolution Vs Pt
            drawplots.makeresol(
                nvtx_suffix = s,
                h2d = ['h_ResponseVsPt_Jet_plots_{}'.format(eta_range) for eta_range in eta_ranges],
                xtitle = 'p_{T}^{reco jet} (GeV)',
                ytitle = '(p_{T}^{L1 jet}/p_{T}^{reco jet})',
                #extralabel = '#splitline{Z#rightarrowee}{Non Iso.}',
                legend_pos = 'top',
                legendlabels = eta_labels,
                plotname = 'L1Jet_FromEGamma_ResponseVsPt',
                axisranges = [0, 200, 0.6, 1.5], 
                **common_kwargs,
                )

            # Resolution Vs RunNb
            drawplots.makeresol(
                nvtx_suffix = s,
                h2d = ['h_ResponseVsRunNb_Jet_plots_{}'.format(eta_range) for eta_range in eta_ranges],
                xtitle = 'run number',
                ytitle = '(p_{T}^{L1 jet}/p_{T}^{reco jet})',
                #extralabel = '#splitline{Z#rightarrowee}{Non Iso.}',
                legend_pos = 'top',
                legendlabels = eta_labels,
                plotname = 'L1Jet_FromEGamma_ResponseVsRunNb',
                axisranges = [355374, 362760, 0.7, 1.5],
                **common_kwargs,
                )

            drawplots.makeresol(
                nvtx_suffix = s,
                h2d = ['h_ResponseVsPt_big_bins_Jet_plots_{}'.format(eta_range) for eta_range in eta_ranges],
                xtitle = 'p_{T}^{reco jet} (GeV)',
                ytitle = '(p_{T}^{L1 jet}/p_{T}^{reco jet})',
                #extralabel = '#splitline{Z#rightarrowee}{Non Iso.}',
                legend_pos = 'top',
                legendlabels = eta_labels,
                plotname = 'L1Jet_FromEGamma_ResponseVsPt_big_bins',
                axisranges = [0, 200, 0.6, 1.5], 
                **common_kwargs,
                )

            # Zoomed version
#            drawplots.makeresol(
#                nvtx_suffix = s,
#                h2d = ['h_ResponseVsRunNb_Jet_plots_{}'.format(eta_range) for eta_range in eta_ranges],
#                xtitle = 'run number',
#                ytitle = '(p_{T}^{L1 jet}/p_{T}^{reco jet})',
#                #extralabel = '#splitline{Z#rightarrowee}{Non Iso.}',
#                legend_pos = 'top',
#                legendlabels = eta_labels,
#                plotname = 'L1Jet_FromEGamma_ResponseVsRunNb_Zoom',
#                axisranges = [355374, 362760, 0.8, 1.1],
#                **common_kwargs,
#                )

        # Pt Balance plots

        if config['PtBalance']:

            drawplots.makeprof(
                nvtx_suffix = s,
                h2d = ['h_L1PtBalanceVsRunNb_{}'.format(eta_range) for eta_range in eta_ranges],
                xtitle = 'run number',
                ytitle = '(p_{T}^{L1 jet}/p_{T}^{reco #gamma})',
                extralabel = "#splitline{$selection_label, PFMET<50 GeV}{p_{T}^{jet} > 30 GeV, #Delta#phi(#gamma, jet) > 2.9}",
                legendlabels = eta_labels,
                axisranges = [320673, 325173, 0, 1.5],
                plotname = 'L1Jet_FromEGamma_PtBalancevsRun',
                **common_kwargs,
                )

            drawplots.makeprof(
                nvtx_suffix = s,
                h2d = ['h_L1PtBalanceVsRunNb_singlejet_{}'.format(eta_range) for eta_range in eta_ranges],
                xtitle = 'run number',
                ytitle = '(p_{T}^{L1 jet}/p_{T}^{reco #gamma})',
                extralabel = "#splitline{$selection_label, PFMET<50 GeV}{= 1 clean jet, p_{T}^{jet} > 30 GeV, #Delta#phi(#gamma, jet) > 2.9}",
                legendlabels = eta_labels,
                axisranges = [320673, 325173, 0, 1.5],
                plotname = 'L1Jet_FromEGamma_PtBalancevsRun_singlejet',
                **common_kwargs,
                )

if __name__ == '__main__':
    main()
