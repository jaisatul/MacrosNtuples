# For 2022 setup:
#for dir in `ls -d outdir/2022Run?v?`
# For 2023 setup:
for dir in "outdir/2023B" "outdir/2023C" "outdir/golden_2023B" "outdir/golden_2023C"
# Re-processed 2018 and 2022:
#for dir in "outdir/2018Nano" "outdir/golden_2018Nano" "outdir/2022Nano" "outdir/golden_2022Nano"
do
    for skim in "ZToMuMu" "MuonJet" "ZToEE" "PhotonJet"
    do
        subdir=$dir/outputcondor_$skim
        nb_files=`ls $subdir/*.root | wc | awk '{ print $1 }' -`
        echo $subdir $nb_files
        if [ ${#nb_files} -lt 4 ]
        then
            hadd -f $dir/all_"$skim".root $dir/outputcondor_$skim/*.root
        else
            # hadd 1000 files at a time, to prevent the process taking more than 1h and getting killed 
            thousands=${nb_files:0:1}
            hadd $dir/0to999_"$skim".root $dir/outputcondor_$skim/output_?.root $dir/outputcondor_$skim/output_??.root $dir/outputcondor_$skim/output_???.root
            for i in $(seq 1 $thousands)
            do
                echo $i
                hadd $dir/"$i"000to"$i"999_"$skim".root $dir/outputcondor_$skim/output_"$i"???.root
                echo $list_dir
            done

            hadd $dir/all_"$skim".root $dir/*to*_"$skim".root

        fi
    done
done

# Un-comment these lines for the 2022 setup:

#hadd outdir/2022RunCv1_start/start_ZToMuMu.root outdir/2022RunCv1_start/outputcondor_ZToMuMu/*.root
#hadd outdir/2022RunCv1_start/start_MuonJet.root outdir/2022RunCv1_start/outputcondor_MuonJet/*.root

#mv outdir/2022RunCv1/all_ZToMuMu.root outdir/2022RunCv1/end_ZToMuMu.root
#mv outdir/2022RunCv1/all_MuonJet.root outdir/2022RunCv1/end_MuonJet.root

#hadd outdir/2022RunCv1/all_ZToMuMu.root outdir/2022RunCv1_start/start_ZToMuMu.root outdir/2022RunCv1/end_ZToMuMu.root
#hadd outdir/2022RunCv1/all_MuonJet.root outdir/2022RunCv1_start/start_MuonJet.root outdir/2022RunCv1/end_MuonJet.root
