import matplotlib.pylab as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import datetime
import numpy as np
import json
from Q2point import Q2point

plt.rc('font', family='serif', size=15)
plt.rc('text', usetex=True)
plt.rcParams['axes.linewidth']=1.3
plt.rcParams['xtick.major.width']=1
plt.rcParams['ytick.major.width']=1
plt.rcParams['xtick.minor.width']=1
plt.rcParams['ytick.minor.width']=1
plt.rcParams['xtick.major.size']=10
plt.rcParams['ytick.major.size']=10
plt.rcParams['xtick.minor.size']=5
plt.rcParams['ytick.minor.size']=5
plt.rcParams["figure.figsize"] = [ 7.2,4.8 ]  # was 6.4,4.8

mn = 0.4
mx = 1.6
RKtex = "$R_K$"
RKstartex = "$R_{K^*}$"
Rphitex = "$R_\phi$"
Rpitex = "$R_\pi$"
RpKtex = "$R_{pK}$"
RKpipitex = "$R_{K\pi\pi}$"
m_B     = 5.28
m_Bs    = 5.366
m_Lb    = 5.620
m_Kstar = 0.892
m_K     = 0.494
m_p     = 0.938
m_phi   = 1.02
m_pi    = 0.139
res = 0.0101
Bd = "Bd2llKstar"
Bu = "Bu2llKstar" 
Bs = "Bs2llPhi" 
Both = "B2llKstar"
allObs = [ "P1", "P2", "P3", "P4'", "P5'", "P6'", "P8'", "FL", "S3", "S4", "S5", "AFB", "S7", "S8", "S9", "dBr/dq2", "Q4", "Q5" ]
m_average = 'Our average'
m_significance = 'significance'

from matplotlib.ticker import StrMethodFormatter

def niceVar(var):
    return var.replace('$','').replace(' ','_').replace('\\','_').replace('<','_').replace('^','_').replace(':','_').replace('__','_')

def savefig(fig,name,pos=[0.01,0.01],dir="BllXs",watermark=True,fontsize=10):
    if watermark:
        td = datetime.datetime.today().strftime('%Y-%m-%d')
        fig.text(pos[0],pos[1], 'patrick.koppenburg@cern.ch '+td,
                 fontsize=fontsize, color='black',
                 ha='left', va='bottom', alpha=0.5,
                 transform=plt.gcf().transFigure)
    plt.savefig("{0}/{1}.pdf".format(dir,niceVar(name)))
    plt.savefig("{0}/{1}.png".format(dir,niceVar(name)))

def formatPlot(obs,q2max=None,minY=mn,maxY=mx):
    """
    common formatting
    """
    plt.close('all')
    plt.clf()
    fig, ax = plt.subplots()
    fig.subplots_adjust(top=0.98,right=0.98,bottom=0.16,left=0.15)
    
    plt.rc('text', usetex=True)
    plt.ylim(minY,maxY)
    plt.xlabel("$q^2$ [GeV$^2/c^4$]", fontsize='x-large')
    plt.ylabel(obs, fontsize='x-large')
    if minY == -1 and maxY == 1: # asymmetry
        plt.yticks(np.arange(minY, maxY+0.5, 0.5))
    if minY!=0: plt.axhline(y = (minY+maxY)/2., clip_on = False, color='r')
    # x axis up to kinematic limit
    if not q2max : 
        if RKtex==obs: q2max = (m_B-m_K)**2
        elif RKstartex==obs: q2max = (m_B-m_Kstar)**2
        elif RpKtex==obs: q2max = (m_Lb-m_K-m_p)**2
        elif Rphitex==obs: q2max = (m_Bs-m_phi)**2
        elif Rpitex==obs : q2max = (m_B-m_pi)**2
        elif RKpipitex==obs : q2max = (m_B-2*m_pi-m_K)**2
        else :
            q2max = (m_B-m_K)**2
            print('Unknown R ratio {0}'.format(obs))
    plt.xlim(0.1134**2,q2max)  
    plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    return fig,ax

