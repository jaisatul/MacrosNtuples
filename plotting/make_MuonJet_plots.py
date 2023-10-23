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
    
    parser.add_argument("-d", "--dir", dest="dir", help="The directory to read the inputs files from and draw the plots to", type=str, default='./')
    parser.add_argument("-c", "--config", dest="config", help="The YAML config to read from", type=str, default=topDir+'config_cards/full_MuonJet.yaml')
    parser.add_argument("-l", "--lumi", dest="lumi", help="The integrated luminosity to display in the top right corner of the plot", type=str, default='')

    args = parser.parse_args()
    config = yaml.safe_load(open(args.config, 'r'))

    input_file = args.dir + "/all_MuonJet.root"
    if args.lumi != '':
        toplabel="#sqrt{s} = 13.6 TeV, L_{int} = " + args.lumi #+ " fb^{-1}"
    else:
        toplabel="#sqrt{s} = 13.6 TeV"

    # Some keyword arguments common to all figures:
    common_kwargs = {
            'inputFiles_list': [input_file],
            'saveplot': True,
            'dirname': args.dir + '/plotsL1Run3',
            'top_label': toplabel,
            }

    suffixes = ['']
    if config['PU_plots']['make_histos']:
        bins = config['PU_plots']['nvtx_bins']
        suffixes += ['_nvtx{}to{}'.format(bins[i], bins[i+1]) for i in range(len(bins) - 1)]

    # NVTX distribution:
    drawplots.makedist(
            h1d = ['h_nvtx'],
            xtitle = 'N_{vtx}',
            ytitle = 'Events',
            plotname = 'L1Jet_FromSingleMuon_nvtx',
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

                TurnOn_kwargs = {
                        'nvtx_suffix': s,
                        'den': ['h_Jet_plots_{}'.format(eta_range) for eta_range in eta_ranges],
                        'num': ['h_Jet_plots_{}_l1thrgeq{}'.format(eta_range, thr).replace(".", "p") for eta_range in eta_ranges],
                        'xtitle': 'p_{T}^{jet}(reco) (GeV)',
                        'ytitle': 'Efficiency',
                        'legendlabels': eta_labels,
                        'extralabel': "#splitline{{#geq 1 tight #mu (p_{{T}} > 25 GeV), pass HLT_IsoMu24, p_{{T}}^{{jet}} > 30 GeV}}{{p_{{T}}^{{L1 jet}} #geq {} GeV}}".format(thr), 
                        }

                drawplots.makeeff(
                    #axisranges = [0, 500],
                    setlogx = True,
                    plotname = 'L1Jet{}_FromSingleMuon_TurnOn_EtaComparison'.format(thr).replace(".", "p") ,
                    **TurnOn_kwargs, **common_kwargs,
                    )

                drawplots.makeeff(
                    axisranges = [0, 300],
                    #setlogx = True,
                    plotname = 'L1Jet{}_FromSingleMuon_TurnOn_EtaComparison_Zoom'.format(thr).replace(".", "p") ,
                    **TurnOn_kwargs, **common_kwargs,
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
                    plotname = "L1Jet_FromSingleMuon_EffVsRunNb_{}".format(r),
                    **common_kwargs,
                    )

            if config['TurnOns']:

                TurnOn_kwargs = {
                        'nvtx_suffix': s,
                        'den': ['h_Jet_plots_{}'.format(eta_range)],
                        'num': ['h_Jet_plots_{}_l1thrgeq{}'.format(eta_range, thr).replace(".", "p") for thr in  config['Thresholds']],
                        'xtitle': 'p_{T}^{jet}(reco) (GeV)',
                        'ytitle': 'Efficiency',
                        'legendlabels': ['p_{{T}}^{{L1 jet}} #geq {} GeV'.format(thr) for thr in config['Thresholds']],
                        'extralabel': "#splitline{{#geq 1 tight #mu (p_{{T}} > 25 GeV), pass HLT_IsoMu24, p_{{T}}^{{jet}} > 30 GeV}}{}".format(eta_label), 
                        }

                # Efficiency vs pT
                # all eta ranges and all qualities
                drawplots.makeeff(
                    #axisranges = [0, 500],
                    setlogx = True,
                    plotname = 'L1Jet_FromSingleMuon_TurnOn_{}'.format(r) ,
                    **TurnOn_kwargs, **common_kwargs,
                    )

                # same thing, zoom on the 0 - 50 GeV region in pT
                drawplots.makeeff(
                    axisranges = [0, 300],
                    #setlogx = True,
                    plotname = 'L1Jet_FromSingleMuon_TurnOn_{}'.format(r) ,
                    **TurnOn_kwargs, **common_kwargs,
                    )

                # Comparisons between bins of PU:
                if config['PU_plots']['make_histos'] and s == '':
                    bins = config['PU_plots']['nvtx_bins']
                    for thr in config['PU_plots']['draw_thresholds']:

                        TurnOn_kwargs = {
                                'den': ['h_Jet_plots_{}{}'.format(eta_range, suf) for suf in suffixes[1:]],
                                'num': ['h_Jet_plots_{}_l1thrgeq{}{}'.format(eta_range, thr, suf).replace(".", "p") for suf in suffixes[1:]],
                                'xtitle': 'p_{T}^{jet}(reco) (GeV)',
                                'ytitle': 'Efficiency',
                                'legendlabels': ['{} #leq nvtx < {}'.format(bins[i], bins[i+1]) for i in range(len(bins)-1)],
                                'extralabel': "#splitline{{#geq 1 tight #mu (p_{{T}} > 25 GeV), pass HLT_IsoMu24, p_{{T}}^{{jet}} > 30 GeV}}{}".format(eta_label), 
                                }

                        drawplots.makeeff(
                            #axisranges = [3, 300],
                            setlogx = True,
                            plotname = 'L1Jet{}_FromSingleMuon_TurnOn_{}_vsPU'.format(thr, r),
                            **TurnOn_kwargs, **common_kwargs,
                            )

                        drawplots.makeeff(
                            axisranges = [0, 300],
                            setlogx = True,
                            plotname = 'L1Jet{}_FromSingleMuon_TurnOn_{}_vsPU_Zoom'.format(thr, r),
                            **TurnOn_kwargs, **common_kwargs,
                            )


        if config['Efficiency']:
            # Efficiency vs Eta Phi
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['h_L1Jet50vsEtaPhi_Numerator'],
                den = ['h_L1Jet50vsEtaPhi_EtaRestricted'],
                xtitle = '#eta^{jet}(reco)',
                ytitle = '#phi^{jet}(reco)',
                ztitle = 'L1Jet50 efficiency',
                legendlabels = [''],
                extralabel = '#splitline{#geq 1 tight #mu (p_{T} > 25 GeV), pass HLT_IsoMu24}{p_{T}^{jet} > 30 GeV}',
                plotname = 'L1Jet_FromSingleMuon_EffVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 1.1],
                **common_kwargs,
                )

        if config['Prefiring']:

            pre_post_firing_kwargs = {
                    'nvtx_suffix': s,
                    'xtitle': '#eta^{jet}(reco)',
                    'legendlabels': [''],
                    'extralabel': '#splitline{#geq 1 tight #mu (p_{T} > 25 GeV), pass HLT_IsoMu24}{p_{T}^{jet} > 30 GeV}',
                    'addnumtoden': True,
                    }
            # Postfiring vs Eta Phi
            drawplots.makeeff(
                num = ['L1Jet100to150_bxplus1_etaphi'],
                den = ['L1Jet100to150_bx0_etaphi'],
                ytitle = '#phi^{jet}(reco)',
                ztitle = 'bx+1 / (bx0 or bx+1)',
                plotname = 'L1Jet_FromSingleMuon_PostfiringVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 1.1],
                **pre_post_firing_kwargs, **common_kwargs,
                )

            # Prefiring vs Eta Phi
            drawplots.makeeff(
                num = ['L1Jet100to150_bxmin1_etaphi'],
                den = ['L1Jet100to150_bx0_etaphi'],
                ytitle = '#phi^{jet}(reco)',
                ztitle = 'bx-1 / (bx0 or bx-1)',
                plotname = 'L1Jet_FromSingleMuon_PrefiringVsEtaPhi',
                axisranges = [-5, 5, -3.1416, 3.1416, 0, 1.1],
                **pre_post_firing_kwargs, **common_kwargs,
                )

            # Postfiring vs Eta 
            drawplots.makeeff(
                num = ['L1Jet100to150_bxplus1_eta'],
                den = ['L1Jet100to150_bx0_eta'],
                ytitle = 'bx+1 / (bx0 or bx+1)',
                plotname = 'L1Jet_FromSingleMuon_PostfiringVsEta',
                axisranges = [-5, 5, 0, 0.1],
                **pre_post_firing_kwargs, **common_kwargs,
                )

            # Prefiring vs Eta 
            drawplots.makeeff(
                num = ['L1Jet100to150_bxmin1_eta'],
                den = ['L1Jet100to150_bx0_eta'],
                ytitle = 'bx-1 / (bx0 or bx-1)',
                plotname = 'L1Jet_FromSingleMuon_PrefiringVsEta',
                axisranges = [-5, 5, 0, 0.1],
                **pre_post_firing_kwargs, **common_kwargs,
                )
        

        if config['Response']:

            regions = config['Regions'].values()
            eta_ranges = ["eta{}to{}".format(region[0], region[1]).replace(".","p") for region in regions]
            eta_labels = ['{} #leq | #eta| < {}'.format(region[0], region[1]) for region in regions]

            # Resolution Vs Pt
            drawplots.makeresol(
                nvtx_suffix = s,
                h2d = ['h_ResponseVsPt_Jet_plots_{}'.format(eta_range) for eta_range in eta_ranges],
                xtitle = 'p_{T}^{reco jet} (GeV)',
                ytitle = '(p_{T}^{L1 jet}/p_{T}^{reco jet})',
                #extralabel = '#splitline{Z#rightarrowee}{Non Iso.}',
                legend_pos = 'top',
                legendlabels = eta_labels,
                plotname = 'L1Jet_FromSingleMuon_ResponseVsPt',
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
                plotname = 'L1Jet_FromSingleMuon_ResponseVsRunNb',
                axisranges = [355374, 362760, 0.7, 1.5],
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
#                plotname = 'L1Jet_FromSingleMuon_ResponseVsRunNb_Zoom',
#                axisranges = [355374, 362760, 0.8, 1.1],
#                **common_kwargs,
#                )

        # MET plots

        if config['MET_plots']:

            extralabel='#splitline{#geq 1 tight #mu (p_{T} > 27 GeV), pass HLT_IsoMu24}{#geq 1 jet (p_{T} > 30 GeV, 0 #leq |#eta| < 5)}'

            MET_kwargs = {
                'nvtx_suffix': s,
                'ytitle': 'Efficiency',
                'extralabel': extralabel,
                }

            ###

            HLTMET120_kwargs = {
                'num': ['h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight'],
                'den': ['h_MetNoMu_Denominator'],
                'legendlabels': ['PFMHTNoMu120'],
                'xtitle': 'PFMET(#mu subtracted) (GeV)',
                }

            drawplots.makeeff(
                axisranges = [0., 2000.],
                plotname = 'L1ETSum_FromSingleMuon_HLTMET120_TurnOn',
                **HLTMET120_kwargs, **MET_kwargs, **common_kwargs,
                )

            drawplots.makeeff(
                axisranges = [0., 400.],
                plotname = 'L1ETSum_FromSingleMuon_HLTMET120_TurnOn_Zoom',
                **HLTMET120_kwargs, **MET_kwargs, **common_kwargs,
                )

            ###

            HLT1050_kwargs = {
                'num': ['h_HLT_PFHT1050'],
                'den': ['h_HT_Denominator'],
                'legendlabels': ['PFHT1050'],
                'xtitle': 'HT=#sum(p_{T}^{jets}(p_{T}>30 GeV, 0<|#eta|<2.5)) (GeV)',
                }

            drawplots.makeeff(
                axisranges = [0., 2000.],
                plotname = 'L1ETSum_FromSingleMuon_HLT1050_TurnOn',
                **HLT1050_kwargs, **MET_kwargs, **common_kwargs,
                )

            drawplots.makeeff(
                axisranges = [0., 400.],
                plotname = 'L1ETSum_FromSingleMuon_HLT1050_TurnOn_Zoom',
                **HLT1050_kwargs, **MET_kwargs, **common_kwargs,
                )

            ###

            ETMHF_kwargs = {
                'num': ['h_MetNoMu_ETMHF80', 'h_MetNoMu_ETMHF90', 'h_MetNoMu_ETMHF100'],
                'den': ['h_MetNoMu_Denominator'],
                'legendlabels': ['ETMHF80', 'ETMHF90', 'ETMHF100'],
                'xtitle': 'PFMET(#mu subtracted) (GeV)',
                }

            drawplots.makeeff(
                axisranges = [0., 2000.],
                plotname = 'L1ETSum_FromSingleMuon_ETMHF_TurnOn',
                **ETMHF_kwargs, **MET_kwargs, **common_kwargs,
                )

            drawplots.makeeff(
                axisranges = [0., 400.],
                plotname = 'L1ETSum_FromSingleMuon_ETMHF_TurnOn_Zoom',
                **ETMHF_kwargs, **MET_kwargs, **common_kwargs,
                )

            ### 

            HTT_kwargs = {
                'num': ['h_HT_L1_HTT200er', 'h_HT_L1_HTT280er', 'h_HT_L1_HTT360er'],
                'den': ['h_HT_Denominator'],
                'legendlabels': ['HTT200er', 'HTT280er', 'HTT360er'],
                'xtitle': 'HT=#sum(p_{T}^{jets}(p_{T}>30 GeV, 0<=|#eta|<2.5)) (GeV)',
                }

            drawplots.makeeff(
                axisranges = [0., 3000.],
                plotname = 'L1ETSum_FromSingleMuon_HTT_TurnOn',
                **HTT_kwargs, **MET_kwargs, **common_kwargs,
                )

            drawplots.makeeff(
                axisranges = [0., 1000.],
                plotname = 'L1ETSum_FromSingleMuon_HTT_TurnOn_Zoom',
                **HTT_kwargs, **MET_kwargs, **common_kwargs,
                )

            # Comparisons between bins of PU:
            if config['PU_plots']['make_histos'] and s == '':
                bins = config['PU_plots']['nvtx_bins']

                MET_PU_kwargs = {
                    'ytitle': 'Efficiency',
                    'legendlabels': ['{} #leq nvtx < {}'.format(bins[i], bins[i+1]) for i in range(len(bins)-1)],
                    }

                ###

                HLTMET120_kwargs = {
                    'num': ['h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight{}'.format(suf) for suf in suffixes[1:]],
                    'den': ['h_MetNoMu_Denominator{}'.format(suf) for suf in suffixes[1:]],
                    'xtitle': 'PFMET(#mu subtracted) (GeV)',
                    'extralabel': '#splitline{#geq 1 tight #mu (p_{T} > 27 GeV), pass HLT_IsoMu24}{#geq 1 jet (p_{T} > 30 GeV, 0 #leq |#eta| < 5), PFMHTNoMu120}',
                    }

                drawplots.makeeff(
                    axisranges = [0, 2000],
                    plotname = 'L1ETSum_FromSingleMuon_HLTMET120_TurnOn_vsPU',
                    **HLTMET120_kwargs, **MET_PU_kwargs, **common_kwargs,
                    )

                drawplots.makeeff(
                    axisranges = [0, 400],
                    plotname = 'L1ETSum_FromSingleMuon_HLTMET120_TurnOn_vsPU_Zoom',
                    **HLTMET120_kwargs, **MET_PU_kwargs, **common_kwargs,
                    )

                ###

                HLT1050_kwargs = {
                    'num': ['h_HLT_PFHT1050{}'.format(suf) for suf in suffixes[1:]],
                    'den': ['h_HT_Denominator{}'.format(suf) for suf in suffixes[1:]],
                    'xtitle': 'HT=#sum(p_{T}^{jets}(p_{T}>30 GeV, 0<|#eta|<2.5)) (GeV)',
                    'extralabel': '#splitline{#geq 1 tight #mu (p_{T} > 27 GeV), pass HLT_IsoMu24}{#geq 1 jet (p_{T} > 30 GeV, 0 #leq |#eta| < 5), PFHLT1050}',
                    }

                drawplots.makeeff(
                    axisranges = [0, 2000],
                    plotname = 'L1ETSum_FromSingleMuon_HLT1050_TurnOn_vsPU',
                    **HLT1050_kwargs, **MET_PU_kwargs, **common_kwargs,
                    )

                drawplots.makeeff(
                    axisranges = [0, 400],
                    plotname = 'L1ETSum_FromSingleMuon_HLT1050_TurnOn_vsPU_Zoom',
                    **HLT1050_kwargs, **MET_PU_kwargs, **common_kwargs,
                    )

                ETMHF90_kwargs = {
                    'num': ['h_MetNoMu_ETMHF90{}'.format(suf) for suf in suffixes[1:]],
                    'den': ['h_MetNoMu_Denominator{}'.format(suf) for suf in suffixes[1:]],
                    'xtitle': 'PFMET(#mu subtracted) (GeV)',
                    'extralabel': '#splitline{#geq 1 tight #mu (p_{T} > 27 GeV), pass HLT_IsoMu24}{#geq 1 jet (p_{T} > 30 GeV, 0 #leq |#eta| < 5), ETMHF90}',
                    }

                drawplots.makeeff(
                    axisranges = [0, 2000],
                    plotname = 'L1ETSum_FromSingleMuon_ETMHF90_TurnOn_vsPU',
                    **ETMHF90_kwargs, **MET_PU_kwargs, **common_kwargs,
                    )

                drawplots.makeeff(
                    axisranges = [0, 400],
                    plotname = 'L1ETSum_FromSingleMuon_ETMHF90_TurnOn_vsPU_Zoom',
                    **ETMHF90_kwargs, **MET_PU_kwargs, **common_kwargs,
                    )

                HTT280_kwargs = {
                    'num': ['h_HT_L1_HTT280er{}'.format(suf) for suf in suffixes[1:]],
                    'den': ['h_HT_Denominator{}'.format(suf) for suf in suffixes[1:]],
                    'xtitle': 'HT=#sum(p_{T}^{jets}(p_{T}>30 GeV, 0<=|#eta|<2.5)) (GeV)',
                    'extralabel': '#splitline{#geq 1 tight #mu (p_{T} > 27 GeV), pass HLT_IsoMu24}{#geq 1 jet (p_{T} > 30 GeV, 0 #leq |#eta| < 5), HTT280er}',
                    }

                drawplots.makeeff(
                    axisranges = [0, 3000],
                    plotname = 'L1ETSum_FromSingleMuon_HTT280_TurnOn_vsPU',
                    **HTT280_kwargs, **MET_PU_kwargs, **common_kwargs,
                    )

                drawplots.makeeff(
                    axisranges = [0, 1000],
                    plotname = 'L1ETSum_FromSingleMuon_HTT280_TurnOn_vsPU_Zoom',
                    **HTT280_kwargs, **MET_PU_kwargs, **common_kwargs,
                    )

            # VBF plot
#            VBF75_40_500_kwargs = {
#                'num': ['HLT_VBF_DiPFJet75_40_Mjj500_Detajj2p5_PFMET85'],
#                'den': ['h_MetNoMu_Denominator_VBF_DiJet70_40_500'],
#                'legendlabels': ['VBF_DiPFJet75_40_Mjj500'],
#                'xtitle': 'PuppiMET(#mu subtracted) (GeV)',
#                }

#            drawplots.makeeff(
#                axisranges = [0., 2000.],
#                plotname = 'L1ETSum_FromSingleMuon_DiPFJet75_40_Mjj500_TurnOn',
#                **VBF75_40_500_kwargs, **MET_kwargs, **common_kwargs,
#                )

#            drawplots.makeeff(
#                axisranges = [0., 400.],
#                plotname = 'L1ETSum_FromSingleMuon_DiPFJet75_40_Mjj500_TurnOn_Zoom',
#                **VBF75_40_500_kwargs, **MET_kwargs, **common_kwargs,
#                )



if __name__ == '__main__':
    main()
