import ROOT
import yaml
import json
from array import array
from math import floor, ceil

from bins import *

response_bins = array('f',[0.+float(i)/100. for i in range(200)] )

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



#String printing stuff for a few events
stringToPrint = '''
if(EventsToPrint <100) {

cout << "*********New Event********"<<endl;
cout << "run " << run<<endl;

for(unsigned int i = 0;i< (_lPt).size();i++ ){
cout << "Lepton Pt, Eta, Phi: " << (_lPt)[i]<<", "<<(_lEta)[i]<<", "<<(_lPhi)[i]<<endl;
cout << "Lepton pdgId: " << (_lpdgId)[i]<<endl;
}
for(unsigned int i = 0;i< (Photon_pt).size();i++ ){
cout << "Photon Pt, Eta, Phi: " << (Photon_pt)[i]<<", "<<(Photon_eta)[i]<<", "<<(Photon_phi)[i]<<endl;
}
for(unsigned int i = 0;i< (Jet_pt).size();i++ ){
cout << "jet Pt, Eta, Phi: " << (Jet_pt)[i]<<", "<<(Jet_eta)[i]<<", "<<(Jet_phi)[i]<<endl;
cout << "jet PassID, MUEF, CEEF, CHEF: " << (_jetPassID)[i]<<", "<<(Jet_muEF)[i]<<", "<<(Jet_chEmEF)[i]<<", "<<  (Jet_chHEF)[i]<<endl;
}

for(unsigned int i = 0;i< (L1EG_pt).size();i++ ){
cout << "L1 EG Pt, Eta, Phi: " << (L1EG_pt)[i]<<", "<<(L1EG_eta)[i]<<", "<<(L1EG_phi)[i]<<endl;
}

cout << "probe_L1PtoverRecoPt probe_Pt sizes: "<<probe_L1PtoverRecoPt.size()<<", " <<probe_Pt.size()<<endl;
for(unsigned int i = 0;i< probe_Pt.size();i++ ){
cout << "probe_Pt, probe_L1PtoverRecoPt: "<<probe_L1PtoverRecoPt[i]<<", "<<probe_Pt[i]<<endl;
}

cout << "response, denominator_pt sizes: " << response.size()<<", " <<denominator_pt.size()<<endl;
for(unsigned int i = 0;i<response.size() ;i++ ){
cout <<"response, denominator_pt "<<response[i]<<", "<<denominator_pt[i]<<endl; 
} 
cout <<endl;

EventsToPrint++;
} 
return true;
'''


stringToPrintJets = '''
for(unsigned int i = 0;i< (cleanJet_MUEF).size();i++ ){ 
if((cleanJet_MUEF)[i]>0.5){
cout << "jet Pt, Eta, Phi: " << (cleanJet_Pt)[i]<<", "<<(cleanJet_Eta)[i]<<", "<<(cleanJet_Phi)[i]<<", " << (cleanJet_MUEF)[i]<<endl;

}
}
return true;
'''

stringFailingJets = '''

bool findbadjet = false;
for(unsigned int i = 0;i< (cleanJet_MUEF).size();i++ ){
if((cleanJet_Pt)[i]>300&&abs((cleanJet_Eta)[i])<2.5&&cleanJet_L1Pt[i]<50){
cout << "runNb: "<< run<<endl;
cout << "jet Pt, Eta, Phi: " << (cleanJet_Pt)[i]<<", "<<(cleanJet_Eta)[i]<<", "<<(cleanJet_Phi)[i]<< endl; 
cout << "jet NHEF, CHEF, NEEF, CEEF, MUEF: "<<(cleanJet_NHEF)[i]<< ", " << (cleanJet_CHEF)[i]<< ", " << (cleanJet_NEEF)[i]<< ", "<< (cleanJet_CEEF)[i]<< ", " << (cleanJet_MUEF)[i]<<endl;

findbadjet = true;
}
}
if(findbadjet){
for(unsigned int i = 0;i< (L1Jet_pt).size();i++ ){
cout << "L1 JET Pt, Eta, Phi, Bx: " << (L1Jet_pt)[i]<<", "<<(L1Jet_eta)[i]<<", "<<(L1Jet_phi)[i]<< ", "<<(L1Jet_bx)[i]<<endl;
}
}

return true;
'''

stringToPrintHF = '''
if(EventsToPrint <100) {

cout << "*********New Event********"<<endl;
cout << "run " << run<<endl;
cout << "met, met_phi " << PuppiMET_pt <<", "<<PuppiMET_phi<<endl;
for(unsigned int i = 0;i< (_lPt).size();i++ ){
cout << "Lepton Pt, Eta, Phi: " << (_lPt)[i]<<", "<<(_lEta)[i]<<", "<<(_lPhi)[i]<<endl;
cout << "Lepton pdgId: " << (_lpdgId)[i]<<endl;
}
for(unsigned int i = 0;i< (Photon_pt).size();i++ ){
cout << "Photon Pt, Eta, Phi: " << (Photon_pt)[i]<<", "<<(Photon_eta)[i]<<", "<<(Photon_phi)[i]<<endl;
}
for(unsigned int i = 0;i< (Jet_pt).size();i++ ){
cout << "jet Pt, Eta, Phi: " << (Jet_pt)[i]<<", "<<(Jet_eta)[i]<<", "<<(Jet_phi)[i]<<endl;
cout << "jet PassID, MUEF, CEEF, CHEF, NHEF: " << (_jetPassID)[i]<<", "<<(Jet_muEF)[i]<<", "<<(Jet_chEmEF)[i]<<", "<<  (Jet_chHEF)[i]<<", "<<  (Jet_neHEF)[i]<<endl;
cout << "jethfsigmaEtaEta jethfsigmaPhiPhi jethfcentralEtaStripSize "<< (Jet_hfsigmaEtaEta)[i]<<", "<<  (Jet_hfsigmaPhiPhi)[i]<<", "<<(Jet_hfcentralEtaStripSize)[i]<<endl;
}


for(unsigned int i = 0;i< (L1Jet_pt).size();i++ ){
cout << "L1 JET Pt, Eta, Phi, Bx: " << (L1Jet_pt)[i]<<", "<<(L1Jet_eta)[i]<<", "<<(L1Jet_phi)[i]<<", " << (L1Jet_bx)[i]<<endl;
}



cout <<endl;

EventsToPrint++;
} 
return true;
'''

highEnergyJet = '''
for( unsigned int i = 0; i < (Jet_pt).size(); i++){
    if(Jet_pt[i] * cosh(Jet_eta[i]) > 6000){
        return false;
    }
}
return true;
'''

def SinglePhotonSelection(df):
    '''
    Select events with exactly one photon with pT>20 GeV.
    The event must pass a photon trigger. 
    '''
#    df = df.Filter('PuppiMET_pt<50')
    df = df.Filter('HLT_Photon110EB_TightID_TightIso')

    df = df.Define('photonsptgt20','Photon_pt>20')
    df = df.Filter('Sum(photonsptgt20)==1','=1 photon with p_{T}>20 GeV')

    df = df.Define('isRefPhoton','Photon_mvaID_WP80&&Photon_pt>115&&abs(Photon_eta)<1.479')
    df = df.Filter('Sum(isRefPhoton)==1','Photon has p_{T}>115 GeV, passes tight ID and is in EB')
    
    df = df.Define('cleanPh_Pt','Photon_pt[isRefPhoton]')
    df = df.Define('cleanPh_Eta','Photon_eta[isRefPhoton]')
    df = df.Define('cleanPh_Phi','Photon_phi[isRefPhoton]')
    
    df = df.Define('ref_Pt','cleanPh_Pt[0]')
    df = df.Define('ref_Phi','cleanPh_Phi[0]')
    
    return df
    
def MuonJet_MuonSelection(df):
    '''
    Select events with >= 1 muon with pT>25 GeV.
    The event must pass a single muon trigger. 
    '''
    df = df.Filter('HLT_IsoMu24')

    df = df.Define('Muon_PassTightId','Muon_pfIsoId>=3&&Muon_mediumPromptId') 
    df = df.Define('goodmuonPt25','Muon_pt>25&&abs(Muon_pdgId)==13&&Muon_PassTightId')
    df = df.Filter('Sum(goodmuonPt25)>=1','>=1 muon with p_{T}>25 GeV')
    df = df.Define('badmuonPt10','Muon_pt>10&&abs(Muon_pdgId)==13&&Muon_PassTightId==0')
    df = df.Filter('Sum(badmuonPt10)==0','No bad quality muon')

    # reject events containing a jet with energy > 6000 GeV
#    df = df.Filter(highEnergyJet, 'No high energy jet')
    return df
    
def ZEE_EleSelection(df):
    '''
    Select Z->ee events passing a single electron trigger. Defines probe pt/eta/phi
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
    df = df.Define('Electron_trig_idx', 'MatchObjToTrig(Electron_eta, Electron_phi, TrigObj_pt, TrigObj_eta, TrigObj_phi, TrigObj_id, 11, TrigObj_filterBits)')
    df = df.Define('Electron_passHLT_Ele32_WPTight_Gsf', 'trig_is_filterbit1_set(Electron_trig_idx, TrigObj_filterBits)')

    df = df.Define('isTag','_lPt>35&&abs(_lpdgId)==11&&Electron_mvaIso_WP90&&Electron_passHLT_Ele32_WPTight_Gsf==true')
    df = df.Filter('Sum(isTag)>0')

    df = df.Define('isProbe','_lPt>5&&abs(_lpdgId)==11&&Electron_mvaIso_WP90&&(Sum(isTag)>=2|| isTag==0)')

    df = df.Define('_mll', 'mll(Electron_pt, Electron_eta, Electron_phi, isTag, isProbe)')
    df = df.Filter('_mll>80&&_mll<100')

    df = df.Define('probe_Pt','_lPt[isProbe]')
    df = df.Define('probe_Eta','_lEta[isProbe]')
    df = df.Define('probe_Phi','_lPhi[isProbe]')

    return df


def ZMuMu_MuSelection(df):
    '''
    Selects Z->mumu events passing a single muon trigger. Defines probe pt/eta/phi
    '''
    df = df.Filter('HLT_IsoMu24')

    # Trigged on a Muon (probably redondant)
    df = df.Filter('''
    bool trigged_on_mu = false;
    for (unsigned int i = 0; i < TrigObj_id.size(); i++){
        if(TrigObj_id[i] == 13) trigged_on_mu = true;
    }
    return trigged_on_mu;
    ''')

    # TrigObj matching
    df = df.Define('Muon_trig_idx', 'MatchObjToTrig(Muon_eta, Muon_phi, TrigObj_pt, TrigObj_eta, TrigObj_phi, TrigObj_id, 13, TrigObj_filterBits)')

    df = df.Define('Muon_passHLT_IsoMu24', 'trig_is_filterbit1_set(Muon_trig_idx, TrigObj_filterBits)')
    df = df.Define('Muon_PassTightId','Muon_pfIsoId>=3&&Muon_mediumPromptId') 

    df = df.Define('isTag','Muon_pt>25&&abs(Muon_pdgId)==13&&Muon_PassTightId&&Muon_passHLT_IsoMu24')

    df = df.Filter('Sum(isTag)>0')

    df = df.Define('isProbe','Muon_pt>3&&abs(Muon_pdgId)==13&&Muon_PassTightId&& (Sum(isTag)>=2||isTag==0)')
    df = df.Define('dr_mll', 'dR_mll(Muon_pt, Muon_eta, Muon_phi, isTag, isProbe)')


    df = df.Define('probe_Pt','Muon_pt[isProbe]')
    df = df.Define('probe_Eta','Muon_eta[isProbe]')
    df = df.Define('probe_Phi','Muon_phi[isProbe]')
    df = df.Define('probe_Charge', 'Muon_charge[isProbe]')

    # Filter on pairs of lepton with DeltaR > 0.4 and 80 < mll < 100
    df = df.Filter('''
    for (unsigned int line = 0; line < dr_mll.size(); line++){
        for (unsigned int col = 0; col < 2; col++){
            float DeltaR = dr_mll[line][col][0];
            float mll = dr_mll[line][col][1];
            if (DeltaR > 0.4 && mll > 80 && mll < 100){
                return true;
            }
        }
    }
    return false;
    ''')

    return df


def DQMOff_EleSelection(df):
    '''
    Select Z->ee events passing a single electron trigger. Defines probe pt/eta/phi
    The selections are modified w.r.t ZEE_EleSelection method.
    This is done so to match the DQM Off selections
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
    df = df.Define('Electron_trig_idx', 'MatchObjToTrig_DQMOff(Electron_eta, Electron_phi, TrigObj_pt, TrigObj_eta, TrigObj_phi, TrigObj_id, 11, TrigObj_filterBits, 1, 0.3)')
    df = df.Define('Electron_passHLT_Ele32_WPTight_Gsf', 'trig_is_filterbit_set_DQMOff(Electron_trig_idx, TrigObj_filterBits, 1)')

    df = df.Define('isTag','Electron_pt>30&&abs(Electron_pdgId)==11&&Electron_mvaNoIso_WP90&&Electron_passHLT_Ele32_WPTight_Gsf==true')
    df = df.Filter('Sum(isTag)>0')

    df = df.Define('isProbe','abs(Electron_pdgId)==11&&Electron_mvaNoIso_WP80&&(Sum(isTag)>=2||isTag==0)')

    df = df.Define('dr_mll', 'dR_mll(Electron_pt, Electron_eta, Electron_phi, isTag, isProbe)')

    # Filter on pairs of lepton with DeltaR > 0.5
    df = df.Filter('''
    for (unsigned int line = 0; line < dr_mll.size(); line++){
        for (unsigned int col = 0; col < 2; col++){
            float DeltaR = dr_mll[line][col][0];
            float mll = dr_mll[line][col][1];
            if (mll > 60 && mll < 120){
                return true;
            }
        }
    }
    return false;
    ''')

    # df = df.Define('_mll', 'mll(Electron_pt, Electron_eta, Electron_phi, isTag, isProbe)')
    # df = df.Filter('_mll>60&&_mll<120')

    df = df.Define('probe_Pt','Electron_pt[isProbe]')
    df = df.Define('probe_Eta','Electron_eta[isProbe]')
    df = df.Define('probe_Phi','Electron_phi[isProbe]')

    return df


