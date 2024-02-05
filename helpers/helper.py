import ROOT
from array import array
from math import floor, ceil

from bins import *

'''

jetEtaBins = [0., 1.3, 2.5, 3., 3.5, 4., 5.]
egEtaBins = [0., 1.479, 2.5]
muEtaBins = [0., 0.83, 1.24, 2.4]


ht_bins = array('f', [ i*10 for i in range(50) ] + [ 500+ i*20 for i in range(25) ] + [1000 + i*50 for i in range(10)] +[1500,1600,1700,1800,2000,2500,3000])
leptonpt_bins = array('f',[ i for i in range(50) ] + [ 50+2*i for i in range(10) ] + [ 70+3*i for i in range(10) ] + [100+10*i for i in range(10) ] + [200, 250, 300, 400, 500])
jetmetpt_bins = array('f',[ i*5 for i in range(50) ] +  [250+10*i for i in range(25) ]  + [500+20*i for i in range(10) ] + [700, 800, 900, 1000, 1200, 1500, 2000 ])
'''

#from runsBinning import *
#runnb_bins = array('f', runbinning())

response_bins = array('f',[0.+float(i)/100. for i in range(200)] )

runnb_bins = None

def set_runnb_bins(df):
    global runnb_bins
    if runnb_bins is None:
        # +1: to get [run, run+1] bin, +0.5 and floor to prevent float rounding errors + high bound
        # in range is excluded, so feed run, and run+2 to get [run, run+1]
        runNb_max = ceil(df.Max("_runNb").GetValue() + 1.5)
        runNb_min = floor(df.Min("_runNb").GetValue())
        runnb_bins = array('f', [r for r in range(runNb_min, runNb_max)])
        print("minimum run number: {}".format(runNb_min))
    else:
        print("runnb_bins are already set")

#String printing stuff for a few events
stringToPrint = '''
if(EventsToPrint <100) {

cout << "*********New Event********"<<endl;
cout << "_runNb " << _runNb<<endl;

for(unsigned int i = 0;i< (_lPt).size();i++ ){
cout << "Lepton Pt, Eta, Phi: " << (_lPt)[i]<<", "<<(_lEta)[i]<<", "<<(_lPhi)[i]<<endl;
cout << "Lepton pdgId: " << (_lpdgId)[i]<<endl;
}
for(unsigned int i = 0;i< (_phPt).size();i++ ){
cout << "Photon Pt, Eta, Phi: " << (_phPt)[i]<<", "<<(_phEta)[i]<<", "<<(_phPhi)[i]<<endl;
}
for(unsigned int i = 0;i< (_jetPt).size();i++ ){
cout << "jet Pt, Eta, Phi: " << (_jetPt)[i]<<", "<<(_jetEta)[i]<<", "<<(_jetPhi)[i]<<endl;
cout << "jet PassID, MUEF, CEEF, CHEF: " << (_jetPassID)[i]<<", "<<(_jet_MUEF)[i]<<", "<<(_jet_CEEF)[i]<<", "<<  (_jet_CHEF)[i]<<endl;
}

for(unsigned int i = 0;i< (_L1eg_pt).size();i++ ){
cout << "L1 EG Pt, Eta, Phi: " << (_L1eg_pt)[i]<<", "<<(_L1eg_eta)[i]<<", "<<(_L1eg_phi)[i]<<endl;
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
cout << "runNb: "<< _runNb<<endl;
cout << "jet Pt, Eta, Phi: " << (cleanJet_Pt)[i]<<", "<<(cleanJet_Eta)[i]<<", "<<(cleanJet_Phi)[i]<< endl; 
cout << "jet NHEF, CHEF, NEEF, CEEF, MUEF: "<<(cleanJet_NHEF)[i]<< ", " << (cleanJet_CHEF)[i]<< ", " << (cleanJet_NEEF)[i]<< ", "<< (cleanJet_CEEF)[i]<< ", " << (cleanJet_MUEF)[i]<<endl;

findbadjet = true;
}
}
if(findbadjet){
for(unsigned int i = 0;i< (_L1jet_pt).size();i++ ){
cout << "L1 JET Pt, Eta, Phi, Bx: " << (_L1jet_pt)[i]<<", "<<(_L1jet_eta)[i]<<", "<<(_L1jet_phi)[i]<< ", "<<(_L1jet_bx)[i]<<endl;
}
}

return true;
'''

stringToPrintHF = '''
if(EventsToPrint <100) {

cout << "*********New Event********"<<endl;
cout << "_runNb " << _runNb<<endl;
cout << "met, met_phi " << _met <<", "<<_met_phi<<endl;
for(unsigned int i = 0;i< (_lPt).size();i++ ){
cout << "Lepton Pt, Eta, Phi: " << (_lPt)[i]<<", "<<(_lEta)[i]<<", "<<(_lPhi)[i]<<endl;
cout << "Lepton pdgId: " << (_lpdgId)[i]<<endl;
}
for(unsigned int i = 0;i< (_phPt).size();i++ ){
cout << "Photon Pt, Eta, Phi: " << (_phPt)[i]<<", "<<(_phEta)[i]<<", "<<(_phPhi)[i]<<endl;
}
for(unsigned int i = 0;i< (_jetPt).size();i++ ){
cout << "jet Pt, Eta, Phi: " << (_jetPt)[i]<<", "<<(_jetEta)[i]<<", "<<(_jetPhi)[i]<<endl;
cout << "jet PassID, MUEF, CEEF, CHEF, NHEF: " << (_jetPassID)[i]<<", "<<(_jet_MUEF)[i]<<", "<<(_jet_CEEF)[i]<<", "<<  (_jet_CHEF)[i]<<", "<<  (_jet_NHEF)[i]<<endl;
cout << "jethfsigmaEtaEta jethfsigmaPhiPhi jethfcentralEtaStripSize "<< (_jethfsigmaEtaEta)[i]<<", "<<  (_jethfsigmaPhiPhi)[i]<<", "<<(_jethfcentralEtaStripSize)[i]<<endl;
}


for(unsigned int i = 0;i< (_L1jet_pt).size();i++ ){
cout << "L1 JET Pt, Eta, Phi, Bx: " << (_L1jet_pt)[i]<<", "<<(_L1jet_eta)[i]<<", "<<(_L1jet_phi)[i]<<", " << (_L1jet_bx)[i]<<endl;
}



cout <<endl;

EventsToPrint++;
} 
return true;
'''

