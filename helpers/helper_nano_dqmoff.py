import ROOT
import yaml
import json
from array import array
from math import floor, ceil

from bins_dqmoff import *

runnb_bins = None
def set_runnb_bins(df):
    global runnb_bins
    if runnb_bins is None:
        # +1: to get [run, run+1] bin, +0.5 and floor to prevent float rounding errors + high bound
        # in range is excluded, so feed run, and run+2 to get [run, run+1]
        runNb_max = ceil(df.Max("run").GetValue() + 1.5)
        runNb_min = floor(df.Min("run").GetValue())
        runnb_bins = array('f', [r for r in range(runNb_min, runNb_max)])
    else:
        print("runnb_bins are already set")

config = None
def set_config(stream):
    global config
    if config is None:
        config = yaml.safe_load(stream)
    else:
        print("config_dict is already set")

def make_filter(golden_json):
    fltr = ''
    if golden_json != '':
        with open(golden_json) as j:
            J = json.load(j)
        for run_nb in J:
            fltr += '(run=={}&&('.format(run_nb)
            for lumis in J[run_nb]:
                fltr += '(luminosityBlock>={}&&luminosityBlock<={})||'.format(lumis[0], lumis[1])
            fltr = fltr[:-2] + '))||'

        fltr = fltr[:-2]
    return(fltr)



def DQMOff_EleSelection(df, massmin=60, massmax=120):
    '''
    Select Z->ee events passing a single electron trigger. Defines probe pt/eta/phi
    The selections are done to match the DQM Off selections
    '''
    df = df.Filter('HLT_Ele32_WPTight_Gsf')

    # Trigged on a Electron (probably redondant)
    df = df.Filter('''
    bool trigged_on_e = false;
    for (unsigned int i = 0; i < TrigObj_id.size(); i++){
        if(TrigObj_id[i] == 11) trigged_on_e = true;
    }
    return trigged_on_e;
    ''')

    # TrigObj matching
    df = df.Filter('nElectron > 2')
    df = df.Define('Electron_trig_idx', 'MatchObjToTrig(Electron_eta, Electron_phi, TrigObj_pt, TrigObj_eta, TrigObj_phi, TrigObj_id, 11, TrigObj_filterBits, 1, 0.3)')
    df = df.Define('Electron_passHLT_Ele32_WPTight_Gsf', 'trig_is_filterbit1_set(Electron_trig_idx, TrigObj_filterBits, 1)')

    # Tag and Probe Selection
    df = df.Define('isTag','Electron_pt>30&&abs(Electron_pdgId)==11&&Electron_mvaNoIso_WP90&&Electron_passHLT_Ele32_WPTight_Gsf==true')
    df = df.Filter('Sum(isTag)>0')
    df = df.Define('isProbe','abs(Electron_pdgId)==11&&Electron_mvaNoIso_WP90&&(Sum(isTag)>=2||isTag==0)')
    # df = df.Define('isTag','Electron_pt>30&&abs(Electron_pdgId)==11&&Electron_mvaNoIso_Fall17V2_WP90&&Electron_passHLT_Ele32_WPTight_Gsf==true')
    # df = df.Filter('Sum(isTag)>0')
    # df = df.Define('isProbe','abs(Electron_pdgId)==11&&Electron_mvaNoIso_Fall17V2_WPL&&(Sum(isTag)>=2||isTag==0)')

    # df = df.Define('dr_mll', 'dR_mll(Electron_pt, Electron_eta, Electron_phi, isTag, isProbe)')
    # df = df.Filter('''
    # for (unsigned int line = 0; line < dr_mll.size(); line++){
    #     for (unsigned int col = 0; col < 2; col++){
    #         float DeltaR = dr_mll[line][col][0];
    #         float mll = dr_mll[line][col][1];
    #         if (mll > 60 && mll < 120){
    #             return true;
    #         }
    #     }
    # }
    # return false;
    # ''')

    df = df.Define('_mll', 'mll(Electron_pt, Electron_eta, Electron_phi, isTag, isProbe)')
    df = df.Filter('_mll>{}&&_mll<{}'.format(massmin, massmax))

    df = df.Define('tag_Pt', 'Electron_pt[isTag]')
    df = df.Define('tag_Eta', 'Electron_eta[isTag]')
    df = df.Define('tag_Phi', 'Electron_phi[isTag]')

    df = df.Define('probe_Pt','Electron_pt[isProbe]')
    df = df.Define('probe_Eta','Electron_eta[isProbe]')
    df = df.Define('probe_Phi','Electron_phi[isProbe]')

    df = df.Define('barrelbarrel','abs(Electron_eta[0])<1.479&&abs(Electron_eta[1])<1.479')
    df = df.Define('endcapendcap','abs(Electron_eta[0])>1.479&&abs(Electron_eta[1])>1.479')

    return df


def DQMOff_MuSelection(df, massmin=60, massmax=120):
    '''
    Selects Z->mumu events passing a single muon trigger. Defines probe pt/eta/phi
    The selections are done to match the DQM Off selections
    '''
    df = df.Filter('HLT_IsoMu27')

    # Trigged on a Muon (probably redondant)
    df = df.Filter('''
    bool trigged_on_mu = false;
    for (unsigned int i = 0; i < TrigObj_id.size(); i++){
        if(TrigObj_id[i] == 13) trigged_on_mu = true;
    }
    return trigged_on_mu;
    ''')

    # TrigObj matching
    df = df.Define('Muon_trig_idx', 'MatchObjToTrig(Muon_eta, Muon_phi, TrigObj_pt, TrigObj_eta, TrigObj_phi, TrigObj_id, 13, TrigObj_filterBits, 3, 0.1)')
    df = df.Define('Muon_passHLT_IsoMu27', 'trig_is_filterbit1_set(Muon_trig_idx, TrigObj_filterBits, 3)') 

    # Tag and Probe Selection
    # df = df.Define('Muon_PassId', 'Muon_tightId')
    df = df.Define('Muon_PassId', 'Muon_looseId')
    df = df.Define('isTag','Muon_pt>20&&abs(Muon_pdgId)==13&&Muon_PassId&&Muon_passHLT_IsoMu27')
    # df = df.Define('isTag','Muon_pt>5&&abs(Muon_pdgId)==13&&Muon_PassId&&Muon_passHLT_IsoMu27')
    df = df.Filter('Sum(isTag)>0')

    # nEvents = df.Count().GetValue()
    # print('After muon selection, There are {} events'.format(nEvents))

    df = df.Define('isProbe','abs(Muon_pdgId)==13&&Muon_PassId&&(Sum(isTag)>=2||isTag==0)')
    df = df.Define('_mll', 'mll(Muon_pt, Muon_eta, Muon_phi, isTag, isProbe)')
    df = df.Filter('_mll>{}&&_mll<{}'.format(massmin, massmax))

    # df = df.Define('dr_mll', 'dR_mll(Muon_pt, Muon_eta, Muon_phi, isTag, isProbe)')
    # df = df.Filter('''
    # for (unsigned int line = 0; line < dr_mll.size(); line++){
    #     for (unsigned int col = 0; col < 2; col++){
    #         float DeltaR = dr_mll[line][col][0];
    #         if (DeltaR > 0.5){
    #             return true;
    #         }
    #     }
    # }
    # return false;
    # ''')
    df = df.Define('tag_Pt', 'Muon_pt[isTag]')
    df = df.Define('tag_Eta', 'Muon_eta[isTag]')
    df = df.Define('tag_Phi', 'Muon_phi[isTag]')

    df = df.Define('probe_Pt','Muon_pt[isProbe]')
    df = df.Define('probe_Eta','Muon_eta[isProbe]')
    df = df.Define('probe_Phi','Muon_phi[isProbe]')
    df = df.Define('probe_Charge', 'Muon_charge[isProbe]')

    df = df.Define('barrelbarrel','abs(Muon_eta[0])<1.24&&abs(Muon_eta[1])<1.24')
    df = df.Define('endcapendcap','abs(Muon_eta[0])>1.24&&abs(Muon_eta[1])>1.24')

    return df


def DQMOff_TauSelection(df):
    '''
    Selects Z->tautau events passing a single muon trigger. Defines probe tau pt/eta/phi
    The selections are made to match with DQM Off selections
    '''
    df = df.Filter('HLT_IsoMu24||HLT_IsoMu27','HLT_IsoMu24||HLT_IsoMu27')

    # Trigged on a Muon (probably redundant)
    df = df.Filter('''
    bool trigged_on_mu = false;
    for (unsigned int i = 0; i < TrigObj_id.size(); i++){
        if(TrigObj_id[i] == 13) trigged_on_mu = true;
    }
    return trigged_on_mu;
    ''','trigger on muon')

    # TrigObj matching
    df = df.Define('Muon_trig_idx', 'MatchObjToTrig(Muon_eta, Muon_phi, TrigObj_pt, TrigObj_eta, TrigObj_phi, TrigObj_id, 13, TrigObj_filterBits, 3, 0.6)')
    df = df.Define('Muon_passHLT_IsoMu24', 'trig_is_filterbit1_set(Muon_trig_idx, TrigObj_filterBits, 3)')

    # Tag Muon Selection
    df = df.Define('Muon_PassTightId','Muon_pfIsoId>=3&&Muon_mediumPromptId') 
    df = df.Define('Muon_MassId', 'pass_muon_met_mass_belowX(Muon_pt, Muon_phi, PuppiMET_pt, PuppiMET_phi, 30)')
    df = df.Define('isTag','Muon_pt>24&&abs(Muon_eta)<2.1&&abs(Muon_pdgId)==13&&Muon_PassTightId&&Muon_passHLT_IsoMu24&&Muon_MassId')
    df = df.Filter('Sum(isTag)==1', 'found a tag')
    df = df.Define('tagIdx', 'first_tagmuon_idx(isTag)')
    df = df.Filter('tagIdx!=-1','tagIdx!=-1')

    df = df.Define('tagPt', 'Muon_pt[tagIdx]')
    df = df.Define('tagEta', 'Muon_eta[tagIdx]')
    df = df.Define('tagPhi', 'Muon_phi[tagIdx]')
    df = df.Define('tagMass', 'Muon_mass[tagIdx]')
    df = df.Define('tagCharge', 'Muon_charge[tagIdx]')

    # Decay mode 5 and 6 are unphysical, so removing them
    # Applying Tau_Id_Discrimination against e, mu, jets
    # Applying probe tau selection criterion with the given tag muon
    df = df.Define('Tau_PassDecayMode', 'Tau_decayMode!=5&&Tau_decayMode!=6')
    df = df.Define('Tau_PassTightId', 'Tau_idDeepTau2018v2p5VSe>=1&&Tau_idDeepTau2018v2p5VSjet>=2&&Tau_idDeepTau2018v2p5VSmu>=1')
    df = df.Define('Tau_PassProbe', 'pass_probeTau(Tau_pt, Tau_eta, Tau_phi, Tau_mass, Tau_charge, tagPt, tagEta, tagPhi, tagMass, tagCharge)')
    df = df.Define('isProbeTau', 'Tau_PassDecayMode&&Tau_PassTightId&&Tau_PassProbe')
    df = df.Filter('Sum(isProbeTau)==1','=1 probe tau')

    df = df.Define('probe_Pt','Tau_pt[isProbeTau]')
    df = df.Define('probe_Eta','Tau_eta[isProbeTau]')
    df = df.Define('probe_Phi','Tau_phi[isProbeTau]')

    df = df.Define('barrelbarrel','abs(Tau_eta[0])<1.5&&abs(Tau_eta[1])<1.5')
    df = df.Define('endcapendcap','abs(Tau_eta[0])>1.5&&abs(Tau_eta[1])>1.5')

    return df


