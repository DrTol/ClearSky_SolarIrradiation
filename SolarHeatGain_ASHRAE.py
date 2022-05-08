# -*- coding: utf-8 -*-
"""
Solar Heat Gain
Written on Tue Jan 18 08:13:57 2022

@author: Hakan İbrahim Tol, PhD

References: 
ASHRAE Handbook Fundamentals (SI Edition), Ch. 14 Climatic Design Information. pp 188 - 204.
Spindler, Henry C. | Residential Building Energy Analysis: Development and Uncertainty Assessment of a Simplified Model, M.Sc. Thesis, Massachusetts Institute of Technology
Inao Charlton, Chapter 4 | Solar Radiation in HVAC, https://www.slideshare.net/CharltonInao/chap4-solar-radiation-in-hvac
Oh, John Kie-Whan, An Effective Algorithm for Transmitted Solar Radiation Calculation through Window Glazing on a Clear Day, KIEAE Journal, 35-45
Hensen, Jan LM & Lamberts, Roberto. | Building Performance Simulation for Design and Operation. 

"""

""" Libraries """

import datetime
import math
import numpy as np

""" User-Defined Functions """
# extraterrestrial radiant flux E_o [W/m2] (d : day in a year)
def E_o(d):
    E_sc=1367   # [W/m2] Solar constant
    
    return E_sc*(1+0.033*math.cos(math.radians(360/365*(d-3))))

# Equation of Time [minutes] (d : day in a year)
def EoT(d):
    
    Gamma=math.radians(360/365*(d-1))
    
    return 2.2918*(0.0075 + 0.1868*math.cos(Gamma) - 3.2077*math.sin(Gamma) -1.4615*math.cos(2*Gamma) - 4.089*math.sin(2*Gamma))

# Sun's Declination [°] (d : day in a year)
def sD(d):
    
    return 23.45*math.sin(math.radians(360/365*(d+284)))

# Solar Hour Angle [°]
def h(LST):
    
    return 15 * (-12 + LST.hour+LST.minute/60)

# Beam Optical Depth (m: month in a year)
def bod(m):
    # Data for Atlanta
    tau_b=[0.325,0.349,0.383,0.395,0.448,0.505,0.556,0.593,0.431,0.373,0.339,0.320]
    
    # # Data for İstanbul
    # tau_b=[0.354,0.386,0.430,0.457,0.451,0.449,0.460,0.470,0.444,0.408,0.376,0.357]
    
    return tau_b[m-1]

# Diffuse Optical Depth (m: month in a year)
def dod(m):
    # Data for Atlanta
    tau_d=[2.461,2.316,2.176,2.175,2.028,1.892,1.779,1.679,2.151,2.317,2.422,2.514]
    
    # # Data for İstanbul
    # tau_d=[2.210,2.057,1.931,1.892,1.986,2.046,2.015,1.973,2.011,2.107,2.167,2.217]
         
    return tau_d[m-1]

# # Validate the User-Defined Functions (see Table 2 - Ch 14 ASHRAE)
# d_l=np.array((21,52,80,111,141,172,202,233,264,294,325,355))  # Day in Year
# l_sD=np.array([sD(d) for d in d_l])                           # Sun's Declination 
# l_eT=np.array([EoT(d) for d in d_l])                          # Equation of Time
# l_E_o=np.array([E_o(d) for d in d_l])                         # Extraterrestrial Radiant Flux

""" Inputs """
longitude = -84.43          # [°]   E (negative in west)
latitude = 33.64            # [°]   N
DST=1                       # [h]   day light saving (Summer : 1 & Winter : 0)
TZ=-5                       # [h]   Time Zone (LSM = 15 * TZ)
LSM=15*TZ                   # [°]   Local standard time meridian (negative in western hemisphere)
# Time Zone Name  | TZ [Hours ±UTC] | Local Standard Meridian Longitude [°E]
# Newfoundland      -3.5                -52.5
# Atlantic          -4                  -60
# Eastern           -5                  -75
# Central           -6                  -90
# Mountain          -7                  -105
# Pacific           -8                  -120
# Alaska            -9                  -135
# Hawaii- Aleutian  -10                 -150

time = datetime.datetime (year = 2022, month = 7, day = 21, hour = 15, minute = 00, second = 00)

SC = 1                  # [-]   shading coefficient (value between 0 and 1)
rho_g = 0.2             # [-]   reflectance of ground (see: Table 5 Ground Reflectance of Foreground Surfaces | Ch. 14 Climatic Design Information - ASHRAE)

""" Solar Time """
# day of year
DoY=time.timetuple().tm_yday

# local standard time
LST=time-datetime.timedelta(hours=DST)
print('LST = ',LST)

# apparent solar time [Date Time]
AST=LST+datetime.timedelta(minutes=EoT(DoY))+datetime.timedelta(hours=(longitude-LSM)/15)
print('AST = ',AST)

