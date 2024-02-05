import ROOT
import correctionlib._core as core

cornames = ['L1FastJet', 'L2Relative', 'L3Absolute']

cset = core.CorrectionSet.from_file('2022_Summer22/jet_jerc.json.gz')
for c in cornames:
    sf = cset['Summer22_22Sep2023_RunCD_V2_DATA_{}_AK4PFPuppi'.format(c)]
    print('Arguments for: ',c,)
    print([input.name for input in sf.inputs])
    print()