def DQMOff_JetSelection(df):
    '''
    Selects high jet pT events passing a single muon trigger. Defines leadjet pt/eta/phi
    The selections are made to match with DQM Off selections
    '''

    df = df.Filter('HLT_IsoMu24||HLT_IsoMu27')
    df = df.Filter('''
    if (Jet_pt.size() > 0) return true;
    return false;
    ''')

    df = df.Define('isGoodJet', 'Jet_jetId>=4')
    df = df.Filter('Sum(isGoodJet)>0')
    df = df.Define('isLead', 'isLeadJet(Jet_pt, isGoodJet)')

    df = df.Define('leadJetPt', 'Jet_pt[isLead]')
    df = df.Define('leadJetEta','Jet_eta[isLead]')
    df = df.Define('leadJetPhi','Jet_phi[isLead]')

    return df


def DQMOff_EtSumSelection(df):
    '''
    Selects events passing a single muon trigger. Defines Et Sums
    The selections are made to match with DQM Off selections
    '''

    df = df.Filter('HLT_IsoMu24||HLT_IsoMu27')

    df = df.Define('recoMET', 'CaloMET_pt')
    df = df.Define('recoMETPhi','CaloMET_phi')
    df = df.Define('recoETT', 'CaloMET_sumEt')
    df = df.Define('recoHTTandMHT', 'RecoHTTandMHT(Jet_pt, Jet_eta, Jet_phi,  2.5, 2.5)')
    df = df.Define('recoHTT', 'recoHTTandMHT[0]')
    df = df.Define('recoMHT', 'recoHTTandMHT[1]')
    df = df.Define('recoMHTPhi', 'recoHTTandMHT[2]')

    return df


def ZEE_DQMOff_Plots(df, suffix = ''):

    recoToL1PtCutFactor = config['RecoToL1PtCutFactor']
    probeToL1Offset = config['probeToL1Offset']

    df = df.Define('probe_Nvtx', 'GetProbeNvtxArray(probe_Pt, PV_npvs)')

    histos = {}

    df_eg = [None] * len(config['Isos'])
    for i, iso in enumerate(config['Isos']):

        prefix = iso

        # Get Ids for L1 Electrons which match with probe
        df_eg[i] = df.Define('probe_idxL1EG','FindL1ObjIdx(L1EG_eta, L1EG_phi, probe_Eta, probe_Phi, L1EG_hwIso, {}, 0.3)'.format(config['Isos'][iso]))
        df_eg[i] = df_eg[i].Define('probe_idxL1EG_Bx0', 'FindL1ObjIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, 0, L1EG_hwIso, {}, 0.3)'.format(config['Isos'][iso]))
        df_eg[i] = df_eg[i].Define('probe_idxL1EG_Bxmin1', 'FindL1ObjIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, -1, L1EG_hwIso, {}, 0.3)'.format(config['Isos'][iso]))
        df_eg[i] = df_eg[i].Define('probe_idxL1EG_Bxplus1', 'FindL1ObjIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, 1, L1EG_hwIso, {}, 0.3)'.format(config['Isos'][iso]))

        for bx in ['min1', '0', 'plus1'] :
            df_eg[i] = df_eg[i].Define('probe_L1Pt_Bx{}'.format(bx), 'GetVal(probe_idxL1EG_Bx{}, L1EG_pt)'.format(bx))
            df_eg[i] = df_eg[i].Define('probe_L1Eta_Bx{}'.format(bx), 'GetVal(probe_idxL1EG_Bx{}, L1EG_eta)'.format(bx))
            df_eg[i] = df_eg[i].Define('probe_L1Phi_Bx{}'.format(bx), 'GetVal(probe_idxL1EG_Bx{}, L1EG_phi)'.format(bx))
            df_eg[i] = df_eg[i].Define('probe_L1Iso_Bx{}'.format(bx), 'GetVal(probe_idxL1EG_Bx{}, L1EG_hwIso)'.format(bx))

        # Resolution Histograms
        df_eg[i] = df_eg[i].Define('probe_L1PtReso', '(probe_L1Pt_Bx0 - probe_Pt)/probe_Pt')
        df_eg[i] = df_eg[i].Define('probe_L1EtaReso', '(probe_L1Eta_Bx0 - probe_Eta)')
        df_eg[i] = df_eg[i].Define('probe_L1PhiReso', 'GetReducedDeltaphi(probe_L1Phi_Bx0, probe_Phi)')

        pt_binning = dqmoff_egpt_bins
        eta_binning = dqmoff_egeta_bins
        phi_binning = dqmoff_egphi_bins
        nvtx_binning = dqmoff_egnvtx_bins
        reso_pt_binning = dqmoff_egresolution_pt_bins
        reso_eta_binning = dqmoff_egresolution_eta_bins
        reso_phi_binning = dqmoff_egresolution_phi_bins
        n_ptbins = len(pt_binning) - 1
        n_etabins = len(eta_binning) - 1
        n_phibins = len(phi_binning) - 1
        n_nvtxbins = len(nvtx_binning) - 1
        n_resoptbins = len(reso_pt_binning) - 1
        n_resoetabins = len(reso_eta_binning) - 1
        n_resophibins = len(reso_phi_binning) - 1

        if iso == 'NonIso' and config['Prefiring']:
            
            pref_l1thres = 30
            pref_probethres = 38

            colname = 'probe_L1{}'.format(pref_l1thres).replace(".","p")  
            colname1 = 'probe_L1{}_Reco{}'.format(pref_l1thres, pref_probethres).replace(".","p")
            colname2 = 'probe_Reco{}'.format(pref_probethres).replace(".","p")

            df_eg[i] = df_eg[i].Define(colname2+'_Pt', 'probe_Pt[probe_Pt>{}]'.format(pref_probethres))
            df_eg[i] = df_eg[i].Define(colname2+'_Eta', 'probe_Eta[probe_Pt>{}]'.format(pref_probethres))
            df_eg[i] = df_eg[i].Define(colname2+'_Phi', 'probe_Phi[probe_Pt>{}]'.format(pref_probethres))

            for bx in ['min1', '0', 'plus1'] :
                df_eg[i] = df_eg[i].Define(colname+'_Bx{}_Pt'.format(bx), 'probe_Pt[probe_L1Pt_Bx{}>{}]'.format(bx, pref_l1thres))
                df_eg[i] = df_eg[i].Define(colname+'_Bx{}_Eta'.format(bx), 'probe_Eta[probe_L1Pt_Bx{}>{}]'.format(bx, pref_l1thres))
                df_eg[i] = df_eg[i].Define(colname+'_Bx{}_Phi'.format(bx), 'probe_Phi[probe_L1Pt_Bx{}>{}]'.format(bx, pref_l1thres))

                df_eg[i] = df_eg[i].Define(colname1+'_Bx{}_Pt'.format(bx), 'probe_Pt[probe_Pt>{}&&probe_L1Pt_Bx{}>{}]'.format(pref_probethres, bx, pref_l1thres))
                df_eg[i] = df_eg[i].Define(colname1+'_Bx{}_Eta'.format(bx), 'probe_Eta[probe_Pt>{}&&probe_L1Pt_Bx{}>{}]'.format(pref_probethres, bx, pref_l1thres))
                df_eg[i] = df_eg[i].Define(colname1+'_Bx{}_Phi'.format(bx), 'probe_Phi[probe_Pt>{}&&probe_L1Pt_Bx{}>{}]'.format(pref_probethres, bx, pref_l1thres))

                # df_eg[i] = df_eg[i].Define(colname+'Bx{}_runnb'.format(bx), 'return ROOT::VecOps::RVec<int>('+colname+'Bx{}_Eta'.format(bx)+'.size(), run);')

            for typeofevents in ['L1_UnprefireableEvent', 'L1_FirstBunchInTrain' , 'AllEvents'] :
            # for typeofevents in ['AllEvents'] :
                cut_typeofevents = typeofevents
                if typeofevents == 'AllEvents': cut_typeofevents = 'return true;'

                for bx in ['min1', '0', 'plus1'] :           
                    
                    str_pref = 'h_EG_pref_L1{}'.format(pref_l1thres).replace(".","p")
                    str_pref1 = 'h_EG_pref_L1{}_Reco{}'.format(pref_l1thres, pref_probethres).replace(".","p")

                    hname = str_pref+'_'+typeofevents+'_bx'+bx+'_eta'+suffix
                    histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), colname+'_Bx{}_Eta'.format(bx))

                    hname = str_pref+'_'+typeofevents+'_bx'+bx+'_phi'+suffix
                    histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), colname+'_Bx{}_Phi'.format(bx))

                    hname = str_pref+'_'+typeofevents+'_bx'+bx+'_etapt'+suffix
                    histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), colname+'_Bx{}_Eta'.format(bx), colname+'_Bx{}_Pt'.format(bx))

                    hname = str_pref+'_'+typeofevents+'_bx'+bx+'_etaphi'+suffix
                    histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), colname+'_Bx{}_Eta'.format(bx), colname+'_Bx{}_Phi'.format(bx))
                    
                    hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_eta'+suffix
                    histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), colname1+'_Bx{}_Eta'.format(bx))

                    hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_phi'+suffix
                    histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), colname1+'_Bx{}_Phi'.format(bx))

                    hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_etapt'+suffix
                    histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), colname1+'_Bx{}_Eta'.format(bx), colname1+'_Bx{}_Pt'.format(bx))

                    hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_etaphi'+suffix
                    histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), colname1+'_Bx{}_Eta'.format(bx), colname1+'_Bx{}_Phi'.format(bx))
                    

                #Denominators
                hname = 'h_EG_pref_'+typeofevents+'_eta'+suffix
                histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), 'probe_Eta')

                hname = 'h_EG_pref_'+typeofevents+'_phi'+suffix
                histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), 'probe_Phi')

                hname = 'h_EG_pref_'+typeofevents+'_etapt'+suffix
                histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), 'probe_Eta', 'probe_Pt')

                hname = 'h_EG_pref_'+typeofevents+'_etaphi'+suffix
                histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), 'probe_Eta', 'probe_Phi')

                hname = 'h_EG_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_eta'+suffix
                histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), colname2+'_Eta')

                hname = 'h_EG_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_phi'+suffix
                histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), colname2+'_Phi')

                hname = 'h_EG_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_etapt'+suffix
                histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), colname2+'_Eta', colname2+'_Pt')

                hname = 'h_EG_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_etaphi'+suffix
                histos[hname] = df_eg[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), colname2+'_Eta', colname2+'_Phi')


                # #Prefiring vs run nb
                # hname = l1objname+'{}'.format(l1threshold)+'_'+typeofevents+'_Denominator'+'_runnb'+suffix
                # histos[hname] = df.Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '',  len(runnb_bins)-1, runnb_bins), colname+'_runnb')

        if iso == 'NonIso' and config['L1TResolution']:

            df_etarange = [None] * len(config['Regions'])
            for ireg, reg in enumerate(config['Regions']):

                region = config["Regions"][reg]

                df_etarange[ireg] = df_eg[i].Define('inEtaRange','abs(probe_Eta)>={}'.format(region[0])+'&&abs(probe_Eta)<{}'.format(region[1]))
                df_etarange[ireg] = df_etarange[ireg].Define('reso_pt', 'probe_L1PtReso[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('reso_eta', 'probe_L1EtaReso[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('reso_phi', 'probe_L1PhiReso[inEtaRange]')

                histos['resolutionElectronET_{}'.format(reg)] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('resolutionElectronET_{}'.format(reg), '', n_resoptbins, reso_pt_binning), 
                    'reso_pt'
                )
                histos['resolutionElectronPhi_{}'.format(reg)] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('resolutionElectronPhi_{}'.format(reg), '', n_resophibins, reso_phi_binning), 
                    'reso_phi'
                )
                if reg == 'EB_EE':
                    histos['resolutionElectronEta'] = df_etarange[ireg].Histo1D (
                        ROOT.RDF.TH1DModel('resolutionElectronEta', '', n_resoetabins, reso_eta_binning), 
                        'reso_eta'
                    )

        if config['L1TEfficiency']:

            df_etarange = [None] * len(config['Regions'])
            for ireg, reg in enumerate(config['Regions']):
                region = config["Regions"][reg]

                df_etarange[ireg] = df_eg[i].Define('inEtaRange', 'abs(probe_Eta)>={}'.format(region[0])+'&&abs(probe_Eta)<{}'.format(region[1]))
                df_etarange[ireg] = df_etarange[ireg].Define('denominator_pt', 'probe_Pt[inEtaRange]')

                l1thresholds = config["Thresholds"]
                for ipt in l1thresholds:

                    df_loc = df_etarange[ireg].Define('passL1Cond', 'probe_L1Pt_Bx0>={}'.format(ipt))
                    df_loc = df_loc.Define('numerator_pt', 'probe_Pt[inEtaRange&&passL1Cond]')

                    if (ipt < 48):
                        
                        histos['efficiencyElectronET_{}_threshold_{}_Den'.format(reg, ipt)] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('efficiencyElectronET_{}_threshold_{}_Den'.format(reg, ipt), '', n_ptbins, pt_binning), 
                            'denominator_pt'
                        )

                        histos['efficiencyElectronET_{}_threshold_{}_Num'.format(reg, ipt)] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('efficiencyElectronET_{}_threshold_{}_Num'.format(reg, ipt), '', n_ptbins, pt_binning), 
                            'numerator_pt'
                        )

                    if (reg == 'EB_EE') and (ipt >= 48): 

                        cutfactor = ipt * recoToL1PtCutFactor
                        offsetfactor = ipt + probeToL1Offset

                        df_loc = df_loc.Define('passRecoToL1PtCutFactor', 'probe_Pt>={}'.format(cutfactor))
                        df_loc = df_loc.Define('passL1OffsetCond', 'probe_L1Pt_Bx0>={}'.format(offsetfactor))

                        df_loc = df_loc.Define('denominator_eta', 'probe_Eta[inEtaRange&&passRecoToL1PtCutFactor]')
                        df_loc = df_loc.Define('denominator_phi', 'probe_Phi[inEtaRange&&passRecoToL1PtCutFactor]')
                        df_loc = df_loc.Define('denominator_nvtx', 'probe_Nvtx[inEtaRange&&passRecoToL1PtCutFactor]')

                        histos['efficiencyElectronEta_threshold_{}_Den'.format(ipt)] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('efficiencyElectronEta_threshold_{}_Den'.format(ipt), '', n_etabins, eta_binning), 
                            'denominator_eta'
                        )
                        histos['efficiencyElectronPhi_threshold_{}_Den'.format(ipt)] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('efficiencyElectronPhi_threshold_{}_Den'.format(ipt), '', n_phibins, phi_binning), 
                            'denominator_phi'
                        )
                        histos['efficiencyElectronNVertex_threshold_{}_Den'.format(ipt)] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('efficiencyElectronNVertex_threshold_{}_Den'.format(ipt), '', n_nvtxbins, nvtx_binning), 
                            'denominator_nvtx'
                        )

                        df_loc = df_loc.Define('numerator_eta', 'probe_Eta[inEtaRange&&passL1OffsetCond&&passRecoToL1PtCutFactor]')
                        df_loc = df_loc.Define('numerator_phi', 'probe_Phi[inEtaRange&&passL1OffsetCond&&passRecoToL1PtCutFactor]')
                        df_loc = df_loc.Define('numerator_nvtx', 'probe_Nvtx[inEtaRange&&passL1OffsetCond&&passRecoToL1PtCutFactor]')

                        histos['efficiencyElectronEta_threshold_{}_Num'.format(ipt)] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('efficiencyElectronEta_threshold_{}_Num'.format(ipt), '', n_etabins, eta_binning), 
                            'numerator_eta'
                        )
                        histos['efficiencyElectronPhi_threshold_{}_Num'.format(ipt)] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('efficiencyElectronPhi_threshold_{}_Num'.format(ipt), '', n_phibins, phi_binning), 
                            'numerator_phi'
                        )
                        histos['efficiencyElectronNVertex_threshold_{}_Num'.format(ipt)] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('efficiencyElectronNVertex_threshold_{}_Num'.format(ipt), '', n_nvtxbins, nvtx_binning), 
                            'numerator_nvtx'
                        )

    return df, histos