def plotExperiment( data, name, ignoreDerived = False, withavg = False):
    """
    plot experimental data point
    """
    colour,fmt = getMarker(name)
    # print('Plotting {0} {1}').format(name,len(data))
    ms=8
    if withavg :
        if 'average' in name: el = 3
        else:
            el = 0.5
            ms = 3
    elif 'LHCb' in name : el = 3
    else: el=None
    for i in range(len(data)):
        # print('Plotting {0} from {1} in {2} {3}'.format(data[i].qRange(),name,fmt,colour))
        if (ignoreDerived and data[i].ls): continue
        if i==0: data[0].plot(colour,fmt,name,el=el,ms=ms)
        else: data[i].plot(colour,fmt,el=el,ms=ms)

    # return format to build the legend manually
    return lines.Line2D([], [], color=colour, marker=fmt, linestyle='None',
                        markersize=10, label=name)    

def plotTheory( data, name, ax):
    """
    plot theory predictions
    """
    colour,fmt = getMarker(name)
    # print('Plotting {0} {1}').format(name,len(data))
    for i in range(len(data)):
        # print('Plotting {0} from {1} in {2} {3}'.format(data[i].qRange(),name,fmt,colour))
        if i==0: data[0].plot(colour,fmt,name,theory=True,ax=ax)
        else: data[i].plot(colour,fmt,theory=True,ax=ax)

    # return format to build the legend manually
    return patches.Patch(color=colour, label=name)

def muPoints(exp,theo,signed=False):
    """
    rescale experiment and theory to get a strength
    """
    theoOffset = theo.obs                               # offset to zero
    if exp.obs>theo.obs:
        scale  = np.sqrt(((exp.totError()[0][0])**2)+(theo.totError()[1][0])**2)
        newT = Q2point(theo.q2low,theo.q2high,0.,theo.StatUp/scale,theo.StatDown/scale)
        newE = Q2point(exp.q2low,exp.q2high,(exp.obs-theoOffset)/scale,exp.StatUp/scale,exp.StatDown/scale,exp.SystUp/scale,exp.SystDown/scale)
    else:
        scale  = np.sqrt(((exp.totError()[1][0])**2)+(theo.totError()[0][0])**2)
        newT = Q2point(theo.q2low,theo.q2high,0.,theo.StatDown/scale,theo.StatUp/scale)
        newE = Q2point(exp.q2low,exp.q2high,-(exp.obs-theoOffset)/scale,exp.StatDown/scale,exp.StatUp/scale,exp.SystDown/scale,exp.SystUp/scale)
    if signed:
        newT = Q2point(theo.q2low,theo.q2high,0.,theo.StatUp/scale,theo.StatDown/scale)
        newE = Q2point(exp.q2low,exp.q2high,(exp.obs-theoOffset)/scale,exp.StatUp/scale,exp.StatDown/scale,exp.SystUp/scale,exp.SystDown/scale)
    if exp.significance:
        # print("Using significance {0} instead of computed pull {1}".format(exp.significance, newE.obs))
        newE.obs = exp.significance
        if signed: newE.obs *= np.sign(exp.obs-theoOffset)

#    print("offset {0} and scale {1}".format(theoOffset,scale))
#    print("theory {0} and exp {1}".format(theo,exp))
#    print("become {0} and     {1}".format(newT,newE))
    return newE,newT

def signedMuPoints(exp,theo):
    return muPoints(exp,theo,True)

########################################################################################


def getObservable( obs = "P5'", inputfile = "LHCb-Run1-2016-P"):
    """
    Get observable from json file

    Adapted from @author Tom Blake 
    """
    result = []
    # print('Opening {0}'.format(inputfile))
    with open( inputfile ) as json_file:
        json_data = json.load( json_file )

        if obs not in json_data : return []
        if "date" in json_data :
            dd = datetime.datetime.strptime(json_data["date"] , '%d/%m/%Y')
        else:
            dd = None
        
        pred      = json_data[obs]
        # look for significance
        if m_significance in json_data:
            signif = json_data[m_significance]
        else:
            signif = [ None ]*len(pred)
        
        for i in range(0,len(pred)):
