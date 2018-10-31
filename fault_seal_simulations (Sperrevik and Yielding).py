import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import colors
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import pandas as pd
import random
import sklearn as sci

# default variables ()
y_hw=30 #fluid tension for HC dynes/cm
y_ma=480 #fluid tension for mercury and air dynes/cm
theta_hw=30 # contact angle for HC degrees
theta_ma=40 #contact angle for for mercury and air degrees
g=9.8 #gravitational constant, m/s^s
den_water=1.030 #water density g/cm^3
den_hw=0.700 #HC density g/cm^3

#Sperrevik's coefficients, where a - constatnt
a1=80000
a2=19.4
a3=0.00403
a4=0.0055
a5=12.5

# create lists of random variables: SGR, Zmax and Throw
SGR_list = []
for i in range(0,10000):
    x = random.randint(1,100)
    SGR_list.append(x)

Zmax_list = []
for i in range(0,10000):
    y = random.randint(10,8000)
    Zmax_list.append(y)

Throw_list = []
for i in range(0,10000):
    z = random.randint(10,2000)
    Throw_list.append(z)
#convert to arrays
SGR = np.asarray(SGR_list)
Zmax = np.asarray(Zmax_list)
Throw = np.asarray(Throw_list)

# calculation Sperrevik's Kf 
Kf_ma=a1*np.exp(-(a2*(SGR/100)+a3*Zmax+(((Zmax-Throw)*a4)-a5)*((1-SGR/100)**7)))

# 1) mercury-Air threshold pressure from Kf (psi)
Pf_cma=31.838*(Kf_ma**-0.3848)
#2) HC-water capillary pressure (psi)
TP=(y_hw*np.cos(np.deg2rad(theta_hw))*Pf_cma)/(y_ma*np.cos(np.deg2rad(theta_ma)))
#3) # Sperrevik's HC column heights calculations (feet)
HC_Sper=TP/(0.433*(den_water-den_hw))

# getting a combined matrix with pandas
data = {'SGR': SGR, 'Zmax': Zmax, 'Throw':Throw, 'Zf':(Zmax-Throw), 'Kf_ma':Kf_ma, 'TP':TP, 'HC_Sper':(HC_Sper*0.3048)}
df = pd.DataFrame(data)

# calculation Yielding's (2010) Bouyancy pressure (psi) from random SGR values

df.loc[df['Zmax'] < 3000, 'BP'] = (df.SGR*0.175-3.5)*14.5038
df.loc[df['Zmax'] > 3500, 'BP'] = (df.SGR*0.15+1.9)*14.5038
df.loc[((df['Zmax'] > 3000) & (df['Zmax'] < 3500)), 'BP'] = (df.SGR*0.17+0.92)*14.5038


# calculation Yielding's (2010) HC column heights (m)
df ['HC_Yield'] = (df.BP/(0.433*(den_water-den_hw)))*0.3048

# removing negatives
df = df[df['Zf'] > 0]

# plotting it together - HC height vs Zmax SGR colorcoded
xS = df.HC_Sper
xY= df.HC_Yield
y = df.Zmax
colors = df.SGR
plt.rcParams.update({'font.size': 20})
cmap = plt.get_cmap('jet')
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2,figsize=(32, 8))
ax1.scatter(xS, y, c=colors, norm=norm, alpha=1, s=5)
cax=ax1.scatter(xS, y, c=colors, norm=norm, alpha=1, s=5)
ax1.set_title('HC column heights simulations using Sperrevik et al (2002)')
ax1.set_xlabel('HC column height,m')
ax1.set_ylabel('Zmax (maximum fault depth), m')
ax1.set_xlim(0.1, 10000000)
ax1.set_ylim(50, 8000)
ax1.set_yscale('log')
ax1.set_xscale('log')
ax1.invert_yaxis()
cbar = fig.colorbar(cax)
cbar.ax.set_ylabel('SGR,%', rotation=90)

ax2.scatter(xY, y, c=colors, norm=norm, alpha=1, s=5)
ax2.set_title('HC column heights simulations using Yielding et al (2010)')
ax2.set_xlabel('HC column height,m')
ax2.set_ylabel('Zmax (maximum fault depth), m')
ax2.set_xlim(5, 600)
ax2.set_ylim(50, 8000)
ax2.set_yscale('log')
ax2.set_xscale('linear')
ax2.invert_yaxis()