def ZMuMu_DQMOff_Plots(df, suffix = ''):

    recoToL1PtCutFactor = config['RecoToL1PtCutFactor']

    df = df.Define('probe_Nvtx', 'GetProbeNvtxArray(probe_Pt, PV_npvs)')
     
    # L1Mu_hwCharge = 0 corresponds to Muon_charge = +1
    # L1Mu_hwCharge = 1 corresponds to Muon_charge = -1
    df = df.Define('L1Mu_charge', 'charge_conversion(L1Mu_hwCharge)')

    n_controlhist_ptbins = len(dqmoff_controlhist_muonpt_bins) - 1
    n_controlhist_etabins = len(dqmoff_controlhist_muoneta_bins) - 1
    n_controlhist_phibins = len(dqmoff_controlhist_muonphi_bins) - 1
    histos = {}
    if config['ControlVariables']:
        histos['control_probeMuonPt'] = df.Histo1D (ROOT.RDF.TH1DModel('ProbeMuonPt', '', n_controlhist_ptbins, dqmoff_controlhist_muonpt_bins), 'probe_Pt')
        histos['control_probeMuonEta'] = df.Histo1D (ROOT.RDF.TH1DModel('ProbeMuonEta', '', n_controlhist_etabins, dqmoff_controlhist_muoneta_bins), 'probe_Eta')
        histos['control_probeMuonPhi'] = df.Histo1D (ROOT.RDF.TH1DModel('ProbeMuonPhi', '', n_controlhist_phibins, dqmoff_controlhist_muonphi_bins), 'probe_Phi')

        histos['control_tagMuonPt'] = df.Histo1D (ROOT.RDF.TH1DModel('TagMuonPt', '', n_controlhist_ptbins, dqmoff_controlhist_muonpt_bins), 'tag_Pt')
        histos['control_tagMuonEta'] = df.Histo1D (ROOT.RDF.TH1DModel('TagMuonEta', '', n_controlhist_etabins, dqmoff_controlhist_muoneta_bins), 'tag_Eta')
        histos['control_tagMuonPhi'] = df.Histo1D (ROOT.RDF.TH1DModel('TagMuonPhi', '', n_controlhist_phibins, dqmoff_controlhist_muonphi_bins), 'tag_Phi')


    df_mu = [None] * len(config['Qualities'])

    for i, qual in enumerate(config['Qualities']):

        prefix = qual

        # Get Ids for L1 Muons which match with probe
        df_mu[i] = df.Define('probe_idxL1Mu','FindL1MuIdx(L1Mu_eta, L1Mu_phi, probe_Eta, probe_Phi, probe_Pt, probe_Charge, L1Mu_hwQual, {}, 0.3)'.format(config["Qualities"][qual]))
        df_mu[i] = df_mu[i].Define('probe_idxL1Mu_Bx0','FindL1MuIdx_setBx(L1Mu_eta, L1Mu_phi, L1Mu_bx, probe_Eta, probe_Phi, probe_Pt, probe_Charge, 0, L1Mu_hwQual, {}, 0.3)'.format(config["Qualities"][qual]))
        df_mu[i] = df_mu[i].Define('probe_idxL1Mu_Bxmin1','FindL1MuIdx_setBx(L1Mu_eta, L1Mu_phi, L1Mu_bx, probe_Eta, probe_Phi, probe_Pt, probe_Charge, -1, L1Mu_hwQual, {}, 0.3)'.format(config["Qualities"][qual]))
        df_mu[i] = df_mu[i].Define('probe_idxL1Mu_Bxplus1','FindL1MuIdx_setBx(L1Mu_eta, L1Mu_phi, L1Mu_bx, probe_Eta, probe_Phi, probe_Pt, probe_Charge, 1, L1Mu_hwQual, {}, 0.3)'.format(config["Qualities"][qual]))

        for bx in ['min1', '0', 'plus1'] :
            df_mu[i] = df_mu[i].Define('probe_L1Pt_Bx{}'.format(bx), 'GetVal(probe_idxL1Mu_Bx{}, L1Mu_pt)'.format(bx))
            df_mu[i] = df_mu[i].Define('probe_L1Eta_Bx{}'.format(bx), 'GetVal(probe_idxL1Mu_Bx{}, L1Mu_eta)'.format(bx))
            df_mu[i] = df_mu[i].Define('probe_L1Phi_Bx{}'.format(bx), 'GetVal(probe_idxL1Mu_Bx{}, L1Mu_phi)'.format(bx))
            df_mu[i] = df_mu[i].Define('probe_L1Qual_Bx{}'.format(bx), 'GetVal(probe_idxL1Mu_Bx{}, L1Mu_hwQual)'.format(bx))

        df_mu[i] = df_mu[i].Define('probe_L1Pt','GetVal(probe_idxL1Mu, L1Mu_pt)')
        df_mu[i] = df_mu[i].Define('probe_L1Eta','GetVal(probe_idxL1Mu, L1Mu_eta)')
        df_mu[i] = df_mu[i].Define('probe_L1Phi','GetVal(probe_idxL1Mu, L1Mu_phi)')
        df_mu[i] = df_mu[i].Define('probe_L1Bx','GetVal(probe_idxL1Mu, L1Mu_bx)')
        df_mu[i] = df_mu[i].Define('probe_L1Qual','GetVal(probe_idxL1Mu, L1Mu_hwQual)')
        df_mu[i] = df_mu[i].Define('probe_L1Charge','GetVal(probe_idxL1Mu, L1Mu_charge)')

        df_mu[i] = df_mu[i].Define('probe_L1PtReso','((probe_L1Charge*probe_Charge*probe_Pt)-probe_L1Pt)/probe_L1Pt')
        df_mu[i] = df_mu[i].Define('probe_L1EtaReso','(probe_L1Eta-probe_Eta)')
        df_mu[i] = df_mu[i].Define('probe_L1PhiReso','CorrectedDeltaPhi_OfflineMuStation_L1Mu(probe_Charge, probe_Pt, probe_Eta, probe_Phi, probe_L1Phi)')


        pt_binning = dqmoff_muonpt_bins
        eta_binning = dqmoff_muoneta_bins
        phi_binning = dqmoff_muonphi_bins
        nvtx_binning = dqmoff_muonnvtx_bins
        reso_pt_binning = dqmoff_muonresolution_pt_bins
        reso_eta_binning = dqmoff_muonresolution_eta_bins
        reso_phi_binning = dqmoff_muonresolution_phi_bins
        n_ptbins = len(pt_binning) - 1
        n_etabins = len(eta_binning) - 1
        n_phibins = len(phi_binning) - 1
        n_nvtxbins = len(nvtx_binning) - 1
        n_resoptbins = len(reso_pt_binning) - 1
        n_resoetabins = len(reso_eta_binning) - 1
        n_resophibins = len(reso_phi_binning) - 1

        if qual == 'qualSingle' and config['Prefiring']:
            
            pref_l1thres = 10
            pref_probethres = 12

            colname = 'probe_L1{}'.format(pref_l1thres).replace('.','p')  
            colname1 = 'probe_L1{}_Reco{}'.format(pref_l1thres, pref_probethres).replace('.','p')
            colname2 = 'probe_Reco{}'.format(pref_probethres).replace('.','p')

            df_mu[i] = df_mu[i].Define(colname2+'_Pt', 'probe_Pt[probe_Pt>{}]'.format(pref_probethres))
            df_mu[i] = df_mu[i].Define(colname2+'_Eta', 'probe_Eta[probe_Pt>{}]'.format(pref_probethres))
            df_mu[i] = df_mu[i].Define(colname2+'_Phi', 'probe_Phi[probe_Pt>{}]'.format(pref_probethres))

            for bx in ['min1', '0', 'plus1'] :
                df_mu[i] = df_mu[i].Define(colname+'_Bx{}_Pt'.format(bx), 'probe_Pt[probe_L1Pt_Bx{}>{}]'.format(bx, pref_l1thres))
                df_mu[i] = df_mu[i].Define(colname+'_Bx{}_Eta'.format(bx), 'probe_Eta[probe_L1Pt_Bx{}>{}]'.format(bx, pref_l1thres))
                df_mu[i] = df_mu[i].Define(colname+'_Bx{}_Phi'.format(bx), 'probe_Phi[probe_L1Pt_Bx{}>{}]'.format(bx, pref_l1thres))

                df_mu[i] = df_mu[i].Define(colname1+'_Bx{}_Pt'.format(bx), 'probe_Pt[probe_Pt>{}&&probe_L1Pt_Bx{}>{}]'.format(pref_probethres, bx, pref_l1thres))
                df_mu[i] = df_mu[i].Define(colname1+'_Bx{}_Eta'.format(bx), 'probe_Eta[probe_Pt>{}&&probe_L1Pt_Bx{}>{}]'.format(pref_probethres, bx, pref_l1thres))
                df_mu[i] = df_mu[i].Define(colname1+'_Bx{}_Phi'.format(bx), 'probe_Phi[probe_Pt>{}&&probe_L1Pt_Bx{}>{}]'.format(pref_probethres, bx, pref_l1thres))

                # df_mu[i] = df_mu[i].Define(colname+'Bx{}_runnb'.format(bx), 'return ROOT::VecOps::RVec<int>('+colname+'Bx{}_Eta'.format(bx)+'.size(), run);')

            for typeofevents in ['L1_UnprefireableEvent', 'L1_FirstBunchInTrain' , 'AllEvents'] :
            # for typeofevents in ['AllEvents'] :
                cut_typeofevents = typeofevents
                if typeofevents == 'AllEvents': cut_typeofevents = 'return true;'

                for bx in ['min1', '0', 'plus1'] :           
                    
                    str_pref = 'h_Mu_pref_L1{}'.format(pref_l1thres).replace(".","p")
                    str_pref1 = 'h_Mu_pref_L1{}_Reco{}'.format(pref_l1thres, pref_probethres).replace(".","p")

                    hname = str_pref+'_'+typeofevents+'_bx'+bx+'_eta'+suffix
                    histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), colname+'_Bx{}_Eta'.format(bx))

                    hname = str_pref+'_'+typeofevents+'_bx'+bx+'_phi'+suffix
                    histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), colname+'_Bx{}_Phi'.format(bx))

                    hname = str_pref+'_'+typeofevents+'_bx'+bx+'_etapt'+suffix
                    histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), colname+'_Bx{}_Eta'.format(bx), colname+'_Bx{}_Pt'.format(bx))

                    hname = str_pref+'_'+typeofevents+'_bx'+bx+'_etaphi'+suffix
                    histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), colname+'_Bx{}_Eta'.format(bx), colname+'_Bx{}_Phi'.format(bx))
                    
                    hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_eta'+suffix
                    histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), colname1+'_Bx{}_Eta'.format(bx))

                    hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_phi'+suffix
                    histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), colname1+'_Bx{}_Phi'.format(bx))

                    hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_etapt'+suffix
                    histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), colname1+'_Bx{}_Eta'.format(bx), colname1+'_Bx{}_Pt'.format(bx))

                    hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_etaphi'+suffix
                    histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), colname1+'_Bx{}_Eta'.format(bx), colname1+'_Bx{}_Phi'.format(bx))
                    

                #Denominators
                hname = 'h_Mu_pref_'+typeofevents+'_eta'+suffix
                histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), 'probe_Eta')

                hname = 'h_Mu_pref_'+typeofevents+'_phi'+suffix
                histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), 'probe_Phi')

                hname = 'h_Mu_pref_'+typeofevents+'_etapt'+suffix
                histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), 'probe_Eta', 'probe_Pt')

                hname = 'h_Mu_pref_'+typeofevents+'_etaphi'+suffix
                histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), 'probe_Eta', 'probe_Phi')

                hname = 'h_Mu_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_eta'+suffix
                histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), colname2+'_Eta')

                hname = 'h_Mu_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_phi'+suffix
                histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), colname2+'_Phi')

                hname = 'h_Mu_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_etapt'+suffix
                histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), colname2+'_Eta', colname2+'_Pt')

                hname = 'h_Mu_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_etaphi'+suffix
                histos[hname] = df_mu[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), colname2+'_Eta', colname2+'_Phi')

        if qual == 'qualAll' and config['L1TResolution']:

            df_etarange = [None] * len(config['Regions'])
            for ireg, reg in enumerate(config['Regions']):

                region = config["Regions"][reg]
                str_binEta = "etaMin{}_etaMax{}".format(region[0], region[1]).replace(".","p").replace("p0", "")

                df_etarange[ireg] = df_mu[i].Define('inEtaRange','abs(probe_Eta)>={}'.format(region[0])+'&&abs(probe_Eta)<{}'.format(region[1]))
                df_etarange[ireg] = df_etarange[ireg].Define('reso_pt', 'probe_L1PtReso[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('reso_eta', 'probe_L1EtaReso[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('reso_phi', 'probe_L1PhiReso[inEtaRange]')

                histos['resolution_qoverpt_{}_{}'.format(str_binEta, prefix)] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('resolution_qoverpt_{}_{}'.format(str_binEta, prefix), '', n_resoptbins, reso_pt_binning), 
                    'reso_pt'
                )
                histos['resolution_eta_{}_{}'.format(str_binEta, prefix)] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('resolution_eta_{}_{}'.format(str_binEta, prefix), '', n_resoetabins, reso_eta_binning), 
                    'reso_eta'
                )
                histos['resolution_phi_{}_{}'.format(str_binEta, prefix)] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('resolution_phi_{}_{}'.format(str_binEta, prefix), '', n_resophibins, reso_phi_binning), 
                    'reso_phi'
                )

        if config['L1TEfficiency']:

            df_etarange = [None] * len(config['Regions'])
            for ireg, reg in enumerate(config['Regions']):
                region = config["Regions"][reg]
                
                df_etarange[ireg] = df_mu[i].Define('inEtaRange', 'abs(probe_Eta)>={}'.format(region[0])+'&&abs(probe_Eta)<{}'.format(region[1]))
                
                if qual == 'qualAll':
                    df_etarange[ireg] = df_etarange[ireg].Define('denominator_pt', 'probe_Pt[inEtaRange]')
                    hname = 'effDen_pt_etaMin{}_etaMax{}'.format(region[0], region[1]).replace('.','p').replace('p0', '')
                    histos[hname] = df_etarange[ireg].Histo1D(
                        ROOT.RDF.TH1DModel(hname, '', n_ptbins, pt_binning), 
                        'denominator_pt'
                    )

                l1thresholds = config["Thresholds"]
                for ipt in l1thresholds:

                    cutfactor = ipt * recoToL1PtCutFactor
                    df_loc = df_etarange[ireg].Define('passRecoToL1PtCutFactor', 'probe_Pt>={}'.format(cutfactor))
                    
                    str_PtEta = "{}_etaMin{}_etaMax{}".format(ipt, region[0], region[1]).replace('.','p').replace('p0', '')
                    if qual == 'qualAll':
                        df_loc = df_loc.Define('denominator_phi', 'probe_Phi[inEtaRange&&passRecoToL1PtCutFactor]')
                        df_loc = df_loc.Define('denominator_nvtx', 'probe_Nvtx[inEtaRange&&passRecoToL1PtCutFactor]')

                        histos['effDen_phi_{}'.format(str_PtEta)] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('effDen_phi_{}'.format(str_PtEta), '', n_phibins, phi_binning), 
                            'denominator_phi'
                        )
                        histos['effDen_vtx_{}'.format(str_PtEta)] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('effDen_vtx_{}'.format(str_PtEta), '', n_nvtxbins, nvtx_binning), 
                            'denominator_nvtx'
                        )
                        if (reg == 'AllEta'): 
                            df_loc = df_loc.Define('denominator_eta', 'probe_Eta[inEtaRange&&passRecoToL1PtCutFactor]')
                            histos['effDen_eta_{}'.format(ipt)] = df_loc.Histo1D (
                                ROOT.RDF.TH1DModel('effDen_eta_{}'.format(ipt), '', n_etabins, eta_binning), 
                                'denominator_eta'
                            )

                    df_loc = df_loc.Define('passL1Cond', 'probe_L1Pt>={}'.format(ipt))
                    df_loc = df_loc.Define('numerator_pt', 'probe_Pt[inEtaRange&&passL1Cond]')
                    df_loc = df_loc.Define('numerator_phi', 'probe_Phi[inEtaRange&&passL1Cond&&passRecoToL1PtCutFactor]')
                    df_loc = df_loc.Define('numerator_nvtx', 'probe_Nvtx[inEtaRange&&passL1Cond&&passRecoToL1PtCutFactor]')

                    histos['effNum_pt_{}_{}'.format(str_PtEta, prefix)] = df_loc.Histo1D (
                        ROOT.RDF.TH1DModel('effNum_pt_{}_{}'.format(str_PtEta, prefix), '', n_ptbins, pt_binning), 
                        'numerator_pt'
                    )
                    histos['effNum_phi_{}_{}'.format(str_PtEta, prefix)] = df_loc.Histo1D (
                        ROOT.RDF.TH1DModel('effNum_phi_{}_{}'.format(str_PtEta, prefix), '', n_phibins, phi_binning), 
                        'numerator_phi'
                    )
                    histos['effNum_vtx_{}_{}'.format(str_PtEta, prefix)] = df_loc.Histo1D (
                        ROOT.RDF.TH1DModel('effNum_vtx_{}_{}'.format(str_PtEta, prefix), '', n_nvtxbins, nvtx_binning), 
                        'numerator_nvtx'
                    )
                    if (reg == 'AllEta'):
                        df_loc = df_loc.Define('numerator_eta', 'probe_Eta[inEtaRange&&passL1Cond&&passRecoToL1PtCutFactor]')
                        histos['effNum_eta_{}_{}'.format(ipt, prefix)] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('effNum_eta_{}_{}'.format(ipt, prefix), '', n_etabins, eta_binning), 
                            'numerator_eta'
                        )
    return df, histos


