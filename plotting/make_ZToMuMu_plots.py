# make_mu_plots.py, a program to draw the L1Studies plots obtained from the histograms extracted from NanoAOD

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
    parser.add_argument("-c", "--config", dest="config", help="The YAML config to read from", type=str, default=topDir+'config_cards/full_ZToMuMu.yaml')
    parser.add_argument("-l", "--lumi", dest="lumi", help="The integrated luminosity to display in the top right corner of the plot", type=str, default='')

    args = parser.parse_args()
    config = yaml.safe_load(open(args.config, 'r'))

    input_file = args.dir + "/all_ZToMuMu.root"
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
            plotname = 'L1Mu_nvtx',
            **common_kwargs,
            )

    for s in suffixes:

        for r in config['Regions']:
            region = config['Regions'][r]
            eta_range = "eta{}to{}".format(region[0], region[1]).replace(".","p")
            eta_label = '{{{} #leq | #eta^{{#mu}}(reco)| < {}}}'.format(region[0], region[1])

            if config['Efficiency']:

                # Efficiency vs Run Number
                drawplots.makeeff(
                    nvtx_suffix = s,
                    den = ['h_PlateauEffVsRunNb_Denominator_AllQual_plots_{}'.format(eta_range)],
                    num = ['h_PlateauEffVsRunNb_Numerator_{}_plots_{}'.format(qual, eta_range) for qual in config['Qualities']],
                    xtitle = 'run number',
                    ytitle = 'Efficiency',
                    axisranges = [0, 1, 0.8, 1.05],
                    legendlabels = [label(qual) for qual in config['Qualities']],
                    extralabel = "#splitline{{Z#rightarrow#mu#mu, p_{{T}}^{{#mu}}(reco) #geq 27 GeV}}{}".format(eta_label),
                    plotname = "L1Mu_EffVsRunNb_{}".format(r),
                    **common_kwargs,
                    )

            for qual in config['Qualities']:
                if config['TurnOns']:

                    TurnOn_kwargs = {
                            'nvtx_suffix': s,
                            'den': ['h_{}_plots_{}'.format(qual, eta_range)],
                            'num': ['h_{}_plots_{}_l1thrgeq{}'.format(qual, eta_range, thr) for thr in  config['Thresholds']],
                            'xtitle': 'p_{T}^{#mu}(reco) (GeV)',
                            'ytitle': 'Efficiency',
                            'legendlabels': ['p_{{T}}^{{L1 #mu}} #geq {} GeV'.format(thr) for thr in config['Thresholds']],
                            'extralabel': "#splitline{{Z#rightarrow#mu#mu, {}}}{}".format(label(qual), eta_label),
                            }

                    # Efficiency vs pT
                    # all eta ranges and all qualities
                    drawplots.makeeff(
                        axisranges = [3, 1000],
                        setlogx = True,
                        plotname = 'L1Mu_TurnOn{}_{}'.format(qual, r) ,
                        **TurnOn_kwargs, **common_kwargs,
                        )

                    # same thing, zoom on the 0 - 50 GeV region in pT
                    drawplots.makeeff(
                        axisranges = [3, 50],
                        setlogx = True,
                        plotname = 'L1Mu_TurnOn{}_{}_Zoom'.format(qual, r) ,
                        **TurnOn_kwargs, **common_kwargs,
                        )

                    # Comparisons between bins of PU:
                    if config['PU_plots']['make_histos'] and s == '':
                        bins = config['PU_plots']['nvtx_bins']
                        for thr in config['PU_plots']['draw_thresholds']:
                            drawplots.makeeff(
                                den = ['h_{}_plots_{}{}'.format(qual, eta_range, suf) for suf in suffixes[1:]],
                                num = ['h_{}_plots_{}_l1thrgeq{}{}'.format(qual, eta_range, thr, suf) for suf in suffixes[1:]],
                                xtitle = 'p_{T}^{#mu}(reco) (GeV)',
                                ytitle = 'Efficiency',
                                legendlabels = ['{} #leq nvtx < {}'.format(bins[i], bins[i+1]) for i in range(len(bins)-1)],
                                axisranges = [3, 1000],
                                extralabel = "#splitline{{Z#rightarrow#mu#mu, {}}}{}".format(label(qual), eta_label),
                                setlogx = True,
                                plotname = 'L1Mu{}_TurnOn{}_{}_vsPU'.format(thr, qual, r) ,
                                **common_kwargs,
                                )

        if config['Efficiency']:
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['h_Mu22_EtaPhi_Numerator'],
                den = ['h_Mu22_EtaPhi_Denominator'],
                xtitle = '#eta^{#mu}(reco)',
                ytitle = '#phi^{#mu}(reco)',
                ztitle = 'L1Mu22 efficiency (p_{T}^{#mu}(reco) > 27 GeV)',
                legendlabels = [''],
                extralabel = '#splitline{Z#rightarrow#mu#mu}{L1 Qual. #geq 12}',
                plotname = 'L1Mu_EffVsEtaPhi',
                axisranges = [-2.4, 2.4, -3.1416, 3.1416, 0, 1.1],
                **common_kwargs,
                )

        if config['Prefiring']:

            pre_post_firing_kwargs = {
                    'nvtx_suffix': s,
                    'xtitle': '#eta^{#mu}(reco)',
                    'legendlabels': [''],
                    'extralabel': '#splitline{Z#rightarrow#mu#mu}{10 #leq p_{T}^{#mu}(L1) < 21, L1 Qual. #geq 12}',
                    'addnumtoden': True,
                    }

            # Postfiring vs Eta Phi
            drawplots.makeeff(
                num = ['L1Mu10to21_bxplus1_etaphi'],
                den = ['L1Mu10to21_bx0_etaphi'],
                ytitle = '#phi^{#mu}(reco)',
                ztitle = 'bx+1 / (bx0 or bx+1)',
                plotname = 'L1Mu_PostfiringVsEtaPhi',
                axisranges = [-2.4, 2.4, -3.1416, 3.1416, 0, 1.1],
                addnumtoden = True,
                **common_kwargs,
                )

            # Prefiring vs Eta Phi
            drawplots.makeeff(
                num = ['L1Mu10to21_bxmin1_etaphi'],
                den = ['L1Mu10to21_bx0_etaphi'],
                ytitle = '#phi^{#mu}(reco)',
                ztitle = 'bx-1 / (bx0 or bx-1)',
                plotname = 'L1Mu_PrefiringVsEtaPhi',
                axisranges = [-2.4, 2.4, -3.1416, 3.1416, 0, 1.1],
                addnumtoden = True,
                **common_kwargs,
                )
        
            # Postfiring vs Eta
            drawplots.makeeff(
                num = ['L1Mu10to21_bxplus1_eta'],
                den = ['L1Mu10to21_bx0_eta'],
                ytitle = 'bx+1 / (bx0 or bx+1)',
                plotname = 'L1Mu_PostfiringVsEta',
                axisranges = [-2.4, 2.4, 0, 0.1],
                addnumtoden = True,
                **common_kwargs,
                )

            # Prefiring vs Eta
            drawplots.makeeff(
                num = ['L1Mu10to21_bxmin1_eta'],
                den = ['L1Mu10to21_bx0_eta'],
                ytitle = 'bx-1 / (bx0 or bx-1)',
                plotname = 'L1Mu_PrefiringVsEta',
                axisranges = [-2.4, 2.4, 0, 0.1],
                addnumtoden = True,
                **common_kwargs,
                )
            
            # Same thing, for Mu 10 and 22
            # Postfiring vs Eta Phi
            for pt_thr in ['10', '22']:

                pre_post_firing_kwargs = {
                        'nvtx_suffix': s,
                        'xtitle': '#eta^{#mu}(reco)',
                        'legendlabels': [''],
                        'addnumtoden': True,
                        }

                drawplots.makeeff(
                    num = ['L1Mu{}_bxplus1_etaphi'.format(pt_thr)],
                    den = ['L1Mu{}_bx0_etaphi'.format(pt_thr)],
                    ytitle = '#phi^{#mu}(reco)',
                    ztitle = 'bx+1 / (bx0 or bx+1)',
                    extralabel = '#splitline{Z#rightarrow#mu#mu}{p_{T}^{#mu}(L1) > ' + pt_thr + ', L1 Qual. #geq 12}',
                    plotname = 'L1Mu{}_PostfiringVsEtaPhi'.format(pt_thr),
                    axisranges = [-2.4, 2.4, -3.1416, 3.1416, 0, 1.1],
                    **pre_post_firing_kwargs, **common_kwargs,
                    )

                # Prefiring vs Eta Phi
                drawplots.makeeff(
                    #num = ['L1Mu22_FirstBunchInTrain_bxmin1_etaphi'],
                    num = ['L1Mu{}_OR_bxmin1_etaphi'.format(pt_thr)],
                    den = ['L1Mu{}_OR_bx0_etaphi'.format(pt_thr)],
                    ytitle = '#phi^{#mu}(reco)',
                    ztitle = 'bx-1 / (bx0 or bx-1)',
                    extralabel = '#splitline{Z#rightarrow#mu#mu, unprefirable events}{p_{T}^{#mu}(L1) > ' + pt_thr + ', L1 Qual. #geq 12}',
                    plotname = 'L1Mu{}_PrefiringVsEtaPhi'.format(pt_thr),
                    axisranges = [-2.4, 2.4, -3.1416, 3.1416, 0, 1.1],
                    **pre_post_firing_kwargs, **common_kwargs,
                    )
            
                # Postfiring vs Eta
                drawplots.makeeff(
                    num = ['L1Mu{}_bxplus1_eta'.format(pt_thr)],
                    den = ['L1Mu{}_bx0_eta'.format(pt_thr)],
                    ytitle = 'bx+1 / (bx0 or bx+1)',
                    extralabel = '#splitline{Z#rightarrow#mu#mu}{p_{T}^{#mu}(L1) > ' + pt_thr + ', L1 Qual. #geq 12}',
                    plotname = 'L1Mu{}_PostfiringVsEta'.format(pt_thr),
                    axisranges = [-2.4, 2.4, 0, 0.1],
                    **pre_post_firing_kwargs, **common_kwargs,
                    )

                # Prefiring vs Eta
                drawplots.makeeff(
                    #num = ['L1Mu22_FirstBunchInTrain_bxmin1_eta'],
                    num = ['L1Mu{}_OR_bxmin1_eta'.format(pt_thr)],
                    den = ['L1Mu{}_OR_bx0_eta'.format(pt_thr)],
                    ytitle = 'bx-1 / (bx0 or bx-1)',
                    extralabel = '#splitline{Z#rightarrow#mu#mu, unprefirable events}{p_{T}^{#mu}(L1) > ' + pt_thr + ', L1 Qual. #geq 12}',
                    plotname = 'L1Mu{}_PrefiringVsEta'.format(pt_thr),
                    axisranges = [-2.4, 2.4, 0, 0.1],
                    **pre_post_firing_kwargs, **common_kwargs,
                    )

                drawplots.makeeff(
                    nvtx_suffix = s,
                    num = ['L1Mu{}_bx0_etaphi'.format(pt_thr)],
                    den = ['L1Mu{}_all_etaphi'.format(pt_thr)],
                    xtitle = '#eta^{#mu}(reco)',
                    ytitle = '#phi^{#mu}(reco)',
                    ztitle = 'bx0 / all bx',
                    legendlabels = [''],
                    extralabel = '#splitline{Z#rightarrow#mu#mu, all events}{p_{T}^{#mu}(L1) > ' + pt_thr + ', L1 Qual. #geq 12}',
                    plotname = 'L1Mu{}_OccupancyVsEtaPhi'.format(pt_thr),
                    axisranges = [-2.4, 2.4, -3.1416, 3.1416, 0, 1.1],
                    **common_kwargs,
                    )

            # Occupancy vs Eta Phi
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['L1Mu10to21_bx0_etaphi'],
                den = ['L1Mu10to21_all_etaphi'],
                xtitle = '#eta^{#mu}(reco)',
                ytitle = '#phi^{#mu}(reco)',
                ztitle = 'bx0 / all bx',
                legendlabels = [''],
                extralabel = '#splitline{Z#rightarrow#mu#mu, all events}{10 #leq p_{T}^{#mu}(L1) < 21, L1 Qual. #geq 12}',
                plotname = 'L1Mu10to21_OccupancyVsEtaPhi',
                axisranges = [-2.4, 2.4, -3.1416, 3.1416, 0, 1.1],
                #addnumtoden = True,
                **common_kwargs,
                )




        if config['Response'] and 'AllQual' in config['Qualities']:

            regions = config['Regions'].values()
            eta_ranges = ["eta{}to{}".format(region[0], region[1]).replace(".","p") for region in regions]
            eta_labels = ['{} #leq | #eta| < {}'.format(region[0], region[1]) for region in regions]

            # Resolution Vs Pt
            drawplots.makeresol(
                nvtx_suffix = s,
                h2d = ['h_ResponseVsPt_AllQual_plots_{}'.format(eta_range) for eta_range in eta_ranges],
                xtitle = 'p_{T}^{reco muon} (GeV)',
                ytitle = '(p_{T}^{L1Mu}/p_{T}^{reco muon})',
                extralabel = '#splitline{Z#rightarrow#mu#mu}{All qual.}',
                legendlabels = eta_labels,
                plotname = 'L1Mu_ResponseVsPt',
                axisranges = [0, 100, 0.8, 1.6], 
                **common_kwargs,
                )

            # Resolution Vs RunNb
            drawplots.makeresol(
                nvtx_suffix = s,
                h2d = ['h_ResponseVsRunNb_AllQual_plots_{}'.format(eta_range) for eta_range in eta_ranges],
                xtitle = 'run number',
                ytitle = '(p_{T}^{L1Mu}/p_{T}^{reco muon})',
                extralabel = '#splitline{Z#rightarrow#mu#mu}{All qual.}',
                legendlabels = eta_labels,
                plotname = 'L1Mu_ResponseVsRunNb',
                axisranges = [355374, 362760, 0.9, 1.5],
                **common_kwargs,
                )

        if config['TurnOns'] and 'Qual12' in config['Qualities']:

            regions = config['Regions'].values()
            eta_ranges = ["eta{}to{}".format(region[0], region[1]).replace(".","p") for region in regions]
            eta_labels = ['{} #leq | #eta| < {}'.format(region[0], region[1]) for region in regions]

            # Efficiency vs pT
            # Comparison between track finders
            for thr in [5, 22]:
                drawplots.makeeff(
                    nvtx_suffix = s,
                    den = ['h_Qual12_plots_{}'.format(eta_range) for eta_range in eta_ranges],
                    num = ['h_Qual12_plots_{}_l1thrgeq{}'.format(eta_range, thr) for eta_range in eta_ranges],
                    xtitle = 'p_{T}^{#mu}(reco) (GeV)',
                    ytitle = 'Efficiency',
                    legendlabels = eta_labels,
                    axisranges = [3, 1000],
                    extralabel = "#splitline{{Z#rightarrow#mu#mu, All qual.}}{{p_{{T}}^{{L1 #mu}} #geq {} GeV}}".format(thr),
                    setlogx = True,
                    plotname = 'L1Mu{}_TurnOnQual12_EtaComparison'.format(thr) ,
                    **common_kwargs,
                    )

                drawplots.makeeff(
                    nvtx_suffix = s,
                    den = ['h_Qual12_plots_{}'.format(eta_range) for eta_range in eta_ranges],
                    num = ['h_Qual12_plots_{}_l1thrgeq{}'.format(eta_range, thr) for eta_range in eta_ranges],
                    xtitle = 'p_{T}^{#mu}(reco) (GeV)',
                    ytitle = 'Efficiency',
                    legendlabels = eta_labels,
                    axisranges = [3, 50],
                    extralabel = "#splitline{{Z#rightarrow#mu#mu, All qual.}}{{p_{{T}}^{{L1 #mu}} #geq {} GeV}}".format(thr),
                    #setlogx = True,
                    plotname = 'L1Mu{}_TurnOnQual12_EtaComparison_Zoom'.format(thr) ,
                    **common_kwargs,
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
