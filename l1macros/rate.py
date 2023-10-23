from datetime import datetime
import ROOT
import json
import os
import sys
import csv
import argparse
import ROOT
import pandas as pd
from array import array
from glob import glob

#Get absolute location of code package
topDir = os.getcwd().split('MacrosNtuples')[0]+'MacrosNtuples/'

ROOT.gInterpreter.Declare('#include "'+topDir+'helpers/Helper.h"')

#A few global variables
lumisection_in_seconds = 23.2
#prescale = 450. #Prescale of HLTPhysics
pu_ref = 70 #
rate_meas = 5.7*2450. #SingleMu22 @PU70 from fill 8456, for ZB this would be 3e8/26659*2450





#Thresholds for testing various VBF seeds: dijet_PtA_PtB_MjjC/dEtaD_dPhiE (where A, B, C, D are lower cuts and E is upper cut)
leadingpt = [60, 70, 80, 90, 100, 110, 120, 130]
trailingpt = [30, 35, 40, 50, 60, 70]
deta = [2., 2.5, 3., 3.5, 4.0, 4.5, 5]
mjj = [400., 500., 550., 600., 650., 700.]
dphi = [0.8, 1.6, 2.4, 3.2]


#Grouping seeds from the 2022 2e34 L1 menu.   
singledoublemu_seeds = [
'L1_SingleMu22',
'L1_SingleMu25',
'L1_DoubleMu8_SQ',
'L1_DoubleMu9_SQ',
'L1_DoubleMu_15_5_SQ',
'L1_DoubleMu_15_7',
'L1_DoubleMu_15_7_SQ',
'L1_DoubleMu18er2p1_SQ',
'L1_DoubleMu0_Upt6_IP_Min1_Upt4',
'L1_DoubleMu0_Upt15_Upt7'
]

singledoubleg_seeds = [
'L1_SingleEG36er2p5',
'L1_SingleEG38er2p5',
'L1_SingleEG40er2p5',
'L1_SingleEG42er2p5',
'L1_SingleEG45er2p5',
'L1_SingleIsoEG30er2p5',
'L1_SingleIsoEG30er2p1',
'L1_SingleIsoEG32er2p5',
'L1_SingleIsoEG32er2p1',
'L1_SingleIsoEG34er2p5',
'L1_DoubleEG_25_12_er2p5',
'L1_DoubleEG_25_14_er2p5',
'L1_DoubleEG_27_14_er2p5',
'L1_DoubleEG_LooseIso22_12_er2p5',
'L1_DoubleEG_LooseIso25_12_er2p5',
'L1_DoubleEG_LooseIso18_LooseIso12_er1p5',
'L1_DoubleEG_LooseIso20_LooseIso12_er1p5',
'L1_DoubleEG_LooseIso22_LooseIso12_er1p5',
'L1_DoubleEG_LooseIso25_LooseIso12_er1p5',
'L1_DoubleLooseIsoEG22er2p1',
'L1_DoubleLooseIsoEG24er2p1',
'L1_TripleEG_18_17_8_er2p5',
'L1_TripleEG_18_18_12_er2p5',
'L1_TripleEG16er2p5'
]

centraljet_ht_seeds = [
'L1_SingleJet180er2p5',
'L1_DoubleJet150er2p5',
'L1_DoubleJet112er2p3_dEta_Max1p6',
'L1_DoubleJet30er2p5_Mass_Min300_dEta_Max1p5',
'L1_DoubleJet30er2p5_Mass_Min330_dEta_Max1p5',
'L1_DoubleJet30er2p5_Mass_Min360_dEta_Max1p5',
'L1_TripleJet_95_75_65_DoubleJet_75_65_er2p5',
'L1_TripleJet_100_80_70_DoubleJet_80_70_er2p5',
'L1_TripleJet_105_85_75_DoubleJet_85_75_er2p5',
'L1_QuadJet_95_75_65_20_DoubleJet_75_65_er2p5_Jet20_FWD3p0',
'L1_HTT320er_QuadJet_70_55_40_40_er2p5',
'L1_HTT320er_QuadJet_80_60_er2p1_45_40_er2p3',
'L1_HTT320er_QuadJet_80_60_er2p1_50_45_er2p3',
'L1_HTT360er',
'L1_HTT400er',
'L1_HTT450er'
]

met_seeds = [
'L1_ETMHF90_SingleJet60er2p5_dPhi_Min2p1',
'L1_ETMHF90_SingleJet60er2p5_dPhi_Min2p6',
'L1_ETMHF90_SingleJet80er2p5_dPhi_Min2p1',
'L1_ETMHF90_SingleJet80er2p5_dPhi_Min2p6',
'L1_ETT2000',
'L1_ETM150',
'L1_ETM150',
'L1_ETMHF100',
'L1_ETMHF110',
'L1_ETMHF120',
'L1_ETMHF130',
'L1_ETMHF140',
'L1_ETMHF150',
'L1_ETMHF90_HTT60er',
'L1_ETMHF100_HTT60er',
'L1_ETMHF110_HTT60er',
'L1_ETMHF120_HTT60er',
'L1_ETMHF130_HTT60er'
]