def ZTauTau_DQMOff_Plots(df, suffix = ''):

    df = df.Define('probe_Nvtx', 'GetProbeNvtxArray(probe_Pt, PV_npvs)')
    histos = {}

    df_tau = [None] * len(config['Isos'])
    for i, iso in enumerate(config['Isos']):

        prefix = iso

        # Get Ids for L1 Taus which match with probe
        df_tau[i] = df.Define('probe_idxL1Tau','FindL1ObjIdx(L1Tau_eta, L1Tau_phi, probe_Eta, probe_Phi, L1Tau_hwIso, {}, 0.5)'.format(config['Isos'][iso]))
        df_tau[i] = df_tau[i].Define('probe_idxL1Tau_Bx0','FindL1ObjIdx_setBx(L1Tau_eta, L1Tau_phi, L1Tau_bx, probe_Eta, probe_Phi, 0, L1Tau_hwIso, {}, 0.5)'.format(config['Isos'][iso]))
        df_tau[i] = df_tau[i].Define('probe_idxL1Tau_Bxmin1','FindL1ObjIdx_setBx(L1Tau_eta, L1Tau_phi, L1Tau_bx, probe_Eta, probe_Phi, -1, L1Tau_hwIso, {}, 0.5)'.format(config['Isos'][iso]))
        df_tau[i] = df_tau[i].Define('probe_idxL1Tau_Bxplus1','FindL1ObjIdx_setBx(L1Tau_eta, L1Tau_phi, L1Tau_bx, probe_Eta, probe_Phi, 1, L1Tau_hwIso, {}, 0.5)'.format(config['Isos'][iso]))

        for bx in ['min1', '0', 'plus1'] :
            df_tau[i] = df_tau[i].Define('probe_L1Pt_Bx{}'.format(bx), 'GetVal(probe_idxL1Tau_Bx{}, L1Tau_pt)'.format(bx))
            df_tau[i] = df_tau[i].Define('probe_L1Eta_Bx{}'.format(bx), 'GetVal(probe_idxL1Tau_Bx{}, L1Tau_eta)'.format(bx))
            df_tau[i] = df_tau[i].Define('probe_L1Phi_Bx{}'.format(bx), 'GetVal(probe_idxL1Tau_Bx{}, L1Tau_phi)'.format(bx))
            df_tau[i] = df_tau[i].Define('probe_L1Iso_Bx{}'.format(bx), 'GetVal(probe_idxL1Tau_Bx{}, L1Tau_hwIso)'.format(bx))

        df_tau[i] = df_tau[i].Define('probe_L1Pt','GetVal(probe_idxL1Tau, L1Tau_pt)')
        df_tau[i] = df_tau[i].Define('probe_L1Eta','GetVal(probe_idxL1Tau, L1Tau_eta)')
        df_tau[i] = df_tau[i].Define('probe_L1Phi','GetVal(probe_idxL1Tau, L1Tau_phi)')
        df_tau[i] = df_tau[i].Define('probe_L1Bx','GetVal(probe_idxL1Tau, L1Tau_bx)')
        df_tau[i] = df_tau[i].Define('probe_L1Iso','GetVal(probe_idxL1Tau, L1Tau_hwIso)')

        df_tau[i] = df_tau[i].Define('probe_L1PtReso','(probe_Pt-probe_L1Pt)/probe_L1Pt')
        df_tau[i] = df_tau[i].Define('probe_L1EtaReso','(probe_L1Eta-probe_Eta)')
        df_tau[i] = df_tau[i].Define('probe_L1PhiReso','(probe_L1Phi-probe_Phi)')

        pt_binning = dqmoff_taupt_bins
        eta_binning = dqmoff_taueta_bins
        phi_binning = dqmoff_tauphi_bins
        nvtx_binning = dqmoff_taunvtx_bins
        reso_pt_binning = dqmoff_tauresolution_pt_bins
        reso_eta_binning = dqmoff_tauresolution_eta_bins
        reso_phi_binning = dqmoff_tauresolution_phi_bins
        n_ptbins = len(pt_binning) - 1
        n_etabins = len(eta_binning) - 1
        n_phibins = len(phi_binning) - 1
        n_nvtxbins = len(nvtx_binning) - 1
        n_resoptbins = len(reso_pt_binning) - 1
        n_resoetabins = len(reso_eta_binning) - 1
        n_resophibins = len(reso_phi_binning) - 1

        if iso == 'Iso' and config['Prefiring']:
            
            pref_l1thres = 30
            pref_probethres = 38

            colname = 'probe_L1{}'.format(pref_l1thres).replace(".","p")  
            colname1 = 'probe_L1{}_Reco{}'.format(pref_l1thres, pref_probethres).replace(".","p")
            colname2 = 'probe_Reco{}'.format(pref_probethres).replace(".","p")

            df_tau[i] = df_tau[i].Define(colname2+'_Pt', 'probe_Pt[probe_Pt>{}]'.format(pref_probethres))
            df_tau[i] = df_tau[i].Define(colname2+'_Eta', 'probe_Eta[probe_Pt>{}]'.format(pref_probethres))
            df_tau[i] = df_tau[i].Define(colname2+'_Phi', 'probe_Phi[probe_Pt>{}]'.format(pref_probethres))

            for bx in ['min1', '0', 'plus1'] :
                df_tau[i] = df_tau[i].Define(colname+'_Bx{}_Pt'.format(bx), 'probe_Pt[probe_L1Pt_Bx{}>{}]'.format(bx, pref_l1thres))
                df_tau[i] = df_tau[i].Define(colname+'_Bx{}_Eta'.format(bx), 'probe_Eta[probe_L1Pt_Bx{}>{}]'.format(bx, pref_l1thres))
                df_tau[i] = df_tau[i].Define(colname+'_Bx{}_Phi'.format(bx), 'probe_Phi[probe_L1Pt_Bx{}>{}]'.format(bx, pref_l1thres))

                df_tau[i] = df_tau[i].Define(colname1+'_Bx{}_Pt'.format(bx), 'probe_Pt[probe_Pt>{}&&probe_L1Pt_Bx{}>{}]'.format(pref_probethres, bx, pref_l1thres))
                df_tau[i] = df_tau[i].Define(colname1+'_Bx{}_Eta'.format(bx), 'probe_Eta[probe_Pt>{}&&probe_L1Pt_Bx{}>{}]'.format(pref_probethres, bx, pref_l1thres))
                df_tau[i] = df_tau[i].Define(colname1+'_Bx{}_Phi'.format(bx), 'probe_Phi[probe_Pt>{}&&probe_L1Pt_Bx{}>{}]'.format(pref_probethres, bx, pref_l1thres))

                # df_tau[i] = df_tau[i].Define(colname+'Bx{}_runnb'.format(bx), 'return ROOT::VecOps::RVec<int>('+colname+'Bx{}_Eta'.format(bx)+'.size(), run);')

            for typeofevents in ['L1_UnprefireableEvent', 'L1_FirstBunchInTrain' , 'AllEvents'] :
            # for typeofevents in ['AllEvents'] :
                cut_typeofevents = typeofevents
                if typeofevents == 'AllEvents': cut_typeofevents = 'return true;'

                for bx in ['min1', '0', 'plus1'] :           
                    
                    str_pref = 'h_Tau_pref_L1{}'.format(pref_l1thres).replace(".","p")
                    str_pref1 = 'h_Tau_pref_L1{}_Reco{}'.format(pref_l1thres, pref_probethres).replace(".","p")

                    hname = str_pref+'_'+typeofevents+'_bx'+bx+'_eta'+suffix
                    histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), colname+'_Bx{}_Eta'.format(bx))

                    hname = str_pref+'_'+typeofevents+'_bx'+bx+'_phi'+suffix
                    histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), colname+'_Bx{}_Phi'.format(bx))

                    hname = str_pref+'_'+typeofevents+'_bx'+bx+'_etapt'+suffix
                    histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), colname+'_Bx{}_Eta'.format(bx), colname+'_Bx{}_Pt'.format(bx))

                    hname = str_pref+'_'+typeofevents+'_bx'+bx+'_etaphi'+suffix
                    histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), colname+'_Bx{}_Eta'.format(bx), colname+'_Bx{}_Phi'.format(bx))
                    
                    hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_eta'+suffix
                    histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), colname1+'_Bx{}_Eta'.format(bx))

                    hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_phi'+suffix
                    histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), colname1+'_Bx{}_Phi'.format(bx))

                    hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_etapt'+suffix
                    histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), colname1+'_Bx{}_Eta'.format(bx), colname1+'_Bx{}_Pt'.format(bx))

                    hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_etaphi'+suffix
                    histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), colname1+'_Bx{}_Eta'.format(bx), colname1+'_Bx{}_Phi'.format(bx))
                    

                #Denominators
                hname = 'h_Tau_pref_'+typeofevents+'_eta'+suffix
                histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), 'probe_Eta')

                hname = 'h_Tau_pref_'+typeofevents+'_phi'+suffix
                histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), 'probe_Phi')

                hname = 'h_Tau_pref_'+typeofevents+'_etapt'+suffix
                histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), 'probe_Eta', 'probe_Pt')

                hname = 'h_Tau_pref_'+typeofevents+'_etaphi'+suffix
                histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), 'probe_Eta', 'probe_Phi')

                hname = 'h_Tau_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_eta'+suffix
                histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), colname2+'_Eta')

                hname = 'h_Tau_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_phi'+suffix
                histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), colname2+'_Phi')

                hname = 'h_Tau_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_etapt'+suffix
                histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), colname2+'_Eta', colname2+'_Pt')

                hname = 'h_Tau_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_etaphi'+suffix
                histos[hname] = df_tau[i].Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), colname2+'_Eta', colname2+'_Phi')


        if iso == 'NonIso' and config['L1TResolution']:

            df_etarange = [None] * len(config['Regions'])
            for ireg, reg in enumerate(config['Regions']):

                region = config["Regions"][reg]
                str_binEta = "eta{}to{}".format(region[0], region[1]).replace(".","p")

                df_etarange[ireg] = df_tau[i].Define('inEtaRange','abs(probe_Eta)>={}'.format(region[0])+'&&abs(probe_Eta)<{}'.format(region[1]))
                df_etarange[ireg] = df_etarange[ireg].Define('reso_pt', 'probe_L1PtReso[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('reso_eta', 'probe_L1EtaReso[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('reso_phi', 'probe_L1PhiReso[inEtaRange]')

                histos['resolutionTauET_{}'.format(reg)] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('resolutionTauET_{}'.format(reg), '', n_resoptbins, reso_pt_binning), 
                    'reso_pt'
                )
                histos['resolutionTauPhi_{}'.format(reg)] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('resolutionTauPhi_{}'.format(reg), '', n_resophibins, reso_phi_binning), 
                    'reso_phi'
                )
                if reg == 'EB_EE':
                    histos['resolutionTauEta'] = df_etarange[ireg].Histo1D (
                        ROOT.RDF.TH1DModel('resolutionTauEta', '', n_resoetabins, reso_eta_binning), 
                        'reso_eta'
                    )


        if config['L1TEfficiency']:

            df_etarange = [None] * len(config['Regions'])
            for ireg, reg in enumerate(config['Regions']):

                region = config["Regions"][reg]

                df_etarange[ireg] = df_tau[i].Define('inEtaRange','abs(probe_Eta)>={}'.format(region[0])+'&&abs(probe_Eta)<{}'.format(region[1]))
                df_etarange[ireg] = df_etarange[ireg].Define('denominator_pt', 'probe_Pt[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('denominator_phi', 'probe_Phi[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('denominator_nvtx', 'probe_Nvtx[inEtaRange]')
                if (reg == 'EB_EE'): 
                    df_etarange[ireg] = df_etarange[ireg].Define('denominator_eta', 'probe_Eta[inEtaRange]')

                l1thresholds = config["Thresholds"]
                for ipt in l1thresholds:
                    str_binEtaPt = "eta{}to{}_l1thrgeq{}".format(region[0], region[1], ipt).replace(".","p")
                    df_loc = df_etarange[ireg].Define('passL1Cond', 'probe_L1Pt>={}'.format(ipt))
                    df_loc = df_loc.Define('numerator_pt', 'probe_Pt[inEtaRange&&passL1Cond]')
                    df_loc = df_loc.Define('numerator_phi', 'probe_Phi[inEtaRange&&passL1Cond]')
                    df_loc = df_loc.Define('numerator_nvtx', 'probe_Nvtx[inEtaRange&&passL1Cond]')
                    if (reg == 'EB_EE'):
                        df_loc = df_loc.Define('numerator_eta', 'probe_Eta[inEtaRange&&passL1Cond]')

                    histos['efficiency{}TauET_{}_threshold_{}_Den'.format(prefix, reg, ipt)] = df_loc.Histo1D (
                        ROOT.RDF.TH1DModel('efficiency{}TauET_{}_threshold_{}_Den'.format(prefix, reg, ipt), '', n_ptbins, pt_binning), 
                        'denominator_pt'
                    )

                    histos['efficiency{}TauET_{}_threshold_{}_Num'.format(prefix, reg, ipt)] = df_loc.Histo1D (
                        ROOT.RDF.TH1DModel('efficiency{}TauET_{}_threshold_{}_Num'.format(prefix, reg, ipt), '', n_ptbins, pt_binning), 
                        'numerator_pt'
                    )
                   
    return df, histos


def Jet_DQMOff_Plots(df, suffix = ''):

    histos = {}
    prefix = ''

    df = df.Define('probe_Pt', 'leadJetPt')
    df = df.Define('probe_Eta', 'leadJetEta')
    df = df.Define('probe_Phi', 'leadJetPhi')

    df_jet = df.Define('lead_idxL1Jet', 'FindL1ObjIdx(L1Jet_eta, L1Jet_phi, leadJetEta, leadJetPhi, {}, -1, 0.3)')
    df_jet = df_jet.Define('lead_idxL1Jet_Bx0', 'FindL1ObjIdx_setBx(L1Jet_eta, L1Jet_phi, L1Jet_bx, leadJetEta, leadJetPhi, 0, {}, -1, 0.3)')
    df_jet = df_jet.Define('lead_idxL1Jet_Bxmin1', 'FindL1ObjIdx_setBx(L1Jet_eta, L1Jet_phi, L1Jet_bx, leadJetEta, leadJetPhi, -1, {}, -1, 0.3)')
    df_jet = df_jet.Define('lead_idxL1Jet_Bxplus1', 'FindL1ObjIdx_setBx(L1Jet_eta, L1Jet_phi, L1Jet_bx, leadJetEta, leadJetPhi, 1, {}, -1, 0.3)')

    for bx in ['min1', '0', 'plus1'] :
        df_jet = df_jet.Define('probe_L1Pt_Bx{}'.format(bx), 'GetVal(lead_idxL1Jet_Bx{}, L1Jet_pt)'.format(bx))
        df_jet = df_jet.Define('probe_L1Eta_Bx{}'.format(bx), 'GetVal(lead_idxL1Jet_Bx{}, L1Jet_eta)'.format(bx))
        df_jet = df_jet.Define('probe_L1Phi_Bx{}'.format(bx), 'GetVal(lead_idxL1Jet_Bx{}, L1Jet_phi)'.format(bx))


    df_jet = df_jet.Define('lead_L1JetPt', 'GetVal(lead_idxL1Jet_Bx0, L1Jet_pt)')
    df_jet = df_jet.Define('lead_L1JetEta', 'GetVal(lead_idxL1Jet_Bx0, L1Jet_eta)')
    df_jet = df_jet.Define('lead_L1JetPhi', 'GetVal(lead_idxL1Jet_Bx0, L1Jet_phi)')
    df_jet = df_jet.Define('lead_L1JetBx', 'GetVal(lead_idxL1Jet_Bx0, L1Jet_bx)')

    # TrigObj matching
    df_jet = df_jet.Define('LeadJet_trig_idx', 'MatchObjToTrig(lead_L1JetEta, lead_L1JetPhi, TrigObj_pt, TrigObj_eta, TrigObj_phi, TrigObj_id, 1, TrigObj_filterBits, 3, 0.3, 27)')
    df_jet = df_jet.Define('LeadJet_matchHLT', 'trig_is_filterbit1_set(LeadJet_trig_idx, TrigObj_filterBits, 3)')
    df_jet = df_jet.Filter('Sum(LeadJet_matchHLT)==0')

    df_jet = df_jet.Define('lead_L1PtReso', '(lead_L1JetPt - leadJetPt)/leadJetPt')
    df_jet = df_jet.Define('lead_L1EtaReso', '(lead_L1JetEta - leadJetEta)')
    df_jet = df_jet.Define('lead_L1PhiReso', 'GetReducedDeltaphi(lead_L1JetPhi, leadJetPhi)')

    pt_binning = dqmoff_jetpt_bins
    reso_pt_binning = dqmoff_jetresolution_pt_bins
    reso_eta_binning = dqmoff_jetresolution_eta_bins
    reso_phi_binning = dqmoff_jetresolution_phi_bins
    n_ptbins = len(pt_binning) - 1
    n_resoptbins = len(reso_pt_binning) - 1
    n_resoetabins = len(reso_eta_binning) - 1
    n_resophibins = len(reso_phi_binning) - 1

    if config['Prefiring']:
        
        pref_l1thres = 50
        pref_probethres = 65

        colname = 'probe_L1{}'.format(pref_l1thres).replace(".","p")  
        colname1 = 'probe_L1{}_Reco{}'.format(pref_l1thres, pref_probethres).replace(".","p")
        colname2 = 'probe_Reco{}'.format(pref_probethres).replace(".","p")

        df_jet = df_jet.Define(colname2+'_Pt', 'probe_Pt[probe_Pt>{}]'.format(pref_probethres))
        df_jet = df_jet.Define(colname2+'_Eta', 'probe_Eta[probe_Pt>{}]'.format(pref_probethres))
        df_jet = df_jet.Define(colname2+'_Phi', 'probe_Phi[probe_Pt>{}]'.format(pref_probethres))

        for bx in ['min1', '0', 'plus1'] :
            df_jet = df_jet.Define(colname+'_Bx{}_Pt'.format(bx), 'probe_Pt[probe_L1Pt_Bx{}>{}]'.format(bx, pref_l1thres))
            df_jet = df_jet.Define(colname+'_Bx{}_Eta'.format(bx), 'probe_Eta[probe_L1Pt_Bx{}>{}]'.format(bx, pref_l1thres))
            df_jet = df_jet.Define(colname+'_Bx{}_Phi'.format(bx), 'probe_Phi[probe_L1Pt_Bx{}>{}]'.format(bx, pref_l1thres))

            df_jet = df_jet.Define(colname1+'_Bx{}_Pt'.format(bx), 'probe_Pt[probe_Pt>{}&&probe_L1Pt_Bx{}>{}]'.format(pref_probethres, bx, pref_l1thres))
            df_jet = df_jet.Define(colname1+'_Bx{}_Eta'.format(bx), 'probe_Eta[probe_Pt>{}&&probe_L1Pt_Bx{}>{}]'.format(pref_probethres, bx, pref_l1thres))
            df_jet = df_jet.Define(colname1+'_Bx{}_Phi'.format(bx), 'probe_Phi[probe_Pt>{}&&probe_L1Pt_Bx{}>{}]'.format(pref_probethres, bx, pref_l1thres))

            # df_jet = df_jet.Define(colname+'Bx{}_runnb'.format(bx), 'return ROOT::VecOps::RVec<int>('+colname+'Bx{}_Eta'.format(bx)+'.size(), run);')

        for typeofevents in ['L1_UnprefireableEvent', 'L1_FirstBunchInTrain' , 'AllEvents'] :
        # for typeofevents in ['AllEvents'] :
            cut_typeofevents = typeofevents
            if typeofevents == 'AllEvents': cut_typeofevents = 'return true;'

            for bx in ['min1', '0', 'plus1'] :           
                
                str_pref = 'h_Jet_pref_L1{}'.format(pref_l1thres).replace(".","p")
                str_pref1 = 'h_Jet_pref_L1{}_Reco{}'.format(pref_l1thres, pref_probethres).replace(".","p")

                hname = str_pref+'_'+typeofevents+'_bx'+bx+'_eta'+suffix
                histos[hname] = df_jet.Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), colname+'_Bx{}_Eta'.format(bx))

                hname = str_pref+'_'+typeofevents+'_bx'+bx+'_phi'+suffix
                histos[hname] = df_jet.Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), colname+'_Bx{}_Phi'.format(bx))

                hname = str_pref+'_'+typeofevents+'_bx'+bx+'_etapt'+suffix
                histos[hname] = df_jet.Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), colname+'_Bx{}_Eta'.format(bx), colname+'_Bx{}_Pt'.format(bx))

                hname = str_pref+'_'+typeofevents+'_bx'+bx+'_etaphi'+suffix
                histos[hname] = df_jet.Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), colname+'_Bx{}_Eta'.format(bx), colname+'_Bx{}_Phi'.format(bx))
                
                hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_eta'+suffix
                histos[hname] = df_jet.Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), colname1+'_Bx{}_Eta'.format(bx))

                hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_phi'+suffix
                histos[hname] = df_jet.Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), colname1+'_Bx{}_Phi'.format(bx))

                hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_etapt'+suffix
                histos[hname] = df_jet.Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), colname1+'_Bx{}_Eta'.format(bx), colname1+'_Bx{}_Pt'.format(bx))

                hname = str_pref1+'_'+typeofevents+'_bx'+bx+'_etaphi'+suffix
                histos[hname] = df_jet.Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), colname1+'_Bx{}_Eta'.format(bx), colname1+'_Bx{}_Phi'.format(bx))
                

            #Denominators
            hname = 'h_Jet_pref_'+typeofevents+'_eta'+suffix
            histos[hname] = df_jet.Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), 'probe_Eta')

            hname = 'h_Jet_pref_'+typeofevents+'_phi'+suffix
            histos[hname] = df_jet.Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), 'probe_Phi')

            hname = 'h_Jet_pref_'+typeofevents+'_etapt'+suffix
            histos[hname] = df_jet.Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), 'probe_Eta', 'probe_Pt')

            hname = 'h_Jet_pref_'+typeofevents+'_etaphi'+suffix
            histos[hname] = df_jet.Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), 'probe_Eta', 'probe_Phi')

            hname = 'h_Jet_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_eta'+suffix
            histos[hname] = df_jet.Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -5, 5), colname2+'_Eta')

            hname = 'h_Jet_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_phi'+suffix
            histos[hname] = df_jet.Filter(cut_typeofevents).Histo1D(ROOT.RDF.TH1DModel(hname, '', 100, -3.1416, 3.1416), colname2+'_Phi')

            hname = 'h_Jet_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_etapt'+suffix
            histos[hname] = df_jet.Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', len(dqmoff_prefire_etabins)-1, dqmoff_prefire_etabins, len(dqmoff_prefire_ptbins)-1, dqmoff_prefire_ptbins), colname2+'_Eta', colname2+'_Pt')

            hname = 'h_Jet_pref_Reco{}_'.format(pref_probethres).replace(".","p")+typeofevents+'_etaphi'+suffix
            histos[hname] = df_jet.Filter(cut_typeofevents).Histo2D(ROOT.RDF.TH2DModel(hname, '', 100, -5, 5, 100, -3.1416, 3.1416), colname2+'_Eta', colname2+'_Phi')

    if config['L1TResolution']:
        df_etarange = [None] * len(config['Regions'])
        for ireg, reg in enumerate(config['Regions']):
            region = config["Regions"][reg]
            str_binEta = "eta{}to{}".format(region[0], region[1]).replace(".","p")

            df_etarange[ireg] = df_jet.Define('inEtaRange','abs(leadJetEta)>={}'.format(region[0])+'&&abs(leadJetEta)<{}'.format(region[1]))
            df_etarange[ireg] = df_etarange[ireg].Define('reso_pt', 'lead_L1PtReso[inEtaRange]')
            df_etarange[ireg] = df_etarange[ireg].Define('reso_eta', 'lead_L1EtaReso[inEtaRange]')
            df_etarange[ireg] = df_etarange[ireg].Define('reso_phi', 'lead_L1PhiReso[inEtaRange]')

            histos['resolutionJetET_{}'.format(reg)] = df_etarange[ireg].Histo1D (
                ROOT.RDF.TH1DModel('resolutionJetET_{}'.format(reg), '', n_resoptbins, reso_pt_binning), 
                'reso_pt'
            )
            histos['resolutionJetPhi_{}'.format(reg)] = df_etarange[ireg].Histo1D (
                ROOT.RDF.TH1DModel('resolutionJetPhi_{}'.format(reg), '', n_resophibins, reso_phi_binning), 
                'reso_phi'
            )
            if reg == 'HB_HE': # Check! resolutionJetEta plot title in centrally produced DQM ROOT file shows (HB)
                histos['resolutionJetEta'.format(reg)] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('resolutionJetEta'.format(reg), '', n_resoetabins, reso_eta_binning), 
                    'reso_eta'
                )

    if config['L1TEfficiency']:
        df_etarange = [None] * len(config['Regions'])
        for ireg, reg in enumerate(config['Regions']):
            region = config["Regions"][reg]

            df_etarange[ireg] = df_jet.Define('inEtaRange','abs(leadJetEta)>={}'.format(region[0])+'&&abs(leadJetEta)<{}'.format(region[1]))
            df_etarange[ireg] = df_etarange[ireg].Define('denominator_pt', 'leadJetPt[inEtaRange]')

            l1thresholds = config["Thresholds"]
            for ipt in l1thresholds:

                df_loc = df_etarange[ireg].Define('passL1Cond', 'lead_L1JetPt>={}'.format(ipt))
                df_loc = df_loc.Define('numerator_pt', 'leadJetPt[inEtaRange&&passL1Cond]')

                histos['efficiencyJetEt_{}_threshold_{}_Den'.format(reg, ipt)] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('efficiencyJetEt_{}_threshold_{}_Den'.format(reg, ipt), '', n_ptbins, pt_binning), 
                    'denominator_pt'
                )
                histos['efficiencyJetEt_{}_threshold_{}_Num'.format(reg, ipt)] = df_loc.Histo1D (
                    ROOT.RDF.TH1DModel('efficiencyJetEt_{}_threshold_{}_Num'.format(reg, ipt), '', n_ptbins, pt_binning), 
                    'numerator_pt'
                )

    return df, histos


