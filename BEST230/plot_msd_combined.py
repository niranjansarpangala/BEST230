import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from math import exp,sqrt,cos,sin
import numpy as np
#from mfpt import *
import pandas as pd
from plot_class import *
import os
import sys
def plot_function_multiple_data(x,y,legend_holder,xlab,ylab,fnam,log_scal):
    fig, ax =plt.subplots(figsize=(8,8))
    [lfsiz,llsiz]=[20,15]
    count=0
    for y1 in y:
        ax.plot(x,y1,'.-',label=legend_holder[count])
        count+=1
    ax.set_xlabel(xlab,fontname='serif',fontsize=lfsiz)
    ax.set_ylabel(ylab,fontname='serif',fontsize=lfsiz)
    if log_scal==1:
        ax.set_yscale('log')
    elif log_scal==2:
        ax.set_yscale('log')
        ax.set_xscale('log')
    elif log_scal==3:
        ax.set_xscale('log')
    ax.minorticks_on()
    ax.legend()
    #ax.set_ylim(1e-3,2)
    ax.tick_params(axis='both', direction='in',which='both', labelsize=llsiz)
    ax.tick_params(axis='both',which='major',length=10,width=1.5 )
    ax.tick_params(axis='both',which='minor',length=4,width=0.5 )
    plt.show()
    fig.savefig(fnam+".png")
    fig.savefig(fnam+".svg",format='svg', dpi=1200)
    fig.savefig(fnam+".eps",format='eps', dpi=1000)
    
#data = pd.read_csv(os.getenv("HOME")+'/data/uttam_project/Test/1541192728/0.csv')
#data.columns = ['time','x','y','stat']
#print(data['time'])

#SIMS=["A422","A441","A442","A443","A444","A432","A433","A434","A412","A413"]
#LEG=["N=96 D=0.6, ON=50","N=96 D=10 ON=5","N=96 D=10 ON=50","N=96 D=10 ON=200","N=96 D=10 ON=800","N=96 D=1.3 ON=50","N=96 D=1.3 ON=200","N=96 D=1.3 ON=800","N=96 D=0.06 ON=50","N=96 D=0.06 ON=200"]


#SIMS=["A412","A422","A432","A442","sim5"]
#LEG=["N=96 D=0.06 ON=50","N=96 D=0.6, ON=50","N=96 D=1.3 ON=50","N=96 D=10 ON=50","N=96 D=1.3 Infinite on rate"]
#SIMS=["A432","A433","A434","sim5"]
#LEG=["N=96 D=1.3 ION=50","N=96 D=1.3 ON=200","N=96 D=1.3 ON=800","N=96 D=1.3 Infinite on rate"]
#SIMS=["test_l_1","sim3"]
#LEG=["N=24 ON=800","N=24 Infinite on"]
#SIMS=["B122_2","B122_5","B122"]
#LEG=["S=200","S=500","S=2000"]
#SIMS=["B111","B112","B113","B114"]
SIMS=["B121","B122","B123","B124","B120"]
#sting1=r'$N=12 \, D=1.3 \mu m^2/s $'
LEG=[ r'$ N=12 \ D=1.3 \mu m^2/s \ \pi_o=5s^{-1}$',r'$ N=12 \ D=1.3 \mu m^2/s \ \pi_o=50s^{-1}$',r'$ N=12 \ D=1.3 \mu m^2/s \ \pi_o=200s^{-1}$',r'$ N=12 \ D=1.3 \mu m^2/s \ \pi_o=800s^{-1}$',r'$ N=12 \ D=1.3 \mu m^2/s \ PRE MODEL$']
MX=[]
MY=[]
def msd(SIMS,LEG):
    simlist=[SIMS[0]]
    a=analyse(simlist)
    for count in range(len(SIMS)):
        sim=SIMS[count]
        lab=LEG[count]
        print(sim,lab)
        simlist=[sim]
        a=analyse(simlist)
        r=result(simlist[0])
        r.mkdir(r.resdir)
        a.get_samdirs()
        [time,msd]=a.msd_calc()
        MX.append(np.log10(time))
        MY.append(np.log10(msd))
    r.curdir=r.curdir=r.chandra+"msd_04_Dec"
    r.mkdir(r.curdir)
    r.curdir=r.curdir+"/AM1"
    r.mkdir(r.curdir)
    a.master_plot_run_length(r.curdir,MX,MY,LEG,"time (s)","MSD",'msd_plot')