vbfjet_seeds = [
'L1_SingleJet180',
'L1_SingleJet200',
'L1_DoubleJet_120_45_DoubleJet45_Mass_Min620',
'L1_DoubleJet_115_40_DoubleJet40_Mass_Min620_Jet60TT28',
'L1_DoubleJet_120_45_DoubleJet45_Mass_Min620_Jet60TT28',
'L1_DoubleJet35_Mass_Min450_IsoTau45er2p1_RmOvlp_dR0p5'
]

egmu_seeds = [
'L1_Mu7_EG20er2p5',
'L1_Mu7_EG23er2p5',
'L1_Mu20_EG10er2p5',
'L1_Mu7_LooseIsoEG20er2p5',
'L1_Mu7_LooseIsoEG23er2p5',
'L1_Mu6_DoubleEG12er2p5',
'L1_Mu6_DoubleEG15er2p5',
'L1_Mu6_DoubleEG17er2p5',
'L1_DoubleMu5_SQ_EG9er2p5'
]

tau_seeds = [
'L1_SingleTau120er2p1',
'L1_SingleTau130er2p1',
'L1_DoubleTau70er2p1',
'L1_DoubleIsoTau34er2p1',
'L1_DoubleIsoTau35er2p1',
'L1_DoubleIsoTau36er2p1',
'L1_DoubleIsoTau26er2p1_Jet70_RmOvlp_dR0p5'
]

egormu_tau_seeds = [
'L1_LooseIsoEG22er2p1_IsoTau26er2p1_dR_Min0p3',
'L1_LooseIsoEG24er2p1_IsoTau27er2p1_dR_Min0p3',
'L1_LooseIsoEG22er2p1_Tau70er2p1_dR_Min0p3',
'L1_Mu18er2p1_Tau24er2p1',
'L1_Mu18er2p1_Tau26er2p1',
'L1_Mu18er2p1_Tau26er2p1_Jet55',
'L1_Mu18er2p1_Tau26er2p1_Jet70',
'L1_Mu22er2p1_IsoTau32er2p1',
'L1_Mu22er2p1_IsoTau34er2p1',
'L1_Mu22er2p1_IsoTau36er2p1',
'L1_Mu22er2p1_IsoTau40er2p1',
'L1_Mu22er2p1_Tau70er2p1'
]

 
egmutau_jetmet_forsusexo_seeds = [
'L1_Mu3er1p5_Jet100er2p5_ETMHF40',
'L1_Mu3er1p5_Jet100er2p5_ETMHF50',
'L1_Mu6_HTT240er',
'L1_Mu6_HTT250er',
'L1_DoubleMu3_SQ_ETMHF40_HTT60er',
'L1_DoubleMu3_SQ_ETMHF50_HTT60er',
'L1_DoubleMu3_SQ_ETMHF40_Jet60er2p5_OR_DoubleJet40er2p5',
'L1_DoubleMu3_SQ_ETMHF50_Jet60er2p5_OR_DoubleJet40er2p5',
'L1_DoubleMu3_SQ_ETMHF50_Jet60er2p5',
'L1_DoubleMu3_SQ_ETMHF60_Jet60er2p5',
'L1_DoubleMu3_SQ_HTT220er',
'L1_DoubleMu3_SQ_HTT240er',
'L1_DoubleMu3_SQ_HTT260er',
'L1_DoubleEG8er2p5_HTT300er',
'L1_DoubleEG8er2p5_HTT320er',
'L1_DoubleEG8er2p5_HTT340er'
]

egjet_fortop_seeds = [
'L1_LooseIsoEG28er2p1_Jet34er2p5_dR_Min0p3',
'L1_LooseIsoEG30er2p1_Jet34er2p5_dR_Min0p3',
'L1_LooseIsoEG28er2p1_HTT100er',
'L1_LooseIsoEG30er2p1_HTT100er'
]


dimulowpt_seeds = [
'L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4',
'L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4',
'L1_DoubleMu4_SQ_OS_dR_Max1p2',
'L1_DoubleMu4p5_SQ_OS_dR_Max1p2',
'L1_DoubleMu4p5er2p0_SQ_OS_Mass_Min7',
'L1_DoubleMu4p5er2p0_SQ_OS_Mass_7to18',
'L1_DoubleMu3_OS_er2p3_Mass_Max14_DoubleEG7p5_er2p1_Mass_Max20',
'L1_DoubleMu5_OS_er2p3_Mass_8to14_DoubleEG3er2p1_Mass_Max20'
]

triplemulowpt_seeds = [
'L1_TripleMu3_SQ',
'L1_TripleMu_5_3_3',
'L1_TripleMu_5_3_3_SQ',
'L1_TripleMu_5_5_3',
'L1_TripleMu_5_3p5_2p5_DoubleMu_5_2p5_OS_Mass_5to17',
'L1_TripleMu_5_4_2p5_DoubleMu_5_2p5_OS_Mass_5to17',
'L1_TripleMu_5SQ_3SQ_0OQ_DoubleMu_5_3_SQ_OS_Mass_Max9',
'L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9'
]