highEnergyJet = '''
for( unsigned int i = 0; i < (_jetPt).size(); i++){
    if(_jetPt[i] * cosh(_jetEta[i]) > 6000){
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
#    df = df.Filter('_met<50')
    df = df.Filter('HLT_Photon110EB_TightID_TightIso')
    df = df.Define('photonsptgt20','_phPt>20')
    df = df.Filter('Sum(photonsptgt20)==1','=1 photon with p_{T}>20 GeV')
    
    df = df.Define('isRefPhoton','_phPassTightID&&_phPassIso&&_phPt>115&&abs(_phEta)<1.479')
    df = df.Filter('Sum(isRefPhoton)==1','Photon has p_{T}>115 GeV, passes tight ID and is in EB')
    
    df = df.Define('cleanPh_Pt','_phPt[isRefPhoton]')
    df = df.Define('cleanPh_Eta','_phEta[isRefPhoton]')
    df = df.Define('cleanPh_Phi','_phPhi[isRefPhoton]')
    
    df = df.Define('ref_Pt','cleanPh_Pt[0]')
    df = df.Define('ref_Phi','cleanPh_Phi[0]')
    
    return df
    
    
    
    
def MuonJet_MuonSelection(df):
    '''
    Select events with >= 1 muon with pT>25 GeV.
    The event must pass a single muon trigger. 
    '''
    df = df.Filter('HLT_IsoMu24')

    df = df.Define('goodmuonPt25','_lPt>25&&abs(_lpdgId)==13&&_lPassTightID')
    df = df.Filter('Sum(goodmuonPt25)>=1','>=1 muon with p_{T}>25 GeV')
    df = df.Define('badmuonPt10','_lPt>10&&abs(_lpdgId)==13&&_lPassTightID==0')
    df = df.Filter('Sum(badmuonPt10)==0','No bad quality muon')

    # reject events containing a jet with energy > 6000 GeV
#    df = df.Filter(highEnergyJet, 'No high energy jet')
    return df
    
    

def ZEE_EleSelection(df):
    '''
    Select Z->ee events passing a single electron trigger. Defines probe pt/eta/phi
    '''
    df = df.Filter('HLT_Ele32_WPTight_Gsf')

    df = df.Define('isTag','_lPt>35&&abs(_lpdgId)==11&&_lPassTightID&&_lpassHLT_Ele32_WPTight_Gsf')
    df = df.Filter('Sum(isTag)>0')
    df = df.Define('isProbe','_lPt>5&&abs(_lpdgId)==11&&_lPassTightID&& (Sum(isTag)>=2|| isTag==0)')
    df = df.Filter('_mll>80&&_mll<100')

    df = df.Define('probe_Pt','_lPt[isProbe]')
    df = df.Define('probe_Eta','_lEta[isProbe]')
    df = df.Define('probe_Phi','_lPhi[isProbe]')

    #df = df.Define('probe_Charge', '_l
    
    return df


def ZMuMu_MuSelection(df):
    '''
    Selects Z->mumu events passing a single muon trigger. Defines probe pt/eta/phi
    '''
    df = df.Filter('HLT_IsoMu24')

    df = df.Define('isTag','_lPt>25&&abs(_lpdgId)==13&&_lPassTightID&&_lpassHLT_IsoMu24')
    df = df.Filter('Sum(isTag)>0')
    df = df.Define('isProbe','_lPt>3&&abs(_lpdgId)==13&&_lPassTightID&& (Sum(isTag)>=2|| isTag==0)')
    df = df.Filter('_mll>80&&_mll<100')

    df = df.Define('probe_Pt','_lPt[isProbe]')
    df = df.Define('probe_Eta','_lEta[isProbe]')
    df = df.Define('probe_Phi','_lPhi[isProbe]')
    
    return df



    

def makehistosforturnons_inprobeetaranges(df, histos, etavarname, phivarname, ptvarname, responsevarname, etabins, l1varname, l1thresholds, prefix, binning, l1thresholdforeffvsrunnb, offlinethresholdforeffvsrunnb, suffix = ''):
    '''Make histos for turnons vs pt (1D histos for numerator and denominator) in ranges of eta
    Also look at response vs run number (2D histo) '''

    # check that runnb_bins are set
    if runnb_bins is None:
        set_runnbbins(df)

    for i in range(len(etabins)-1):
        str_bineta = "eta{}to{}".format(etabins[i],etabins[i+1]).replace(".","p")
        #Define columns corresponding to pt and response for the selected eta range 
        df_etarange = df.Define('inEtaRange','abs({})>={}'.format(etavarname, etabins[i])+'&&abs({})<{}'.format(etavarname, etabins[i+1]))
        df_etarange = df_etarange.Filter('_met<100')
        df_etarange = df_etarange.Define('denominator_pt',ptvarname+'[inEtaRange]')
        df_etarange = df_etarange.Define('response',responsevarname+'[inEtaRange]')
        df_etarange = df_etarange.Define('runnb',"return ROOT::VecOps::RVec<int>(response.size(), _runNb);")

        #Response vs pt and vs runnb (2d)
        histos[prefix+str_bineta+suffix] = df_etarange.Histo1D(ROOT.RDF.TH1DModel('h_{}_{}'.format(prefix, str_bineta)+suffix, '', len(binning)-1, binning), 'denominator_pt')
        histos[prefix+str_bineta+'_ResponseVsPt'+suffix] = df_etarange.Histo2D(ROOT.RDF.TH2DModel('h_ResponseVsPt_{}_{}'.format(prefix, str_bineta)+suffix, '', 200, 0, 200, 100, 0, 2), 'denominator_pt', 'response')
        histos[prefix+str_bineta+'_ResponseVsRunNb'+suffix] = df_etarange.Histo2D(ROOT.RDF.TH2DModel('h_ResponseVsRunNb_{}_{}'.format(prefix, str_bineta)+suffix, '', len(runnb_bins)-1, runnb_bins, len(response_bins)-1, response_bins), 'runnb', 'response')

        if i ==1 and prefix == 'EGNonIso_plots':
            df_etarange = df_etarange.Filter(stringToPrint)

            
        #Numerator/denominator for plateau eff vs runnb
        df_etarange = df_etarange.Define('inplateau','{}>={}&&inEtaRange'.format(ptvarname,offlinethresholdforeffvsrunnb))
        df_etarange = df_etarange.Define('N_inplateau','Sum(inplateau)')
        df_etarange = df_etarange.Define('runnb_inplateau',"return ROOT::VecOps::RVec<int>(N_inplateau, _runNb);")
        df_etarange = df_etarange.Define('inplateaupassL1','inplateau && {}>={}'.format(l1varname,l1thresholdforeffvsrunnb))
        df_etarange = df_etarange.Define('N_inplateaupassL1','Sum(inplateaupassL1)')
        df_etarange = df_etarange.Define('runnb_inplateaupassL1',"return ROOT::VecOps::RVec<int>(N_inplateaupassL1, _runNb);")
        histos[prefix+"_plateaueffvsrunnb_numerator_"+str_bineta+suffix] = df_etarange.Histo1D(ROOT.RDF.TH1DModel('h_PlateauEffVsRunNb_Numerator_{}_{}'.format(prefix, str_bineta)+suffix, '', len(runnb_bins)-1, runnb_bins),'runnb_inplateaupassL1')
        histos[prefix+"_plateaueffvsrunnb_denominator_"+str_bineta+suffix] = df_etarange.Histo1D(ROOT.RDF.TH1DModel('h_PlateauEffVsRunNb_Denominator_{}_{}'.format(prefix, str_bineta)+suffix, '', len(runnb_bins)-1, runnb_bins),'runnb_inplateau')

        for ipt in l1thresholds:
            str_binetapt = "eta{}to{}_l1thrgeq{}".format(etabins[i], etabins[i+1],ipt).replace(".","p")
            df_loc = df_etarange.Define('passL1Cond','{}>={}'.format(l1varname, ipt))
            df_loc = df_loc.Define('numerator_pt',ptvarname+'[inEtaRange&&passL1Cond]')
            histos[prefix+str_binetapt+suffix] = df_loc.Histo1D(ROOT.RDF.TH1DModel('h_{}_{}'.format(prefix, str_binetapt)+suffix, '', len(binning)-1, binning), 'numerator_pt')


    return df

    

def ZEE_Plots(df, suffix = ''):
    histos = {}
    
    label = ['EGNonIso','EGLooseIso', 'EGTightIso']
    df_eg = [None, None, None]
    for i in range(3): 
        
        if i ==0:
            df_eg[i] = df.Define('probe_idxL1jet','FindL1ObjIdx(_L1eg_eta, _L1eg_phi, probe_Eta, probe_Phi)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bx0','FindL1ObjIdx_setBx(_L1eg_eta, _L1eg_phi, _L1eg_bx, probe_Eta, probe_Phi, 0)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bxmin1','FindL1ObjIdx_setBx(_L1eg_eta, _L1eg_phi, _L1eg_bx, probe_Eta, probe_Phi, -1)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bxplus1','FindL1ObjIdx_setBx(_L1eg_eta, _L1eg_phi, _L1eg_bx, probe_Eta, probe_Phi, 1)')
        if i ==1:
            df_eg[i] = df.Define('probe_idxL1jet','FindL1ObjIdx(_L1eg_eta, _L1eg_phi, probe_Eta, probe_Phi, _L1eg_iso, 2)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bx0','FindL1ObjIdx_setBx(_L1eg_eta, _L1eg_phi, _L1eg_bx, probe_Eta, probe_Phi, 0, _L1eg_iso, 2)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bxmin1','FindL1ObjIdx_setBx(_L1eg_eta, _L1eg_phi, _L1eg_bx, probe_Eta, probe_Phi, -1, _L1eg_iso, 2)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bxplus1','FindL1ObjIdx_setBx(_L1eg_eta, _L1eg_phi, _L1eg_bx, probe_Eta, probe_Phi, 1, _L1eg_iso, 2)')
        if i ==2:
            df_eg[i] = df.Define('probe_idxL1jet','FindL1ObjIdx(_L1eg_eta, _L1eg_phi, probe_Eta, probe_Phi, _L1eg_iso, 3)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bx0','FindL1ObjIdx_setBx(_L1eg_eta, _L1eg_phi, _L1eg_bx, probe_Eta, probe_Phi, 0, _L1eg_iso, 3)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bxmin1','FindL1ObjIdx_setBx(_L1eg_eta, _L1eg_phi, _L1eg_bx, probe_Eta, probe_Phi, -1, _L1eg_iso, 3)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bxplus1','FindL1ObjIdx_setBx(_L1eg_eta, _L1eg_phi, _L1eg_bx, probe_Eta, probe_Phi, 1, _L1eg_iso, 3)')

        df_eg[i] = df_eg[i].Define('probe_L1Pt','GetVal(probe_idxL1jet, _L1eg_pt)')
        df_eg[i] = df_eg[i].Define('probe_L1Bx','GetVal(probe_idxL1jet, _L1eg_bx)')
        df_eg[i] = df_eg[i].Define('probe_L1PtoverRecoPt','probe_L1Pt/probe_Pt')

        df_eg[i] = df_eg[i].Define('probe_L1Pt_Bx0', 'GetVal(probe_idxL1jet_Bx0, _L1eg_pt)')
        df_eg[i] = df_eg[i].Define('probe_L1Pt_Bxmin1', 'GetVal(probe_idxL1jet_Bxmin1, _L1eg_pt)')
        df_eg[i] = df_eg[i].Define('probe_L1Pt_Bxplus1', 'GetVal(probe_idxL1jet_Bxplus1, _L1eg_pt)')

        pt_binning = leptonpt_bins
        if suffix != '':
            pt_binning = coarse_leptonpt_bins
        
        df_eg[i] = makehistosforturnons_inprobeetaranges(df_eg[i], histos, etavarname='probe_Eta', phivarname='probe_Phi', ptvarname='probe_Pt', responsevarname='probe_L1PtoverRecoPt', etabins=egEtaBins, l1varname='probe_L1Pt', l1thresholds=[5,10,15,20,25,30,36,37], prefix=label[i]+"_plots", binning=pt_binning, l1thresholdforeffvsrunnb = 30, offlinethresholdforeffvsrunnb = 35, suffix = suffix)
        
        
        df_eg[i] = df_eg[i].Define('probePt30_Eta','probe_Eta[probe_Pt>30]')
        df_eg[i] = df_eg[i].Define('probePt30_Phi','probe_Phi[probe_Pt>30]')
        df_eg[i] = df_eg[i].Define('probePt30PassL1EG25_Eta','probe_Eta[probe_Pt>30&&probe_L1Pt>25]')
        df_eg[i] = df_eg[i].Define('probePt30PassL1EG25_Phi','probe_Phi[probe_Pt>30&&probe_L1Pt>25]')
        histos['h_EG25_EtaPhi_Numerator'+label[i]+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('h_EG25_EtaPhi_Numerator'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probePt30PassL1EG25_Eta', 'probePt30PassL1EG25_Phi')
        histos['h_EG25_EtaPhi_Denominator'+label[i]+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('h_EG25_EtaPhi_Denominator'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probePt30_Eta', 'probePt30_Phi')

        
        if i ==0:
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bxmin1_Eta', 'probe_Eta[probe_Pt>12&&probe_Pt<23&&probe_L1Pt_Bxmin1>15&&probe_L1Pt_Bxmin1<=26&&probe_L1Bx==-1]')
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bxmin1_Phi', 'probe_Phi[probe_Pt>12&&probe_Pt<23&&probe_L1Pt_Bxmin1>15&&probe_L1Pt_Bxmin1<=26&&probe_L1Bx==-1]')
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bx0_Eta', 'probe_Eta[probe_Pt>12&&probe_Pt<23&&probe_L1Pt_Bx0>15&&probe_L1Pt_Bx0<=26&&probe_L1Bx==0]')
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bx0_Phi', 'probe_Phi[probe_Pt>12&&probe_Pt<23&&probe_L1Pt_Bx0>15&&probe_L1Pt_Bx0<=26&&probe_L1Bx==0]')
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bxplus1_Eta', 'probe_Eta[probe_Pt>12&&probe_Pt<23&&probe_L1Pt_Bxplus1>15&&probe_L1Pt_Bxplus1<=26&&probe_L1Bx==1]')
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bxplus1_Phi', 'probe_Phi[probe_Pt>12&&probe_Pt<23&&probe_L1Pt_Bxplus1>15&&probe_L1Pt_Bxplus1<=26&&probe_L1Bx==1]')
            
            
            histos['L1EG15to26_bxmin1_etaphi'+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('L1EG15to26_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1EG15to26Bxmin1_Eta', 'probeL1EG15to26Bxmin1_Phi')
            histos['L1EG15to26_bx0_etaphi'+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('L1EG15to26_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1EG15to26Bx0_Eta', 'probeL1EG15to26Bx0_Phi')
            histos['L1EG15to26_bxplus1_etaphi'+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('L1EG15to26_bxplus1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1EG15to26Bxplus1_Eta', 'probeL1EG15to26Bxplus1_Phi')

            histos['L1EG15to26_bxmin1_eta'+suffix] = df_eg[i].Histo1D(ROOT.RDF.TH1DModel('L1EG15to26_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1EG15to26Bxmin1_Eta')
            histos['L1EG15to26_bx0_eta'+suffix] = df_eg[i].Histo1D(ROOT.RDF.TH1DModel('L1EG15to26_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1EG15to26Bx0_Eta')
            histos['L1EG15to26_bxplus1_eta'+suffix] = df_eg[i].Histo1D(ROOT.RDF.TH1DModel('L1EG15to26_bxplus1_eta'+suffix, '', 100, -5, 5), 'probeL1EG15to26Bxplus1_Eta')

    return df, histos
    


def ZMuMu_Plots(df, suffix = ''):

    #df = df.Define('L1_FirstBunchInTrain', 'passL1_Initial_bx0[473]')
    #df = df.Filter('L1_FirstBunchInTrain')
                                                                                          
    histos = {}
    label = ['AllQual', 'Qual8', 'Qual12']
    df_mu = [None, None, None]
    
    for i in range(3):
        if i == 0:
            df_mu[i] = df.Define('probe_idxL1jet','FindL1MuIdx(_L1mu_eta, _L1mu_phi, probe_Eta, probe_Phi, probe_Pt, _L1mu_charge)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bx0','FindL1MuIdx_setBx(_L1mu_eta, _L1mu_phi, _L1mu_bx, probe_Eta, probe_Phi, probe_Pt, _L1mu_charge, 0)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bxmin1','FindL1MuIdx_setBx(_L1mu_eta, _L1mu_phi, _L1mu_bx, probe_Eta, probe_Phi, probe_Pt, _L1mu_charge, -1)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bxplus1','FindL1MuIdx_setBx(_L1mu_eta, _L1mu_phi, _L1mu_bx, probe_Eta, probe_Phi, probe_Pt, _L1mu_charge, 1)')
        if i == 1:
            df_mu[i] = df.Define('probe_idxL1jet','FindL1MuIdx(_L1mu_eta, _L1mu_phi, probe_Eta, probe_Phi, probe_Pt, _L1mu_charge, _L1mu_Qual, 8)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bx0','FindL1MuIdx_setBx(_L1mu_eta, _L1mu_phi, _L1mu_bx, probe_Eta, probe_Phi, probe_Pt, _L1mu_charge, 0, _L1mu_Qual, 8)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bxmin1','FindL1MuIdx_setBx(_L1mu_eta, _L1mu_phi, _L1mu_bx, probe_Eta, probe_Phi, probe_Pt, _L1mu_charge, -1, _L1mu_Qual, 8)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bxplus1','FindL1MuIdx_setBx(_L1mu_eta, _L1mu_phi, _L1mu_bx, probe_Eta, probe_Phi, probe_Pt, _L1mu_charge, 1, _L1mu_Qual, 8)')
        if i == 2:
            df_mu[i] = df.Define('probe_idxL1jet','FindL1MuIdx(_L1mu_eta, _L1mu_phi, probe_Eta, probe_Phi, probe_Pt, _L1mu_charge, _L1mu_Qual, 12)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bx0','FindL1MuIdx_setBx(_L1mu_eta, _L1mu_phi, _L1mu_bx, probe_Eta, probe_Phi, probe_Pt, _L1mu_charge, 0, _L1mu_Qual, 12)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bxmin1','FindL1MuIdx_setBx(_L1mu_eta, _L1mu_phi, _L1mu_bx, probe_Eta, probe_Phi, probe_Pt, _L1mu_charge, -1, _L1mu_Qual, 12)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bxplus1','FindL1MuIdx_setBx(_L1mu_eta, _L1mu_phi, _L1mu_bx, probe_Eta, probe_Phi, probe_Pt, _L1mu_charge, 1, _L1mu_Qual, 12)')

            

        df_mu[i] = df_mu[i].Define('probe_L1Pt','GetVal(probe_idxL1jet, _L1mu_pt)')
        df_mu[i] = df_mu[i].Define('probe_L1Bx','GetVal(probe_idxL1jet, _L1mu_bx)')
        df_mu[i] = df_mu[i].Define('probe_L1Qual','GetVal(probe_idxL1jet, _L1mu_Qual)')

        df_mu[i] = df_mu[i].Define('probe_L1Pt_Bx0', 'GetVal(probe_idxL1jet_Bx0, _L1mu_pt)')
        df_mu[i] = df_mu[i].Define('probe_L1Qual_Bx0', 'GetVal(probe_idxL1jet_Bx0, _L1mu_Qual)')

        df_mu[i] = df_mu[i].Define('probe_L1Pt_Bxmin1', 'GetVal(probe_idxL1jet_Bxmin1, _L1mu_pt)')
        df_mu[i] = df_mu[i].Define('probe_L1Qual_Bxmin1', 'GetVal(probe_idxL1jet_Bxmin1, _L1mu_Qual)')

        df_mu[i] = df_mu[i].Define('probe_L1Pt_Bxplus1', 'GetVal(probe_idxL1jet_Bxplus1, _L1mu_pt)')
        df_mu[i] = df_mu[i].Define('probe_L1Qual_Bxplus1', 'GetVal(probe_idxL1jet_Bxplus1, _L1mu_Qual)')

        df_mu[i] = df_mu[i].Define('probe_L1PtoverRecoPt','probe_L1Pt/probe_Pt')
        
        
        pt_binning = leptonpt_bins
        if suffix != '':
            pt_binning = coarse_leptonpt_bins


        df_mu[i] = makehistosforturnons_inprobeetaranges(df_mu[i], histos, etavarname='probe_Eta', phivarname='probe_Phi', ptvarname='probe_Pt', responsevarname='probe_L1PtoverRecoPt', etabins=muEtaBins, l1varname='probe_L1Pt', l1thresholds=[3, 5,10,15,20,22,26],  prefix=label[i]+"_plots" , binning = pt_binning, l1thresholdforeffvsrunnb = 22, offlinethresholdforeffvsrunnb = 27, suffix = suffix)
        
        # Same plots, with smaller bins in EMTF
        df_mu[i] = makehistosforturnons_inprobeetaranges(df_mu[i], histos, etavarname='probe_Eta', phivarname='probe_Phi', ptvarname='probe_Pt', responsevarname='probe_L1PtoverRecoPt', etabins=muEMTFBins, l1varname='probe_L1Pt', l1thresholds=[3, 5,10,15,20,22,26],  prefix=label[i]+"_plots" , binning = pt_binning, l1thresholdforeffvsrunnb = 22, offlinethresholdforeffvsrunnb = 27, suffix = suffix)
    
        df_mu[i] = df_mu[i].Define('probePt30_Eta','probe_Eta[probe_Pt>30]')
        df_mu[i] = df_mu[i].Define('probePt30_Phi','probe_Phi[probe_Pt>30]')
        df_mu[i] = df_mu[i].Define('probePt30PassL1Mu22_Eta','probe_Eta[probe_Pt>30&&probe_L1Pt>22]')
        df_mu[i] = df_mu[i].Define('probePt30PassL1Mu22_Phi','probe_Phi[probe_Pt>30&&probe_L1Pt>22]')
        df_mu[i] = df_mu[i].Define('probePt30PassL1Mu22_L1Bx','probe_L1Bx[probe_Pt>30&&probe_L1Pt>22]')

        histos['h_Mu22_EtaPhi_Denominator'+label[i]+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('h_Mu22_EtaPhi_Denominator'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probePt30_Eta', 'probePt30_Phi')
        histos['h_Mu22_EtaPhi_Numerator'+label[i]+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('h_Mu22_EtaPhi_Numerator'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probePt30PassL1Mu22_Eta', 'probePt30PassL1Mu22_Phi')
        
        
        if i == 2:
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bxmin1_Eta', 'probe_Eta[probe_Pt>8&&probe_Pt<25&&probe_L1Pt_Bxmin1>10&&probe_L1Pt_Bxmin1<=21&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bxmin1_Phi', 'probe_Phi[probe_Pt>8&&probe_Pt<25&&probe_L1Pt_Bxmin1>10&&probe_L1Pt_Bxmin1<=21&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bx0_Eta', 'probe_Eta[probe_Pt>8&&probe_Pt<25&&probe_L1Pt_Bx0>10&&probe_L1Pt_Bx0<=21&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bx0_Phi', 'probe_Phi[probe_Pt>8&&probe_Pt<25&&probe_L1Pt_Bx0>10&&probe_L1Pt_Bx0<=21&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bxplus1_Eta', 'probe_Eta[probe_Pt>8&&probe_Pt<25&&probe_L1Pt_Bxplus1>10&&probe_L1Pt_Bxplus1<=21&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bxplus1_Phi', 'probe_Phi[probe_Pt>8&&probe_Pt<25&&probe_L1Pt_Bxplus1>10&&probe_L1Pt_Bxplus1<=21&&probe_L1Qual>=12]')
            
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bxmin1_Eta', 'probe_Eta[probe_Pt>20&&probe_L1Pt_Bxmin1>22&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bxmin1_Phi', 'probe_Phi[probe_Pt>20&&probe_L1Pt_Bxmin1>22&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bx0_Eta', 'probe_Eta[probe_Pt>20&&probe_L1Pt_Bx0>22&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bx0_Phi', 'probe_Phi[probe_Pt>20&&probe_L1Pt_Bx0>22&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bxplus1_Eta', 'probe_Eta[probe_Pt>20&&probe_L1Pt_Bxplus1>22&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bxplus1_Phi', 'probe_Phi[probe_Pt>20&&probe_L1Pt_Bxplus1>22&&probe_L1Qual>=12]')

                        
            histos['L1Mu10to21_bxmin1_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu10to21_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu10to21Bxmin1_Eta', 'probeL1Mu10to21Bxmin1_Phi')
            histos['L1Mu10to21_bx0_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu10to21_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu10to21Bx0_Eta', 'probeL1Mu10to21Bx0_Phi')
            histos['L1Mu10to21_bxplus1_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu10to21_bxplus1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu10to21Bxplus1_Eta', 'probeL1Mu10to21Bxplus1_Phi')

            histos['L1Mu10to21_bxmin1_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu10to21_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu10to21Bxmin1_Eta')
            histos['L1Mu10to21_bx0_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu10to21_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Mu10to21Bx0_Eta')
            histos['L1Mu10to21_bxplus1_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu10to21_bxplus1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu10to21Bxplus1_Eta')

            ###

            histos['L1Mu22_bxplus1_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu22_bxplus1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bxplus1_Eta', 'probeL1Mu22Bxplus1_Phi')
            histos['L1Mu22_bx0_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu22_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bx0_Eta', 'probeL1Mu22Bx0_Phi')

            histos['L1Mu22_bxplus1_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu22_bxplus1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bxplus1_Eta')
            histos['L1Mu22_bx0_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu22_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bx0_Eta') 

            #

            histos['L1Mu22_IsUnprefireable_bx0_etaphi'+suffix] = df_mu[i].Filter("Flag_IsUnprefirable").Histo2D(ROOT.RDF.TH2DModel('L1Mu22_IsUnprefireable_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bx0_Eta', 'probeL1Mu22Bx0_Phi')
            histos['L1Mu22_IsUnprefireable_bx0_eta'+suffix] = df_mu[i].Filter("Flag_IsUnprefirable").Histo1D(ROOT.RDF.TH1DModel('L1Mu22_IsUnprefireable_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bx0_Eta') 

            histos['L1Mu22_IsUnprefireable_bxmin1_etaphi'+suffix] = df_mu[i].Filter("Flag_IsUnprefirable").Histo2D(ROOT.RDF.TH2DModel('L1Mu22_IsUnprefireable_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bxmin1_Eta', 'probeL1Mu22Bxmin1_Phi')
            histos['L1Mu22_IsUnprefireable_bxmin1_eta'+suffix] = df_mu[i].Filter("Flag_IsUnprefirable").Histo1D(ROOT.RDF.TH1DModel('L1Mu22_IsUnprefireable_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bxmin1_Eta') 

            #

            histos['L1Mu22_FirstBunchInTrain_bx0_etaphi'+suffix] = df_mu[i].Filter("passL1_Final_bxmin1[472]").Histo2D(ROOT.RDF.TH2DModel('L1Mu22_FirstBunchInTrain_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bx0_Eta', 'probeL1Mu22Bx0_Phi')
            histos['L1Mu22_FirstBunchInTrain_bx0_eta'+suffix] = df_mu[i].Filter("passL1_Final_bxmin1[472]").Histo1D(ROOT.RDF.TH1DModel('L1Mu22_FirstBunchInTrain_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bx0_Eta') 

            histos['L1Mu22_FirstBunchInTrain_bxmin1_etaphi'+suffix] = df_mu[i].Filter("passL1_Final_bxmin1[472]").Histo2D(ROOT.RDF.TH2DModel('L1Mu22_FirstBunchInTrain_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bxmin1_Eta', 'probeL1Mu22Bxmin1_Phi')

            histos['L1Mu22_FirstBunchInTrain_bxmin1_eta'+suffix] = df_mu[i].Filter("passL1_Final_bxmin1[472]").Histo1D(ROOT.RDF.TH1DModel('L1Mu22_FirstBunchInTrain_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bxmin1_Eta') 

            ###

            #histos['L1Mu22_bxmin1_eta_noflag'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu22_bxmin1_eta_noflag'+suffix, '', 100, -5, 5), 'probeL1Mu22Bxmin1_Eta')
            #histos['L1Mu22_bx0_eta_noflag'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu22_bx0_eta_noflag'+suffix, '', 100, -5, 5), 'probeL1Mu22Bx0_Eta')
            #histos['L1Mu22_bxplus1_eta_noflag'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu22_bxplus1_eta_noflag'+suffix, '', 100, -5, 5), 'probeL1Mu22Bxplus1_Eta')

            '''
            #L1 prefiring measurement with unprefirable events
            
            #First find if there's a L1 mu in bx -1 and store its index
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_inbxmin1','FindL1ObjBxMin1Idx(_L1mu_eta, _L1mu_phi, probe_Eta, probe_Phi, _L1mu_Qual, 12)')
            df_mu[i] = df_mu[i].Define('probe_L1Pt_inbxmin1','GetVal(probe_idxL1jet, _L1mu_pt)')
            df_mu[i] = df_mu[i].Define('probeEta_L1Mu22_inbxmin1','probe_Eta[probe_Pt>30&&probe_L1Pt_inbxmin1>22]')
            df_mu[i] = df_mu[i].Define('probePhi_L1Mu22_inbxmin1','probe_Phi[probe_Pt>30&&probe_L1Pt_inbxmin1>22]')

            #Next lines are still WIP
            histos['L1Mu22_denforPrefiring_etaphi'] = df_mu[i].Filter('Flag_IsUnprefirable').Histo2D(ROOT.RDF.TH2DModel('', '', 100, -5,5, 100, -3.1416, 3.1416), 'probePt30PassL1Mu22_Eta', 'probePt30PassL1Mu22_Phi')
            histos['L1Mu22_numforPrefiring_etaphi'] = df_mu[i].Filter('Flag_IsUnprefirable').Histo2D(ROOT.RDF.TH2DModel('', '', 100, -5,5, 100, -3.1416, 3.1416), 'probeEta_L1Mu22_inbxmin1', 'probePhi_L1Mu22_inbxmin1')
            '''



    return df, histos
    




def CleanJets(df):
    #List of cleaned jets (noise cleaning + lepton/photon overlap removal)
    
    #df = df.Define('isCleanJet','_puppijetPassID&&_puppijetLeptonPhotonCleaned&&_puppijetPt>30')
    df = df.Define('isCleanJet','IsCleanJet(_puppijetPt, _puppijetEta, _puppijetPhi, _lPt, _lEta, _lPhi, _lPassVetoID,  _phPt, _phEta, _phPhi, _phPassIso)')
    #df = df.Define('isCleanJet','_puppijetPassID&&_puppijetPt>30')
    df = df.Define('cleanJet_Pt','_puppijetPt[isCleanJet]')
    df = df.Define('cleanJet_Eta','_puppijetEta[isCleanJet]')
    df = df.Define('cleanJet_Phi','_puppijetPhi[isCleanJet]')

    '''
    df = df.Define('isCleanJet','_jetPassID&&_jetLeptonPhotonCleaned&&_jetPt>30&&_jet_MUEF<0.5&&_jet_CEEF<0.5')
    df = df.Define('cleanJet_Pt','_jetPt[isCleanJet]')
    df = df.Define('cleanJet_Eta','_jetEta[isCleanJet]')
    df = df.Define('cleanJet_Phi','_jetPhi[isCleanJet]')
    df = df.Define('cleanJet_NHEF','_jet_NHEF[isCleanJet]')
    df = df.Define('cleanJet_NEEF','_jet_NEEF[isCleanJet]')
    df = df.Define('cleanJet_CHEF','_jet_CHEF[isCleanJet]')
    df = df.Define('cleanJet_CEEF','_jet_CEEF[isCleanJet]')
    df = df.Define('cleanJet_MUEF','_jet_MUEF[isCleanJet]')
    #df = df.Filter(stringToPrintJets)
    '''
    df = df.Filter('Sum(isCleanJet)>=1','>=1 clean jet with p_{T}>30 GeV')

    return df



def EtSum(df, suffix = ''):
    histos = {}
    #HT=scalar pt sum of all jets with pt>30 and |eta|<2.5 
    df = df.Define('iscentraljet','cleanJet_Pt>30&&abs(cleanJet_Eta)<2.5')
    #df = df.Filter('Sum(iscentraljet)>0')
    df = df.Define('HT','Sum(cleanJet_Pt[cleanJet_Pt>30&&abs(cleanJet_Eta)<2.5])')

    df = df.Define('muons_px','Sum(_lPt[abs(_lpdgId)==13]*cos(_lPhi[abs(_lpdgId)==13]))')
    df = df.Define('muons_py','Sum(_lPt[abs(_lpdgId)==13]*sin(_lPhi[abs(_lpdgId)==13]))')
    df = df.Define('metnomu_x','_met*cos(_met_phi)+muons_px')
    df = df.Define('metnomu_y','_met*sin(_met_phi)+muons_py')
    df = df.Define('MetNoMu','sqrt(metnomu_x*metnomu_x+metnomu_y*metnomu_y)')
    df = df.Define('L1_ETMHF65','_L1etsum_etmhf[2]>=65')
    df = df.Define('L1_ETMHF80','passL1_Initial_bx0[419]')
    df = df.Define('L1_ETMHF90','passL1_Initial_bx0[420]')
    df = df.Define('L1_ETMHF100','passL1_Initial_bx0[421]')
    df = df.Define('L1_ETMHF110','passL1_Initial_bx0[422]')
    
    df = df.Define("mhthf","L1MHTHF(_L1jet_pt, _L1jet_eta, _L1jet_phi, _L1jet_bx)[0]")
    df = df.Define("passL1_MHTHF100","mhthf>=100")
    df = df.Define("passL1_MHTHF110","mhthf>=110")
    df = df.Define("passL1_MHTHF120","mhthf>=120")
    df = df.Define("passL1_MHTHF130","mhthf>=130")
    df = df.Define("passL1_MHTHF140","mhthf>=140")
    df = df.Define("passL1_MHTHF150","mhthf>=150")


    # Dijet selections
    df = df.Define('hastwocleanjets', 'PassDiJet80_40_Mjj500(cleanJet_Pt, cleanJet_Eta, cleanJet_Phi)')
    df = df.Define('vbf_selection', 'PassDiJet140_70_Mjj900(cleanJet_Pt, cleanJet_Eta, cleanJet_Phi)')
    df = df.Define('hastwocentraljets', 'PassDiJet80_40_Mjj500_central(cleanJet_Pt, cleanJet_Eta, cleanJet_Phi)')
    df = df.Define('hastwoHFjets', 'PassDiJet80_40_Mjj500_HF(cleanJet_Pt, cleanJet_Eta, cleanJet_Phi)')

    histos['h_MetNoMu_Denominator'+suffix] = df.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_Denominator'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu') 
    
    
    dfmetl1 = df.Filter('L1_ETMHF65')
    histos['L1_ETMHF65'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF65'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dfmetl1 = df.Filter('passL1_Initial_bx0[419]')
    histos['L1_ETMHF80'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF80'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dfmetl1 = df.Filter('passL1_Initial_bx0[420]')
    histos['L1_ETMHF90'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF90'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dfmetl1 = df.Filter('passL1_Initial_bx0[421]')
    histos['L1_ETMHF100'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF100'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dfmetl1 = df.Filter('passL1_Initial_bx0[422]')
    histos['L1_ETMHF110'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF110'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')

    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight'+suffix] =  df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60'+suffix] =  df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    

    histos['h_HT_Denominator'+suffix] = df.Filter('_met<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_Denominator'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT') 
    histos['L1_HTT200er'+suffix] = df.Filter('passL1_Initial_bx0[400]').Filter('_met<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_L1_HTT200er'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT')  
    histos['L1_HTT280er'+suffix] = df.Filter('passL1_Initial_bx0[402]').Filter('_met<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_L1_HTT280er'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT')
    histos['L1_HTT360er'+suffix] = df.Filter('passL1_Initial_bx0[404]').Filter('_met<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_L1_HTT360er'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT')
    histos['HLT_PFHT1050'+suffix] =  df.Filter('HLT_PFHT1050').Filter('_met<50').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFHT1050'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT')


    dfmhthfl1 = df.Filter('passL1_MHTHF100')
    histos['L1_MHTHF100'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_MHTHF100'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dfmhthfl1 = df.Filter('passL1_MHTHF110')
    histos['L1_MHTHF110'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_MHTHF110'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dfmhthfl1 = df.Filter('passL1_MHTHF120')
    histos['L1_MHTHF120'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_MHTHF120'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dfmhthfl1 = df.Filter('passL1_MHTHF130')
    histos['L1_MHTHF130'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_MHTHF130'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dFmhthfl1 = df.Filter('passL1_MHTHF140')
    histos['L1_MHTHF140'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_MHTHF140'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dfmhthfl1 = df.Filter('passL1_MHTHF150')
    histos['L1_MHTHF150'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_MHTHF150'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')


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

    return df, histos

def AnalyzeCleanJets(df, JetRecoPtCut, L1JetPtCut, suffix = ''):    
    histos = {}
    #Find L1 jets matched to the offline jet
    #df = df.Define('cleanJet_idxL1jet','FindL1ObjIdx(_L1jet_eta, _L1jet_phi, cleanJet_Eta, cleanJet_Phi)')
    # only take jets in bx 0
    df = df.Define('cleanJet_idxL1jetbx0', 'FindL1ObjIdx_setBx(_L1jet_eta, _L1jet_phi, _L1jet_bx, cleanJet_Eta, cleanJet_Phi, 0)')
    #Select L1 jets in bx+/-1
    df = df.Define('cleanJet_idxL1jetbxmin1', 'FindL1ObjIdx_setBx(_L1jet_eta, _L1jet_phi, _L1jet_bx, cleanJet_Eta, cleanJet_Phi, -1)')
    df = df.Define('cleanJet_idxL1jetbx1', 'FindL1ObjIdx_setBx(_L1jet_eta, _L1jet_phi, _L1jet_bx, cleanJet_Eta, cleanJet_Phi, 1)')
    
    
    df = df.Define('cleanJet_L1Pt','GetVal(cleanJet_idxL1jetbx0,_L1jet_pt)')
    df = df.Define('cleanJet_L1PtoverRecoPt','cleanJet_L1Pt/cleanJet_Pt')

    df = df.Define('cleanJet_L1Ptbxmin1','GetVal(cleanJet_idxL1jetbxmin1,_L1jet_pt)')
    df = df.Define('cleanJet_L1Ptbx1','GetVal(cleanJet_idxL1jetbx1,_L1jet_pt)')
    #df = df.Filter(stringFailingJets)
    ##Now some plotting (turn ons for now)
    L1PtCuts = [30., 40., 60., 80., 100., 120., 140., 160., 170., 180., 200.]
    

    df = makehistosforturnons_inprobeetaranges(df, histos, etavarname='cleanJet_Eta', phivarname='cleanJet_Phi', ptvarname='cleanJet_Pt', responsevarname='cleanJet_L1PtoverRecoPt', etabins=jetEtaBins, l1varname='cleanJet_L1Pt', l1thresholds=L1PtCuts, prefix="Jet_plots", binning=jetmetpt_bins, l1thresholdforeffvsrunnb = L1JetPtCut, offlinethresholdforeffvsrunnb = JetRecoPtCut, suffix = suffix) 

    # Make same histosgrams, in a single bin of eta (abs(eta) < 5)
    df = makehistosforturnons_inprobeetaranges(df, histos, etavarname='cleanJet_Eta', phivarname='cleanJet_Phi', ptvarname='cleanJet_Pt', responsevarname='cleanJet_L1PtoverRecoPt', etabins=[0., 5.], l1varname='cleanJet_L1Pt', l1thresholds=[40., 180.], prefix="Jet_plots_eta_inclusive", binning=jetmetpt_bins, l1thresholdforeffvsrunnb = L1JetPtCut, offlinethresholdforeffvsrunnb = JetRecoPtCut, suffix = suffix) 

    
    df = df.Define('cleanHighPtJet_Eta','cleanJet_Eta[cleanJet_Pt>{}]'.format(JetRecoPtCut))
    df = df.Define('cleanHighPtJet_Phi','cleanJet_Phi[cleanJet_Pt>{}]'.format(JetRecoPtCut))
    df = df.Define('cleanHighPtJet_Eta_PassL1Jet','cleanJet_Eta[cleanJet_L1Pt>={}&&cleanJet_Pt>{}]'.format(L1JetPtCut, JetRecoPtCut))
    df = df.Define('cleanHighPtJet_Phi_PassL1Jet','cleanJet_Phi[cleanJet_L1Pt>={}&&cleanJet_Pt>{}]'.format(L1JetPtCut, JetRecoPtCut))
    
    histos["L1JetvsEtaPhi_Numerator"+suffix] = df.Histo2D(ROOT.RDF.TH2DModel('h_L1Jet{}vsEtaPhi_Numerator'.format(int(L1JetPtCut))+suffix, '', 100,-5,5,100,-3.1416,3.1416), 'cleanHighPtJet_Eta_PassL1Jet','cleanHighPtJet_Phi_PassL1Jet')
    histos["L1JetvsEtaPhi_EtaRestricted"+suffix] = df.Histo2D(ROOT.RDF.TH2DModel('h_L1Jet{}vsEtaPhi_EtaRestricted'.format(int(L1JetPtCut))+suffix, '', 100,-5,5,100,-3.1416,3.1416), 'cleanHighPtJet_Eta','cleanHighPtJet_Phi')
    
    df = df.Define('probe_cleanJet_Eta','cleanJet_Eta[cleanJet_Pt>100&&cleanJet_Pt<16000]')
    df = df.Define('probe_cleanJet_Phi','cleanJet_Phi[cleanJet_Pt>100&&cleanJet_Pt<16000]')
    df = df.Define('probe_cleanJet_Pt','cleanJet_Pt[cleanJet_Pt>100&&cleanJet_Pt<16000]')

    L1Ptjetrange = ['50', '150']
    L1Ptcut = '&&cleanJet_L1Ptbxmin1>'+L1Ptjetrange[0]+'&&cleanJet_L1Ptbxmin1<='+L1Ptjetrange[1]
    df = df.Define('probeL1Jet'+L1Ptjetrange[0]+'to'+L1Ptjetrange[1]+'Bxmin1_Eta','cleanJet_Eta[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    df = df.Define('probeL1Jet'+L1Ptjetrange[0]+'to'+L1Ptjetrange[1]+'Bxmin1_Phi','cleanJet_Phi[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    df = df.Define('probeL1Jet'+L1Ptjetrange[0]+'to'+L1Ptjetrange[1]+'Bxmin1_Pt','cleanJet_Pt[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')

    L1Ptcut = '&&cleanJet_L1Pt>'+L1Ptjetrange[0]+'&&cleanJet_L1Pt<='+L1Ptjetrange[1]
    df = df.Define('probeL1Jet'+L1Ptjetrange[0]+'to'+L1Ptjetrange[1]+'Bx0_Eta','cleanJet_Eta[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    df = df.Define('probeL1Jet'+L1Ptjetrange[0]+'to'+L1Ptjetrange[1]+'Bx0_Phi','cleanJet_Phi[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    df = df.Define('probeL1Jet'+L1Ptjetrange[0]+'to'+L1Ptjetrange[1]+'Bx0_Pt','cleanJet_Pt[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    
    L1Ptcut = '&&cleanJet_L1Ptbx1>'+L1Ptjetrange[0]+'&&cleanJet_L1Ptbx1<='+L1Ptjetrange[1]
    df = df.Define('probeL1Jet'+L1Ptjetrange[0]+'to'+L1Ptjetrange[1]+'Bxplus1_Eta','cleanJet_Eta[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    df = df.Define('probeL1Jet'+L1Ptjetrange[0]+'to'+L1Ptjetrange[1]+'Bxplus1_Phi','cleanJet_Phi[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    df = df.Define('probeL1Jet'+L1Ptjetrange[0]+'to'+L1Ptjetrange[1]+'Bxplus1_Pt','cleanJet_Pt[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')    


    L1Ptcut = '&&cleanJet_L1Ptbxmin1>180'
    df = df.Define('probeL1Jet180Bxmin1_Eta','cleanJet_Eta[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    df = df.Define('probeL1Jet180Bxmin1_Phi','cleanJet_Phi[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    df = df.Define('probeL1Jet180Bxmin1_Pt','cleanJet_Pt[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')

    L1Ptcut = '&&cleanJet_L1Pt>'+L1Ptjetrange[0]+'&&cleanJet_L1Pt<='+L1Ptjetrange[1]
    df = df.Define('probeL1Jet180Bx0_Eta','cleanJet_Eta[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    df = df.Define('probeL1Jet180Bx0_Phi','cleanJet_Phi[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    df = df.Define('probeL1Jet180Bx0_Pt','cleanJet_Pt[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')

    L1Ptcut = '&&cleanJet_L1Ptbx1>'+L1Ptjetrange[0]+'&&cleanJet_L1Ptbx1<='+L1Ptjetrange[1]
    df = df.Define('probeL1Jet180Bxplus1_Eta','cleanJet_Eta[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    df = df.Define('probeL1Jet180Bxplus1_Phi','cleanJet_Phi[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    df = df.Define('probeL1Jet180Bxplus1_Pt','cleanJet_Pt[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')

    '''
    df = df.Define('probeL1Jet180Bxmin1_Eta','cleanJet_Eta[cleanJet_Pt>100&&cleanJet_Pt<160'+'&&'+L1Ptcut+'&&cleanJet_L1Bx==-1]')
    df = df.Define('probeL1Jet180Bxmin1_Phi','cleanJet_Phi[cleanJet_Pt>100&&cleanJet_Pt<160'+'&&'+L1Ptcut+'&&cleanJet_L1Bx==-1]')
    df = df.Define('probeL1Jet180Bx0_Eta','cleanJet_Eta[cleanJet_Pt>100&&cleanJet_Pt<160'+'&&'+L1Ptcut+'&&cleanJet_L1Bx==0]')
    df = df.Define('probeL1Jet180Bx0_Phi','cleanJet_Phi[cleanJet_Pt>100&&cleanJet_Pt<160'+'&&'+L1Ptcut+'&&cleanJet_L1Bx==0]')
    df = df.Define('probeL1Jet180Bxplus1_Eta','cleanJet_Eta[cleanJet_Pt>100&&cleanJet_Pt<160'+'&&'+L1Ptcut+'&&cleanJet_L1Bx==1]')
    df = df.Define('probeL1Jet180Bxplus1_Phi','cleanJet_Phi[cleanJet_Pt>100&&cleanJet_Pt<160'+'&&'+L1Ptcut+'&&cleanJet_L1Bx==1]')
    '''

    #For study of SingleJet100-150, we can use all events
    theprefix = 'L1Jet'+L1Ptjetrange[0]+'to'+L1Ptjetrange[1]
    probejetprefix = 'probeL1Jet'+L1Ptjetrange[0]+'to'+L1Ptjetrange[1]
    histos['AllEvts_probe_cleanJet_etaphi'+suffix] = df.Histo2D(ROOT.RDF.TH2DModel('AllEvts_probe_cleanJet_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probe_cleanJet_Eta', 'probe_cleanJet_Phi')
    histos[theprefix+'_bxmin1_etaphi'+suffix] = df.Histo2D(ROOT.RDF.TH2DModel(theprefix+'_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), probejetprefix+'Bxmin1_Eta', probejetprefix+'Bxmin1_Phi')
    histos[theprefix+'_bx0_etaphi'+suffix] = df.Histo2D(ROOT.RDF.TH2DModel(theprefix+'_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), probejetprefix+'Bx0_Eta', probejetprefix+'Bx0_Phi')
    histos[theprefix+'_bxplus1_etaphi'+suffix] = df.Histo2D(ROOT.RDF.TH2DModel(theprefix+'_bxplus1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), probejetprefix+'Bxplus1_Eta', probejetprefix+'Bxplus1_Phi')

    histos['AllEvts_probe_cleanJet_eta'+suffix] = df.Histo1D(ROOT.RDF.TH1DModel('AllEvts_probe_cleanJet_eta'+suffix, '', 100, -5, 5), 'probe_cleanJet_Eta')
    histos[theprefix+'_bxmin1_eta'+suffix] = df.Histo1D(ROOT.RDF.TH1DModel(theprefix+'_bxmin1_eta'+suffix, '', 100, -5, 5), probejetprefix+'Bxmin1_Eta')
    histos[theprefix+'_bx0_eta'+suffix] = df.Histo1D(ROOT.RDF.TH1DModel(theprefix+'_bx0_eta'+suffix, '', 100, -5, 5), probejetprefix+'Bx0_Eta')
    histos[theprefix+'_bxplus1_eta'+suffix] = df.Histo1D(ROOT.RDF.TH1DModel(theprefix+'_bxplus1_eta'+suffix, '', 100, -5, 5), probejetprefix+'Bxplus1_Eta')
    
    histos['AllEvts_probe_cleanJet_etapt'+suffix] = df.Histo2D(ROOT.RDF.TH2DModel('AllEvts_probe_cleanJet_etapt'+suffix, '', 100, -5,5, len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'probe_cleanJet_Eta', 'probe_cleanJet_Pt')
    histos[theprefix+'_bxmin1_etapt'+suffix] = df.Histo2D(ROOT.RDF.TH2DModel(theprefix+'_bxmin1_etapt'+suffix, '', 100, -5,5, len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), probejetprefix+'Bxmin1_Eta', probejetprefix+'Bxmin1_Pt')
    histos[theprefix+'_bx0_etapt'+suffix] = df.Histo2D(ROOT.RDF.TH2DModel(theprefix+'_bx0_etapt'+suffix, '', 100, -5,5, len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), probejetprefix+'Bx0_Eta', probejetprefix+'Bx0_Pt')
    histos[theprefix+'_bxplus1_etapt'+suffix] = df.Histo2D(ROOT.RDF.TH2DModel(theprefix+'_bxplus1_etapt'+suffix, '', 100, -5,5, len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), probejetprefix+'Bxplus1_Eta', probejetprefix+'Bxplus1_Pt')



    #For study of SingleJet180, we need unprefirable events only 
    filterunprefevents = 'passL1_Final_bxmin1[472]||Flag_IsUnprefirable'
    df_unpref = df.Filter(filterunprefevents)
    #Add a global denominator (no matching condition to a L1 jet)
    histos['Unpref_probe_cleanJet_etaphi'+suffix] = df_unpref.Histo2D(ROOT.RDF.TH2DModel('Unpref_probe_cleanJet_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probe_cleanJet_Eta', 'probe_cleanJet_Phi')
    histos['L1Jet180_bxmin1_etaphi'+suffix] = df_unpref.Histo2D(ROOT.RDF.TH2DModel('L1Jet180_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Jet180Bxmin1_Eta', 'probeL1Jet180Bxmin1_Phi')
    histos['L1Jet180_bx0_etaphi'+suffix] = df_unpref.Histo2D(ROOT.RDF.TH2DModel('L1Jet180_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Jet180Bx0_Eta', 'probeL1Jet180Bx0_Phi')
    histos['L1Jet180_bxplus1_etaphi'+suffix] = df_unpref.Histo2D(ROOT.RDF.TH2DModel('L1Jet180_bxplus1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Jet180Bxplus1_Eta', 'probeL1Jet180Bxplus1_Phi')

    histos['Unpref_probe_cleanJet_eta'+suffix] = df_unpref.Histo1D(ROOT.RDF.TH1DModel('Unpref_probe_cleanJet_eta'+suffix, '', 100, -5, 5), 'probe_cleanJet_Eta')
    histos['L1Jet180_bxmin1_eta'+suffix] = df_unpref.Histo1D(ROOT.RDF.TH1DModel('L1Jet180_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1Jet180Bxmin1_Eta')
    histos['L1Jet180_bx0_eta'+suffix] = df_unpref.Histo1D(ROOT.RDF.TH1DModel('L1Jet180_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Jet180Bx0_Eta')
    histos['L1Jet180_bxplus1_eta'+suffix] = df_unpref.Histo1D(ROOT.RDF.TH1DModel('L1Jet180_bxplus1_eta'+suffix, '', 100, -5, 5), 'probeL1Jet180Bxplus1_Eta')

    histos['Unpref_probe_cleanJet_etapt'+suffix] = df_unpref.Histo2D(ROOT.RDF.TH2DModel('Unpref_probe_cleanJet_etapt'+suffix, '', 100, -5,5, len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'probe_cleanJet_Eta', 'probe_cleanJet_Pt')
    histos['L1Jet180_bxmin1_etapt'+suffix] = df_unpref.Histo2D(ROOT.RDF.TH2DModel('L1Jet180_bxmin1_etapt'+suffix, '', 100, -5,5, len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'probeL1Jet180Bxmin1_Eta', 'probeL1Jet180Bxmin1_Pt')
    histos['L1Jet180_bx0_etapt'+suffix] = df_unpref.Histo2D(ROOT.RDF.TH2DModel('L1Jet180_bx0_etapt'+suffix, '', 100, -5,5, len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'probeL1Jet180Bx0_Eta', 'probeL1Jet180Bx0_Pt')
    histos['L1Jet180_bxplus1_etapt'+suffix] = df_unpref.Histo2D(ROOT.RDF.TH2DModel('L1Jet180_bxplus1_etapt'+suffix, '', 100, -5,5, len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'probeL1Jet180Bxplus1_Eta', 'probeL1Jet180Bxplus1_Pt')



    #Now taus 

    df = df.Define('_L1isotauer2p1_eta','_L1tau_eta[abs(_L1tau_eta)<2.1&&_L1tau_iso]')
    df = df.Define('_L1isotauer2p1_pt','_L1tau_pt[abs(_L1tau_eta)<2.1&&_L1tau_iso]')
    df = df.Define('_L1isotauer2p1_phi','_L1tau_phi[abs(_L1tau_eta)<2.1&&_L1tau_iso]')
    df = df.Define('_L1isotauer2p1_bx','_L1tau_bx[abs(_L1tau_eta)<2.1&&_L1tau_iso]')

    df = df.Define('cleanJet_idxL1taubx0', 'FindL1ObjIdx_setBx(_L1isotauer2p1_eta, _L1isotauer2p1_phi, _L1isotauer2p1_bx, cleanJet_Eta, cleanJet_Phi, 0)')
    df = df.Define('cleanJet_idxL1taubxmin1', 'FindL1ObjIdx_setBx(_L1isotauer2p1_eta, _L1isotauer2p1_phi, _L1isotauer2p1_bx, cleanJet_Eta, cleanJet_Phi, -1)')
    df = df.Define('cleanJet_idxL1taubx1', 'FindL1ObjIdx_setBx(_L1isotauer2p1_eta, _L1isotauer2p1_phi, _L1isotauer2p1_bx, cleanJet_Eta, cleanJet_Phi, 1)')
    
    df = df.Define('cleanJet_L1tauPt','GetVal(cleanJet_idxL1taubx0,_L1tau_pt)')
    df = df.Define('cleanJet_L1tauPtbxmin1','GetVal(cleanJet_idxL1taubxmin1,_L1tau_pt)')
    df = df.Define('cleanJet_L1tauPtbx1','GetVal(cleanJet_idxL1taubx1,_L1tau_pt)')
    
    L1Ptcut = '&&cleanJet_L1tauPtbxmin1>34'
    df = df.Define('probeL1isotau34er2p1Bxmin1_Eta','cleanJet_Eta[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    df = df.Define('probeL1isotau34er2p1Bxmin1_Phi','cleanJet_Phi[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    df = df.Define('probeL1isotau34er2p1Bxmin1_Pt','cleanJet_Pt[cleanJet_Pt>100&&cleanJet_Pt<16000'+L1Ptcut+']')
    
    histos['L1IsoTau34Er2p1_bxmin1_etapt'+suffix] = df.Histo2D(ROOT.RDF.TH2DModel('L1IsoTau34Er2p1_bxmin1_etapt'+suffix, '', 100, -5,5, len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'probeL1isotau34er2p1Bxmin1_Eta', 'probeL1isotau34er2p1Bxmin1_Pt')
    




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

    dfhfnoise = dfhfnoise.Define('HighPtJet_HFSEtaEta','_jethfsigmaEtaEta[_jetPt>250&&((_jetEta>3.0&&_jetEta<5)||(_jetEta>-5&&_jetEta<-3.))]')
    dfhfnoise = dfhfnoise.Define('HighPtJet_HFSPhiPhi','_jethfsigmaPhiPhi[_jetPt>250&&((_jetEta>3.0&&_jetEta<5)||(_jetEta>-5&&_jetEta<-3.))]')
    dfhfnoise = dfhfnoise.Define('HighPtJet_HFCentralEtaStripSize','_jethfcentralEtaStripSize[_jetPt>250&&((_jetEta>3.0&&_jetEta<5)||(_jetEta>-5&&_jetEta<-3.))]')
    dfhfnoise = dfhfnoise.Define('HighPtJet_HFAdjacentEtaStripSize','_jethfadjacentEtaStripsSize[_jetPt>250&&((_jetEta>3.0&&_jetEta<5)||(_jetEta>-5&&_jetEta<-3.))]')
    
    
    prefix = ['failL1Jet80', 'passL1Jet80']
    df_passvsfailL1 = [dfhfnoise.Filter('Sum(passL1Pt80&&isHFJetPt250)==0'), dfhfnoise.Filter('Sum(passL1Pt80&&isHFJetPt250)>=1')]
    
    for i, p in enumerate(prefix):
        if i == 0:
            df_passvsfailL1[i] = df_passvsfailL1[i].Filter(stringToPrintHF)
        

        histos[p+'_nhfjets'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_nhfjets'+suffix, '', 100, 0, 100), 'nHFJets')
        histos[p+'_npv'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_npv'+suffix, '', 100, 0, 100), '_n_PV')
        histos[p+'_runnb'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_runnb'+suffix, '', len(runnb_bins)-1, runnb_bins), '_runNb')
        '''
        histos[p+'_photonpt'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_photonpt'+suffix, '', 100, 0, 1000), 'ref_Pt')
        histos[p+'_ptbalance'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_ptbalance'+suffix, '', len(response_bins)-1, response_bins), 'ptbalance')
        histos[p+'_ptbalanceL1'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_ptbalanceL1'+suffix, '', len(response_bins)-1, response_bins), 'ptbalanceL1')
        '''
        histos[p+'_HighPtHFJet_Eta'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_HighPtHFJet_Eta'+suffix, '', 1000, -5, 5), 'HighPtHFJet_Eta')
        histos[p+'_HighPtHFJet_Pt'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_HighPtHFJet_Pt'+suffix, '', 80, 100, 500), 'HighPtHFJet_Pt')
        histos[p+'_HighPtJet_HFSEtaEtavsPhiPhi'+suffix] = df_passvsfailL1[i].Histo2D(ROOT.RDF.TH2DModel(p+'_HighPtJet_HFSEtaEtavsPhiPhi'+suffix, '', 100, 0, 0.2, 100, 0, 0.2), 'HighPtJet_HFSEtaEta','HighPtJet_HFSPhiPhi')
        histos[p+'_HighPtJet_HFCentralVsAdjacentEtaStripSize'+suffix] = df_passvsfailL1[i].Histo2D(ROOT.RDF.TH2DModel(p+'_HighPtJet_HFCentralVsAdjacentEtaStripSize'+suffix, '', 10, 0, 10, 10, 0, 10), 'HighPtJet_HFCentralEtaStripSize', 'HighPtJet_HFAdjacentEtaStripSize')

        histos[p+'_met'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_met'+suffix, '', 100,0,500), '_met')





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
    df = df.Define('ptbalanceL1','_L1jet_pt[cleanJet_idxL1jetbx0[0]]/ref_Pt')
    df = df.Define('probe_Eta','cleanJet_Eta[0]') 
    df = df.Define('probe_Phi','cleanJet_Phi[0]')
    return df

def AnalyzePtBalance(df, suffix = ''):
    histos = {}
    df_JetsBinnedInEta ={}
    histos['L1JetvsEtaPhi'+suffix] = df.Histo3D(ROOT.RDF.TH3DModel('h_L1PtBalanceVsEtaPhi'+suffix, 'ptbalanceL1', 100, -5, 5, 100, -3.1416, 3.1416, 100, 0, 2), 'probe_Eta','probe_Phi','ptbalanceL1')
    for i in range(len(jetEtaBins)-1):
        str_bineta = "eta{}to{}".format(jetEtaBins[i],jetEtaBins[i+1]).replace(".","p")
        df_JetsBinnedInEta[str_bineta] = df.Filter('abs(cleanJet_Eta[0])>={}&&abs(cleanJet_Eta[0])<{}'.format(jetEtaBins[i],jetEtaBins[i+1]))
        histos['RecoJetvsRunNb'+str_bineta+suffix] = df_JetsBinnedInEta[str_bineta].Histo2D(ROOT.RDF.TH2DModel('h_PtBalanceVsRunNb_{}'.format(str_bineta)+suffix, 'ptbalance', len(runnb_bins)-1, runnb_bins, len(response_bins)-1, response_bins), '_runNb','ptbalance')
        histos['L1JetvsRunNb'+str_bineta+suffix] = df_JetsBinnedInEta[str_bineta].Histo2D(ROOT.RDF.TH2DModel('h_L1PtBalanceVsRunNb_{}'.format(str_bineta)+suffix, 'ptbalanceL1', len(runnb_bins)-1, runnb_bins, len(response_bins)-1, response_bins), '_runNb','ptbalanceL1')
        histos['L1JetvsPU'+str_bineta+suffix] = df_JetsBinnedInEta[str_bineta].Histo2D(ROOT.RDF.TH2DModel('h_L1PtBalanceVsPU_{}'.format(str_bineta)+suffix, 'ptbalanceL1', 100, 0, 100, 100, 0, 2), '_n_PV','ptbalanceL1')

        
    return df, histos



    