def DQMOff_MuSelection(df):
    '''
    Selects Z->mumu events passing a single muon trigger. Defines probe pt/eta/phi
    The selections are modified w.r.t ZMuMu_MuSelection method.
    This is done so to match the DQM Off selections
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
    df = df.Define('Muon_trig_idx', 'MatchObjToTrig_DQMOff(Muon_eta, Muon_phi, TrigObj_pt, TrigObj_eta, TrigObj_phi, TrigObj_id, 13, TrigObj_filterBits, 3, 0.1)')
    df = df.Define('Muon_passHLT_IsoMu27', 'trig_is_filterbit_set_DQMOff(Muon_trig_idx, TrigObj_filterBits, 3)')
    df = df.Define('Muon_PassTightId','Muon_tightId') 

    df = df.Define('isTag','Muon_pt>26&&abs(Muon_pdgId)==13&&Muon_PassTightId&&Muon_passHLT_IsoMu27')
    df = df.Filter('Sum(isTag)>0')

    df = df.Define('isProbe','abs(Muon_pdgId)==13&&Muon_PassTightId&& (Sum(isTag)>=2||isTag==0)')
    df = df.Define('dr_mll', 'dR_mll(Muon_pt, Muon_eta, Muon_phi, isTag, isProbe)')

    # Filter on pairs of lepton with DeltaR > 0.5
    df = df.Filter('''
    for (unsigned int line = 0; line < dr_mll.size(); line++){
        for (unsigned int col = 0; col < 2; col++){
            float DeltaR = dr_mll[line][col][0];
            if (DeltaR > 0.5){
                return true;
            }
        }
    }
    return false;
    ''')

    df = df.Define('probe_Pt','Muon_pt[isProbe]')
    df = df.Define('probe_Eta','Muon_eta[isProbe]')
    df = df.Define('probe_Phi','Muon_phi[isProbe]')
    df = df.Define('probe_Charge', 'Muon_charge[isProbe]')

    return df


def DQMOff_TauSelection(df):
    '''
    Selects Z->tautau events passing a single muon trigger. Defines probe tau pt/eta/phi
    The selections are made to match with DQM Off selections
    '''
    df = df.Filter('HLT_IsoMu20')

    # Trigged on a Muon (probably redundant)
    df = df.Filter('''
    bool trigged_on_mu = false;
    for (unsigned int i = 0; i < TrigObj_id.size(); i++){
        if(TrigObj_id[i] == 13) trigged_on_mu = true;
    }
    return trigged_on_mu;
    ''')

    # Charge 
    # L1Mu_hwCharge = 0 corresponds to Muon_charge = +1
    # L1Mu_hwCharge = 1 corresponds to Muon_charge = -1
    # df = df.Define('L1Mu_charge', 'charge_conversion(L1Mu_hwCharge)')

    # --------------------------------------------------------
    # Match L1Mu to trig obj with id == 13 -> L1Mu_trig_idx
    # with L1Mu_trig_idx -> check filter bits -> L1Mu_passHLT
    # --------------------------------------------------------

    # TrigObj matching
    df = df.Define('Muon_trig_idx', 'MatchObjToTrig_DQMOff(Muon_eta, Muon_phi, TrigObj_pt, TrigObj_eta, TrigObj_phi, TrigObj_id, 13, TrigObj_filterBits, 3, 0.6)')
    df = df.Define('Muon_passHLT_IsoMu24', 'trig_is_filterbit_set_DQMOff(Muon_trig_idx, TrigObj_filterBits, 3)')

    df = df.Define('Muon_PassTightId','Muon_pfIsoId>=3&&Muon_mediumPromptId') 
    df = df.Define('Muon_MassId', 'pass_muon_met_mass_below30(Muon_pt, Muon_phi, MET_pt, MET_phi)')

    df = df.Define('isTag','Muon_pt>24&&abs(Muon_eta)<2.1&&abs(Muon_pdgId)==13&&Muon_PassTightId&&Muon_passHLT_IsoMu24&&Muon_MassId')
    df = df.Filter('Sum(isTag)>0')

    df = df.Define('tagIdx', 'first_tagmuon_idx(isTag)')
    df = df.Filter('tagIdx!=-1')

    df = df.Define('tagPt', 'Muon_pt[tagIdx]')
    df = df.Define('tagEta', 'Muon_eta[tagIdx]')
    df = df.Define('tagPhi', 'Muon_phi[tagIdx]')
    df = df.Define('tagMass', 'Muon_mass[tagIdx]')
    df = df.Define('tagCharge', 'Muon_charge[tagIdx]')

    nEvts = df.Count().GetValue()
    print("There are {} events after finding tag muon".format(nEvts))

    # Decay mode 5 and 6 are unphysical, so removing them
    # Applying Tau_Id_Discrimination against e, mu, jets
    # Applying probe tau selection criterion with the given tag muon
    df = df.Define('Tau_PassDecayMode', 'Tau_decayMode!=5&&Tau_decayMode!=6')
    df = df.Define('Tau_PassTightId', 'Tau_idDeepTau2018v2p5VSe>=1&&Tau_idDeepTau2018v2p5VSjet>=2&&Tau_idDeepTau2018v2p5VSmu>=1')
    df = df.Define('Tau_PassProbe', 'pass_probeTau(Tau_pt, Tau_eta, Tau_phi, Tau_mass, Tau_charge, tagPt, tagEta, tagPhi, tagMass, tagCharge)')

    ## Commenting TauID cuts for testing. 
    ## !! Need to uncomment later
    df = df.Define('isProbeTau', 'Tau_PassDecayMode&&Tau_PassTightId&&Tau_PassProbe')
    # df = df.Define('isProbeTau', 'Tau_PassProbe')
    df = df.Filter('Sum(isProbeTau)>0')

    nEvts = df.Count().GetValue()
    print("There are {} events after finding probe Taus".format(nEvts))

    df = df.Define('probe_Pt','Tau_pt[isProbeTau]')
    df = df.Define('probe_Eta','Tau_eta[isProbeTau]')
    df = df.Define('probe_Phi','Tau_phi[isProbeTau]')

    return df


def DQMOff_JetSelection(df):
    '''
    Selects high jet pT events passing a single muon trigger. Defines probe leadjet pt/eta/phi
    The selections are made to match with DQM Off selections
    '''

    df = df.Filter('HLT_IsoMu20') # Add a condition to include all the HLT filters if they exist otherwise not 
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
    Selects events passing a single muon trigger. Defines Et sums
    The selections are made to match with DQM Off selections
    '''

    df = df.Filter('HLT_IsoMu20') # Add a condition to include all the HLT filters if they exist otherwise not 

    df = df.Define('recoMET', 'CaloMET_pt')
    df = df.Define('recoMETPhi','CaloMET_phi')
    df = df.Define('recoMETSumEt', 'CaloMET_sumEt')

    return df


def makehistosforturnons_inprobeetaranges(df, histos, etavarname, phivarname, ptvarname, responsevarname, l1varname, l1thresholds, prefix, binning, l1thresholdforeffvsrunnb, offlinethresholdforeffvsrunnb, suffix = ''):
    '''Make histos for turnons vs pt (1D histos for numerator and denominator) in ranges of eta
    Also look at response vs run number (2D histo) '''

    for (i, r) in enumerate(config["Regions"]):
        region = config["Regions"][r]

        # check that runnb_bins are set
        if runnb_bins is None:
            set_runnbbins(df)

        str_bineta = "eta{}to{}".format(region[0], region[1]).replace(".","p")
        #Define columns corresponding to pt and response for the selected eta range 
        df_etarange = df.Define('inEtaRange','abs({})>={}'.format(etavarname, region[0])+'&&abs({})<{}'.format(etavarname, region[1]))
        df_etarange = df_etarange.Filter('PuppiMET_pt<100')
        df_etarange = df_etarange.Define('denominator_pt',ptvarname+'[inEtaRange]')
        df_etarange = df_etarange.Define('response',responsevarname+'[inEtaRange]')
        df_etarange = df_etarange.Define('runnb',"return ROOT::VecOps::RVec<int>(response.size(), run);")
        histos[prefix+str_bineta+suffix] = df_etarange.Histo1D(ROOT.RDF.TH1DModel('h_{}_{}'.format(prefix, str_bineta)+suffix, '', len(binning)-1, binning), 'denominator_pt')

        if config["Response"]:
            #Response vs pt and vs runnb (2d)
            histos[prefix+str_bineta+'_ResponseVsPt'+suffix] = df_etarange.Histo2D(ROOT.RDF.TH2DModel('h_ResponseVsPt_{}_{}'.format(prefix, str_bineta)+suffix, '', 200, 0, 200, 100, 0, 2), 'denominator_pt', 'response')
            histos[prefix+str_bineta+'_ResponseVsPt_big_bins'+suffix] = df_etarange.Histo2D(ROOT.RDF.TH2DModel('h_ResponseVsPt_big_bins_{}_{}'.format(prefix, str_bineta)+suffix, '', 20, 0, 200, 100, 0, 2), 'denominator_pt', 'response')
            histos[prefix+str_bineta+'_ResponseVsRunNb'+suffix] = df_etarange.Histo2D(ROOT.RDF.TH2DModel('h_ResponseVsRunNb_{}_{}'.format(prefix, str_bineta)+suffix, '', len(runnb_bins)-1, runnb_bins, len(response_bins)-1, response_bins), 'runnb', 'response')

        #if i ==1 and prefix == 'EGNonIso_plots':
        #    df_etarange = df_etarange.Filter(stringToPrint)

        if config["Efficiency"]:
            #Numerator/denominator for plateau eff vs runnb
            df_etarange = df_etarange.Define('inplateau','{}>={}&&inEtaRange'.format(ptvarname,offlinethresholdforeffvsrunnb))
            df_etarange = df_etarange.Define('N_inplateau','Sum(inplateau)')
            df_etarange = df_etarange.Define('runnb_inplateau',"return ROOT::VecOps::RVec<int>(N_inplateau, run);")
            df_etarange = df_etarange.Define('inplateaupassL1','inplateau && {}>={}'.format(l1varname,l1thresholdforeffvsrunnb))
            df_etarange = df_etarange.Define('N_inplateaupassL1','Sum(inplateaupassL1)')
            df_etarange = df_etarange.Define('runnb_inplateaupassL1',"return ROOT::VecOps::RVec<int>(N_inplateaupassL1, run);")
            histos[prefix+"_plateaueffvsrunnb_numerator_"+str_bineta+suffix] = df_etarange.Histo1D(ROOT.RDF.TH1DModel('h_PlateauEffVsRunNb_Numerator_{}_{}'.format(prefix, str_bineta)+suffix, '', len(runnb_bins)-1, runnb_bins),'runnb_inplateaupassL1')
            histos[prefix+"_plateaueffvsrunnb_denominator_"+str_bineta+suffix] = df_etarange.Histo1D(ROOT.RDF.TH1DModel('h_PlateauEffVsRunNb_Denominator_{}_{}'.format(prefix, str_bineta)+suffix, '', len(runnb_bins)-1, runnb_bins),'runnb_inplateau')

        if config["TurnOns"]:
            for ipt in l1thresholds:
                str_binetapt = "eta{}to{}_l1thrgeq{}".format(region[0], region[1], ipt).replace(".","p")
                df_loc = df_etarange.Define('passL1Cond','{}>={}'.format(l1varname, ipt))
                df_loc = df_loc.Define('numerator_pt',ptvarname+'[inEtaRange&&passL1Cond]')
                histos[prefix+str_binetapt+suffix] = df_loc.Histo1D(ROOT.RDF.TH1DModel('h_{}_{}'.format(prefix, str_binetapt)+suffix, '', len(binning)-1, binning), 'numerator_pt')

    return df


