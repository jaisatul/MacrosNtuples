from array import array

## Bin edges for histograms (booking and plotting)
jetetaBins    = array('f', [0.0, 1.3, 2.5, 3.0, 3.5, 4.0, 5.0 ])
alphaBins     = array('f', [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00 ])
jetptBins     = array('f', [20.0, 35.0, 50.0, 65.0, 85.0, 115.0, 150.0, 200.0, 300.0, 500.0, 1000.0 ])
ptbalanceBins = array('f', [0.+float(i)/100. for i in range(200) ])

## Binning as strings (histogram names, dictionary keys etc)
str_binetas = []
NetaBins = len(jetetaBins)-1
for e in range(NetaBins):
    str_binetas.append("eta{}to{}".format("{:.1f}".format(jetetaBins[e]), "{:.1f}".format(jetetaBins[e+1])).replace(".","p"))

str_binalphas = []
NalphaBins = len(alphaBins)-1
for a in range(NalphaBins):
    str_binalphas.append("alpha{}to{}".format("{:.2f}".format(alphaBins[a]), "{:.2f}".format(alphaBins[a+1])).replace(".","p"))

str_binpts = []
NptBins = len(jetptBins)-1
for p in range(NptBins):
    str_binpts.append("pt{}to{}".format(int(jetptBins[p]), int(jetptBins[p+1])))

## For pt balance bins only the length is used: no transformation to string is required
NptbalanceBins = len(ptbalanceBins)-1