# print('AST = ',AST)
# print('hour = ',AST.hour + AST.minute/60.0)
# print('Hour of Angle = ',h(AST))

""" Solar Angles """
# Sun's altitude angle (β | beta in °)
beta=math.degrees(math.asin(
    math.cos(math.radians(latitude))
    *math.cos(math.radians(h(AST)))
    *math.cos(math.radians(sD(DoY)))
    +math.sin(math.radians(latitude))
    *math.sin(math.radians(sD(DoY)))))

if beta>0:
    # Solar azimuth angle (Φ | phi in °)
    phi=math.degrees(math.acos(
        (math.sin(math.radians(beta))
         *math.sin(math.radians(latitude))
         -math.sin(math.radians(sD(DoY))))
        /(math.cos(math.radians(beta))
          *math.cos(math.radians(latitude)))))
    
    """ Clear-Sky Solar Radiation """
    # Relative air mass
    m=1/(math.sin(math.radians(beta))+0.50572*(6.07995+beta)**(-1.6364))
    
    # beam optical depth (τ_b | tau_b)
    tau_b=bod(AST.month)
    
    # diffuse optical depth (τ_d | tau_d)
    tau_d=dod(AST.month)
    
    # Air Mass Exponents (ab and ad)
    ab=1.219-0.043*tau_b-0.151*tau_d-0.204*tau_b*tau_d
    ad=0.202+0.852*tau_b-0.007*tau_d-0.357*tau_b*tau_d
    
    # Extraterrestrial normal irradiance (E_o) [W/m2]
    E_o=E_o(DoY)
    
    # Beam Normal Irradiance (E_b) [W/m2]
    E_b=E_o*math.exp(-tau_b*m**ab)
    
    # Diffuse Normal Irradiance (E_b) [W/m2]
    E_d=E_o*math.exp(-tau_d*m**ad)
    
    """ Surface Orientation """
    #   Surface Azimuth (Ψ | psi in ° - N 180° | NE -135° | E -90° | SE -45° | S 0° | SW 45° | W 90° | NW 135°)
    psi=0
    
    # surface-solar azimuth angle (γ | gamma in °)
    gamma=phi-psi
    
    if gamma>90 or gamma<-90:
        print('Surface is in shade')
        
        Et_b=0
        Et_d=0
        Et_r=0
        ASGH=0
        TSGH=0
        
    else:
    
        #   Tilt angle of surface (Σ  | Sigma in ° - 0° for a horizontal surface (face up), 180° for a horizontal surface (face down), and 90° for a vertical surface)
        sigma=90
        
        # Angle of incidence (Θ | theta in °)
        theta=math.degrees(math.acos(
            math.cos(math.radians(beta))*math.cos(math.radians(gamma))*math.sin(math.radians(sigma))+
            math.sin(math.radians(beta))*math.cos(math.radians(sigma))))  
        
        """ Clear-Sky Solar Irradiance Incident On Receiving Surface """
        # Beam Component (Et_b) [W/m2]
        Et_b=E_b*math.cos(math.radians(theta))
        
        # Diffuse Componenet (Et_d) [W/m2]
        Y=max(0.45,0.55+0.437*math.cos(math.radians(theta))+0.313*(math.cos(math.radians(theta)))**2)
        Et_d=E_d*Y
        
        # Ground-Reflected Component
        Et_r=(E_b*math.sin(math.radians(beta))+E_d)*rho_g*(1-math.cos(math.radians(sigma)))/2
        
        """ Solar Heat Gain Factor """
        # Coefficients for DSA glass for calculation of transmittance and absorptance
        a_j=np.array((0.01154, 0.77674, -3.94657, 8.57881, -8.38135, 3.01188))
        t_j=np.array((-0.00885, 2.71235, -0.62062, -7.07329, 9.75995, -3.89922))
        
        # transmitted solar heat gain factor (TSHGF) [W/m2]
        tau_D=0
        tau_d=0
        for index in range(len(t_j)):
            tau_D += t_j[index]*math.cos(math.radians(theta))
            tau_d += 2*t_j[index]/(index+2)
        
        TSGHF = Et_b * tau_D + Et_d * tau_d
        TSGH = SC * TSGHF
        
        # absorbed solar heat gain factor (ASHGF) [W/m2]
        alpha_D=0
        alpha_d=0
        for index in range(len(t_j)):
            alpha_D += a_j[index]*math.cos(math.radians(theta))
            alpha_d += 2*a_j[index]/(index+2)
        
        ASGHF = Et_b * alpha_D + Et_d * alpha_d
        ASGH = SC * ASGHF
        
        print('TSGH = ', TSGH)
        print('ASGH = ', ASGH)
    
else: # beta < 0 : Negative values corresponds to night time
    print('Night Time')
    Et_b=0
    Et_d=0
    Et_r=0
    ASGH=0
    TSGH=0
