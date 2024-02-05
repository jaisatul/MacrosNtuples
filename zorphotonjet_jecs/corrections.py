import ROOT
import correctionlib
correctionlib.register_pyroot_binding()

# json file with Jet Energy Corrections
# TODO: make it generic and read the files that corresponds to the year provided when sybmitting the jobs
ROOT.gInterpreter.Declare('auto cset = correction::CorrectionSet::from_file("JEC/2022_Summer22/jet_jerc.json.gz");')

# C++ function to apply the Jet Energy Corrections 
# TODO: Improve and make generic reading of file with the corrections (year, era, correction_name, algo)
ROOT.gInterpreter.Declare('''
ROOT::VecOps::RVec<float> JetEnergyCorrections(const ROOT::VecOps::RVec<float> &area, 
                                               const ROOT::VecOps::RVec<float> &eta,
                                               const ROOT::VecOps::RVec<float> &pt,
                                               const float &rho){

    ROOT::VecOps::RVec<float> corrected_pt;

    for(unsigned int i=0; i<area.size(); i++){
       float sf = cset->at("Summer22_22Sep2023_RunCD_V2_DATA_L1FastJet_AK4PFPuppi")->evaluate({area[i], eta[i], pt[i], rho});
       sf *= cset->at("Summer22_22Sep2023_RunCD_V2_DATA_L2Relative_AK4PFPuppi")->evaluate({eta[i], pt[i]});
       sf *= cset->at("Summer22_22Sep2023_RunCD_V2_DATA_L3Absolute_AK4PFPuppi")->evaluate({eta[i], pt[i]});
       corrected_pt.push_back(sf*pt[i]);
       //std::cout << "Area: " << area[i] << "\t\t" << "Eta: " << eta[i] << "\t\t" << "Pt: " << pt[i] << "\t\t" << "Rho: " << rho << "\t\t" << "Correction: " << sf << endl;
    }

    return corrected_pt;

}
''')