#msd(SIMS,LEG)
def msd_single(SIMS,LEG):
    simlist=[SIMS[0]]
    a=analyse(simlist)
    for count in range(len(SIMS)):
        sim=SIMS[count]
        lab=LEG[count]
        print(sim,lab)
        simlist=[sim]
        a=analyse(simlist)
        r=result(simlist[0])
        r.mkdir(r.resdir)
        a.get_samdirs()
        [time,msd]=a.msd_calc()
        mx=np.log10(time)
        my=np.log10(msd)
        mxn=[]
        myn=[]
        for ii in range(len(mx)):
            if mx[ii]> -1.0 and mx[ii]< 1.2:
                mxn.append(mx[ii])
                myn.append(my[ii])
        mxn=np.array(mxn)
        myn=np.array(myn)
        [po,p1]=np.polyfit(mxn,myn,1)
        myn2=po*mxn+p1
        print(po)
        [fig,ax]=a.plot_generator()
        [fig,ax]=a.plot_fit([fig,ax],mx,my,mxn,myn2,lab,'fit, slope:'+str(round(po,4)),count)
        r.curdir=r.curdir=r.chandra+"msd_04_Dec"
        r.mkdir(r.curdir)
        r.curdir=r.curdir+"/AM4"
        r.mkdir(r.curdir)
        [fig,ax]=a.titler([fig,ax],"Simname:"+sim+" Exponent: "+str(po))
        a.axis_modify([fig,ax],r.curdir,r'$log_{10}(t)$',r'$log_{10} (MSD)$','msd'+str(sim),3)
#msd_single(SIMS,LEG)
def msd_combined(SIMS,LEG):
    simlist=[SIMS[0]]
    a=analyse(simlist)
    [fig,ax]=a.plot_generator()
    for count in range(len(SIMS)):
        sim=SIMS[count]
        lab=LEG[count]
        print(sim,lab)
        simlist=[sim]
        a=analyse(simlist)
        r=result(simlist[0])
        r.mkdir(r.resdir)
        a.get_samdirs()
        [time,msd]=a.msd_calc()
        mx=np.log10(time)
        my=np.log10(msd)
        mxn=[]
        myn=[]
        for ii in range(len(mx)):
            if mx[ii]> -1.0 and mx[ii]< 1.2:
                mxn.append(mx[ii])
                myn.append(my[ii])
        mxn=np.array(mxn)
        myn=np.array(myn)
        [po,p1]=np.polyfit(mxn,myn,1)
        myn2=po*mxn+p1
        print(sim,po)
        [fig,ax]=a.plot_fit([fig,ax],mx,my,mxn,myn2,lab,'fit, slope:'+str(round(po,4)),count)
    r.curdir=r.curdir=r.chandra+"msd_04_Dec"
    r.mkdir(r.curdir)
    r.curdir=r.curdir+"/AM5_combined_500"
    r.mkdir(r.curdir)
    a.axis_modify([fig,ax],r.curdir,r'$log_{10}(t)$',r'$log_{10} (MSD)$','msd_combined',1)
msd_combined(SIMS,LEG)

def radial_distribution(SIMS):
    for count in range(len(SIMS)):
        sim=SIMS[count]
        lab=LEG[count]
        print(sim,lab)
        simlist=[sim]
        a=analyse(simlist)
        r=result(simlist[0])
        r.mkdir(r.resdir)
        a.get_samdirs()
        fig_arr=a.plot_boundary()
        fig_arr=a.rad_theta_distribution(fig_arr,lab)
        r.curdir=r.curdir=r.chandra+"27_Nov"
        r.mkdir(r.curdir)
        a.axis_modify(fig_arr,r.curdir,'x','y','density2'+str(sim))
#radial_distribution(SIMS)
#fig, ax =plt.subplots(figsize=(8,8))
#ax=data.plot(x='x',y='y',ax=ax)
#plt.show()



#df = pd.DataFrame([[w.time,w.x,w.y,w.stat]],columns=['time','x','y','stat'])
