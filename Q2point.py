import numpy as np
import matplotlib.pylab as plt
import matplotlib.patches as patches
################################################################################################
class Q2point():
    """
    One point on obs (R, P_i...) vs q2
    """

    def __init__(self,q2low=None,q2high=None,obs=None,StatUp=None,StatDown=None,SystUp=None,SystDown=None,ls=None,J=None,date=None,significance=None):
        self.debug = False
        self.SystDown = 0.
        self.SystUp = 0.
        self.ls = ''
        self.date = date
        if q2low:
            self.q2low = q2low
            self.q2high = q2high
            self.obs = obs
            self.StatUp = StatUp
            self.StatDown = np.abs(StatDown)  # may be given as negative 
            if SystUp: self.SystUp = SystUp
            else: self.SystUp = 0
            if SystDown: self.SystDown = np.abs(SystDown)  # may be given as negative
            else: self.SystDown = self.SystUp
            self.TotUp = np.sqrt(self.StatUp**2+self.SystUp**2)
            self.TotDown = np.sqrt(self.StatDown**2+self.SystDown**2)
            self.ls = ls
        elif J:
            if self.debug: print("J is {0}".format(J))
            self.q2low = J[0]
            self.q2high = J[1]
            self.obs = J[2]
            self.StatUp = J[3]
            self.StatDown = np.abs(J[4])  # may be given as negative
            if len(J)>5:
                self.SystUp = J[5]
            if len(J)>6:
                if SystDown: self.SystDown = np.abs(J[6])  # may be given as negative
                else: self.SystDown = self.SystUp
            if len(J)>7 and J[7] == 1.: self.ls = '--'
        else:
            Exception("Not a valid constructor")

        self.q2 = self.q2low+0.5*(self.q2high-self.q2low)
        self.TotUp = np.sqrt(self.StatUp**2+self.SystUp**2)
        self.TotDown = np.sqrt(self.StatDown**2+self.SystDown**2)
        self.AverageErr = (self.TotDown+self.TotUp)/2.
#        self.RelativeErr = self.AverageErr/self.obs

        self.significance = significance

        if self.debug: print(self)
        

    def __repr__(self):
         return self.__str__()
     
    def __str__(self):
        if self.q2high>0:
            if self.SystUp:
                return "Data in {0:4.1f}-{1:4.1f} are {2:5.3f} +{3:5.3f}-{4:5.3f} (stat) +{5:5.3f}-{6:5.3f} (syst)".format( self.q2low, self.q2high, self.obs, self.StatUp, self.StatDown, self.SystUp, self.SystDown)
            else:
                return "Data in {0:4.1f}-{1:4.1f} are {2:5.3f} +{3:5.3f}-{4:5.3f} (stat)".format( self.q2low, self.q2high, self.obs, self.StatUp, self.StatDown)
                
        else:
            if self.SystUp:
                return "Data are {2:6.3f} +{3:6.3f}-{4:6.3f} (stat) +{5:6.3f}-{6:6.3f} (syst)".format( self.q2low, self.q2high, self.obs, self.StatUp, self.StatDown, self.SystUp, self.SystDown)
            else:
                return "Data are {2:6.3f} +{3:6.3f}-{4:6.3f} (stat)".format( self.q2low, self.q2high, self.obs, self.StatUp, self.StatDown)
            

    def totError(self):
        """
        vector of vectors to please plt.errorbars
        """
        return [ [self.TotDown], [self.TotUp] ]

    def totError2(self):
        return (0.5*(self.TotDown+self.TotUp))**2

    def statError(self):
        return [ [self.StatDown], [self.StatUp] ]

    def qRange(self):
        return [ [self.q2-self.q2low], [self.q2high-self.q2] ]

    def scaleByQ2(self):
        """
        Scale value and errors by q2 range width. Useful to convert Br into dBr/dq2
        """
        factor = 1./(self.q2high-self.q2low)
        return self.scaleLinear(factor,0.)

    def scaleLinear(self, factor = 1., offset = 0.):
        """
        Scale value by linear combination
        """
        self.obs      = factor*self.obs+offset
        if factor > 0 :
            self.StatUp   = factor*self.StatUp
            self.StatDown = factor*self.StatDown
            self.SystUp   = factor*self.SystUp
            self.SystDown = factor*self.SystDown
        else :  # invert 
            self.StatUp   = factor*self.StatDown
            self.StatDown = factor*self.StatUp
            self.SystUp   = factor*self.SystDown
            self.SystDown = factor*self.SystUp
        return self

    def plot(self,colour,fmt='o',label='',ls=None,theory=False,ax=None,el=None,ms=8):
        """
        The plotting function
        """
        if not el:
            if ls or self.ls: el = 1 # line width
            else : el = 2
        if (theory):
            rect = patches.Rectangle( (self.q2low,self.obs-self.StatDown), self.q2high-self.q2low, self.StatUp+self.StatDown, color=colour )
            ax.add_patch(rect)
#            eb1=plt.errorbar(self.q2,self.obs,xerr=self.qRange(),yerr=self.totError(),fmt=fmt,color=colour,capsize=10,label=label,elinewidth=el,capthick=el)
        else:
            eb1=plt.errorbar(self.q2,self.obs,xerr=self.qRange(),yerr=self.totError(),fmt=fmt,color=colour,capsize=4,label=label,elinewidth=el,capthick=el,markersize=ms)
        # eb2=plt.errorbar(self.q2,self.R,xerr=self.qRange(),yerr=self.statError(),fmt='o',color=colour,capsize=10)
        if ls or self.ls:
            if not ls : ls = self.ls
            eb1[-1][0].set_linestyle(ls)
            eb1[-1][1].set_linestyle(ls)