bsmumu_seeds = [
'L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p5'
]

tau3mu_seeds = [
'L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12'
]

'''
multimulowpt_seeds = [
'L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p5',
'L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4',
'L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4',
'L1_DoubleMu4_SQ_OS_dR_Max1p2',
'L1_DoubleMu4p5_SQ_OS_dR_Max1p2',
'L1_DoubleMu4p5er2p0_SQ_OS_Mass_Min7',
'L1_DoubleMu4p5er2p0_SQ_OS_Mass_7to18',
'L1_TripleMu3_SQ',
'L1_TripleMu_5_3_3',
'L1_TripleMu_5_3_3_SQ',
'L1_TripleMu_5_5_3',
'L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12',
'L1_TripleMu_5_3p5_2p5_DoubleMu_5_2p5_OS_Mass_5to17',
'L1_TripleMu_5_4_2p5_DoubleMu_5_2p5_OS_Mass_5to17',
'L1_TripleMu_5SQ_3SQ_0OQ_DoubleMu_5_3_SQ_OS_Mass_Max9',
'L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9',
'L1_DoubleMu3_OS_er2p3_Mass_Max14_DoubleEG7p5_er2p1_Mass_Max20',
'L1_DoubleMu5_OS_er2p3_Mass_8to14_DoubleEG3er2p1_Mass_Max20'
]
'''


llp_seeds = [
'L1_SingleMuShower_Nominal',
'L1_SingleMuShower_Tight',
'L1_DoubleLLPJet40',
'L1_HTT200_SingleLLPJet60',
'L1_HTT240_SingleLLPJet70',
'L1_SingleMuOpen_er1p4_NotBptxOR_3BX',
'L1_SingleMuOpen_er1p1_NotBptxOR_3BX',
'L1_SingleJet43er2p5_NotBptxOR_3BX',
'L1_SingleJet46er2p5_NotBptxOR_3BX'
]

others_seeds = [
'L1_Mu12er2p3_Jet40er2p3_dR_Max0p4_DoubleJet40er2p3_dEta_Max1p6',
'L1_Mu12er2p3_Jet40er2p1_dR_Max0p4_DoubleJet40er2p1_dEta_Max1p6',
'L1_DoubleMu0_dR_Max1p6_Jet90er2p5_dR_Max0p8',
'L1_DoubleMu3_dR_Max1p6_Jet90er2p5_dR_Max0p8'
]

dict_runls_to_pu = {}
with open(topDir+'json_csv_files/run_lumi_pu_Fill8456.json', 'r', encoding='utf-8') as f_in:
    dict_runls_to_pu = json.load(f_in)
    

def getpileup(run, lumi):
    keystring = "{},{}".format(int(run),int(lumi))
    if keystring in dict_runls_to_pu:
        return dict_runls_to_pu[keystring]
    else:
        return 0




def addmenu(dict_menus, key_name, df_menu, ps_column, disableprescaledseeds=False, disable_zerobias=False, disabledtriggers=[], manually_enabledtriggers=[], customseeds = [], debug=False , dataset='ZeroBias'):
    
    '''
    One can check the L1 bit decision stored by the uGT either before ("Initial") or after ("Final") prescales and trigger rules are applied.
    For a study based on ZeroBias, the former applies. 

    For a study based on HLTPhysics, the latter applies because of the following
    - say that you start from a menu with SingleEG10 prescaled by 100 and SingleEG30 unprescaled by default. 
    - You now want to study the same menu, with only SingleEG36 unprescaled => you disable SingleEG30...SingleEG35
    - All the rejectected events would however pass the SingleEG10 Initial decision bit, leading to no change in rate for the menu if the Initial decision is used. 
    Note also that for a study based on HLTPhysics, you can only tighten the L1 menu with respect to the menu used to take the data !!! 
    
    '''
    ugtdecisionstep = "Final"
    if dataset == "ZeroBias":
        ugtdecisionstep = "Initial"

    
    #list enabled bits
    #First enable all bits with PS !=0
    enabledbits = df_menu[(df_menu[ps_column] != 0)].loc[:,"Index"]
    enabledbits_name = df_menu[(df_menu[ps_column] != 0)].loc[:,"Name"]
    df_index = df_menu[(df_menu[ps_column] != 0)].index
    #Optionnally disable prescaled seeds 
    if disableprescaledseeds:
        enabledbits = df_menu[(df_menu[ps_column] == 1)].loc[:,"Index"]
        enabledbits_name = df_menu[(df_menu[ps_column] == 1)].loc[:,"Name"]
        df_index  = df_menu[(df_menu[ps_column] == 1)].index
    string_finor = ''
    
    for ctr, i in enumerate(df_index):
        
        #Optionnally disable ZeroBias
        #Mind that HLTPhysics picks all L1 triggers *EXCEPT* L1_ZeroBias_copy (used for EphemeralZeroBias) => L1_ZeroBias_copy is essentially disabled 
        if (disable_zerobias) and (enabledbits_name[i] == 'L1_ZeroBias' or enabledbits_name[i] == 'L1_ZeroBias_copy'):
            continue
        
        if debug: 
            print("i: ", i, "enabledbits_name[i] ", enabledbits_name[i], type(enabledbits_name[i]), 'passL1_'+ugtdecisionstep+'_bx0[{}]'.format(enabledbits[i]))
        if enabledbits_name[i] in disabledtriggers:
            continue
        if ctr == 0:
            string_finor = 'passL1_'+ugtdecisionstep+'_bx0[{}]'.format(enabledbits[i])
        else:
            string_finor += '||passL1_'+ugtdecisionstep+'_bx0[{}]'.format(enabledbits[i])
    
    
    #This part to manually enable some triggers
    if len(manually_enabledtriggers)>0:
        bitnames = pd.Series()
        
        for ctr, i in enumerate(manually_enabledtriggers):
            if ctr == 0:
                bitnames = (df_menu['Name']==i)
            else:
                bitnames = bitnames | (df_menu['Name']==i)
                if debug:
                    print(bitnames)
                    
        listofmanuallyaddedbits = df_menu[bitnames].index
        allbits = df_menu.loc[:,"Index"]
        for i in listofmanuallyaddedbits:
            if debug:
                print("i in listofmanuallyaddedbits: ",i)
            if string_finor == '':
                string_finor = 'passL1_'+ugtdecisionstep+'_bx0[{}]'.format(allbits[i])
            else:
                string_finor += '||passL1_'+ugtdecisionstep+'_bx0[{}]'.format(allbits[i])
    
    
    #Now add customized bits for seeds not present in the menu
    #This will make the code crash if the bit name wasn't defined in the dataframe.
    for i in customseeds:
        string_finor += '||'+i
                    
    dict_menus[key_name] = string_finor
    
    if debug:
        print("Final or is: ", string_finor)
    

    
