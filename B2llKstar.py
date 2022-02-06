"""
Generates plots comparing all measurements of angular observables in B0->llKstar

References used so far:

"""
import matplotlib.pylab as plt
import numpy as np
import sys

#from math import *
amn = -1.0
amx = 1.0
from Utilities import *
import Utilities

def PiTex(i,prime=False):
    if prime: return "$P_{"+str(i)+"}'$"
    else: return "$P_{"+str(i)+"}$"

def SiTex(i):
    return "$S_{"+str(i)+"}$"

def QiTex(i):
    return "$Q_{"+str(i)+"}$"

def guessTex(name):
    if "AFB" == name : return "$A_{\\rm FB}$"
    if "FL" == name : return "$F_{\\rm L}$"
    if "dBr/dq2" == name : return "${\\rm d}{\\cal B}/{\\rm d}q^2\ (10^{-7})$"
    if "Br" == name : return "${\\cal B}\ (10^{-7})$"
    for i in range(10):
        if str(i) in name : break
    if 'S' in name : return SiTex(i)
    elif 'Q' in name : return QiTex(i)
    else:
        prime = ("'" in name)
        return PiTex(i,prime)

def goodName(decay,name):
    return decay+"-"+name.replace("'",'prime').replace("/",'')

def makePlot(expdata,theodata,decay,obs,add="",watermark=True):
    """
    what makes each plot
    """
    handles = []
    ok = False
    for exp,r in expdata.items() :
        if not ok:   # create plot
            print('### Creating plot for {0} {1}'.format(obs,add))
            if 'dBr' in obs: fig, ax = formatPlot(guessTex(obs),(m_B-m_Kstar)**2,0.,1.5)
            elif 'Br' in obs: fig, ax = formatPlot(guessTex(obs),(m_B-m_Kstar)**2,0.,3.)
            else: fig, ax = formatPlot(guessTex(obs),(m_B-m_Kstar)**2,amn,amx)
            ok = True
        # print("### Adding {0} from {1}: {2}".format(obs,exp,r))
        if r:
            a = plotExperiment( r, exp, ignoreDerived=True, withavg = ('average' in add) )  # 
            handles.append( a ) 

    if not ok: return  # no data found
    for th,r in theodata.items() :
        a = plotTheory( r, th, ax )
        handles.append( a ) 
    if obs in ['AFB', 'FL']:
        plt.legend(handles=handles,loc="lower right")
    else:
        plt.legend(handles=handles,loc="upper right")
        
    savefig(fig,goodName(decay,obs)+add,watermark=watermark)
    plt.clf()
    plt.cla()
 

def plotOnlyAverage(expjson,theojson,decay,watermark=True):
    """
    make averages and plot
    """
    # print(theojson)
    for obs in allObs:
        avg = {}
        avg[m_average] = getAverage(expjson,theojson,decay,obs)
        if avg[m_average]:
            makePlot(avg,getObsData(theojson,obs),decay,obs,add="-average",watermark=True)

def plotLL(expjson,theojson,decay,avg=False,watermark=True):
    """
    make plots
    """
    add = ""
    if avg: add = "-with-average"
    for obs in allObs:
        expData = {}
        if avg:
            expData[m_average] = getAverage(expjson,theojson,decay,obs)
            if not expData[m_average] : continue
        expData.update( getObsData(expjson,obs) )
        makePlot(expData,getObsData(theojson,obs),decay,obs,add=add,watermark=True)
    
def plotEmu(emujson,theojson,decay,watermark=True):
    """
    make plots
    """
    if not emujson: return
    for obs in [ "P4'", "P5'" ]:
        makePlot(getObsData(emujson,obs),getObsData(theojson,obs),decay,obs,add="-ee-mumu",watermark=True)
    
    
############################################
# main
############################################

watermark = True
if len(sys.argv)<2:
    print('Assuming B0')
    decay = Bd
else:
    B = sys.argv[1]
    if "B0"==B.upper() or "BD"==B.upper(): decay = Bd
    elif "B+"==B.upper() or "BU"==B.upper(): decay = Bu
    elif "BOTH"==B.upper() or "B"==B.upper(): decay = Both
    elif "AVERAGE"==B.upper(): decay = Both
    elif "BS"==B.upper(): decay = Bs
    else:
        print("Unknown B ``{0}''".format(B))
        sys.exit()
    if len(sys.argv)==3:
        watermark = not ("no-watermark" == (sys.argv[2]).lower())

print("Will make plots for {0}".format(decay))

## Load all data points

theojson = getTheory(decay)
expjson  = getExperiment(decay)
emujson  = getExperiment_emu(decay)

if "AVERAGE"==B.upper():
    plotOnlyAverage(expjson,theojson,decay,watermark=watermark)   
    plotLL(expjson,theojson,decay,avg=True,watermark=watermark)     
else:
    plotLL(expjson,theojson,decay,watermark=watermark)   
    plotEmu(emujson,theojson,decay,watermark=watermark)   
