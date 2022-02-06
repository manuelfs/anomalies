"""
Generates a "mu" plot of the anomalies

Only anomalous measurements are represented. It's thus for illustration only.
"""
import matplotlib.pylab as plt
import numpy as np
import collections
import sys
#from math import *

from Utilities import *
plt.rcParams["figure.figsize"] = [ 7.2,7.2 ]  # was 6.4,4.8
# plt.rcParams['font.size'] = 16

m_dimuons = 'dimuons'
m_muons   = 'muons'
m_e       = 'e'
m_DeltaMs = 'DeltaMs'
m_Z       = 'Z'


############################################

def drawTwoPoints(plt,labels,pts,yoffset=0.04):
    """
    Draw experiment and theory
    """
    yo = yoffset # y offset for theory (0.05 causes it to break)
    plt.errorbar(y=len(labels)-2-yo,x=pts[1].obs,xerr=pts[1].totError(),color='orange',marker='d')
    plt.errorbar(y=len(labels)-2+yo,x=pts[0].obs,xerr=pts[0].totError(),color='b',marker='o')
    

def anomaliesPlot(blocks=['dimuons'],watermark=True,LHCbOnly=False):
    """
    Make anomalies plot
    """
    add = ""
    if LHCbOnly: add = "-LHCb"
    if not [m_dimuons,m_muons] == blocks :
        for i in blocks: add += "-"+i
   
    fig, ax = plt.subplots()
    fig.subplots_adjust(top=0.98,right=0.98,bottom=0.1,left=0.33)

    labels = [ '' ]
 
    ### RK and RKstar
    RKs2021 = getObservable( 'R_Ks', "experiments/LHCb-PAPER-2021-038.json" )
    RK2021 = getObservable( 'R_K', "experiments/LHCb-PAPER-2021-004.json" )
    RKstar2021 = getObservable( "R_K*+", "experiments/LHCb-PAPER-2021-038.json" )
    RKstar2017 = getObservable( "R_K*", "experiments/LHCb-PAPER-2017-013.json" )
    RKstarT = getObservable( "R_K*", "theory/RKstar.json" )
    RKT = getObservable( "R_K", "theory/RKstar.json" )
    RpK = getObservable( "R_pK^-1", "experiments/LHCb-PAPER-2019-040.json" )
#    print("RK {0}".format(RK2021[0]))
    labels += ['$R_K\ [1.1,6]$']
    drawTwoPoints(plt,labels,muPoints(RK2021[0],RKT[0]))
    labels += ['$R_{K_{\\rm S}^0}\ [1.1,6]$']
    drawTwoPoints(plt,labels,muPoints(RKs2021[0],RKT[0]))
    labels += [ '$R_{K^{*+}}\ [0.045,1.1]$' ]
    drawTwoPoints(plt,labels,muPoints(RKstar2017[0],RKstarT[0]))
    labels += [ '$R_{K^{*0}}\ [1.1,6]$' ]
    drawTwoPoints(plt,labels,muPoints(RKstar2017[1],RKstarT[1]))
    labels += ['$R_{K^{*0}}\ [0.045,6]$']
    drawTwoPoints(plt,labels,muPoints(RKstar2021[0],RKstarT[1]))
    labels += [ '$R_{pK}\ [0.1,6]$' ]
    drawTwoPoints(plt,labels,muPoints(RpK[0],Q2point(0.1,6.0,1.,1e-2,1e-2)))
     
    ### P5'
    obs = "P5'"
    expjson = getExperiment( Both, LHCbOnly=LHCbOnly )
    theojson = getTheory( )
    theoP5p  = getObsData(theojson,obs)['ASZB']
    avgP5p = getAverage(expjson,theojson,Both,obs)
    
#    print("{0} is {1} and {2}".format(obs,avgP5p[2],avgP5p[3]))
#    print("{0} is {1} and {2}".format(obs,theoP5p[2],theoP5p[3]))
    labels += [  "$P_5'\ [2.5,4]$" ]
    drawTwoPoints(plt,labels,muPoints(avgP5p[2],theoP5p[2]))
    labels += [  "$P_5'\ [4,6]$" ]
    drawTwoPoints(plt,labels,muPoints(avgP5p[3],theoP5p[3]))
    
    # Bs->phimumu
    labels += [  "${\\cal B}(B_s^0\\to\\phi\mu^+\mu^-)\ [1.1,6]$" ]
    Bsp  = getObservable( "dBr/dq2", "experiments/LHCb-PAPER-2021-014.json" )
    TBsp = getObservable( "dBr/dq2", "theory/LHCb-PAPER-2021-014.json" )
    drawTwoPoints(plt,labels,muPoints(Bsp[8],TBsp[6]))
        

    # Bs->mumu
    labels += [  "${\\cal B}(B_s^0\\to\mu^+\mu^-)$" ]