def ZEE_Plots(df, suffix = ''):
    histos = {}
    
    df_eg = [None] * len(config['Isos'])

    for i, iso in enumerate(config['Isos']):
        
        df_eg[i] = df.Define('probe_idxL1EG','FindL1EGIdx(L1EG_eta, L1EG_phi, probe_Eta, probe_Phi, probe_Pt, L1EG_hwIso, {})'.format(config['Isos'][iso]))
        df_eg[i] = df_eg[i].Define('probe_idxL1EG_Bx0','FindL1EGIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, probe_Pt, 0, L1EG_hwIso, {})'.format(config['Isos'][iso]))
        df_eg[i] = df_eg[i].Define('probe_idxL1EG_Bxmin1','FindL1EGIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, probe_Pt, -1, L1EG_hwIso, {})'.format(config['Isos'][iso]))
        df_eg[i] = df_eg[i].Define('probe_idxL1EG_Bxplus1','FindL1EGIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, probe_Pt, 1, L1EG_hwIso, {})'.format(config['Isos'][iso]))

        df_eg[i] = df_eg[i].Define('probe_L1Pt','GetVal(probe_idxL1EG, L1EG_pt)')
        df_eg[i] = df_eg[i].Define('probe_L1Bx','GetVal(probe_idxL1EG, L1EG_bx)')
        df_eg[i] = df_eg[i].Define('probe_L1PtoverRecoPt','probe_L1Pt/probe_Pt')

        df_eg[i] = df_eg[i].Define('probe_L1Pt_Bx0', 'GetVal(probe_idxL1EG_Bx0, L1EG_pt)')
        df_eg[i] = df_eg[i].Define('probe_L1Pt_Bxmin1', 'GetVal(probe_idxL1EG_Bxmin1, L1EG_pt)')
        df_eg[i] = df_eg[i].Define('probe_L1Pt_Bxplus1', 'GetVal(probe_idxL1EG_Bxplus1, L1EG_pt)')

        pt_binning = leptonpt_bins
        if suffix != '':
            pt_binning = coarse_leptonpt_bins
        
        df_eg[i] = makehistosforturnons_inprobeetaranges(df_eg[i], histos, etavarname='probe_Eta', phivarname='probe_Phi', ptvarname='probe_Pt', responsevarname='probe_L1PtoverRecoPt',  l1varname='probe_L1Pt', l1thresholds=config["Thresholds"], prefix=iso+"_plots", binning=pt_binning, l1thresholdforeffvsrunnb = 30, offlinethresholdforeffvsrunnb = 35, suffix = suffix)
        
        if config['Efficiency']: 
            df_eg[i] = df_eg[i].Define('probePt30_Eta','probe_Eta[probe_Pt>30]')
            df_eg[i] = df_eg[i].Define('probePt30_Phi','probe_Phi[probe_Pt>30]')
            df_eg[i] = df_eg[i].Define('probePt30PassL1EG25_Eta','probe_Eta[probe_Pt>30&&probe_L1Pt>25]')
            df_eg[i] = df_eg[i].Define('probePt30PassL1EG25_Phi','probe_Phi[probe_Pt>30&&probe_L1Pt>25]')
            histos['h_EG25_EtaPhi_Numerator'+iso+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('h_EG25_EtaPhi_Numerator'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probePt30PassL1EG25_Eta', 'probePt30PassL1EG25_Phi')
            histos['h_EG25_EtaPhi_Denominator'+iso+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('h_EG25_EtaPhi_Denominator'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probePt30_Eta', 'probePt30_Phi')

        
        #if i ==0:
        if iso == 'EGNonIso' and config['Prefiring']:
            filter_15to26 = 'probe_Pt>12&&probe_Pt<23&&probe_L1Pt>15&&probe_L1Pt<=26'
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bxmin1_Eta', 'probe_Eta[{}&&probe_L1Pt_Bxmin1>15&&probe_L1Pt_Bxmin1<=26]'.format(filter_15to26))
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bxmin1_Phi', 'probe_Phi[{}&&probe_L1Pt_Bxmin1>15&&probe_L1Pt_Bxmin1<=26]'.format(filter_15to26))
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bx0_Eta', 'probe_Eta[{}&&probe_L1Pt_Bx0>15&&probe_L1Pt_Bx0<=26]'.format(filter_15to26))
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bx0_Phi', 'probe_Phi[{}&&probe_L1Pt_Bx0>15&&probe_L1Pt_Bx0<=26]'.format(filter_15to26))
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bxplus1_Eta', 'probe_Eta[{}&&probe_L1Pt_Bxplus1>15&&probe_L1Pt_Bxplus1<=26]'.format(filter_15to26))
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bxplus1_Phi', 'probe_Phi[{}&&probe_L1Pt_Bxplus1>15&&probe_L1Pt_Bxplus1<=26]'.format(filter_15to26))
            
            ###

            filter_30 = 'probe_Pt>25&&probe_L1Pt>30'
            df_eg[i] = df_eg[i].Define('probeL1EG30Bxmin1_Eta', 'probe_Eta[{}&&probe_L1Pt_Bxmin1>30]'.format(filter_30))
            df_eg[i] = df_eg[i].Define('probeL1EG30Bxmin1_Phi', 'probe_Phi[{}&&probe_L1Pt_Bxmin1>30]'.format(filter_30))
            df_eg[i] = df_eg[i].Define('probeL1EG30Bx0_Eta', 'probe_Eta[{}&&probe_L1Pt_Bx0>30]'.format(filter_30))
            df_eg[i] = df_eg[i].Define('probeL1EG30Bx0_Phi', 'probe_Phi[{}&&probe_L1Pt_Bx0>30]'.format(filter_30))
            df_eg[i] = df_eg[i].Define('probeL1EG30Bxplus1_Eta', 'probe_Eta[{}&&probe_L1Pt_Bxplus1>30]'.format(filter_30))
            df_eg[i] = df_eg[i].Define('probeL1EG30Bxplus1_Phi', 'probe_Phi[{}&&probe_L1Pt_Bxplus1>30]'.format(filter_30))
            
            ###
            
            histos['L1EG15to26_bxmin1_etaphi'+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('L1EG15to26_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1EG15to26Bxmin1_Eta', 'probeL1EG15to26Bxmin1_Phi')
            histos['L1EG15to26_bx0_etaphi'+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('L1EG15to26_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1EG15to26Bx0_Eta', 'probeL1EG15to26Bx0_Phi')
            histos['L1EG15to26_bxplus1_etaphi'+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('L1EG15to26_bxplus1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1EG15to26Bxplus1_Eta', 'probeL1EG15to26Bxplus1_Phi')

            histos['L1EG15to26_bxmin1_eta'+suffix] = df_eg[i].Histo1D(ROOT.RDF.TH1DModel('L1EG15to26_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1EG15to26Bxmin1_Eta')
            histos['L1EG15to26_bx0_eta'+suffix] = df_eg[i].Histo1D(ROOT.RDF.TH1DModel('L1EG15to26_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1EG15to26Bx0_Eta')
            histos['L1EG15to26_bxplus1_eta'+suffix] = df_eg[i].Histo1D(ROOT.RDF.TH1DModel('L1EG15to26_bxplus1_eta'+suffix, '', 100, -5, 5), 'probeL1EG15to26Bxplus1_Eta')

            ###

            histos['L1EG30_bxmin1_etaphi'+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('L1EG30_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1EG30Bxmin1_Eta', 'probeL1EG30Bxmin1_Phi')
            histos['L1EG30_bx0_etaphi'+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('L1EG30_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1EG30Bx0_Eta', 'probeL1EG30Bx0_Phi')
            histos['L1EG30_bxplus1_etaphi'+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('L1EG30_bxplus1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1EG30Bxplus1_Eta', 'probeL1EG30Bxplus1_Phi')

            histos['L1EG30_bxmin1_eta'+suffix] = df_eg[i].Histo1D(ROOT.RDF.TH1DModel('L1EG30_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1EG30Bxmin1_Eta')
            histos['L1EG30_bx0_eta'+suffix] = df_eg[i].Histo1D(ROOT.RDF.TH1DModel('L1EG30_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1EG30Bx0_Eta')
            histos['L1EG30_bxplus1_eta'+suffix] = df_eg[i].Histo1D(ROOT.RDF.TH1DModel('L1EG30_bxplus1_eta'+suffix, '', 100, -5, 5), 'probeL1EG30Bxplus1_Eta')

            #

            histos['L1EG30_OR_bxmin1_etaphi'+suffix] = df_eg[i].Filter("L1_UnprefireableEvent||((run>=361468)&L1_FirstBunchInTrain)").Histo2D(ROOT.RDF.TH2DModel('L1EG30_OR_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1EG30Bxmin1_Eta', 'probeL1EG30Bxmin1_Phi')
            histos['L1EG30_OR_bx0_etaphi'+suffix] = df_eg[i].Filter("L1_UnprefireableEvent||((run>=361468)&L1_FirstBunchInTrain)").Histo2D(ROOT.RDF.TH2DModel('L1EG30_OR_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1EG30Bx0_Eta', 'probeL1EG30Bx0_Phi')

            histos['L1EG30_OR_bxmin1_eta'+suffix] = df_eg[i].Filter("L1_UnprefireableEvent||((run>=361468)&L1_FirstBunchInTrain)").Histo1D(ROOT.RDF.TH1DModel('L1EG30_OR_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1EG30Bxmin1_Eta')
            histos['L1EG30_OR_bx0_eta'+suffix] = df_eg[i].Filter("L1_UnprefireableEvent||((run>=361468)&L1_FirstBunchInTrain)").Histo1D(ROOT.RDF.TH1DModel('L1EG30_OR_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1EG30Bx0_Eta')

    return df, histos
    
    
def ZMuMu_Plots(df, suffix = ''):

    histos = {}
    df_mu = [None] * len(config["Qualities"])

    for i, qual in enumerate(config["Qualities"]):

        df_mu[i] = df.Define('probe_idxL1Mu','FindL1MuIdx(L1Mu_eta, L1Mu_phi, probe_Eta, probe_Phi, probe_Pt, probe_Charge, L1Mu_hwQual, {})'.format(config["Qualities"][qual]))
        df_mu[i] = df_mu[i].Define('probe_idxL1Mu_Bx0','FindL1MuIdx_setBx(L1Mu_eta, L1Mu_phi, L1Mu_bx, probe_Eta, probe_Phi, probe_Pt, probe_Charge, 0, L1Mu_hwQual, {})'.format(config["Qualities"][qual]))
        df_mu[i] = df_mu[i].Define('probe_idxL1Mu_Bxmin1','FindL1MuIdx_setBx(L1Mu_eta, L1Mu_phi, L1Mu_bx, probe_Eta, probe_Phi, probe_Pt, probe_Charge, -1, L1Mu_hwQual, {})'.format(config["Qualities"][qual]))
        df_mu[i] = df_mu[i].Define('probe_idxL1Mu_Bxplus1','FindL1MuIdx_setBx(L1Mu_eta, L1Mu_phi, L1Mu_bx, probe_Eta, probe_Phi, probe_Pt, probe_Charge, 1, L1Mu_hwQual, {})'.format(config["Qualities"][qual]))
            
        df_mu[i] = df_mu[i].Define('probe_L1Pt','GetVal(probe_idxL1Mu, L1Mu_pt)')
        df_mu[i] = df_mu[i].Define('probe_L1Bx','GetVal(probe_idxL1Mu, L1Mu_bx)')
        df_mu[i] = df_mu[i].Define('probe_L1Qual','GetVal(probe_idxL1Mu, L1Mu_hwQual)')

        df_mu[i] = df_mu[i].Define('probe_L1Pt_Bx0', 'GetVal(probe_idxL1Mu_Bx0, L1Mu_pt)')
        df_mu[i] = df_mu[i].Define('probe_L1Qual_Bx0', 'GetVal(probe_idxL1Mu_Bx0, L1Mu_hwQual)')

        df_mu[i] = df_mu[i].Define('probe_L1Pt_Bxmin1', 'GetVal(probe_idxL1Mu_Bxmin1, L1Mu_pt)')
        df_mu[i] = df_mu[i].Define('probe_L1Qual_Bxmin1', 'GetVal(probe_idxL1Mu_Bxmin1, L1Mu_hwQual)')

        df_mu[i] = df_mu[i].Define('probe_L1Pt_Bxplus1', 'GetVal(probe_idxL1Mu_Bxplus1, L1Mu_pt)')
        df_mu[i] = df_mu[i].Define('probe_L1Qual_Bxplus1', 'GetVal(probe_idxL1Mu_Bxplus1, L1Mu_hwQual)')

        df_mu[i] = df_mu[i].Define('probe_L1PtoverRecoPt','probe_L1Pt/probe_Pt')

        pt_binning = leptonpt_bins
        if suffix != '':
            pt_binning = coarse_leptonpt_bins

        df_mu[i] = makehistosforturnons_inprobeetaranges(df_mu[i], histos, etavarname='probe_Eta', phivarname='probe_Phi', ptvarname='probe_Pt', responsevarname='probe_L1PtoverRecoPt', l1varname='probe_L1Pt', l1thresholds=config["Thresholds"],  prefix=qual+"_plots" , binning = pt_binning, l1thresholdforeffvsrunnb = 22, offlinethresholdforeffvsrunnb = 27, suffix = suffix)
        #df_mu[i] = makehistosforturnons_inprobeetaranges(df_mu[i], histos, etavarname='probe_Eta', phivarname='probe_Phi', ptvarname='probe_Pt', responsevarname='probe_L1PtoverRecoPt', etabins=[0., 2.4], l1varname='probe_L1Pt', l1thresholds=config["Thresholds"],  prefix=qual+"_plots_eta_inclusive" , binning = coarse_leptonpt_bins, l1thresholdforeffvsrunnb = 22, offlinethresholdforeffvsrunnb = 27, suffix = suffix)
        #df_mu[i] = makehistosforturnons_inprobeetaranges(df_mu[i], histos, etavarname='probe_Eta', phivarname='probe_Phi', ptvarname='probe_Pt', responsevarname='probe_L1PtoverRecoPt', etabins=[0., 2.4], l1varname='probe_L1Pt', l1thresholds=config["Thresholds"],  prefix=qual+"_plots_eta_inclusive2" , binning = coarse2_leptonpt_bins, l1thresholdforeffvsrunnb = 22, offlinethresholdforeffvsrunnb = 27, suffix = suffix)
        
        if config["Efficiency"]:
            df_mu[i] = df_mu[i].Define('probePt30_Eta','probe_Eta[probe_Pt>30]')
            df_mu[i] = df_mu[i].Define('probePt30_Phi','probe_Phi[probe_Pt>30]')
            df_mu[i] = df_mu[i].Define('probePt30PassL1Mu22_Eta','probe_Eta[probe_Pt>30&&probe_L1Pt>22]')
            df_mu[i] = df_mu[i].Define('probePt30PassL1Mu22_Phi','probe_Phi[probe_Pt>30&&probe_L1Pt>22]')
            #df_mu[i] = df_mu[i].Define('probePt30PassL1Mu22_L1Bx','probe_L1Bx[probe_Pt>30&&probe_L1Pt>22]')

            histos['h_Mu22_EtaPhi_Denominator'+qual+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('h_Mu22_EtaPhi_Denominator'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probePt30_Eta', 'probePt30_Phi')
            histos['h_Mu22_EtaPhi_Numerator'+qual+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('h_Mu22_EtaPhi_Numerator'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probePt30PassL1Mu22_Eta', 'probePt30PassL1Mu22_Phi')
        
        
        if qual == "Qual12" and config["Prefiring"]:

            filter_10to21 = 'probe_Pt>8&&probe_Pt<25&&probe_L1Pt>10&&probe_L1Pt<=21&&probe_L1Qual>=12'
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bxmin1_Eta','probe_Eta[{}&&probe_L1Pt_Bxmin1>10&&probe_L1Pt_Bxmin1<=21]'.format(filter_10to21))
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bxmin1_Phi','probe_Phi[{}&&probe_L1Pt_Bxmin1>10&&probe_L1Pt_Bxmin1<=21]'.format(filter_10to21))
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bx0_Eta','probe_Eta[{}&&probe_L1Pt_Bx0>10&&probe_L1Pt_Bx0<=21]'.format(filter_10to21))
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bx0_Phi','probe_Phi[{}&&probe_L1Pt_Bx0>10&&probe_L1Pt_Bx0<=21]'.format(filter_10to21))
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bxplus1_Eta','probe_Eta[{}&&probe_L1Pt_Bxplus1>10&&probe_L1Pt_Bxplus1<=21]'.format(filter_10to21))
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bxplus1_Phi','probe_Phi[{}&&probe_L1Pt_Bxplus1>10&&probe_L1Pt_Bxplus1<=21]'.format(filter_10to21))
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21All_Eta','probe_Eta[{}]'.format(filter_10to21))
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21All_Phi','probe_Phi[{}]'.format(filter_10to21))
            
            filter_22 = 'probe_Pt>20&&probe_L1Pt>22&&probe_L1Qual>=12'
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bxmin1_Eta', 'probe_Eta[{}&&probe_L1Pt_Bxmin1>22]'.format(filter_22))
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bxmin1_Phi', 'probe_Phi[{}&&probe_L1Pt_Bxmin1>22]'.format(filter_22))
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bx0_Eta', 'probe_Eta[{}&&probe_L1Pt_Bx0>22]'.format(filter_22))
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bx0_Phi', 'probe_Phi[{}&&probe_L1Pt_Bx0>22]'.format(filter_22))
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bxplus1_Eta', 'probe_Eta[{}&&probe_L1Pt_Bxplus1>22]'.format(filter_22))
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bxplus1_Phi', 'probe_Phi[{}&&probe_L1Pt_Bxplus1>22]'.format(filter_22))
            df_mu[i] = df_mu[i].Define('probeL1Mu22All_Eta', 'probe_Eta[{}]'.format(filter_22))
            df_mu[i] = df_mu[i].Define('probeL1Mu22All_Phi', 'probe_Phi[{}]'.format(filter_22))
                        
            # Muon with L1 pt >= 10 GeV, reco pT >= 10 GeV
            filter_10 = 'probe_Pt>=10&&probe_L1Pt>=10&&probe_L1Qual>=12'
            df_mu[i] = df_mu[i].Define('probeL1Mu10Bxmin1_Eta', 'probe_Eta[{}&&probe_L1Pt_Bxmin1>=10]'.format(filter_10))
            df_mu[i] = df_mu[i].Define('probeL1Mu10Bxmin1_Phi', 'probe_Phi[{}&&probe_L1Pt_Bxmin1>=10]'.format(filter_10))
            df_mu[i] = df_mu[i].Define('probeL1Mu10Bx0_Eta', 'probe_Eta[{}&&probe_L1Pt_Bx0>=10]'.format(filter_10))
            df_mu[i] = df_mu[i].Define('probeL1Mu10Bx0_Phi', 'probe_Phi[{}&&probe_L1Pt_Bx0>=10]'.format(filter_10))
            df_mu[i] = df_mu[i].Define('probeL1Mu10Bxplus1_Eta', 'probe_Eta[{}&&probe_L1Pt_Bxplus1>=10]'.format(filter_10))
            df_mu[i] = df_mu[i].Define('probeL1Mu10Bxplus1_Phi', 'probe_Phi[{}&&probe_L1Pt_Bxplus1>=10]'.format(filter_10))
            df_mu[i] = df_mu[i].Define('probeL1Mu10All_Eta', 'probe_Eta[{}]'.format(filter_10))
            df_mu[i] = df_mu[i].Define('probeL1Mu10All_Phi', 'probe_Phi[{}]'.format(filter_10))
                        
            histos['L1Mu10to21_bxmin1_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu10to21_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu10to21Bxmin1_Eta', 'probeL1Mu10to21Bxmin1_Phi')
            histos['L1Mu10to21_bx0_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu10to21_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu10to21Bx0_Eta', 'probeL1Mu10to21Bx0_Phi')
            histos['L1Mu10to21_bxplus1_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu10to21_bxplus1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu10to21Bxplus1_Eta', 'probeL1Mu10to21Bxplus1_Phi')
            histos['L1Mu10to21_all_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu10to21_all_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu10to21All_Eta', 'probeL1Mu10to21All_Phi')

            histos['L1Mu10to21_bxmin1_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu10to21_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu10to21Bxmin1_Eta')
            histos['L1Mu10to21_bx0_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu10to21_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Mu10to21Bx0_Eta')
            histos['L1Mu10to21_bxplus1_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu10to21_bxplus1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu10to21Bxplus1_Eta')

            ###

            histos['L1Mu22_bxplus1_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu22_bxplus1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bxplus1_Eta', 'probeL1Mu22Bxplus1_Phi')
            histos['L1Mu22_bx0_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu22_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bx0_Eta', 'probeL1Mu22Bx0_Phi')
            histos['L1Mu22_all_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu22_all_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22All_Eta', 'probeL1Mu22All_Phi')

            histos['L1Mu22_bxplus1_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu22_bxplus1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bxplus1_Eta')
            histos['L1Mu22_bx0_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu22_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bx0_Eta') 

            #

            histos['L1Mu22_IsUnprefireable_bx0_etaphi'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent").Histo2D(ROOT.RDF.TH2DModel('L1Mu22_IsUnprefireable_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bx0_Eta', 'probeL1Mu22Bx0_Phi')
            histos['L1Mu22_IsUnprefireable_bx0_eta'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent").Histo1D(ROOT.RDF.TH1DModel('L1Mu22_IsUnprefireable_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bx0_Eta') 

            histos['L1Mu22_IsUnprefireable_bxmin1_etaphi'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent").Histo2D(ROOT.RDF.TH2DModel('L1Mu22_IsUnprefireable_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bxmin1_Eta', 'probeL1Mu22Bxmin1_Phi')
            histos['L1Mu22_IsUnprefireable_bxmin1_eta'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent").Histo1D(ROOT.RDF.TH1DModel('L1Mu22_IsUnprefireable_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bxmin1_Eta') 

            #

            histos['L1Mu22_FirstBunchInTrain_bx0_etaphi'+suffix] = df_mu[i].Filter("run>=361468").Filter("L1_FirstBunchInTrain").Histo2D(ROOT.RDF.TH2DModel('L1Mu22_FirstBunchInTrain_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bx0_Eta', 'probeL1Mu22Bx0_Phi')
            histos['L1Mu22_FirstBunchInTrain_bx0_eta'+suffix] = df_mu[i].Filter("run>=361468").Filter("L1_FirstBunchInTrain").Histo1D(ROOT.RDF.TH1DModel('L1Mu22_FirstBunchInTrain_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bx0_Eta') 

            histos['L1Mu22_FirstBunchInTrain_bxmin1_etaphi'+suffix] = df_mu[i].Filter("run>=361468").Filter("L1_FirstBunchInTrain").Histo2D(ROOT.RDF.TH2DModel('L1Mu22_FirstBunchInTrain_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bxmin1_Eta', 'probeL1Mu22Bxmin1_Phi')

            histos['L1Mu22_FirstBunchInTrain_bxmin1_eta'+suffix] = df_mu[i].Filter("run>=361468").Filter("L1_FirstBunchInTrain").Histo1D(ROOT.RDF.TH1DModel('L1Mu22_FirstBunchInTrain_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bxmin1_Eta') 

            #

            histos['L1Mu22_OR_bx0_etaphi'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent||((run>=361468)&L1_FirstBunchInTrain)").Histo2D(ROOT.RDF.TH2DModel('L1Mu22_OR_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bx0_Eta', 'probeL1Mu22Bx0_Phi')
            histos['L1Mu22_OR_bx0_eta'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent||((run>=361468)&L1_FirstBunchInTrain)").Histo1D(ROOT.RDF.TH1DModel('L1Mu22_OR_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bx0_Eta') 

            histos['L1Mu22_OR_bxmin1_etaphi'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent||((run>=361468)&L1_FirstBunchInTrain)").Histo2D(ROOT.RDF.TH2DModel('L1Mu22_OR_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bxmin1_Eta', 'probeL1Mu22Bxmin1_Phi')
            histos['L1Mu22_OR_bxmin1_eta'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent||((run>=361468)&L1_FirstBunchInTrain)").Histo1D(ROOT.RDF.TH1DModel('L1Mu22_OR_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bxmin1_Eta') 

            ###

            histos['L1Mu10_bxplus1_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu10_bxplus1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu10Bxplus1_Eta', 'probeL1Mu10Bxplus1_Phi')
            histos['L1Mu10_bx0_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu10_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu10Bx0_Eta', 'probeL1Mu10Bx0_Phi')
            histos['L1Mu10_all_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu10_all_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu10All_Eta', 'probeL1Mu10All_Phi')

            histos['L1Mu10_bxplus1_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu10_bxplus1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu10Bxplus1_Eta')
            histos['L1Mu10_bx0_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu10_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Mu10Bx0_Eta') 

            #

            histos['L1Mu10_OR_bx0_etaphi'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent||((run>=361468)&L1_FirstBunchInTrain)").Histo2D(ROOT.RDF.TH2DModel('L1Mu10_OR_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu10Bx0_Eta', 'probeL1Mu10Bx0_Phi')
            histos['L1Mu10_OR_bx0_eta'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent||((run>=361468)&L1_FirstBunchInTrain)").Histo1D(ROOT.RDF.TH1DModel('L1Mu10_OR_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Mu10Bx0_Eta') 

            histos['L1Mu10_OR_bxmin1_etaphi'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent||((run>=361468)&L1_FirstBunchInTrain)").Histo2D(ROOT.RDF.TH2DModel('L1Mu10_OR_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu10Bxmin1_Eta', 'probeL1Mu10Bxmin1_Phi')
            histos['L1Mu10_OR_bxmin1_eta'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent||((run>=361468)&L1_FirstBunchInTrain)").Histo1D(ROOT.RDF.TH1DModel('L1Mu10_OR_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu10Bxmin1_Eta') 


            '''
            #L1 prefiring measurement with unprefirable events
            
            #First find if there's a L1 mu in bx -1 and store its index
            df_mu[i] = df_mu[i].Define('probe_idxL1Mu_inbxmin1','FindL1MuBxMin1Idx(L1Mu_eta, L1Mu_phi, probe_Eta, probe_Phi, L1Mu_hwQual, 12)')
            df_mu[i] = df_mu[i].Define('probe_L1Pt_inbxmin1','GetVal(probe_idxL1Mu, L1Mu_pt)')
            df_mu[i] = df_mu[i].Define('probeEta_L1Mu22_inbxmin1','probe_Eta[probe_Pt>30&&probe_L1Pt_inbxmin1>22]')
            df_mu[i] = df_mu[i].Define('probePhi_L1Mu22_inbxmin1','probe_Phi[probe_Pt>30&&probe_L1Pt_inbxmin1>22]')

            #Next lines are still WIP
            histos['L1Mu22_denforPrefiring_etaphi'] = df_mu[i].Filter('Flag_IsUnprefirable').Histo2D(ROOT.RDF.TH2DModel('', '', 100, -5,5, 100, -3.1416, 3.1416), 'probePt30PassL1Mu22_Eta', 'probePt30PassL1Mu22_Phi')
            histos['L1Mu22_numforPrefiring_etaphi'] = df_mu[i].Filter('Flag_IsUnprefirable').Histo2D(ROOT.RDF.TH2DModel('', '', 100, -5,5, 100, -3.1416, 3.1416), 'probeEta_L1Mu22_inbxmin1', 'probePhi_L1Mu22_inbxmin1')
            '''

    return df, histos


def ZEE_DQMOff_Plots(df, suffix = ''):

    recoToL1PtCutFactor = config['RecoToL1PtCutFactor']
    probeToL1Offset = config['probeToL1Offset']

    df = df.Define('probe_Nvtx', 'GetProbeNvtxArray(probe_Pt, PV_npvs)')

    histos = {}

    df_eg = [None] * len(config['Isos'])
    for i, iso in enumerate(config['Isos']):

        prefix = iso

        # Get Ids for L1 Muons which match with probe
        df_eg[i] = df.Define('probe_idxL1EG','FindL1EGIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, probe_Pt, 0, L1EG_hwIso, {})'.format(config['Isos'][iso]))

        df_eg[i] = df_eg[i].Define('probe_L1Pt','GetVal(probe_idxL1EG, L1EG_pt)')
        df_eg[i] = df_eg[i].Define('probe_L1Eta','GetVal(probe_idxL1EG, L1EG_eta)')
        df_eg[i] = df_eg[i].Define('probe_L1Phi','GetVal(probe_idxL1EG, L1EG_phi)')
        df_eg[i] = df_eg[i].Define('probe_L1Bx','GetVal(probe_idxL1EG, L1EG_bx)')
        df_eg[i] = df_eg[i].Define('probe_L1Iso','GetVal(probe_idxL1EG, L1EG_hwIso)')

        df_eg[i] = df_eg[i].Define('probe_L1PtReso','(probe_L1Pt - probe_Pt)/probe_Pt')
        df_eg[i] = df_eg[i].Define('probe_L1EtaReso','(probe_L1Eta-probe_Eta)')
        df_eg[i] = df_eg[i].Define('probe_L1PhiReso','GetReducedDeltaphi(probe_L1Phi, probe_Phi)')

        pt_binning = dqmoff_egpt_bins #leptonpt_bins
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

        if config['L1TResolution']:

            df_etarange = [None] * len(config['Regions'])
            for ireg, reg in enumerate(config['Regions']):

                region = config["Regions"][reg]
                str_binEta = "eta{}to{}".format(region[0], region[1]).replace(".","p")

                df_etarange[ireg] = df_eg[i].Define('inEtaRange','abs(probe_Eta)>={}'.format(region[0])+'&&abs(probe_Eta)<{}'.format(region[1]))
                df_etarange[ireg] = df_etarange[ireg].Define('reso_pt', 'probe_L1PtReso[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('reso_eta', 'probe_L1EtaReso[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('reso_phi', 'probe_L1PhiReso[inEtaRange]')

                # Create resolution histograms
                histos['reso_pt_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('h_EG_reso_pt_{}_{}'.format(str_binEta, prefix)+suffix, '', n_resoptbins, reso_pt_binning), 
                    'reso_pt'
                )
                histos['reso_eta_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('h_EG_reso_eta_{}_{}'.format(str_binEta, prefix)+suffix, '', n_resoetabins, reso_eta_binning), 
                    'reso_eta'
                )
                histos['reso_phi_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('h_EG_reso_phi_{}_{}'.format(str_binEta, prefix)+suffix, '', n_resophibins, reso_phi_binning), 
                    'reso_phi'
                )

        if config['L1TEfficiency']:

            df_etarange = [None] * len(config['Regions'])
            for ireg, reg in enumerate(config['Regions']):
                region = config["Regions"][reg]

                df_etarange[ireg] = df_eg[i].Define('inEtaRange', 'abs(probe_Eta)>={}'.format(region[0])+'&&abs(probe_Eta)<{}'.format(region[1]))
                df_etarange[ireg] = df_etarange[ireg].Define('denominator_pt', 'probe_Pt[inEtaRange]')

                str_binEta = "eta{}to{}".format(region[0], region[1]).replace(".","p")
                histos['eff_pt_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('h_EG_eff_pt_{}_{}'.format(str_binEta, prefix)+suffix, '', n_ptbins, pt_binning), 
                    'denominator_pt'
                )

                # Numerator Histograms for all Et thresholds
                l1thresholds = config["Thresholds"]
                for ipt in l1thresholds:

                    df_loc = df_etarange[ireg].Define('passL1Cond', 'probe_L1Pt>={}'.format(ipt))
                    df_loc = df_loc.Define('numerator_pt', 'probe_Pt[inEtaRange&&passL1Cond]')
                    
                    # Create numerator histograms
                    str_binEtaPt = "eta{}to{}_l1thrgeq{}".format(region[0], region[1], ipt).replace(".","p") 
                    histos['eff_pt_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                        ROOT.RDF.TH1DModel('h_EG_eff_pt_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_ptbins, pt_binning), 
                        'numerator_pt'
                    )

                    if (reg == 'EB_EE'): 

                        cutfactor = ipt * recoToL1PtCutFactor
                        offsetfactor = ipt + probeToL1Offset

                        df_loc = df_loc.Define('passRecoToL1PtCutFactor', 'probe_Pt>={}'.format(cutfactor))
                        df_loc = df_loc.Define('passL1OffsetCond', 'probe_L1Pt>={}'.format(offsetfactor))

                        df_loc = df_loc.Define('denominator_eta', 'probe_Eta[inEtaRange&&passRecoToL1PtCutFactor]')
                        df_loc = df_loc.Define('denominator_phi', 'probe_Phi[inEtaRange&&passRecoToL1PtCutFactor]')
                        df_loc = df_loc.Define('denominator_nvtx', 'probe_Nvtx[inEtaRange&&passRecoToL1PtCutFactor]')

                        # Filling denominator histos for Eff vs Phi (or Eta or Nvtx)
                        str_binEtaPt = "eta{}to{}_probeptgeq{}".format(region[0], region[1], cutfactor).replace(".","p")
                        histos['eff_eta_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('h_EG_eff_eta_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_etabins, eta_binning), 
                            'denominator_eta'
                        )
                        histos['eff_phi_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('h_EG_eff_phi_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_phibins, phi_binning), 
                            'denominator_phi'
                        )
                        histos['eff_nvtx_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('h_EG_eff_nvtx_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_nvtxbins, nvtx_binning), 
                            'denominator_nvtx'
                        )

                        df_loc = df_loc.Define('numerator_eta', 'probe_Eta[inEtaRange&&passL1OffsetCond&&passRecoToL1PtCutFactor]')
                        df_loc = df_loc.Define('numerator_phi', 'probe_Phi[inEtaRange&&passL1OffsetCond&&passRecoToL1PtCutFactor]')
                        df_loc = df_loc.Define('numerator_nvtx', 'probe_Nvtx[inEtaRange&&passL1OffsetCond&&passRecoToL1PtCutFactor]')

                        str_binEtaPt = "eta{}to{}_probeptgeq{}_l1thrgeq{}".format(region[0], region[1], cutfactor, offsetfactor).replace(".","p")
                        histos['eff_eta_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('h_EG_eff_eta_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_etabins, eta_binning), 
                            'numerator_eta'
                        )
                        histos['eff_phi_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('h_EG_eff_phi_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_phibins, phi_binning), 
                            'numerator_phi'
                        )
                        histos['eff_nvtx_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('h_EG_eff_nvtx_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_nvtxbins, nvtx_binning), 
                            'numerator_nvtx'
                        )

    return df, histos


def ZMuMu_DQMOff_Plots(df, suffix = ''):

    recoToL1PtCutFactor = config['RecoToL1PtCutFactor']

    df = df.Define('probe_Nvtx', 'GetProbeNvtxArray(probe_Pt, PV_npvs)')
    df = df.Define('L1Mu_charge', 'charge_conversion(L1Mu_hwCharge)')

    histos = {}
    df_mu = [None] * len(config['Qualities'])

    for i, qual in enumerate(config['Qualities']):

        prefix = qual

        # Get Ids for L1 Muons which match with probe
        df_mu[i] = df.Define('probe_idxL1Mu','FindL1MuIdx_DQMOff(L1Mu_eta, L1Mu_phi, probe_Eta, probe_Phi, probe_Pt, probe_Charge, L1Mu_hwQual, {})'.format(config["Qualities"][qual]))

        df_mu[i] = df_mu[i].Define('probe_L1Pt','GetVal(probe_idxL1Mu, L1Mu_pt)')
        df_mu[i] = df_mu[i].Define('probe_L1Eta','GetVal(probe_idxL1Mu, L1Mu_eta)')
        df_mu[i] = df_mu[i].Define('probe_L1Phi','GetVal(probe_idxL1Mu, L1Mu_phi)')
        df_mu[i] = df_mu[i].Define('probe_L1Bx','GetVal(probe_idxL1Mu, L1Mu_bx)')
        df_mu[i] = df_mu[i].Define('probe_L1Qual','GetVal(probe_idxL1Mu, L1Mu_hwQual)')
        df_mu[i] = df_mu[i].Define('probe_L1Charge','GetVal(probe_idxL1Mu, L1Mu_charge)')

        df_mu[i] = df_mu[i].Define('probe_L1PtReso','((probe_L1Charge*probe_Charge*probe_Pt)-probe_L1Pt)/probe_L1Pt')
        df_mu[i] = df_mu[i].Define('probe_L1EtaReso','(probe_L1Eta-probe_Eta)')
        # df_mu[i] = df_mu[i].Define('probe_L1PhiReso','(probe_L1Phi-probe_Phi)')
        df_mu[i] = df_mu[i].Define('probe_L1PhiReso','GetReducedDeltaphi(probe_L1Phi, probe_Phi)')

        pt_binning = dqmoff_muonpt_bins #leptonpt_bins
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

        if config['L1TResolution']:

            df_etarange = [None] * len(config['Regions'])
            for ireg, reg in enumerate(config['Regions']):

                region = config["Regions"][reg]
                str_binEta = "eta{}to{}".format(region[0], region[1]).replace(".","p")

                df_etarange[ireg] = df_mu[i].Define('inEtaRange','abs(probe_Eta)>={}'.format(region[0])+'&&abs(probe_Eta)<{}'.format(region[1]))
                df_etarange[ireg] = df_etarange[ireg].Define('reso_pt', 'probe_L1PtReso[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('reso_eta', 'probe_L1EtaReso[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('reso_phi', 'probe_L1PhiReso[inEtaRange]')

                # Create resolution histograms
                histos['reso_pt_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('h_Mu_reso_pt_{}_{}'.format(str_binEta, prefix)+suffix, '', n_resoptbins, reso_pt_binning), 
                    'reso_pt'
                )
                histos['reso_eta_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('h_Mu_reso_eta_{}_{}'.format(str_binEta, prefix)+suffix, '', n_resoetabins, reso_eta_binning), 
                    'reso_eta'
                )
                histos['reso_phi_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('h_Mu_reso_phi_{}_{}'.format(str_binEta, prefix)+suffix, '', n_resophibins, reso_phi_binning), 
                    'reso_phi'
                )

        if config['L1TEfficiency']:

            df_etarange = [None] * len(config['Regions'])
            for ireg, reg in enumerate(config['Regions']):
                region = config["Regions"][reg]
                
                df_etarange[ireg] = df_mu[i].Define('inEtaRange', 'abs(probe_Eta)>={}'.format(region[0])+'&&abs(probe_Eta)<{}'.format(region[1]))
                df_etarange[ireg] = df_etarange[ireg].Define('denominator_pt', 'probe_Pt[inEtaRange]')
                
                # Create denominator histograms for pt
                str_binEta = "eta{}to{}".format(region[0], region[1]).replace(".","p")
                histos['eff_pt_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('h_Mu_eff_pt_{}_{}'.format(str_binEta, prefix)+suffix, '', n_ptbins, pt_binning), 
                    'denominator_pt'
                )

                # Numerator Histograms for all Et thresholds
                l1thresholds = config["Thresholds"]
                for ipt in l1thresholds:

                    cutfactor = ipt * recoToL1PtCutFactor
                    df_loc = df_etarange[ireg].Define('passRecoToL1PtCutFactor', 'probe_Pt>={}'.format(cutfactor))
                    
                    df_loc = df_loc.Define('denominator_phi', 'probe_Phi[inEtaRange&&passRecoToL1PtCutFactor]')
                    df_loc = df_loc.Define('denominator_nvtx', 'probe_Nvtx[inEtaRange&&passRecoToL1PtCutFactor]')

                    # Filling denominator histos for Eff vs Phi (or Eta or Nvtx)
                    str_binEtaPt = "eta{}to{}_probeptgeq{}".format(region[0], region[1], cutfactor).replace(".","p")
                    histos['eff_phi_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                        ROOT.RDF.TH1DModel('h_Mu_eff_phi_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_phibins, phi_binning), 
                        'denominator_phi'
                    )
                    histos['eff_nvtx_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                        ROOT.RDF.TH1DModel('h_Mu_eff_nvtx_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_nvtxbins, nvtx_binning), 
                        'denominator_nvtx'
                    )
                    if (reg == 'AllEta'): 
                        df_loc = df_loc.Define('denominator_eta', 'probe_Eta[inEtaRange&&passRecoToL1PtCutFactor]')
                        histos['eff_eta_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('h_Mu_eff_eta_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_etabins, eta_binning), 
                            'denominator_eta'
                        )

                    df_loc = df_loc.Define('passL1Cond', 'probe_L1Pt>={}'.format(ipt))
                    df_loc = df_loc.Define('numerator_pt', 'probe_Pt[inEtaRange&&passL1Cond]')
                    df_loc = df_loc.Define('numerator_phi', 'probe_Phi[inEtaRange&&passL1Cond&&passRecoToL1PtCutFactor]')
                    df_loc = df_loc.Define('numerator_nvtx', 'probe_Nvtx[inEtaRange&&passL1Cond&&passRecoToL1PtCutFactor]')

                    # Create numerator histograms
                    str_binEtaPt = "eta{}to{}_l1thrgeq{}".format(region[0], region[1], ipt).replace(".","p") 
                    histos['eff_pt_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                        ROOT.RDF.TH1DModel('h_Mu_eff_pt_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_ptbins, pt_binning), 
                        'numerator_pt'
                    )

                    str_binEtaPt = "eta{}to{}_probeptgeq{}_l1thrgeq{}".format(region[0], region[1], cutfactor, ipt).replace(".","p") 
                    histos['eff_phi_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                        ROOT.RDF.TH1DModel('h_Mu_eff_phi_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_phibins, phi_binning), 
                        'numerator_phi'
                    )
                    histos['eff_nvtx_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                        ROOT.RDF.TH1DModel('h_Mu_eff_nvtx_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_nvtxbins, nvtx_binning), 
                        'numerator_nvtx'
                    )
                    if (reg == 'AllEta'):
                        df_loc = df_loc.Define('numerator_eta', 'probe_Eta[inEtaRange&&passL1Cond&&passRecoToL1PtCutFactor]')
                        histos['eff_eta_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('h_Mu_eff_eta_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_etabins, eta_binning), 
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
        df_tau[i] = df.Define('probe_idxL1tau','FindL1TauIdx_DQMOff(L1Tau_eta, L1Tau_phi, probe_Eta, probe_Phi, L1Tau_hwIso, {})'.format(config['Isos'][iso]))

        df_tau[i] = df_tau[i].Define('probe_L1Pt','GetVal(probe_idxL1tau, L1Tau_pt)')
        df_tau[i] = df_tau[i].Define('probe_L1Eta','GetVal(probe_idxL1tau, L1Tau_eta)')
        df_tau[i] = df_tau[i].Define('probe_L1Phi','GetVal(probe_idxL1tau, L1Tau_phi)')
        df_tau[i] = df_tau[i].Define('probe_L1Bx','GetVal(probe_idxL1tau, L1Tau_bx)')
        df_tau[i] = df_tau[i].Define('probe_L1Iso','GetVal(probe_idxL1tau, L1Tau_hwIso)')

        df_tau[i] = df_tau[i].Define('probe_L1PtReso','(probe_Pt-probe_L1Pt)/probe_L1Pt')
        df_tau[i] = df_tau[i].Define('probe_L1EtaReso','(probe_L1Eta-probe_Eta)')
        df_tau[i] = df_tau[i].Define('probe_L1PhiReso','(probe_L1Phi-probe_Phi)')

        pt_binning = dqmoff_taupt_bins #leptonpt_bins
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

        if config['L1TResolution']:

            df_etarange = [None] * len(config['Regions'])
            for ireg, reg in enumerate(config['Regions']):

                region = config["Regions"][reg]
                str_binEta = "eta{}to{}".format(region[0], region[1]).replace(".","p")

                df_etarange[ireg] = df_tau[i].Define('inEtaRange','abs(probe_Eta)>={}'.format(region[0])+'&&abs(probe_Eta)<{}'.format(region[1]))
                df_etarange[ireg] = df_etarange[ireg].Define('reso_pt', 'probe_L1PtReso[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('reso_eta', 'probe_L1EtaReso[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('reso_phi', 'probe_L1PhiReso[inEtaRange]')

                # Create resolution histograms
                histos['reso_pt_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('h_Tau_reso_pt_{}_{}'.format(str_binEta, prefix)+suffix, '', n_resoptbins, reso_pt_binning), 
                    'reso_pt'
                )
                histos['reso_eta_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('h_Tau_reso_eta_{}_{}'.format(str_binEta, prefix)+suffix, '', n_resoetabins, reso_eta_binning), 
                    'reso_eta'
                )
                histos['reso_phi_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('h_Tau_reso_phi_{}_{}'.format(str_binEta, prefix)+suffix, '', n_resophibins, reso_phi_binning), 
                    'reso_phi'
                )


        if config['L1TEfficiency']:

            df_etarange = [None] * len(config['Regions'])
            for ireg, reg in enumerate(config['Regions']):

                region = config["Regions"][reg]
                str_binEta = "eta{}to{}".format(region[0], region[1]).replace(".","p")

                df_etarange[ireg] = df_tau[i].Define('inEtaRange','abs(probe_Eta)>={}'.format(region[0])+'&&abs(probe_Eta)<{}'.format(region[1]))
                df_etarange[ireg] = df_etarange[ireg].Define('denominator_pt', 'probe_Pt[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('denominator_phi', 'probe_Phi[inEtaRange]')
                df_etarange[ireg] = df_etarange[ireg].Define('denominator_nvtx', 'probe_Nvtx[inEtaRange]')

                # Create denominator histograms
                histos['eff_pt_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('h_Tau_eff_pt_{}_{}'.format(str_binEta, prefix)+suffix, '', n_ptbins, pt_binning), 
                    'denominator_pt'
                )
                histos['eff_phi_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('h_Tau_eff_phi_{}_{}'.format(str_binEta, prefix)+suffix, '', n_phibins, phi_binning), 
                    'denominator_phi'
                )
                histos['eff_nvtx_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                    ROOT.RDF.TH1DModel('h_Tau_eff_nvtx_{}_{}'.format(str_binEta, prefix)+suffix, '', n_nvtxbins, nvtx_binning), 
                    'denominator_nvtx'
                )

                if (reg == 'EB_EE'): 
                    df_etarange[ireg] = df_etarange[ireg].Define('denominator_eta', 'probe_Eta[inEtaRange]')
                    histos['eff_eta_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                        ROOT.RDF.TH1DModel('h_Tau_eff_eta_{}_{}'.format(str_binEta, prefix)+suffix, '', n_etabins, eta_binning), 
                        'denominator_eta'
                    )

                # Numerator Histograms for all Et thresholds
                l1thresholds = config["Thresholds"]
                for ipt in l1thresholds:
                    str_binEtaPt = "eta{}to{}_l1thrgeq{}".format(region[0], region[1], ipt).replace(".","p")
                    df_loc = df_etarange[ireg].Define('passL1Cond', 'probe_L1Pt>={}'.format(ipt))
                    df_loc = df_loc.Define('numerator_pt', 'probe_Pt[inEtaRange&&passL1Cond]')
                    df_loc = df_loc.Define('numerator_phi', 'probe_Phi[inEtaRange&&passL1Cond]')
                    df_loc = df_loc.Define('numerator_nvtx', 'probe_Nvtx[inEtaRange&&passL1Cond]')

                    # Create numerator histograms
                    histos['eff_pt_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                        ROOT.RDF.TH1DModel('h_Tau_eff_pt_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_ptbins, pt_binning), 
                        'numerator_pt'
                    )
                    histos['eff_phi_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                        ROOT.RDF.TH1DModel('h_Tau_eff_phi_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_phibins, phi_binning), 
                        'numerator_phi'
                    )
                    histos['eff_nvtx_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                        ROOT.RDF.TH1DModel('h_Tau_eff_nvtx_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_nvtxbins, nvtx_binning), 
                        'numerator_nvtx'
                    )

                    if (reg == 'EB_EE'):
                        df_loc = df_loc.Define('numerator_eta', 'probe_Eta[inEtaRange&&passL1Cond]')
                        histos['eff_eta_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                            ROOT.RDF.TH1DModel('h_Tau_eff_eta_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_etabins, eta_binning), 
                            'numerator_eta'
                        )
    return df, histos


def Jet_DQMOff_Plots(df, suffix = ''):

    histos = {}
    prefix = ''

    df_jet = df.Define('lead_idxL1Jet', 'FindL1JetIdx_DQMOff_setBx(L1Jet_eta, L1Jet_phi, L1Jet_bx, leadJetEta, leadJetPhi, 0)')
    df_jet = df_jet.Define('lead_L1JetPt', 'GetVal(lead_idxL1Jet, L1Jet_pt)')
    df_jet = df_jet.Define('lead_L1JetEta', 'GetVal(lead_idxL1Jet, L1Jet_eta)')
    df_jet = df_jet.Define('lead_L1JetPhi', 'GetVal(lead_idxL1Jet, L1Jet_phi)')
    df_jet = df_jet.Define('lead_L1JetBx', 'GetVal(lead_idxL1Jet, L1Jet_bx)')

    # TrigObj matching
    df_jet = df_jet.Define('LeadJet_trig_idx', 'MatchObjToTrig_DQMOff(lead_L1JetEta, lead_L1JetPhi, TrigObj_pt, TrigObj_eta, TrigObj_phi, TrigObj_id, 1, TrigObj_filterBits, 3, 0.3, 27)')
    df_jet = df_jet.Define('LeadJet_matchHLT', 'trig_is_filterbit_set_DQMOff(LeadJet_trig_idx, TrigObj_filterBits, 3)')
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

    if config['L1TResolution']:
        df_etarange = [None] * len(config['Regions'])
        for ireg, reg in enumerate(config['Regions']):
            region = config["Regions"][reg]
            str_binEta = "eta{}to{}".format(region[0], region[1]).replace(".","p")

            df_etarange[ireg] = df_jet.Define('inEtaRange','abs(leadJetEta)>={}'.format(region[0])+'&&abs(leadJetEta)<{}'.format(region[1]))
            df_etarange[ireg] = df_etarange[ireg].Define('reso_pt', 'lead_L1PtReso[inEtaRange]')
            df_etarange[ireg] = df_etarange[ireg].Define('reso_eta', 'lead_L1EtaReso[inEtaRange]')
            df_etarange[ireg] = df_etarange[ireg].Define('reso_phi', 'lead_L1PhiReso[inEtaRange]')

            # Create resolution histograms
            histos['reso_pt_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                ROOT.RDF.TH1DModel('h_LeadJet_reso_pt_{}_{}'.format(str_binEta, prefix)+suffix, '', n_resoptbins, reso_pt_binning), 
                'reso_pt'
            )
            histos['reso_eta_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                ROOT.RDF.TH1DModel('h_LeadJet_reso_eta_{}_{}'.format(str_binEta, prefix)+suffix, '', n_resoetabins, reso_eta_binning), 
                'reso_eta'
            )
            histos['reso_phi_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                ROOT.RDF.TH1DModel('h_LeadJet_reso_phi_{}_{}'.format(str_binEta, prefix)+suffix, '', n_resophibins, reso_phi_binning), 
                'reso_phi'
            )

    if config['L1TEfficiency']:
        df_etarange = [None] * len(config['Regions'])
        for ireg, reg in enumerate(config['Regions']):
            region = config["Regions"][reg]

            df_etarange[ireg] = df_jet.Define('inEtaRange','abs(leadJetEta)>={}'.format(region[0])+'&&abs(leadJetEta)<{}'.format(region[1]))
            df_etarange[ireg] = df_etarange[ireg].Define('denominator_pt', 'leadJetPt[inEtaRange]')
            
            # Create denominator histograms for pt
            str_binEta = "eta{}to{}".format(region[0], region[1]).replace(".","p")
            histos['eff_pt_'+str_binEta+'_'+prefix+'_'+suffix] = df_etarange[ireg].Histo1D (
                ROOT.RDF.TH1DModel('h_LeadJet_eff_pt_{}_{}'.format(str_binEta, prefix)+suffix, '', n_ptbins, pt_binning), 
                'denominator_pt'
            )

            # Numerator Histograms for all Et thresholds
            l1thresholds = config["Thresholds"]
            for ipt in l1thresholds:
                df_loc = df_etarange[ireg].Define('passL1Cond', 'lead_L1JetPt>={}'.format(ipt))
                df_loc = df_loc.Define('numerator_pt', 'leadJetPt[inEtaRange&&passL1Cond]')

                str_binEtaPt = "eta{}to{}_l1thrgeq{}".format(region[0], region[1], ipt).replace(".","p") 
                histos['eff_pt_'+str_binEtaPt+'_'+prefix+'_'+suffix] = df_loc.Histo1D (
                    ROOT.RDF.TH1DModel('h_LeadJet_eff_pt_{}_{}'.format(str_binEtaPt, prefix)+suffix, '', n_ptbins, pt_binning), 
                    'numerator_pt'
                )

    return df, histos


def EtSum_DQMOff_Plots(df, suffix = ''):

    histos = {}
    prefix = ''

    df_met = df.Define('idxL1MET', 'FindL1EtSumIdx_DQMOff_setBx(L1EtSum_etSumType, L1EtSum_bx, 2, 0)')
    df_met = df_met.Define('L1MET', 'L1EtSum_pt[idxL1MET]')
    df_met = df_met.Define('L1METPhi', 'L1EtSum_phi[idxL1MET]')

    df_met = df_met.Define('reso_met', '(L1MET - recoMET)/recoMET')
    df_met = df_met.Define('reso_phi', 'L1METPhi - recoMETPhi')

    met_binning = dqmoff_etsum_bins
    n_metbins = len(met_binning) - 1

    reso_pt_binning = dqmoff_etsumresolution_pt_bins
    reso_phi_binning = dqmoff_etsumresolution_phi_bins

    n_resoptbins = len(reso_pt_binning) - 1
    n_resophibins = len(reso_phi_binning) - 1

    if config['L1TResolution']:

        # Create resolution histograms
        histos['reso_pt_'+prefix+'_'+suffix] = df_met.Histo1D (
            ROOT.RDF.TH1DModel('h_EtSum_reso_met_{}'.format(prefix)+suffix, '', n_resoptbins, reso_pt_binning), 
            'reso_met'
        )
        histos['reso_phi_'+prefix+'_'+suffix] = df_met.Histo1D (
            ROOT.RDF.TH1DModel('h_EtSum_reso_phi_{}'.format(prefix)+suffix, '', n_resophibins, reso_phi_binning), 
            'reso_phi'
        )

    if config['L1TEfficiency']:

        # df_met = df_met.Define('denominator_met', 'recoMET')

        # Create denominator histograms for pt
        histos['eff_met_'+prefix+'_'+suffix] = df_met.Histo1D (
            ROOT.RDF.TH1DModel('h_EtSum_eff_met_{}'.format(prefix)+suffix, '', n_metbins, met_binning), 
            'recoMET'
        )

        # Numerator Histograms for all Et thresholds
        l1thresholds = config["Thresholds"]
        for imet in l1thresholds:
            df_loc = df_met.Define('passL1Cond', 'L1MET>={}'.format(imet))
            # df_loc = df_loc.Define('numerator_met', 'recoMET[passL1Cond]')

            str_binPt = "l1thrgeq{}".format(imet).replace(".","p") 
            histos['eff_met_'+str_binPt+'_'+prefix+'_'+suffix] = df_loc.Filter('passL1Cond').Histo1D (
                ROOT.RDF.TH1DModel('h_EtSum_eff_met_{}_{}'.format(str_binPt, prefix)+suffix, '', n_metbins, met_binning), 
                'recoMET'
            )

    return df, histos

    
def CleanJets(df):
    #List of cleaned jets (noise cleaning + lepton/photon overlap removal)
    df = df.Define('_jetPassID', 'Jet_jetId>=4')
    #df = df.Define('_jetLeptonPhotonCleaned', 'true') 
    #df = df.Define('isCleanJet','_jetPassID&&_jetLeptonPhotonCleaned&&Jet_pt>30&&Jet_muEF<0.5&&Jet_chEmEF<0.5')
    # _jetLeptonPhotonCleaned redondant with _jetPassID
    df = df.Define('isCleanJet','_jetPassID&&Jet_pt>30&&Jet_muEF<0.5&&Jet_chEmEF<0.5')
    df = df.Define('cleanJet_Pt','Jet_pt[isCleanJet]')
    df = df.Define('cleanJet_Eta','Jet_eta[isCleanJet]')
    df = df.Define('cleanJet_Phi','Jet_phi[isCleanJet]')
    df = df.Define('cleanJet_NHEF','Jet_neHEF[isCleanJet]')
    df = df.Define('cleanJet_NEEF','Jet_neEmEF[isCleanJet]')
    df = df.Define('cleanJet_CHEF','Jet_chHEF[isCleanJet]')
    df = df.Define('cleanJet_CEEF','Jet_chEmEF[isCleanJet]')
    df = df.Define('cleanJet_MUEF','Jet_muEF[isCleanJet]')
    df = df.Filter(stringToPrintJets)
    df = df.Filter('Sum(isCleanJet)>=1','>=1 clean jet with p_{T}>30 GeV')

    return df

def lepton_ismuon(df):
    df = df.Define('_lPt', 'Muon_pt')
    df = df.Define('_lEta', 'Muon_eta')
    df = df.Define('_lPhi', 'Muon_phi')
    df = df.Define('_lpdgId', 'Muon_pdgId')
    return(df)

def lepton_iselectron(df):
    df = df.Define('_lPt', 'Electron_pt')
    df = df.Define('_lEta', 'Electron_eta')
    df = df.Define('_lPhi', 'Electron_phi')
    df = df.Define('_lpdgId', 'Electron_pdgId')
    return(df)

def EtSum(df, suffix = ''):
    histos = {}
    #HT=scalar pt sum of all jets with pt>30 and |eta|<2.5 
    df = df.Define('iscentraljet','cleanJet_Pt>30&&abs(cleanJet_Eta)<2.5')
    #df = df.Filter('Sum(iscentraljet)>0')
    df = df.Define('HT','Sum(cleanJet_Pt[cleanJet_Pt>30&&abs(cleanJet_Eta)<2.5])')

    df = df.Define('muons_px','Sum(_lPt[abs(_lpdgId)==13]*cos(_lPhi[abs(_lpdgId)==13]))')
    df = df.Define('muons_py','Sum(_lPt[abs(_lpdgId)==13]*sin(_lPhi[abs(_lpdgId)==13]))')
    df = df.Define('metnomu_x','PuppiMET_pt*cos(PuppiMET_phi)+muons_px')
    df = df.Define('metnomu_y','PuppiMET_pt*sin(PuppiMET_phi)+muons_py')
    df = df.Define('MetNoMu','sqrt(metnomu_x*metnomu_x+metnomu_y*metnomu_y)')

    # Dijet selections
    df = df.Define('hastwocleanjets', 'PassDiJet(cleanJet_Pt, cleanJet_Eta, cleanJet_Phi, 80, 40, 500)')
    df = df.Define('vbf_selection', 'PassDiJet(cleanJet_Pt, cleanJet_Eta, cleanJet_Phi, 140, 70, 900)')
    df = df.Define('hastwocentraljets', 'PassDiJet80_40_Mjj500_central(cleanJet_Pt, cleanJet_Eta, cleanJet_Phi)')
    df = df.Define('hastwoHFjets', 'PassDiJet80_40_Mjj500_HF(cleanJet_Pt, cleanJet_Eta, cleanJet_Phi)')

    # for VBF trig
    #df = df.Define('HLT_VBF_filter', 'run>367661&&PassDiJet75_40_500(cleanJet_Pt, cleanJet_Eta, cleanJet_Phi)')
    df = df.Define('HLT_VBF_filter', 'PassDiJet75_40_500(cleanJet_Pt, cleanJet_Eta, cleanJet_Phi)')

    histos['h_MetNoMu_Denominator'+suffix] = df.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_Denominator'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu') 
    
#    dfmetl1 = df.Filter('L1_ETMHF80')
#    #dfmetl1 = df.Filter('MET_sumEt>80')
#    #dfmetl1 = df.Filter('PuppiMET_sumEt>80')
#    histos['L1_ETMHF80'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF80'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
#    dfmetl1 = df.Filter('L1_ETMHF90')
#    histos['L1_ETMHF90'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF90'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dfmetl1 = df.Filter('L1_ETMHF100')
    histos['L1_ETMHF100'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF100'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dfmetl1 = df.Filter('L1_ETMHF110')
    histos['L1_ETMHF110'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF110'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')

    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight'+suffix] =  df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60'+suffix] =  df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    

    histos['h_HT_Denominator'+suffix] = df.Filter('PuppiMET_pt<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_Denominator'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT') 
    #histos['L1_HTT200er'+suffix] = df.Filter('L1_HTT200er').Filter('PuppiMET_pt<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_L1_HTT200er'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT')  
    histos['L1_HTT200er'+suffix] = df.Filter('L1_HTT200er').Filter('PuppiMET_pt<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_L1_HTT200er'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT')  
    histos['L1_HTT280er'+suffix] = df.Filter('L1_HTT280er').Filter('PuppiMET_pt<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_L1_HTT280er'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT')
    histos['L1_HTT360er'+suffix] = df.Filter('L1_HTT360er').Filter('PuppiMET_pt<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_L1_HTT360er'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT')
    histos['HLT_PFHT1050'+suffix] =  df.Filter('HLT_PFHT1050').Filter('PuppiMET_pt<50').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFHT1050'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT')

    # DiJet selections:

    # DiJet 80 40
    histos['h_MetNoMu_Denominator_DiJet80_40_Mjj500'+suffix] = df.Filter('hastwocleanjets').Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_Denominator_DiJet80_40_Mjj500'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu') 
    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet80_40_Mjj500'+suffix] = df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight&&hastwocleanjets').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet80_40_Mjj500'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_DiJet80_40_Mjj500'+suffix] = df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60&&hastwocleanjets').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_DiJet80_40_Mjj500'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')

    # central dijet
    histos['h_MetNoMu_Denominator_DiJet80_40_Mjj500_central'+suffix] = df.Filter('hastwocentraljets').Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_Denominator_DiJet80_40_Mjj500_central'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu') 
    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet80_40_Mjj500_central'+suffix] = df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight&&hastwocentraljets').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet80_40_Mjj500_central'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')

    # HF dijets
    histos['h_MetNoMu_Denominator_DiJet80_40_Mjj500_HF'+suffix] = df.Filter('hastwoHFjets').Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_Denominator_DiJet80_40_Mjj500_HF'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu') 
    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet80_40_Mjj500_HF'+suffix] = df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight&&hastwoHFjets').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet80_40_Mjj500_HF'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')

    # VBF selection (DiJet 140 70, mjj > 900 GeV) denominator
    histos['h_MetNoMu_Denominator_DiJet140_70_Mjj900'+suffix] = df.Filter('vbf_selection').Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_Denominator_DiJet140_70_Mjj900'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu') 

    # Normal (MET only) trigger
    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet140_70_Mjj900'+suffix] = df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight&&vbf_selection').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet140_70_Mjj900'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')

    # VBF (Met + jet) trigger
    histos['HLT_DiJet110_35_Mjj650_PFMET110_DiJet140_70_Mjj900'+suffix] =  df.Filter('HLT_DiJet110_35_Mjj650_PFMET110&&vbf_selection').Histo1D(ROOT.RDF.TH1DModel('h_HLT_DiJet110_35_Mjj650_PFMET110_DiJet140_70_Mjj900'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')

    # VBF trigger
    if max(runnb_bins) > 367661:
        histos['h_MetNoMu_Denominator_VBF_DiJet70_40_500'+suffix] = df.Filter('run>367661').Filter('HLT_VBF_filter').Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_Denominator_VBF_DiJet70_40_500'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
        histos['HLT_VBF_DiPFJet75_40_Mjj500_Detajj2p5_PFMET85'+suffix] =  df.Filter('run>367661').Filter('HLT_VBF_filter&&HLT_VBF_DiPFJet75_40_Mjj500_Detajj2p5_PFMET85').Histo1D(ROOT.RDF.TH1DModel('HLT_VBF_DiPFJet75_40_Mjj500_Detajj2p5_PFMET85'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')

    return df, histos

def AnalyzeCleanJets(df, JetRecoPtCut, L1JetPtCut, suffix = ''):    
    histos = {}
    #Find L1 jets matched to the offline jet
    #df = df.Define('cleanJet_idxL1jet','FindL1JetIdx(L1Jet_eta, L1Jet_phi, cleanJet_Eta, cleanJet_Phi)')
    # only take jets in bx 0
    df = df.Define('cleanJet_idxL1jet', 'FindL1JetIdx_setBx(L1Jet_eta, L1Jet_phi, L1Jet_bx, cleanJet_Eta, cleanJet_Phi, 0)')
    df = df.Define('cleanJet_L1Pt','GetVal(cleanJet_idxL1jet,L1Jet_pt)')
    df = df.Define('cleanJet_L1Bx','GetVal(cleanJet_idxL1jet,L1Jet_bx)')
    df = df.Define('cleanJet_L1PtoverRecoPt','cleanJet_L1Pt/cleanJet_Pt')
    df = df.Filter(stringFailingJets)
    #Now some plotting (turn ons for now)
    L1PtCuts = [30., 40., 60., 80., 100., 120., 140., 160., 170., 180., 200.]


    df = makehistosforturnons_inprobeetaranges(df, histos, etavarname='cleanJet_Eta', phivarname='cleanJet_Phi', ptvarname='cleanJet_Pt', responsevarname='cleanJet_L1PtoverRecoPt', l1varname='cleanJet_L1Pt', l1thresholds=config['Thresholds'], prefix="Jet_plots", binning=jetmetpt_bins, l1thresholdforeffvsrunnb = L1JetPtCut, offlinethresholdforeffvsrunnb = JetRecoPtCut, suffix = suffix) 

    # Make same histosgrams, in a single bin of eta (abs(eta) < 5)
    #df = makehistosforturnons_inprobeetaranges(df, histos, etavarname='cleanJet_Eta', phivarname='cleanJet_Phi', ptvarname='cleanJet_Pt', responsevarname='cleanJet_L1PtoverRecoPt', etabins=[0., 5.], l1varname='cleanJet_L1Pt', l1thresholds=[40., 180.], prefix="Jet_plots_eta_inclusive", binning=jetmetpt_bins, l1thresholdforeffvsrunnb = L1JetPtCut, offlinethresholdforeffvsrunnb = JetRecoPtCut, suffix = suffix) 

    if config['Efficiency']:
        df = df.Define('cleanHighPtJet_Eta','cleanJet_Eta[cleanJet_Pt>{}]'.format(JetRecoPtCut))
        df = df.Define('cleanHighPtJet_Phi','cleanJet_Phi[cleanJet_Pt>{}]'.format(JetRecoPtCut))
        df = df.Define('cleanHighPtJet_Eta_PassL1Jet','cleanJet_Eta[cleanJet_L1Pt>={}&&cleanJet_Pt>{}]'.format(L1JetPtCut, JetRecoPtCut))
        df = df.Define('cleanHighPtJet_Phi_PassL1Jet','cleanJet_Phi[cleanJet_L1Pt>={}&&cleanJet_Pt>{}]'.format(L1JetPtCut, JetRecoPtCut))
        
        histos["L1JetvsEtaPhi_Numerator"+suffix] = df.Histo2D(ROOT.RDF.TH2DModel('h_L1Jet{}vsEtaPhi_Numerator'.format(int(L1JetPtCut))+suffix, '', 100,-5,5,100,-3.1416,3.1416), 'cleanHighPtJet_Eta_PassL1Jet','cleanHighPtJet_Phi_PassL1Jet')
        histos["L1JetvsEtaPhi_EtaRestricted"+suffix] = df.Histo2D(ROOT.RDF.TH2DModel('h_L1Jet{}vsEtaPhi_EtaRestricted'.format(int(L1JetPtCut))+suffix, '', 100,-5,5,100,-3.1416,3.1416), 'cleanHighPtJet_Eta','cleanHighPtJet_Phi')
    

    if config['Prefiring']:

        df = df.Define('cleanJet_idxL1jet_allBx', 'FindL1JetIdx(L1Jet_eta, L1Jet_phi, cleanJet_Eta, cleanJet_Phi)')
        df = df.Define('cleanJet_L1Pt_allBx','GetVal(cleanJet_idxL1jet_allBx, L1Jet_pt)')

        df = df.Define('cleanJet_idxL1jet_Bxmin1', 'FindL1JetIdx_setBx(L1Jet_eta, L1Jet_phi, L1Jet_bx, cleanJet_Eta, cleanJet_Phi, -1)')
        df = df.Define('cleanJet_L1Pt_Bxmin1','GetVal(cleanJet_idxL1jet_Bxmin1, L1Jet_pt)')

        df = df.Define('cleanJet_idxL1jet_Bxplus1', 'FindL1JetIdx_setBx(L1Jet_eta, L1Jet_phi, L1Jet_bx, cleanJet_Eta, cleanJet_Phi, 1)')
        df = df.Define('cleanJet_L1Pt_Bxplus1','GetVal(cleanJet_idxL1jet_Bxplus1, L1Jet_pt)')

        #

        #df = df.Define('probeL1Jet100to150Bxmin1_Eta','cleanJet_Eta[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==-1]')
        #df = df.Define('probeL1Jet100to150Bxmin1_Phi','cleanJet_Phi[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==-1]')
        #df = df.Define('probeL1Jet100to150Bx0_Eta','cleanJet_Eta[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==0]')
        #df = df.Define('probeL1Jet100to150Bx0_Phi','cleanJet_Phi[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==0]')
        #df = df.Define('probeL1Jet100to150Bxplus1_Eta','cleanJet_Eta[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==1]')
        #df = df.Define('probeL1Jet100to150Bxplus1_Phi','cleanJet_Phi[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==1]')

        filter_100to150 = 'cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt_allBx>100&&cleanJet_L1Pt_allBx<=150'
        df = df.Define('probeL1Jet100to150Bxmin1_Eta','cleanJet_Eta[{}&&cleanJet_L1Pt_Bxmin1>100&&cleanJet_L1Pt_Bxmin1<=150]'.format(filter_100to150))
        df = df.Define('probeL1Jet100to150Bxmin1_Phi','cleanJet_Phi[{}&&cleanJet_L1Pt_Bxmin1>100&&cleanJet_L1Pt_Bxmin1<=150]'.format(filter_100to150))
        df = df.Define('probeL1Jet100to150Bx0_Eta','cleanJet_Eta[{}&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150]'.format(filter_100to150))
        df = df.Define('probeL1Jet100to150Bx0_Phi','cleanJet_Phi[{}&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150]'.format(filter_100to150))
        df = df.Define('probeL1Jet100to150Bxplus1_Eta','cleanJet_Eta[{}&&cleanJet_L1Pt_Bxplus1>100&&cleanJet_L1Pt_Bxplus1<=150]'.format(filter_100to150))
        df = df.Define('probeL1Jet100to150Bxplus1_Phi','cleanJet_Phi[{}&&cleanJet_L1Pt_Bxplus1>100&&cleanJet_L1Pt_Bxplus1<=150]'.format(filter_100to150))



        histos['L1Jet100to150_bxmin1_etaphi'+suffix] = df.Histo2D(ROOT.RDF.TH2DModel('L1Jet100to150_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Jet100to150Bxmin1_Eta', 'probeL1Jet100to150Bxmin1_Phi')
        histos['L1Jet100to150_bx0_etaphi'+suffix] = df.Histo2D(ROOT.RDF.TH2DModel('L1Jet100to150_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Jet100to150Bx0_Eta', 'probeL1Jet100to150Bx0_Phi')
        histos['L1Jet100to150_bxplus1_etaphi'+suffix] = df.Histo2D(ROOT.RDF.TH2DModel('L1Jet100to150_bxplus1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Jet100to150Bxplus1_Eta', 'probeL1Jet100to150Bxplus1_Phi')

        histos['L1Jet100to150_bxmin1_eta'+suffix] = df.Histo1D(ROOT.RDF.TH1DModel('L1Jet100to150_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1Jet100to150Bxmin1_Eta')
        histos['L1Jet100to150_bx0_eta'+suffix] = df.Histo1D(ROOT.RDF.TH1DModel('L1Jet100to150_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Jet100to150Bx0_Eta')
        histos['L1Jet100to150_bxplus1_eta'+suffix] = df.Histo1D(ROOT.RDF.TH1DModel('L1Jet100to150_bxplus1_eta'+suffix, '', 100, -5, 5), 'probeL1Jet100to150Bxplus1_Eta')

    return df, histos

def HFNoiseStudy(df, suffix = ''):
    '''
    Offline study of HF noise.
    '''
    histos={}
    #debugging what happens in the HF 
    dfhfnoise = df.Define('isHFJet','cleanJet_Pt>30&&((cleanJet_Eta>3.0&&cleanJet_Eta<5)||(cleanJet_Eta>-5&&cleanJet_Eta<-3.))' )
    dfhfnoise = dfhfnoise.Define('nHFJets','Sum(isHFJet)')
    dfhfnoise = dfhfnoise.Define('isHFJetPt250','cleanJet_Pt>250&&((cleanJet_Eta>3.0&&cleanJet_Eta<5)||(cleanJet_Eta>-5&&cleanJet_Eta<-3.))' )
    dfhfnoise = dfhfnoise.Filter('Sum(isHFJetPt250)>0')
    dfhfnoise = dfhfnoise.Define('passL1Pt80','cleanJet_L1Pt>80')
    
    dfhfnoise = dfhfnoise.Define('HighPtHFJet_Pt','cleanJet_Pt[isHFJetPt250]')
    dfhfnoise = dfhfnoise.Define('HighPtHFJet_Eta','cleanJet_Eta[isHFJetPt250]')

    dfhfnoise = dfhfnoise.Define('HighPtJet_HFSEtaEta','Jet_hfsigmaEtaEta[Jet_pt>250&&((Jet_eta>3.0&&Jet_eta<5)||(Jet_eta>-5&&Jet_eta<-3.))]')
    dfhfnoise = dfhfnoise.Define('HighPtJet_HFSPhiPhi','Jet_hfsigmaPhiPhi[Jet_pt>250&&((Jet_eta>3.0&&Jet_eta<5)||(Jet_eta>-5&&Jet_eta<-3.))]')
    dfhfnoise = dfhfnoise.Define('HighPtJet_HFCentralEtaStripSize','Jet_hfcentralEtaStripSize[Jet_pt>250&&((Jet_eta>3.0&&Jet_eta<5)||(Jet_eta>-5&&Jet_eta<-3.))]')
    dfhfnoise = dfhfnoise.Define('HighPtJet_HFAdjacentEtaStripSize','Jet_hfadjacentEtaStripsSize[Jet_pt>250&&((Jet_eta>3.0&&Jet_eta<5)||(Jet_eta>-5&&Jet_eta<-3.))]')
    
    
    prefix = ['failL1Jet80', 'passL1Jet80']
    df_passvsfailL1 = [dfhfnoise.Filter('Sum(passL1Pt80&&isHFJetPt250)==0'), dfhfnoise.Filter('Sum(passL1Pt80&&isHFJetPt250)>=1')]
    
    for i, p in enumerate(prefix):
        if i == 0:
            df_passvsfailL1[i] = df_passvsfailL1[i].Filter(stringToPrintHF)
        

        histos[p+'_nhfjets'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_nhfjets'+suffix, '', 100, 0, 100), 'nHFJets')
        histos[p+'_npv'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_npv'+suffix, '', 100, 0, 100), 'PV_npvs')
        histos[p+'_runnb'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_runnb'+suffix, '', len(runnb_bins)-1, runnb_bins), 'run')
        '''
        histos[p+'_photonpt'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_photonpt'+suffix, '', 100, 0, 1000), 'ref_Pt')
        histos[p+'_ptbalance'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_ptbalance'+suffix, '', len(response_bins)-1, response_bins), 'ptbalance')
        histos[p+'_ptbalanceL1'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_ptbalanceL1'+suffix, '', len(response_bins)-1, response_bins), 'ptbalanceL1')
        '''
        histos[p+'_HighPtHFJet_Eta'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_HighPtHFJet_Eta'+suffix, '', 1000, -5, 5), 'HighPtHFJet_Eta')
        histos[p+'_HighPtHFJet_Pt'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_HighPtHFJet_Pt'+suffix, '', 80, 100, 500), 'HighPtHFJet_Pt')
        histos[p+'_HighPtJet_HFSEtaEtavsPhiPhi'+suffix] = df_passvsfailL1[i].Histo2D(ROOT.RDF.TH2DModel(p+'_HighPtJet_HFSEtaEtavsPhiPhi'+suffix, '', 100, 0, 0.2, 100, 0, 0.2), 'HighPtJet_HFSEtaEta','HighPtJet_HFSPhiPhi')
        histos[p+'_HighPtJet_HFCentralVsAdjacentEtaStripSize'+suffix] = df_passvsfailL1[i].Histo2D(ROOT.RDF.TH2DModel(p+'_HighPtJet_HFCentralVsAdjacentEtaStripSize'+suffix, '', 10, 0, 10, 10, 0, 10), 'HighPtJet_HFCentralEtaStripSize', 'HighPtJet_HFAdjacentEtaStripSize')

        histos[p+'MET_pt'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'PuppiMET_pt'+suffix, '', 100,0,500), 'PuppiMET_pt')

    return df, histos
    
def PtBalanceSelection(df):
    '''
    Compute pt balance = pt(jet)/pt(ref)
    ref can be a photon or a Z.
    '''
    
    #Back to back condition
    df = df.Filter('abs(acos(cos(ref_Phi-cleanJet_Phi[0])))>2.9','DeltaPhi(ph,jet)>2.9')

    #Compute Pt balance = pt(jet)/pt(ref) => here ref is a photon
    #Reco first
    df = df.Define('ptbalance','cleanJet_Pt[0]/ref_Pt')
    df = df.Define('ptbalanceL1','L1Jet_pt[cleanJet_idxL1jet[0]]/ref_Pt')
    df = df.Define('probe_Eta','cleanJet_Eta[0]') 
    df = df.Define('probe_Phi','cleanJet_Phi[0]')
    return df

def AnalyzePtBalance(df, suffix = ''):
    histos = {}
    df_JetsBinnedInEta ={}
    histos['L1JetvsEtaPhi'+suffix] = df.Histo3D(ROOT.RDF.TH3DModel('h_L1PtBalanceVsEtaPhi'+suffix, 'ptbalanceL1', 100, -5, 5, 100, -3.1416, 3.1416, 100, 0, 2), 'probe_Eta','probe_Phi','ptbalanceL1')
    for r in config['Regions']:
        region = config['Regions'][r]
        str_bineta = "eta{}to{}".format(region[0], region[1]).replace(".","p")
        df_JetsBinnedInEta[str_bineta] = df.Filter('abs(cleanJet_Eta[0])>={}&&abs(cleanJet_Eta[0])<{}'.format(region[0], region[1]))
        histos['RecoJetvsRunNb'+str_bineta+suffix] = df_JetsBinnedInEta[str_bineta].Histo2D(ROOT.RDF.TH2DModel('h_PtBalanceVsRunNb_{}'.format(str_bineta)+suffix, 'ptbalance', len(runnb_bins)-1, runnb_bins, len(response_bins)-1, response_bins), 'run','ptbalance')
        histos['L1JetvsRunNb'+str_bineta+suffix] = df_JetsBinnedInEta[str_bineta].Histo2D(ROOT.RDF.TH2DModel('h_L1PtBalanceVsRunNb_{}'.format(str_bineta)+suffix, 'ptbalanceL1', len(runnb_bins)-1, runnb_bins, len(response_bins)-1, response_bins), 'run','ptbalanceL1')
        histos['L1JetvsPU'+str_bineta+suffix] = df_JetsBinnedInEta[str_bineta].Histo2D(ROOT.RDF.TH2DModel('h_L1PtBalanceVsPU_{}'.format(str_bineta)+suffix, 'ptbalanceL1', 100, 0, 100, 100, 0, 2), 'PV_npvs','ptbalanceL1')
        # only one jet with pT > 30 GeV
        histos['L1JetvsRunNb_singlejet'+str_bineta+suffix] = df_JetsBinnedInEta[str_bineta].Filter('Sum(isCleanJet)==1','==1 clean jet with p_{T}>30 GeV').Histo2D(ROOT.RDF.TH2DModel('h_L1PtBalanceVsRunNb_singlejet_{}'.format(str_bineta)+suffix, 'ptbalanceL1', len(runnb_bins)-1, runnb_bins, len(response_bins)-1, response_bins), 'run','ptbalanceL1')

    return df, histos