#            print(pred[i])
            result.append( Q2point( J=pred[i], date = dd, significance=signif[i]) )

        return result

def getMarker(label):
    """
    returns color, marker given label
    """
    if 'LHCb' in label:
        if 'B' in label : return 'gray','D'    # means it's a special case, like R_Ks or so
        else: return 'k','o'
    if 'Belle' in label:
        if 'mu' in label: return 'r','s'
        else: return 'b','s'
    if 'BaBar' in label: return 'g','p'
    if 'CMS' in label:
        if 'B^+' in label: return 'pink','D'
        else : return 'r','D'
    if 'ATLAS' in label: return 'm','X'
    if 'ASZB' in label: return 'y',''
    elif 'DHMV' in label: return 'darkseagreen',''
    elif 'HLMW' in label: return 'darkkhaki',''
    elif 'FLAVIO' in label: return 'chocolate',''
    elif 'average' in label: return 'darkviolet','h'
    else:
        return 'thistle',''
    
# averages
def average(qps):
    """
    average q points by PDG method. Assumes symmetric and uncorrelated uncertainties
    """
    if not qps: return None
    sw = 0. # sum of weights
    sv = 0. # sum of values
    for q in qps :
        sw += 1/q.totError2()
        sv += q.obs/q.totError2()
    return Q2point(qps[0].q2low,qps[0].q2high,sv/sw,1/np.sqrt(sw),1/np.sqrt(sw))

# time plot
def timePlot(var,pointsDict,watermark=True):
    """
    A plot of one quantity versus time
    """
    import pandas as pd
    fig, ax = plt.subplots()
    fig.subplots_adjust(top=0.98,right=0.98,bottom=0.16,left=0.15)
    ax.xaxis_date()
    for exp,points in pointsDict.items():
        for q in points:
            k,m = getMarker(exp)
            ax.errorbar(pd.Timestamp(q.date),q.obs,yerr=q.totError(),fmt=m,color=k,label=exp)
            
    ax.legend(loc="lower right",shadow=True)
    ax.text(pd.Timestamp(datetime.date(2013, 1, 1)), 1.2, var)
    plt.xlabel("Date")
    plt.ylabel(var)
    ax.axhline(y = 1., clip_on = False, color='r')
     
    var2 = niceVar(var)
    savefig(plt,"{0}_versus_time".format(var2),dir="RX",watermark=watermark)


def getAverage(expjson,theojson,decay,obs):
    """
    get average experimental data plot
    """
    import Utilities
    avgs = []
    t =  getObservable(obs,list(theojson)[0])
    if not t : return None   # ignore data without theory
    # print("Averages for {0}. Theory {1}".format(obs,t))
    exps = {}
    for filename,exp in expjson.items() :
        r = getObservable(obs,filename)
        if r:
            # print("Averages for {0}: Experiment {1} gets {2}".format(obs,exp,r))
            exps[exp] = r
    for qt in t:                       # loop over q2 ranges in theory
        matches = []
        for exp,r in exps.items():     # loop over experiments
            for qe in r:               # loop over q2 ranges in experiments
                # print(exp,qe)
                                       # if match keep data point
                if abs(qt.q2low-qe.q2low)<res and abs(qt.q2high-qe.q2high)<res:
                    # print("For {0} from {1} in {2} using {3}".format(obs,exp,qe,qt))
                    matches.append(qe)
        qa = average(matches)          # average matching data point
        if qa:
            # print("theory <{0}> and average <{1}>".format(qt,qa) )
            avgs.append(qa)
    return avgs

def getTheory(decay=Bd):
    """
    Get theory data
    """
    theojson = {}
    # theory
    if Bs == decay  :
#        theojson[ "theory/Bs2PhiMuMu.json" ] = "HLMW" # 2015
        theojson[ "theory/LHCb-PAPER-2021-014.json" ] = "HLMW" # 2021
    else:
        theojson[ "theory/2020-ASZB.json" ] = "ASZB" # 2020
        theojson[ "theory/2020-DHMV.json" ] = "DHMV" # 2020
    return theojson

