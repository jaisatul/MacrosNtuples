# make_ZToEE_plots.py, a program to draw the L1Studies plots obtained from the histograms extracted from NanoAOD

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

    args = parser.parse_args()
    config = yaml.safe_load(open(args.config, 'r'))

    input_file = args.dir + "/all_ZToEE.root"
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
            plotname = 'L1EG_nvtx',
            **common_kwargs,
            )

    for s in suffixes:

        for r in config['Regions']:
            region = config['Regions'][r]
            eta_range = "eta{}to{}".format(region[0], region[1]).replace(".","p")
            eta_label = '{{{} #leq | #eta^{{e}}(reco)| < {}}}'.format(region[0], region[1])

            #print(r)
            #print(region)
            #print(eta_range)
            #print(eta_label)

            if config['Efficiency']:

                # Efficiency vs Run Number
                drawplots.makeeff(
                    nvtx_suffix = s,
                    den = ['h_PlateauEffVsRunNb_Denominator_EGNonIso_plots_{}'.format(eta_range)],
                    num = ['h_PlateauEffVsRunNb_Numerator_{}_plots_{}'.format(iso, eta_range) for iso in config['Isos']],
                    xtitle = 'run number',
                    ytitle = 'Efficiency',
                    axisranges = [0, 1, 0.8, 1.05],
                    legendlabels = [label(iso) for iso in config['Isos']],
                    extralabel = "#splitline{{Z#rightarrowee, p_{{T}}^{{e}}(reco) #geq 35 GeV}}{}".format(eta_label),
                    plotname = "L1EG_EffVsRunNb_{}".format(r),
                    **common_kwargs,
                    )

            for iso in config['Isos']:
                if config['TurnOns']:
                    
                    # Efficiency vs pT
                    # all eta ranges and all qualities
                    drawplots.makeeff(
                        nvtx_suffix = s,
                        den = ['h_{}_plots_{}'.format(iso, eta_range)],
                        num = ['h_{}_plots_{}_l1thrgeq{}'.format(iso, eta_range, thr) for thr in  config['Thresholds']],
                        xtitle = 'p_{T}^{e}(reco) (GeV)',
                        ytitle = 'Efficiency',
                        legendlabels = ['p_{{T}}^{{L1 e}} #geq {} GeV'.format(thr) for thr in config['Thresholds']],
                        #axisranges = [0, 500],
                        extralabel = "#splitline{{Z#rightarrowee, {}}}{}".format(label(iso), eta_label),
                        setlogx = True,
                        plotname = 'L1EG_TurnOn{}_{}'.format(iso, r) ,
                        **common_kwargs,
                        )

                    # same thing, zoom on the 0 - 50 GeV region in pT
                    drawplots.makeeff(
                        nvtx_suffix = s,
                        den = ['h_{}_plots_{}'.format(iso, eta_range)],
                        num = ['h_{}_plots_{}_l1thrgeq{}'.format(iso, eta_range, thr) for thr in  config['Thresholds']],
                        xtitle = 'p_{T}^{e}(reco) (GeV)',
                        ytitle = 'Efficiency',
                        legendlabels = ['p_{{T}}^{{L1 e}} #geq {} GeV'.format(thr) for thr in config['Thresholds']],
                        axisranges = [5, 50],
                        extralabel = "#splitline{{Z#rightarrowee, {}}}{}".format(label(iso), eta_label),
                        setlogx = True,
                        plotname = 'L1EG_TurnOn{}_{}_Zoom'.format(iso, r) ,
                        **common_kwargs,
                        )

                    # Comparisons between bins of PU:
                    if config['PU_plots']['make_histos'] and s == '':
                        bins = config['PU_plots']['nvtx_bins']
                        for thr in config['PU_plots']['draw_thresholds']:
                            drawplots.makeeff(
                                den = ['h_{}_plots_{}{}'.format(iso, eta_range, suf) for suf in suffixes[1:]],
                                num = ['h_{}_plots_{}_l1thrgeq{}{}'.format(iso, eta_range, thr, suf) for suf in suffixes[1:]],
                                xtitle = 'p_{T}^{e}(reco) (GeV)',
                                ytitle = 'Efficiency',
                                legendlabels = ['{} #leq nvtx < {}'.format(bins[i], bins[i+1]) for i in range(len(bins)-1)],
                                #axisranges = [3, 300],
                                extralabel = "#splitline{{Z#rightarrowee, {}}}{}".format(label(iso), eta_label),
                                setlogx = True,
                                plotname = 'L1EG{}_TurnOn{}_{}_vsPU'.format(thr, iso, r) ,
                                **common_kwargs,
                                )

            if config['TurnOns']:

                # Efficiency vs pT
                # Comparison between isos
                for thr in [15, 30]:
                    drawplots.makeeff(
                        nvtx_suffix = s,
                        den = ['h_{}_plots_{}'.format(iso, eta_range) for iso in config['Isos']],
                        num = ['h_{}_plots_{}_l1thrgeq{}'.format(iso, eta_range, thr) for iso in config['Isos']],
                        xtitle = 'p_{T}^{#mu}(reco) (GeV)',
                        ytitle = 'Efficiency',
                        legendlabels = [iso for iso in config['Isos']],
                        #axisranges = [3, 1000],
                        extralabel = "#splitline{{Z#rightarrow#mu#mu, All qual.}}{{p_{{T}}^{{L1 #mu}} #geq {} GeV, {}}}".format(thr, eta_label[1:-1]),
                        setlogx = True,
                        plotname = 'L1EG{}_TurnOn_{}_IsoComparison'.format(thr, r) ,
                        **common_kwargs,
                        )

                    drawplots.makeeff(
                        nvtx_suffix = s,
                        den = ['h_{}_plots_{}'.format(iso, eta_range) for iso in config['Isos']],
                        num = ['h_{}_plots_{}_l1thrgeq{}'.format(iso, eta_range, thr) for iso in config['Isos']],
                        xtitle = 'p_{T}^{#mu}(reco) (GeV)',
                        ytitle = 'Efficiency',
                        legendlabels = [iso for iso in config['Isos']],
                        axisranges = [5, 50],
                        extralabel = "#splitline{{Z#rightarrow#mu#mu, All qual.}}{{p_{{T}}^{{L1 #mu}} #geq {} GeV, {}}}".format(thr, eta_label[1:-1]),
                        #setlogx = True,
                        plotname = 'L1EG{}_TurnOn_{}_IsoComparison_Zoom'.format(thr, r) ,
                        **common_kwargs,
                        )

        if config['Efficiency']:
            # Efficiency vs Eta Phi
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['h_EG25_EtaPhi_Numerator'],
                den = ['h_EG25_EtaPhi_Denominator'],
                xtitle = '#eta^{e}(reco)',
                ytitle = '#phi^{e}(reco)',
                ztitle = 'L1Mu22 efficiency (p_{T}^{e}(reco) > 30 GeV)',
                legendlabels = [''],
                extralabel = '#splitline{Z#rightarrowee}{L1 EG Tight Iso}',
                plotname = 'L1EG_EffVsEtaPhi',
                axisranges = [-2.5, 2.5, -3.1416, 3.1416, 0, 1.1],
                **common_kwargs,
                )

        if config['Prefiring']:

            # Postfiring vs Eta Phi
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['L1EG15to26_bxplus1_etaphi'],
                den = ['L1EG15to26_bx0_etaphi'],
                xtitle = '#eta^{e}(reco)',
                ytitle = '#phi^{e}(reco)',
                ztitle = 'bx+1 / (bx0 or bx+1)',
                legendlabels = [''],
                extralabel = '#splitline{Z#rightarrowee}{15 #leq p_{T}^{e}(L1) < 26, L1 EG Non Iso}',
                plotname = 'L1EG_PostfiringVsEtaPhi',
                axisranges = [-2.5, 2.5, -3.1416, 3.1416, 0, 1.1],
                addnumtoden = True,
                **common_kwargs,
                )

            # Prefiring vs Eta Phi
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['L1EG15to26_bxmin1_etaphi'],
                den = ['L1EG15to26_bx0_etaphi'],
                xtitle = '#eta^{e}(reco)',
                ytitle = '#phi^{e}(reco)',
                ztitle = 'bx-1 / (bx0 or bx-1)',
                legendlabels = [''],
                extralabel = '#splitline{Z#rightarrowee, all events}{15 #leq p_{T}^{e}(L1) < 26, L1 EG Non Iso}',
                plotname = 'L1EG_PrefiringVsEtaPhi',
                axisranges = [-2.5, 2.5, -3.1416, 3.1416, 0, 1.1],
                addnumtoden = True,
                **common_kwargs,
                )
        
            # Postfiring vs Eta 
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['L1EG15to26_bxplus1_eta'],
                den = ['L1EG15to26_bx0_eta'],
                xtitle = '#eta^{e}(reco)',
                ytitle = 'bx+1 / (bx0 or bx+1)',
                legendlabels = [''],
                extralabel = '#splitline{Z#rightarrowee}{15 #leq p_{T}^{e}(L1) < 26, L1 EG Non Iso}',
                plotname = 'L1EG_PostfiringVsEta',
                axisranges = [-2.5, 2.5, 0, 0.1],
                addnumtoden = True,
                **common_kwargs,
                )

            # Prefiring vs Eta 
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['L1EG15to26_bxmin1_eta'],
                den = ['L1EG15to26_bx0_eta'],
                xtitle = '#eta^{e}(reco)',
                ytitle = 'bx-1 / (bx0 or bx-1)',
                legendlabels = [''],
                extralabel = '#splitline{Z#rightarrowee, all events}{15 #leq p_{T}^{e}(L1) < 26, L1 EG Non Iso}',
                plotname = 'L1EG_PrefiringVsEta',
                axisranges = [-2.5, 2.5, 0, 0.1],
                addnumtoden = True,
                **common_kwargs,
                )

            # for unprefirable EG30:

            # Postfiring vs Eta Phi
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['L1EG30_bxplus1_etaphi'],
                den = ['L1EG30_bx0_etaphi'],
                xtitle = '#eta^{e}(reco)',
                ytitle = '#phi^{e}(reco)',
                ztitle = 'bx+1 / (bx0 or bx+1)',
                legendlabels = [''],
                extralabel = '#splitline{Z#rightarrowee}{15 #leq p_{T}^{e}(L1) < 26, L1 EG Non Iso}',
                plotname = 'L1EG30_PostfiringVsEtaPhi',
                axisranges = [-2.5, 2.5, -3.1416, 3.1416, 0, 1.1],
                addnumtoden = True,
                **common_kwargs,
                )

            # Prefiring vs Eta Phi
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['L1EG30_OR_bxmin1_etaphi'],
                den = ['L1EG30_OR_bx0_etaphi'],
                xtitle = '#eta^{e}(reco)',
                ytitle = '#phi^{e}(reco)',
                ztitle = 'bx-1 / (bx0 or bx-1)',
                legendlabels = [''],
                extralabel = '#splitline{Z#rightarrowee, unprefireable events}{15 #leq p_{T}^{e}(L1) < 26, L1 EG Non Iso}',
                plotname = 'L1EG30_PrefiringVsEtaPhi',
                axisranges = [-2.5, 2.5, -3.1416, 3.1416, 0, 1.1],
                addnumtoden = True,
                **common_kwargs,
                )
        
            # Postfiring vs Eta 
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['L1EG30_bxplus1_eta'],
                den = ['L1EG30_bx0_eta'],
                xtitle = '#eta^{e}(reco)',
                ytitle = 'bx+1 / (bx0 or bx+1)',
                legendlabels = [''],
                extralabel = '#splitline{Z#rightarrowee}{15 #leq p_{T}^{e}(L1) < 26, L1 EG Non Iso}',
                plotname = 'L1EG30_PostfiringVsEta',
                axisranges = [-2.5, 2.5, 0, 0.1],
                addnumtoden = True,
                **common_kwargs,
                )

            # Prefiring vs Eta 
            drawplots.makeeff(
                nvtx_suffix = s,
                num = ['L1EG30_OR_bxmin1_eta'],
                den = ['L1EG30_OR_bx0_eta'],
                xtitle = '#eta^{e}(reco)',
                ytitle = 'bx-1 / (bx0 or bx-1)',
                legendlabels = [''],
                extralabel = '#splitline{Z#rightarrowee, unprefireable events}{15 #leq p_{T}^{e}(L1) < 26, L1 EG Non Iso}',
                plotname = 'L1EG30_PrefiringVsEta',
                axisranges = [-2.5, 2.5, 0, 0.1],
                addnumtoden = True,
                **common_kwargs,
                )

        if config['Response'] and 'EGNonIso' in config['Isos']:

            regions = config['Regions'].values()
            eta_ranges = ["eta{}to{}".format(region[0], region[1]).replace(".","p") for region in regions]
            eta_labels = ['{} #leq | #eta| < {}'.format(region[0], region[1]) for region in regions]

            # Resolution Vs Pt
            drawplots.makeresol(
                nvtx_suffix = s,
                h2d = ['h_ResponseVsPt_EGNonIso_plots_{}'.format(eta_range) for eta_range in eta_ranges],
                xtitle = 'p_{T}^{reco e} (GeV)',
                ytitle = '(p_{T}^{L1EG}/p_{T}^{reco e})',
                extralabel = '#splitline{Z#rightarrowee}{Non Iso.}',
                legendlabels = eta_labels,
                plotname = 'L1EG_ResponseVsPt',
                axisranges = [0, 100, 0.8, 1.2], 
                **common_kwargs,
                )

            # Resolution Vs RunNb
            drawplots.makeresol(
                nvtx_suffix = s,
                h2d = ['h_ResponseVsRunNb_EGNonIso_plots_{}'.format(eta_range) for eta_range in eta_ranges],
                xtitle = 'run number',
                ytitle = '(p_{T}^{L1EG}/p_{T}^{reco e})',
                extralabel = '#splitline{Z#rightarrowee}{Non Iso.}',
                legendlabels = eta_labels,
                plotname = 'L1EG_ResponseVsRunNb',
                axisranges = [355374, 362760, 0.8, 1.2],
                **common_kwargs,
                )


def label(iso):
    labels = {
            'EGNonIso': 'Non iso',
            'EGLoosIso': 'Loose iso',
            'EGTightIso': 'Tight iso',
            }

    if iso in labels:
        return(labels[iso])
    else:
        return('')

if __name__ == '__main__':
    main()