def EtSum_DQMOff_Plots(df, suffix = ''):

    histos = {}
    prefix = ''

    df_met = df.Define('idxL1MET', 'FindL1EtSumIdx_setBx(L1EtSum_etSumType, L1EtSum_bx, 2, 0)')
    df_met = df_met.Define('L1MET', 'L1EtSum_pt[idxL1MET]')
    df_met = df_met.Define('L1METPhi', 'L1EtSum_phi[idxL1MET]')
    df_met = df_met.Define('reso_met', '(L1MET - recoMET)/recoMET')
    df_met = df_met.Define('reso_metphi', 'L1METPhi - recoMETPhi')

    df_met = df_met.Define('idxL1MHT', 'FindL1EtSumIdx_setBx(L1EtSum_etSumType, L1EtSum_bx, 3, 0)')
    df_met = df_met.Define('L1MHT', 'L1EtSum_pt[idxL1MHT]')
    df_met = df_met.Define('L1MHTPhi', 'L1EtSum_phi[idxL1MHT]')
    df_met = df_met.Define('reso_mht', '(L1MHT - recoMHT)/recoMHT')
    df_met = df_met.Define('reso_mhtphi', 'L1MHTPhi - recoMHTPhi')


    df_met = df_met.Define('idxL1HTT', 'FindL1EtSumIdx_setBx(L1EtSum_etSumType, L1EtSum_bx, 8, 0)')
    df_met = df_met.Define('L1HTT', 'L1EtSum_pt[idxL1HTT]')
    df_met = df_met.Define('reso_htt', '(L1HTT - recoHTT)/recoHTT')
    
    df_met = df_met.Define('idxL1ETT', 'FindL1EtSumIdx_setBx(L1EtSum_etSumType, L1EtSum_bx, 1, 0)')
    df_met = df_met.Define('L1ETT', 'L1EtSum_pt[idxL1ETT]')
    df_met = df_met.Define('reso_ett', '(L1ETT - recoETT)/recoETT')
    

    met_binning = dqmoff_etsum_bins
    n_metbins = len(met_binning) - 1

    reso_pt_binning = dqmoff_etsumresolution_met_bins
    reso_phi_binning = dqmoff_etsumresolution_metphi_bins

    n_resoptbins = len(reso_pt_binning) - 1
    n_resophibins = len(reso_phi_binning) - 1

    if config['L1TResolution']:

        histos['resolutionMET'] = df_met.Histo1D (
            ROOT.RDF.TH1DModel('resolutionMET', '', n_resoptbins, reso_pt_binning), 
            'reso_met'
        )
        histos['resolutionMETPhi'] = df_met.Histo1D (
            ROOT.RDF.TH1DModel('resolutionMETPhi', '', n_resophibins, reso_phi_binning), 
            'reso_metphi'
        )
        histos['resolutionMHT'] = df_met.Histo1D (
            ROOT.RDF.TH1DModel('resolutionMHT', '', n_resoptbins, reso_pt_binning), 
            'reso_mht'
        )
        histos['resolutionMHTPhi'] = df_met.Histo1D (
            ROOT.RDF.TH1DModel('resolutionMHTPhi', '', n_resophibins, reso_phi_binning), 
            'reso_mhtphi'
        )
        histos['resolutionHTT'] = df_met.Histo1D (
            ROOT.RDF.TH1DModel('resolutionHTT', '', n_resoptbins, reso_pt_binning), 
            'reso_htt'
        )
        histos['resolutionETT'] = df_met.Histo1D (
            ROOT.RDF.TH1DModel('resolutionETT', '', n_resoptbins, reso_pt_binning), 
            'reso_ett'
        )

    if config['L1TEfficiency']:

        # Numerator Histograms for all Et thresholds
        l1thresholds = config["Thresholds"]
        for imet in l1thresholds:
            df_loc = df_met.Define('passL1Cond', 'L1MET>={}'.format(imet))

            histos['efficiencyMET_threshold_{}_Den'.format(imet)] = df_loc.Histo1D (
                ROOT.RDF.TH1DModel('efficiencyMET_threshold_{}_Den'.format(imet), '', n_metbins, met_binning), 
                'recoMET'
            )

            histos['efficiencyMET_threshold_{}_Num'.format(imet)] = df_loc.Filter('passL1Cond').Histo1D (
                ROOT.RDF.TH1DModel('efficiencyMET_threshold_{}_Num'.format(imet), '', n_metbins, met_binning), 
                'recoMET'
            )

    return df, histos


