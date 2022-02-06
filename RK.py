"""
Generates plots comparing all measurements of R_X. 

Different q^2 ranges are provided, also plots containing derived quantities (averaging other measurements) or not.

"""

import matplotlib.pylab as plt
import numpy as np
import collections
#from math import *

from Utilities import *
import sys

if len(sys.argv)<2:
    watermark = True
else:
    watermark = not ("no-watermark" == (sys.argv[1]).lower())

############################################
### The RK data points

#  LHCb-PAPER-2019-009
#  BaBar 12 1204.3933
BaBar2012 = getObservable( 'R_K', "experiments/BaBar-RX-2012.json" )   
#  LHCb-PAPER-2019-009
LHCb2014 =  getObservable( 'R_K', "experiments/LHCb-PAPER-2014-024.json" )
LHCb2019 =  getObservable( 'R_K', "experiments/LHCb-PAPER-2019-009.json" )
LHCb2021 =  getObservable( 'R_K', "experiments/LHCb-PAPER-2021-004.json" )
LHCb2021Ks =  getObservable( 'R_Ks', "experiments/LHCb-PAPER-2021-038.json" )
#  Belle 19 1908.01848
Belle2019 = getObservable( 'R_K', "experiments/Belle-RK-2019.json" )
 
formatPlot(RKtex)
plotExperiment( LHCb2021, "LHCb'21")
plotExperiment( LHCb2021Ks, "LHCb'21 ($B^0$)", ignoreDerived=True)
plotExperiment( BaBar2012, "BaBar'12")
plotExperiment( Belle2019, "Belle'19")
# plotExperiment( LHCb2019, "LHCb'19")
plt.legend(loc="lower right", shadow=True)
savefig(plt,"Blls-RK",dir="RX")

timePlot(RKtex+" in $1<q^2<6\:$GeV$^2$",
         {"LHCb": [ LHCb2014[0],LHCb2019[0],LHCb2021[0]],
          "Belle": [ Belle2019[2] ],
          "BaBar": [ BaBar2012[0] ]})

formatPlot(RKtex)
plotExperiment( LHCb2021, "LHCb'21", ignoreDerived=True)
plotExperiment( LHCb2021Ks, "LHCb'21 ($B^0$)", ignoreDerived=True)
plotExperiment( Belle2019, "Belle'19", ignoreDerived=True)
plotExperiment( BaBar2012, "BaBar'12", ignoreDerived=True)
plt.legend(loc="lower right", shadow=True)
savefig(plt,"Blls-RK-NoDerived",dir="RX")

formatPlot(RKtex,q2max=9.)
plotExperiment( LHCb2021, "LHCb'21", ignoreDerived=True)
plotExperiment( LHCb2021Ks, "LHCb'21 ($B^0$)", ignoreDerived=True)
plotExperiment( Belle2019, "Belle'19", ignoreDerived=True)
plotExperiment( BaBar2012, "BaBar'12", ignoreDerived=True)
plt.legend(loc="upper right", shadow=True)
savefig(plt,"Blls-RK-lowQ2",dir="RX")

### The RKstar data points

#  BaBar'12'1204.3933
BaBar2012s = getObservable( "R_K", "experiments/BaBar-RX-2012.json" )   
#  LHCb'17 LHCb-PAPER-2017-013
LHCb2017 = getObservable( "R_K*", "experiments/LHCb-PAPER-2017-013.json" )
#  Belle'19'1904.02440
Belle2019s = getObservable( "R_K*", "experiments/Belle-RKstar-2019.json" )
# LHCb K*+
LHCb2021s =  getObservable( 'R_K*+', "experiments/LHCb-PAPER-2021-038.json" )

formatPlot(RKstartex)
plotExperiment( LHCb2017, "LHCb'17")
plotExperiment( LHCb2021s, "LHCb'21 ($B^+$)")
plotExperiment( Belle2019s, "Belle'19")
plotExperiment( BaBar2012s, "BaBar'12")
plt.legend(loc="lower right", shadow=True)
savefig(plt,"Blls-RKstar",dir="RX")

