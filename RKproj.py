import matplotlib.pylab as plt
import numpy as np
import Utilities

def rPlot(Belle,LHCb,var,bellePubs,LHCbPubs):
    jOffset = 0.4
    colB,marB = Utilities.getMarker('Belle')
    colL,marL = Utilities.getMarker('LHCb')
    plt.subplots_adjust(top=0.98,right=0.98,bottom=0.16,left=0.15)
    plt.plot(Belle.keys(),Belle.values(),label=var+" from Belle (II)",color=colB,marker=marB)
    plt.plot(LHCb.keys(),LHCb.values(),label=var+" from LHCb",color=colL,marker=marL)
    for b,j in bellePubs.items():
        plt.text(b+jOffset, Belle[b], j, fontsize='xx-small')
    for b,j in LHCbPubs.items():
        plt.text(b+jOffset, LHCb[b], j, fontsize='xx-small')
    plt.rc('text', usetex=True)
    plt.xlabel("End of year of data taking", fontsize='x-large')
    plt.ylabel("Total Uncertainty on "+var, fontsize='x-large')
    legend = plt.legend(loc='upper right', shadow=True, fontsize='x-large')
    plt.ylim(bottom=0.005,top=0.5)
    plt.yscale("log")
    nn = "Error_on_"+var.replace('$','').replace('{','').replace('}','').replace('*','star').replace('^','')
    Utilities.savefig(plt,nn,dir="RX",watermark=True,fontsize=8)
    plt.clf()

# date is end of data taking
#
Belle_RK = {}
LHCb_RK = {}
Belle_RKstar = {}
LHCb_RKstar = {}
#
# Expected ends of run
#
Run1 = 2012
Run2 = 2018
Run3 = 2024
Run4 = 2030
Run5 = 2034
Run1EffLumi = 1.*(7./13.)+2.*(8./13.)    # assumes scaling with energy
LHCbLumi = { Run1: Run1EffLumi,
             2016: Run1EffLumi+2.,
             Run2: Run1EffLumi+6.,
             Run3: 23.,
             Run4: 50.,
             Run5: 300. } # /fb
#
KEK1 = 2010
KEK2 = 2026
KEK3 = 2031
KEKLumi = { KEK1: 0.711, KEK2: 18, KEK3: 55. } # /ab (from Moriond QCD)
#
# data uncertainties
#
Belle_RK[2010] = Utilities.getObservable( 'R_K',  "experiments/Belle-RK-2019.json" )[2].AverageErr
Belle_RKstar[2010] = Utilities.getObservable( 'R_K*', "experiments/Belle-RKstar-2019.json" )[1].AverageErr
LHCb_RK[Run1] = Utilities.getObservable( 'R_K',  "experiments/LHCb-PAPER-2014-024.json" )[0].AverageErr
LHCb_RK[2016] = Utilities.getObservable( 'R_K',  "experiments/LHCb-PAPER-2019-009.json" )[0].AverageErr
LHCb_RK[Run2] = Utilities.getObservable( 'R_K',  "experiments/LHCb-PAPER-2021-004.json" )[0].AverageErr
LHCb_RKstar[Run1] = Utilities.getObservable( 'R_K*',  "experiments/LHCb-PAPER-2017-013.json" )[0].AverageErr
#
# Extrapolations
#
Belle_RK[KEK2]     = Belle_RK[KEK1]/np.sqrt(KEKLumi[KEK2]/KEKLumi[KEK1])
Belle_RK[KEK3]     = Belle_RK[KEK1]/np.sqrt(KEKLumi[KEK3]/KEKLumi[KEK1])
Belle_RKstar[KEK2] = Belle_RKstar[KEK1]/np.sqrt(KEKLumi[KEK2]/KEKLumi[KEK1])
Belle_RKstar[KEK3] = Belle_RKstar[KEK1]/np.sqrt(KEKLumi[KEK3]/KEKLumi[KEK1])
#
LHCb_RK[Run3]      = LHCb_RK[Run2]/np.sqrt(LHCbLumi[Run3]/LHCbLumi[Run2])
LHCb_RK[Run4]      = LHCb_RK[Run2]/np.sqrt(LHCbLumi[Run4]/LHCbLumi[Run2])
LHCb_RK[Run5]      = LHCb_RK[Run2]/np.sqrt(LHCbLumi[Run5]/LHCbLumi[Run2])
print("RK at run 5: {0} scaled by sqrt({1}/{2}) is {3}".format(LHCb_RK[Run2],LHCbLumi[Run5],LHCbLumi[Run2],LHCb_RK[Run5]))
LHCb_RKstar[Run2]  = LHCb_RKstar[Run1]/np.sqrt(LHCbLumi[Run2]/LHCbLumi[Run1])
LHCb_RKstar[Run3]  = LHCb_RKstar[Run1]/np.sqrt(LHCbLumi[Run3]/LHCbLumi[Run1])
LHCb_RKstar[Run4]  = LHCb_RKstar[Run1]/np.sqrt(LHCbLumi[Run4]/LHCbLumi[Run1])
LHCb_RKstar[Run5]  = LHCb_RKstar[Run1]/np.sqrt(LHCbLumi[Run5]/LHCbLumi[Run1])

rPlot(Belle_RK,LHCb_RK,"$R_K$",
      {KEK1: 'JHEP 03 (2021) 105'},
      {Run1: 'PRL 113 (2014) 151601',
       2016: 'PRL 122 (2019) 191801',
       Run2: '2003.13649'})
rPlot(Belle_RKstar,LHCb_RKstar,"$R_{K^{*}}$",
      {KEK1: '1904.02440'},
      {Run1: 'JHEP 05 (2017) 055'})

print("Belle RK  : {0}".format(Belle_RK))
print("LHCb  RK  : {0}".format(LHCb_RK))
print("Belle RK* : {0}".format(Belle_RKstar))
print("LHCb  RK* : {0}".format(LHCb_RKstar))