def PrefiringVsMjj(df): 
    histos = {}
    histos['mjj'] =  df.Histo1D(ROOT.RDF.TH1DModel('mjj', '', len(ht_bins)-1, array('d',ht_bins) ), '_mjj') 

    histos['mjj_unpref_trigrules_barrelbarrel'] =  df.Filter('(L1_UnprefireableEvent)').Filter('barrelbarrel').Histo1D(ROOT.RDF.TH1DModel('mjj_unpref_trigrules_barrelbarrel', '', len(ht_bins)-1, array('d',ht_bins) ), '_mjj')
    histos['mjj_unpref_trigrules_L1FinalORBXmin1_barrelbarrel'] =  df.Filter('L1_FinalOR_BXmin1').Filter('(L1_UnprefireableEvent)').Filter('barrelbarrel').Histo1D(ROOT.RDF.TH1DModel('mjj_unpref_trigrules_L1FinalORBXmin1_barrelbarrel', '', len(ht_bins)-1, array('d',ht_bins) ), '_mjj')
    histos['mjj_unpref_trigrules_L1FinalORBXmin2_barrelbarrel'] =  df.Filter('L1_FinalOR_BXmin2').Filter('(L1_UnprefireableEvent)').Filter('barrelbarrel').Histo1D(ROOT.RDF.TH1DModel('mjj_unpref_trigrules_L1FinalORBXmin2_barrelbarrel', '', len(ht_bins)-1, array('d',ht_bins) ), '_mjj')
    histos['mjj_unpref_trigrules_endcapendcap'] =  df.Filter('(L1_UnprefireableEvent)').Filter('endcapendcap').Histo1D(ROOT.RDF.TH1DModel('mjj_unpref_trigrules_endcapendcap', '', len(ht_bins)-1, array('d',ht_bins) ), '_mjj')
    histos['mjj_unpref_trigrules_L1FinalORBXmin1_endcapendcap'] =  df.Filter('L1_FinalOR_BXmin1').Filter('(L1_UnprefireableEvent)').Filter('endcapendcap').Histo1D(ROOT.RDF.TH1DModel('mjj_unpref_trigrules_L1FinalORBXmin1_endcapendcap', '', len(ht_bins)-1, array('d',ht_bins) ), '_mjj')
    histos['mjj_unpref_trigrules_L1FinalORBXmin2_endcapendcap'] =  df.Filter('L1_FinalOR_BXmin2').Filter('(L1_UnprefireableEvent)').Filter('endcapendcap').Histo1D(ROOT.RDF.TH1DModel('mjj_unpref_trigrules_L1FinalORBXmin2_endcapendcap', '', len(ht_bins)-1, array('d',ht_bins) ), '_mjj')

    #1st bx in trains (can only check BX-1, not BX-2)
    histos['mjj_unpref_1stbx_barrelbarrel'] =  df.Filter('(L1_FirstBunchInTrain)').Filter('barrelbarrel').Histo1D(ROOT.RDF.TH1DModel('mjj_unpref_1stbx_barrelbarrel', '', len(ht_bins)-1, array('d',ht_bins) ), '_mjj')
    histos['mjj_unpref_1stbx_L1FinalORBXmin1_barrelbarrel'] =  df.Filter('L1_FinalOR_BXmin1').Filter('(L1_FirstBunchInTrain)').Filter('barrelbarrel').Histo1D(ROOT.RDF.TH1DModel('mjj_unpref_1stbx_L1FinalORBXmin1_barrelbarrel', '', len(ht_bins)-1, array('d',ht_bins) ), '_mjj')
    histos['mjj_unpref_1stbx_endcapendcap'] =  df.Filter('(L1_FirstBunchInTrain)').Filter('endcapendcap').Histo1D(ROOT.RDF.TH1DModel('mjj_unpref_1stbx_endcapendcap', '', len(ht_bins)-1, array('d',ht_bins) ), '_mjj')
    histos['mjj_unpref_1stbx_L1FinalORBXmin1_endcapendcap'] =  df.Filter('L1_FinalOR_BXmin1').Filter('(L1_FirstBunchInTrain)').Filter('endcapendcap').Histo1D(ROOT.RDF.TH1DModel('mjj_unpref_1stbx_L1FinalORBXmin1_endcapendcap', '', len(ht_bins)-1, array('d',ht_bins) ), '_mjj')
    
    return df, histos