#    Bs  = getObservable( "BF", "experiments/LHCb-PAPER-2021-007.json" )
#    Bs  = getObservable( "BF", "experiments/Altmannshofer-LHC.json" )
    if LHCbOnly:
        Bs  = getObservable( "BF", "experiments/LHCb-PAPER-2021-007.json" )
    else:
        Bs  = getObservable( "BF", "experiments/MartinezSantos-LHC.json" )
    TBs = getObservable( "BF", "theory/Bs2MuMu.json" )
    drawTwoPoints(plt,labels,muPoints(Bs[1],TBs[1]))
    labels += [  "${\\cal B}(B^0\\to\mu^+\mu^-)$" ]
    drawTwoPoints(plt,labels,muPoints(Bs[0],TBs[0]))
    
    
    if m_muons in blocks and not LHCbOnly:
        # g-2
        labels += [  "Muon $g-2$" ]
        Gm1  = getObservable( "g-2", "experiments/gMinus2.json" )
        Gm2 = getObservable( "g-2", "theory/gMinus2.json" )
        drawTwoPoints(plt,labels,muPoints(Gm1[0],Gm2[0]))

    if m_e in blocks and not LHCbOnly:
        labels += [  "Electron $g-2$" ]
        Gm1  = getObservable( "g-2", "experiments/gMinus2_e.json" )
        Gm2 = getObservable( "g-2", "theory/gMinus2_e.json" )
        drawTwoPoints(plt,labels,muPoints(Gm1[0],Gm2[0]))
       
    if m_muons in blocks:
        ### RD(*)
        if LHCbOnly:
            RDst  =  getObservable( "R(D*)", "experiments/LHCb-PAPER-2017-017.json" )
        else:
            RDst  =  getObservable( "R(D*)", "experiments/HFLAV-RD.json" )
            RD    =  getObservable( "R(D)", "experiments/HFLAV-RD.json" )
        RJ        =  getObservable( "R(J/psi)", "experiments/LHCb-PAPER-2017-035.json" )
        RLc       =  getObservable( "R(Lc)", "experiments/LHCb-PAPER-2021-044.json" )
        theoRD    =  getObservable( "R(D)", "theory/HFLAV-RD.json" )
        theoRDst  =  getObservable( "R(D*)", "theory/HFLAV-RD.json" )
        theoRJ    =  getObservable( "R(J/psi)", "theory/HFLAV-RD.json" )
        theoRLc   =  getObservable( "R(Lc)", "theory/HFLAV-RD.json" )
        Btau      =  getObservable( "BF", "experiments/B2taunu.json" )
        theoBtau  =  getObservable( "BF", "theory/B2taunu.json" )
#        print("RD  {0}".format(RD[0]))
#        print("RD* {0}".format(RDst[0]))
        if not LHCbOnly:
            labels += [  "$R(D)$" ]
            drawTwoPoints(plt,labels,muPoints(RD[0],theoRD[0]))
        labels += [  "$R(D^*)$" ]
        drawTwoPoints(plt,labels,muPoints(RDst[0],theoRDst[0]))
        labels += [  "$R(J/\\psi)$" ]
        drawTwoPoints(plt,labels,muPoints(RJ[0],theoRJ[0]))
        labels += [  "$R(\\Lambda_c^+)$" ]
        drawTwoPoints(plt,labels,muPoints(RLc[0],theoRLc[0]))
        if not LHCbOnly:
            labels += [  "${\\cal B}(B^+\\to\\tau^+\\nu)$" ]
            drawTwoPoints(plt,labels,muPoints(Btau[0],theoBtau[0]))

    if m_DeltaMs in blocks:

        ## DeltaMs
        Dms  = getObservable( "Delta m", "experiments/LHCb-PAPER-2021-005.json" )
        DmsT = getObservable( "Delta m", "theory/DeltaMs.json" )
        if not LHCbOnly:
            labels += [  "$\\Delta m_d$" ]
            drawTwoPoints(plt,labels,muPoints(Dms[0],DmsT[0]))
        labels += [  "$\\Delta m_s$" ]
        drawTwoPoints(plt,labels,muPoints(Dms[1],DmsT[1]))

    if m_Z in blocks:
        Z  = getObservable( "Z_AFB", "experiments/LEP.json" )
        ZT = getObservable( "Z_AFB", "theory/gFitter.json" )
        labels += [  "$Z\ A_{\\rm FB}^{0,b}$" ]
        drawTwoPoints(plt,labels,muPoints(Z[0],ZT[0]))
    
    ######## plot
    nsigma=5
    nL = len(labels) # length
    plt.locator_params(axis='y', nbins=nL)
    plt.locator_params(axis='x', nbins=int(2*nsigma))
    ll = ax.get_ylim()
    if nL>20:  # else it will label only every other tick
        ax.set_yticks( [float(x) for x in range(-1,nL)] )
        ax.set_ylim(int(ll[1])-0.01,-0.99)
    else:
        ax.set_ylim(ll[1],ll[0])    
    ax.set_yticklabels(labels)
    ax.set_xlim(-0.99,nsigma)
    ax.grid(axis='x')
    plt.xlabel('Pull in $\sigma$')

    print(f'{add}: {ax.get_yticks()} ticks. y lim: {ll[1]}, {ll[0]}. {nL} labels : {labels}') 

    # plt.errorbar(y=pos,x=th,xerr=the,color='orange',marker='d',linestyle='')
    # plt.errorbar(y=pos,x=ex,xerr=exe,color='b',marker='o',linestyle='')
    savefig(plt,"AnomaliesPlot{0}".format(add),watermark=watermark,dir="Anomalies")

##############################################################################

if len(sys.argv)<2:
    watermark = True
else:
    watermark = not ("no-watermark" in (sys.argv[1]).lower())

anomaliesPlot([m_dimuons],watermark=watermark)
anomaliesPlot([m_dimuons],watermark=watermark,LHCbOnly=True)
anomaliesPlot([m_dimuons,m_muons],watermark=watermark)
anomaliesPlot([m_dimuons,m_muons],watermark=watermark,LHCbOnly=True)
anomaliesPlot([m_dimuons,m_muons,m_e],watermark=watermark)
anomaliesPlot([m_dimuons,m_muons,m_Z],watermark=watermark)
anomaliesPlot([m_dimuons,m_muons,m_DeltaMs],watermark=watermark)
anomaliesPlot([m_dimuons,m_muons,m_DeltaMs],watermark=watermark,LHCbOnly=True)
anomaliesPlot([m_dimuons,m_muons,m_e,m_Z,m_DeltaMs],watermark=watermark)

    