def getExperiment(decay, LHCbOnly=False ):
    """
    Get experimental data
    """
    expjson = {}
    if ( Both == decay  ):  # BaBar has an average, so don't mix species.
        if not LHCbOnly: expjson["experiments/BaBar-Kstarll-2015.json"] = "BaBar'15"
    if ( Bd == decay  ):
        if not LHCbOnly: expjson["experiments/BaBar-Kstarzll-2015.json"] = "BaBar'15 ($B^0$)"
    if ( Bu == decay  ):
        if not LHCbOnly: expjson["experiments/BaBar-Kstarpll-2015.json"] = "BaBar'15 ($B^+$)"
    if ( Bd == decay or Both == decay  ):
        if not LHCbOnly: expjson["experiments/Belle-Kstarll-2009.json"] = "Belle'09"
        if not LHCbOnly: expjson["experiments/BaBar-RX-2012.json"] = "BaBar'12"
        # expjson["experiments/CMS-KstarMuMu-2013.json"] = "CMS'13"
        if not LHCbOnly: expjson["experiments/CMS-KstarMuMu-2015.json"] = "CMS'15 ($B^0$)"
        expjson["experiments/LHCb-PAPER-2016-012.json"] = "LHCb'16 ($B^0$)"
        if not LHCbOnly: expjson["experiments/Belle-Kstarll-2016.json"] = "Belle'16"
        if not LHCbOnly: expjson["experiments/CMS-KstarMuMu-2017.json"] = "CMS'17 ($B^0$)"
        if not LHCbOnly: expjson["experiments/ATLAS-KstarMuMu-2018.json"] = "ATLAS'19 ($B^0$)"
        expjson["experiments/LHCb-PAPER-2020-002.json"] = "LHCb'20 ($B^0$)"
    if ( Bu == decay or Both == decay ):
        if not LHCbOnly: expjson["experiments/CMS-KstarpMuMu-2020.json"] = "CMS'20 ($B^+$)"
        expjson["experiments/LHCb-PAPER-2020-041.json"] = "LHCb'20 ($B^+$)"
    if ( Bs == decay ):
        expjson["experiments/LHCb-PAPER-2021-014.json"] = "LHCb'21"
        expjson["experiments/LHCb-PAPER-2015-023.json"] = "LHCb'15"
    
    return expjson
 
def getExperiment_emu(decay, LHCbOnly=False):
    """
    Get experimental data
    """
    #e mu plots. Also add LHCb
    
    if ( Bd == decay or Both == decay  ):
        emujson = {}
        if not LHCbOnly: emujson["experiments/Belle-Kstarll-2016-mumu.json"] = "Belle'16 $\\mu\\mu$"
        if not LHCbOnly: emujson["experiments/Belle-Kstarll-2016-ee.json"] = "Belle'16 $ee$"
        emujson["experiments/LHCb-PAPER-2020-002.json"] = "LHCb'20 $\\mu\\mu$"
        return emujson
    else: return None

    
def getObsData(json,obs):
    """
    get data for plots
    """
    data = {}
    for filename,exp in json.items() :
        r = getObservable(obs,filename)
        if not r and "dBr" in obs : r = convertObservable("Br",filename)    # try to see if there is a Br 
        if not r and "FL" in obs  : r = convertObservable("S1s",filename)   # try to see if there is a S1s
        if not r and "AFB" in obs : r = convertObservable("S6s",filename)   # try to see if there is a S6s
        if r : data[exp] = r
    return data
    
def convertObservable(obs,filename):
    r = getObservable(obs,filename)
    if not r: return r
    if r:
        print("### Found {0} in {1}".format(obs,filename))
        """
        From 2020-041
        FL = 1-(4/3)*S1s
        AFB = (3/4)*S6s
        """
        if "Br"  == obs :  newr = [ i.scaleByQ2() for i in r ]
        if "S1s" == obs :  newr = [ i.scaleLinear(-4./3.,1) for i in r ]
        if "S6s" == obs :  newr = [ i.scaleLinear(3./4.) for i in r ]
        return newr