def PrefiringVsMll(df): 
    histos = {}
    histos['mll'] =  df.Histo1D(ROOT.RDF.TH1DModel('mll', '', len(ht_bins)-1, array('d',ht_bins) ), '_mll') 
    histos['mll_zoom'] =  df.Histo1D(ROOT.RDF.TH1DModel('mll_zoom', '', 60, 60, 120 ), '_mll') 
    histos['mll_unpref_trigrules_barrelbarrel'] =  df.Filter('(L1_UnprefireableEvent)').Filter('barrelbarrel').Histo1D(ROOT.RDF.TH1DModel('mll_unpref_trigrules_barrelbarrel', '', len(ht_bins)-1, array('d',ht_bins) ), '_mll')
    histos['mll_unpref_trigrules_L1FinalORBXmin1_barrelbarrel'] =  df.Filter('L1_FinalOR_BXmin1').Filter('(L1_UnprefireableEvent)').Filter('barrelbarrel').Histo1D(ROOT.RDF.TH1DModel('mll_unpref_trigrules_L1FinalORBXmin1_barrelbarrel', '', len(ht_bins)-1, array('d',ht_bins) ), '_mll')
    histos['mll_unpref_trigrules_L1FinalORBXmin2_barrelbarrel'] =  df.Filter('L1_FinalOR_BXmin2').Filter('(L1_UnprefireableEvent)').Filter('barrelbarrel').Histo1D(ROOT.RDF.TH1DModel('mll_unpref_trigrules_L1FinalORBXmin2_barrelbarrel', '', len(ht_bins)-1, array('d',ht_bins) ), '_mll')
    histos['mll_unpref_trigrules_endcapendcap'] =  df.Filter('(L1_UnprefireableEvent)').Filter('endcapendcap').Histo1D(ROOT.RDF.TH1DModel('mll_unpref_trigrules_endcapendcap', '', len(ht_bins)-1, array('d',ht_bins) ), '_mll')
    histos['mll_unpref_trigrules_L1FinalORBXmin1_endcapendcap'] =  df.Filter('L1_FinalOR_BXmin1').Filter('(L1_UnprefireableEvent)').Filter('endcapendcap').Histo1D(ROOT.RDF.TH1DModel('mll_unpref_trigrules_L1FinalORBXmin1_endcapendcap', '', len(ht_bins)-1, array('d',ht_bins) ), '_mll')
    histos['mll_unpref_trigrules_L1FinalORBXmin2_endcapendcap'] =  df.Filter('L1_FinalOR_BXmin2').Filter('(L1_UnprefireableEvent)').Filter('endcapendcap').Histo1D(ROOT.RDF.TH1DModel('mll_unpref_trigrules_L1FinalORBXmin2_endcapendcap', '', len(ht_bins)-1, array('d',ht_bins) ), '_mll')

    #1st bx in trains (can only check BX-1, not BX-2)
    histos['mll_unpref_1stbx_barrelbarrel'] =  df.Filter('(L1_FirstBunchInTrain)').Filter('barrelbarrel').Histo1D(ROOT.RDF.TH1DModel('mll_unpref_1stbx_barrelbarrel', '', len(ht_bins)-1, array('d',ht_bins) ), '_mll')
    histos['mll_unpref_1stbx_L1FinalORBXmin1_barrelbarrel'] =  df.Filter('L1_FinalOR_BXmin1').Filter('(L1_FirstBunchInTrain)').Filter('barrelbarrel').Histo1D(ROOT.RDF.TH1DModel('mll_unpref_1stbx_L1FinalORBXmin1_barrelbarrel', '', len(ht_bins)-1, array('d',ht_bins) ), '_mll')
    histos['mll_unpref_1stbx_endcapendcap'] =  df.Filter('(L1_FirstBunchInTrain)').Filter('endcapendcap').Histo1D(ROOT.RDF.TH1DModel('mll_unpref_1stbx_endcapendcap', '', len(ht_bins)-1, array('d',ht_bins) ), '_mll')
    histos['mll_unpref_1stbx_L1FinalORBXmin1_endcapendcap'] =  df.Filter('L1_FinalOR_BXmin1').Filter('(L1_FirstBunchInTrain)').Filter('endcapendcap').Histo1D(ROOT.RDF.TH1DModel('mll_unpref_1stbx_L1FinalORBXmin1_endcapendcap', '', len(ht_bins)-1, array('d',ht_bins) ), '_mll')
    