formatPlot(RKstartex)
plotExperiment( LHCb2017, "LHCb'17", ignoreDerived=True)
plotExperiment( LHCb2021s, "LHCb'21 ($B^+$)")
plotExperiment( Belle2019s, "Belle'19", ignoreDerived=True)
plotExperiment( BaBar2012s, "BaBar'12", ignoreDerived=True)
plt.legend(loc="lower right", shadow=True)
savefig(plt,"Blls-RKstar-NoDerived",dir="RX")

formatPlot(RKstartex,q2max=9.)
plotExperiment( LHCb2017, "LHCb'17", ignoreDerived=True)
plotExperiment( LHCb2021s, "LHCb'21 ($B^+$)")
plotExperiment( Belle2019s, "Belle'19", ignoreDerived=True)
plotExperiment( BaBar2012s, "BaBar'12", ignoreDerived=True)
plt.legend(loc="upper right", shadow=True)
savefig(plt,"Blls-RKstar-lowQ2",dir="RX")

#  LHCb 19 LHCb-PAPER-2019-040
LHCb2019pK = [ Q2point(0.1,6.0,0.86,0.14,0.11,0.05) ]
formatPlot(RpKtex)
plotExperiment( LHCb2019pK, "LHCb'19", ignoreDerived=True)
plt.legend(loc="upper right", shadow=True)
savefig(plt,"Blls-RpK",dir="RX")

formatPlot(Rphitex)
savefig(plt,"Blls-Rphi",dir="RX")

formatPlot(Rpitex)
savefig(plt,"Blls-Rpi",dir="RX")

formatPlot(RKpipitex)
savefig(plt,"Blls-RKpipi",dir="RX")

###########################
# summary plot

fig, ax = plt.subplots()
fig.subplots_adjust(top=0.98,right=0.98,bottom=0.15,left=0.33)

labels = [ '' ]

off = 0
labels += ['$R_{K}\ [1.1,6]$']
plt.errorbar(y=len(labels)+off,x=LHCb2021[0].obs,xerr=LHCb2021[0].AverageErr,color='blue',marker='d')

labels += ['$R_{K_{\\rm S}^0}\ [1.1,6]$']
plt.errorbar(y=len(labels)+off,x=LHCb2021Ks[0].obs,xerr=LHCb2021Ks[0].AverageErr,color='blue',marker='d')

labels += [ '$R_{K^{*0}}\ [0.045,1.1]$' ]
plt.errorbar(y=len(labels)+off,x=LHCb2017[0].obs,xerr=LHCb2017[0].AverageErr,color='green',marker='d')

labels += [ '$R_{K^{*0}}\ [1.1,6]$' ]
plt.errorbar(y=len(labels)+off,x=LHCb2017[1].obs,xerr=LHCb2017[1].AverageErr,color='green',marker='d')

labels += ['$R_{K^{*+}}\ [0.045,6]$']
plt.errorbar(y=len(labels)+off,x=LHCb2021s[0].obs,xerr=LHCb2021s[0].AverageErr,color='green',marker='d')

labels += [ '$R_{pK}\ [0.1,6]$' ]
plt.errorbar(y=len(labels)+off,x=LHCb2019pK[0].obs,xerr=LHCb2019pK[0].AverageErr,color='magenta',marker='d')

nL = len(labels) # length
# plt.locator_params(axis='y', nbins=nL)
# plt.locator_params(axis='x', nbins=int(2*nsigma))
ll = ax.get_ylim()
ax.set_ylim(ll[1],ll[0])
ax.set_yticklabels(labels)
# ax.set_xlim(-0.99,nsigma)
ax.grid(axis='x')
plt.xlabel('Value of $R$')

    # plt.errorbar(y=pos,x=th,xerr=the,color='orange',marker='d',linestyle='')
    # plt.errorbar(y=pos,x=ex,xerr=exe,color='b',marker='o',linestyle='')
savefig(plt,"AllRX",watermark=watermark,dir="RX")