def main():
    ###Arguments 
    parser = argparse.ArgumentParser(
        description='''L1 rate measurement''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--max_events", dest="max_events", help="Maximum number of events to analyze. Default=-1 i.e. run on all events.", type=int, default=-1)
    parser.add_argument("--print_events", dest="print_events", help="Print out every Nth event analyzed. Default=100000 i.e. print every 100k-th.", type=int\
, default=100000)
    parser.add_argument("-i", "--input", dest="input_files", help="Input file", nargs='+', type=str, default=[])
    parser.add_argument("-o", "--output", dest="output_file", help="Output file", type=str, default='')
    parser.add_argument("-m", "--l1menucsv", dest="l1menucsv", help="L1 Menu (.csv file)", type=str, default=topDir+'json_csv_files/L1Menu_Collisions2022_Fill8456.csv')
    parser.add_argument("-d", "--dataset", dest="dataset", help="Dataset (HLTPhysics or ZeroBias)", type=str, default='')

    args = parser.parse_args() 

    if args.dataset != 'ZeroBias' and args.dataset != 'HLTPhysics':
        raise Exception('Invalid dataset')
    dataset = args.dataset

    ######################################Input files######################################
    
    ###Define the RDataFrame from the input tree
    input_files = args.input_files
    
    
    #One can put all files from a folder in an array with the following line:
    #input_files = glob('/pnfs/iihe/cms/ph/sc4/store/data/Run2022F/EGamma/NANOAOD/PromptNanoAODv10_v1-v2/*/*.root')
    #input_files = glob('/pnfs/iihe/cms/store/user/lathomas/EphemeralHLTPhysics*/Run2022G_PromptReco_v1_DataRun3_L1Studies_EphemeralZeroBias/2212*/0000/output_*.root')

    #input_files = ['/pnfs/iihe/cms/store/user/lathomas/EphemeralHLTPhysics0/Run2022G_PromptReco_v1_DataRun3_L1Studies_EphemeralZeroBias/221207_104630/0000/output_10.root']
    #Allows to exclude some corrupted/unaccessible files
    badfiles = [
        #'/pnfs/iihe/cms/store/user/lathomas/EphemeralHLTPhysics6/Run2022G_PromptReco_v1_DataRun3_L1Studies_EphemeralZeroBias/221207_105754/0000/output_9.root'
    ]
    print("n input files: ", len(input_files))
    for i in badfiles:
        if i in input_files:
            input_files.remove(i)
    print("n input files: ", len(input_files))
    #print(input_files)

    #Panda df built from the L1 menu CSV file
    df_menu = pd.read_csv(args.l1menucsv)
    
    
    ######################################Creating some L1 menus###################################### 
    
    #A dictionary of customized menus
    dict_menus = {}
    
    #Two examples to add a single seed to the emergency column (which in the case of fill 8456 contains only ZeroBias)
    #addmenu(dict_menus, "L1_ETMHF90", df_menu, "Emergency", disableprescaledseeds=False, disable_zerobias=False, disabledtriggers=[], manually_enabledtriggers=['L1_ETMHF90'])
    #addmenu(dict_menus, "L1_SingleMu25", df_menu, "Emergency", disableprescaledseeds=False, disable_zerobias=False, disabledtriggers=[], manually_enabledtriggers=['L1_SingleMu25'])

    #Copying the column 'High PU'
    addmenu(dict_menus, "2p2e34_orig", df_menu, 'HighPU', disableprescaledseeds=False, disable_zerobias=False, disabledtriggers=[], manually_enabledtriggers=[])
    #Copying the column 'High PU', but disabling zero bias bit
    #addmenu(dict_menus, "2p2e34_nozb", df_menu, 'HighPU', disableprescaledseeds=False, disable_zerobias=True, disabledtriggers=[], manually_enabledtriggers=[])
    addmenu(dict_menus, "2p2e34_nops_nozb", df_menu, 'HighPU', disableprescaledseeds=True, disable_zerobias=True, disabledtriggers=[], manually_enabledtriggers=[])
    #Copying the column 'High PU', and disabling some cherry picked seeds. 
    addmenu(dict_menus, "2p2e34_nops_nozb_novbf", df_menu, 'HighPU', disableprescaledseeds=True, disable_zerobias=True, disabledtriggers=['L1_DoubleJet_120_45_DoubleJet45_Mass_Min620', 'L1_DoubleJet_115_40_DoubleJet40_Mass_Min620_Jet60TT28', 'L1_DoubleJet_120_45_DoubleJet45_Mass_Min620_Jet60TT28', 'L1_DoubleJet35_Mass_Min450_IsoTau45er2p1_RmOvlp_dR0p5'], manually_enabledtriggers=[])
    #Copying the column 'High PU', and enables one more seed. 
    addmenu(dict_menus, "2p2e34_nops_no_zb_dijet30detalt1p5mass250", df_menu, 'HighPU', disableprescaledseeds=True, disable_zerobias=True, disabledtriggers=[], manually_enabledtriggers=['L1_DoubleJet30er2p5_Mass_Min250_dEta_Max1p5'])
    addmenu(dict_menus, "2p2e34_nops_nozb_dijet30detalt1p5mass200", df_menu, 'HighPU', disableprescaledseeds=True, disable_zerobias=True, disabledtriggers=[], manually_enabledtriggers=['L1_DoubleJet30er2p5_Mass_Min200_dEta_Max1p5'])

    addmenu(dict_menus, "2p2e34_nops_nozb_novbf", df_menu, 'HighPU', disableprescaledseeds=True, disable_zerobias=True, disabledtriggers=['L1_DoubleJet_120_45_DoubleJet45_Mass_Min620', 'L1_DoubleJet_115_40_DoubleJet40_Mass_Min620_Jet60TT28', 'L1_DoubleJet_120_45_DoubleJet45_Mass_Min620_Jet60TT28', 'L1_DoubleJet35_Mass_Min450_IsoTau45er2p1_RmOvlp_dR0p5'], manually_enabledtriggers=[])

    addmenu(dict_menus, "2p2e34_nops_no_zb_dimu4p5_sq_os", df_menu, 'HighPU', disableprescaledseeds=True, disable_zerobias=True, disabledtriggers=['L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12','L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p5'], manually_enabledtriggers=['L1_DoubleMu4p5_SQ_OS'])
    addmenu(dict_menus, "2p2e34_nops_no_zb_dimu4_sq_os", df_menu, 'HighPU', disableprescaledseeds=True, disable_zerobias=True, disabledtriggers=['L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12','L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p5'], manually_enabledtriggers=['L1_DoubleMu4_SQ_OS'])
    addmenu(dict_menus, "2p2e34_nops_no_zb_ref_dimu4p5_sq_os", df_menu, 'HighPU', disableprescaledseeds=True, disable_zerobias=True, disabledtriggers=['L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12','L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p5'])

    #Make many copies of 'High PU' column, in each case, one disables all the VBF dijet seeds, and replaces them by a customized one with a customized choice of threshold on pt1, pt2, mjj, deta, dphi.
    #Currently this code is pretty ugly since it requires the corresponding bits to be defined beforehand in the dataframe (in the processfile() function)
    #If you uncomment the next few lines, make sure to the same in processfile as well. 
    '''
    for h in dphi:
        for i in leadingpt:
            for j in trailingpt:
                if j > i:
                    continue

                for k in deta:
                    addmenu(dict_menus, '2p2e34_nops_nozb_L1_DoubleJetPt{}_{}_dEta{}_dPhi{}'.format(i,j,k,h).replace(".","p"), df_menu, 'HighPU', disableprescaledseeds=True, disable_zerobias=True, disabledtriggers=['L1_DoubleJet_120_45_DoubleJet45_Mass_Min620', 'L1_DoubleJet_115_40_DoubleJet40_Mass_Min620_Jet60TT28', 'L1_DoubleJet_120_45_DoubleJet45_Mass_Min620_Jet60TT28', 'L1_DoubleJet35_Mass_Min450_IsoTau45er2p1_RmOvlp_dR0p5'], manually_enabledtriggers=[], customseeds=['passL1_DoubleJetPt{}_{}_dEta{}_dPhi{}'.format(i,j,k,h).replace(".","p")])
                for k in mjj:
                    addmenu(dict_menus, '2p2e34_nops_nozb_L1_DoubleJetPt{}_{}_Mjj{}_dPhi{}'.format(i,j,k,h).replace(".","p"), df_menu, 'HighPU', disableprescaledseeds=True, disable_zerobias=True, disabledtriggers=['L1_DoubleJet_120_45_DoubleJet45_Mass_Min620', 'L1_DoubleJet_115_40_DoubleJet40_Mass_Min620_Jet60TT28', 'L1_DoubleJet_120_45_DoubleJet45_Mass_Min620_Jet60TT28', 'L1_DoubleJet35_Mass_Min450_IsoTau45er2p1_RmOvlp_dR0p5'], manually_enabledtriggers=[], customseeds=['passL1_DoubleJetPt{}_{}_Mjj{}_dPhi{}'.format(i,j,k,h).replace(".","p")])
    '''

    #Some more menus
    '''
    addmenu(dict_menus, "2p2e34_noditau", df_menu, 'HighPU', disableprescaledseeds=False, disable_zerobias=False, disabledtriggers=['L1_DoubleIsoTau32er2p1','L1_DoubleIsoTau34er2p1','L1_DoubleIsoTau35er2p1','L1_DoubleIsoTau36er2p1','L1_DoubleIsoTau26er2p1_Jet70_RmOvlp_dR0p5','L1_DoubleJet35_Mass_Min450_IsoTau45er2p1_RmOvlp_dR0p5'], manually_enabledtriggers=[])
    addmenu(dict_menus, "L1_SingleMu22", df_menu, 'Emergency', disableprescaledseeds=False, disable_zerobias=True, disabledtriggers=[], manually_enabledtriggers=['L1_SingleMu22'])
    addmenu(dict_menus, "L1_DoubleEG_LooseIso18_LooseIso12_er1p5", df_menu, 'Emergency', disableprescaledseeds=False, disable_zerobias=True, disabledtriggers=[], manually_enabledtriggers=['L1_DoubleEG_LooseIso18_LooseIso12_er1p5'])
    addmenu(dict_menus, "L1_DoubleIsoTau34er2p1", df_menu, 'Emergency', disableprescaledseeds=False, disable_zerobias=True, disabledtriggers=[], manually_enabledtriggers=['L1_DoubleIsoTau34er2p1'])
    addmenu(dict_menus, "L1_ETMHF100", df_menu, 'Emergency', disableprescaledseeds=False, disable_zerobias=True, disabledtriggers=[], manually_enabledtriggers=['L1_ETMHF100'])
    addmenu(dict_menus, "L1_DoubleJet_115_40_DoubleJet40_Mass_Min620_Jet60TT28", df_menu, 'Emergency', disableprescaledseeds=False, disable_zerobias=True, disabledtriggers=[], manually_enabledtriggers=['L1_DoubleJet_115_40_DoubleJet40_Mass_Min620_Jet60TT28'])
    addmenu(dict_menus, "2p2e34_noditau35_noditau26jet70", df_menu, 'HighPU', disableprescaledseeds=False, disable_zerobias=False, disabledtriggers=['L1_DoubleIsoTau32er2p1','L1_DoubleIsoTau34er2p1','L1_DoubleIsoTau35er2p1','L1_DoubleIsoTau26er2p1_Jet70_RmOvlp_dR0p5'], manually_enabledtriggers=[])
    addmenu(dict_menus, "2p2e34_noditau35", df_menu, 'HighPU', disableprescaledseeds=False, disable_zerobias=False, disabledtriggers=['L1_DoubleIsoTau32er2p1','L1_DoubleIsoTau34er2p1','L1_DoubleIsoTau35er2p1'], manually_enabledtriggers=[])
    addmenu(dict_menus, "2p2e34_noditau26jet70", df_menu, 'HighPU', disableprescaledseeds=False, disable_zerobias=False, disabledtriggers=['L1_DoubleIsoTau26er2p1_Jet70_RmOvlp_dR0p5'], manually_enabledtriggers=[])
    addmenu(dict_menus, "2p2e34_singleegplus2gev", df_menu, 'HighPU', disableprescaledseeds=False, disable_zerobias=False, disabledtriggers=['L1_SingleEG36er2p5','L1_SingleIsoEG30er2p5','L1_SingleIsoEG30er2p1','L1_LooseIsoEG28er2p1_Jet34er2p5_dR_Min0p3','L1_LooseIsoEG30er2p1_Jet34er2p5_dR_Min0p3','L1_LooseIsoEG28er2p1_HTT100er','L1_LooseIsoEG30er2p1_HTT100er'], manually_enabledtriggers=[])
    addmenu(dict_menus, "2p2e34_singlemuplus3gev", df_menu, 'HighPU', disableprescaledseeds=False, disable_zerobias=False, disabledtriggers=['L1_SingleMu22'], manually_enabledtriggers=[])
    
    addmenu(dict_menus, "2p2e34_raised_egmutau", df_menu, 'HighPU', disableprescaledseeds=False, disable_zerobias=False, disabledtriggers=['L1_SingleEG36er2p5','L1_SingleIsoEG30er2p5','L1_SingleIsoEG30er2p1','L1_LooseIsoEG28er2p1_Jet34er2p5_dR_Min0p3','L1_LooseIsoEG30er2p1_Jet34er2p5_dR_Min0p3','L1_LooseIsoEG28er2p1_HTT100er','L1_LooseIsoEG30er2p1_HTT100er','L1_SingleMu22', 'L1_DoubleIsoTau34er2p1', 'L1_DoubleIsoTau35er2p1','L1_DoubleIsoTau26er2p1_Jet70_RmOvlp_dR0p5'], manually_enabledtriggers=[])
    addmenu(dict_menus, "2p2e34_raisedcentraljets", df_menu, 'HighPU', disableprescaledseeds=False, disable_zerobias=False, disabledtriggers=['L1_SingleJet200', 'L1_SingleJet180er2p5','L1_DoubleJet150er2p5','L1_DoubleJet112er2p3_dEta_Max1p6','L1_DoubleJet30er2p5_Mass_Min300_dEta_Max1p5','L1_TripleJet_95_75_65_DoubleJet_75_65_er2p5','L1_HTT320er_QuadJet_70_55_40_40_er2p5','L1_HTT360er'], manually_enabledtriggers=[])
    '''
    

    #Building a menu from scratch, adding block of similar seeds together 

    seeds_groups = [singledoublemu_seeds, singledoubleg_seeds, centraljet_ht_seeds, met_seeds, vbfjet_seeds, egmu_seeds, tau_seeds, egormu_tau_seeds, egmutau_jetmet_forsusexo_seeds, egjet_fortop_seeds, dimulowpt_seeds, triplemulowpt_seeds, bsmumu_seeds, tau3mu_seeds, llp_seeds, others_seeds]
    seeds_groups_names = ['singledoublemu', 'singledoubleg', 'centraljet_ht', 'met', 'vbfjet', 'egmu', 'tau', 'egormu_tau', 'egmutau_jetmet_forsusexo', 'egjet_fortop', 'dimulowpt_seeds', 'triplemulowpt_seeds', 'bsmumu_seeds', 'tau3mu_seeds', 'llp', 'others_seeds']

    enabledtriggers = []
    menukeyname = ''
    for i, j in zip(seeds_groups, seeds_groups_names):
        enabledtriggers += i
        menukeyname = menukeyname + j + "_"
        addmenu(dict_menus, menukeyname, df_menu, 'Emergency', disableprescaledseeds=False, disable_zerobias=True, disabledtriggers=[], manually_enabledtriggers=enabledtriggers)
        


    ###################################### Counts vs PU ######################################C
    
    #Number of LS vs PU
    h_lsprocessed_vs_pu = ROOT.TH1F("h_lsprocessed_vs_pu","",100,0.5,100.5)
    h_lsprocessed_vs_pu.Sumw2()

    #Number of processed events vs PU
    h_allevents_vs_pu = ROOT.TH1F("h_allevents_vs_pu","",100,0.5,100.5)
    h_allevents_vs_pu.Sumw2()

    #Storing number of events passing a reference seed (can be L1_SingleMu22 or L1_ZeroBias)
    h_passreferencetriggerevents_vs_pu = ROOT.TH1F("h_passreferencetriggerevents_vs_pu", "", 100, 0.5, 100.5)
    h_passreferencetriggerevents_vs_pu.Sumw2()
    
    #Number of passing events vs PU
    h_passevents_vs_pu = {}
    for k in dict_menus.keys():
        h_passevents_vs_pu[k] = ROOT.TH1F("h_passevents_vs_pu_{}".format(k),"",100,0.5,100.5)
        h_passevents_vs_pu[k].Sumw2()
    
        
    ###################################### Processing the files ######################################
    
    for i, input_file in enumerate(input_files):
        processfile('', input_file, args.max_events, dict_menus, h_allevents_vs_pu, h_passevents_vs_pu, h_passreferencetriggerevents_vs_pu, h_lsprocessed_vs_pu, "outputmu_{}.root".format(i))
    

    ###################################### Output  ######################################                                                                                                                         

    if args.output_file == '':
        args.output_file = 'outall_L1rate.root'
    out = ROOT.TFile(args.output_file, "recreate")

    for i in range(1, h_lsprocessed_vs_pu.GetNbinsX()+1):
        h_lsprocessed_vs_pu.SetBinError(i,0)

    
    h_allevents_vs_pu.Write()
    h_passreferencetriggerevents_vs_pu.Write()
    h_lsprocessed_vs_pu.Write()
    
    for i in h_passevents_vs_pu.values():
        i.Write()


def processfile(channel, input_file, max_events, str_l1finalor, h_allevents_vs_pu, h_passevents_vs_pu, h_passreferencetriggerevents_vs_pu, h_lsprocessed_vs_pu, output_file='output_L1rate.root', dataset='ZeroBias'):

    filein = ROOT.TFile(input_file,'open')
    df = ROOT.RDataFrame('ntuplizer/tree', input_file)    
    n_events = df.Count().GetValue()
    if n_events == 0: #for backward compatibility
        df = ROOT.RDataFrame('jmeanalyzer/tree', input_file)
        n_events = df.Count().GetValue()
    
    print('There are {} events'.format(n_events))
    #Max events to run on 
    max_events = min(n_events, max_events) if max_events >=0 else n_events
    df = df.Range(0, max_events)
    runmin, runmax = int(df.Min('_runNb').GetValue()), int(df.Max('_runNb').GetValue())
    


    '''
    #Creating the various customized VBF seeds
    for h in dphi:
        for i in leadingpt:
            for j in trailingpt:
                if j > i: 
                    continue
                for k in deta:
                    print("L1SeedDoubleJetEtaMin(_L1jet_pt, _L1jet_eta, _L1jet_phi, _L1jet_bx, {}, {}, {}, {})".format(i, j, k, h))
                    df = df.Define("passL1_DoubleJetPt{}_{}_dEta{}_dPhi{}".format(i,j,k,h).replace(".","p"),"L1SeedDoubleJetEtaMin(_L1jet_pt, _L1jet_eta, _L1jet_phi, _L1jet_bx, {}, {}, {}, {})".format(i, j, k, h))
                for k in mjj:    
                    df = df.Define("passL1_DoubleJetPt{}_{}_Mjj{}_dPhi{}".format(i,j,k,h).replace(".","p"),"L1SeedDoubleJetMassMin(_L1jet_pt, _L1jet_eta, _L1jet_phi, _L1jet_bx, {}, {}, {}, {})".format(i, j, k, h))
    '''
    
    #The next line does nothing, just prints a line every 100k events
    df = df.Filter('if(tdfentry_ %'+str(args.print_events)+' == 0) {cout << "Event is  " << tdfentry_ << endl;} return true;')

    #For HLT physics studies, only consider fill 8456. Ugly hardcoding for now. 
    if dataset == "HLTPhysics":
        df = df.Filter('_runNb>=362433&&_runNb<=362439')
    

    #Find min/max run nb in the file
    print("runmin, runmax: ", runmin, runmax) 

    #Histogram of run nb vs LS for all events
    histo_all = df.Histo2D(ROOT.RDF.TH2DModel('h_runvslumi_allevents', '', 3000, 0, 3000, runmax+1-runmin, runmin, runmax+1), '_lumiBlock','_runNb')

    #Histogram of run nb vs LS for events passing reference trigger. Used as a normalization for HLTPhysics.
    histo_ref = None
    if dataset == "HLTPhysics":
        histo_ref = df.Filter('passL1_'+ugtdecisionstep+'_bx0[21]','L1_SingleMu22').Histo2D(ROOT.RDF.TH2DModel('h_runvslumi_passrefevents', '', 3000, 0, 3000, runmax+1-runmin, runmin, runmax+1), '_lumiBlock','_runNb')
    #No normalization for ZeroBias, i.e. all events are considered in the reference
    if dataset == "ZeroBias":
        histo_ref = df.Filter('passL1_Initial_bx0[458]','L1_AlwaysTrue').Histo2D(ROOT.RDF.TH2DModel('h_runvslumi_passrefevents', '', 3000, 0, 3000, runmax+1-runmin, runmin, runmax+1), '_lumiBlock','_runNb')
        print("entering here")
    
    histos_pass = {}
    for k in h_passevents_vs_pu.keys():
        histos_pass[k] = df.Filter(str_l1finalor[k]).Histo2D(ROOT.RDF.TH2DModel('h_runvslumi_passevents'+k.replace(".","p").replace("+",""), '', 3000, 0, 3000, runmax+1-runmin, runmin, runmax+1), '_lumiBlock','_runNb')
        
    #df = df.Filter(str_l1finalor,'L1FinalOR')
    #Histogram of run nb vs LS for passing events
    #histos_pass = df.Histo2D(ROOT.RDF.TH2DModel('h_runvslumi_passevents', '', 3000, 0, 3000, runmax+1-runmin, runmin, runmax+1), '_lumiBlock','_runNb')
    df_report = df.Report()    
    
    '''
    The function output is two TH1F storing all vs passing events per PU
    '''

    n_passevents = df.Count().GetValue()
    n_processed_ls = 0
    
    for i in range(histo_all.GetNbinsX()+1):
        for j in range(histo_all.GetNbinsY()+1):
            if histo_all.GetBinContent(i,j) == 0:
                continue
            
            lumi = histo_all.GetXaxis().GetBinLowEdge(i)
            run = histo_all.GetYaxis().GetBinLowEdge(j)
            pu =  getpileup(int(run), int(lumi))
            print("found non empty run:lumi: ", run, ": ", lumi, ", pile up is ", pu)

            for ctr in range(int(histo_all.GetBinContent(i,j))):
                h_allevents_vs_pu.Fill(pu)
            for ctr in range(int(histo_ref.GetBinContent(i,j))):
                h_passreferencetriggerevents_vs_pu.Fill(pu)

            for k in histos_pass.keys():
                for ctr in range(int(histos_pass[k].GetBinContent(i,j))):
                    h_passevents_vs_pu[k].Fill(pu)


            h_lsprocessed_vs_pu.Fill(pu) 

    df_report.Print()






if __name__ == '__main__':
    main()
