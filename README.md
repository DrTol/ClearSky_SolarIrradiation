# Clear-Sky Solar Irradiation
Calculation procedure for Clear-Sky Beam and Diffuse Solar Irradiance via following the Example 1, 3, and 4 in Chapter 14 of ASHRAE Handbook - Fundamentals (SI Edition). 

## Table of Contents
- [How2Use](README.md#how2use)
- [License](README.md#License)
- [Acknowledgement](README.md#Acknowledgement)
- [How2Cite](README.md#How2Cite)
- [References](README.md#References)

## How2Use
The idea here is to calculate the solar heat gain, as dependent to the time, on arbitrary surfaces (i.e. windows) based on the location of the case area. 

#### Inputs
- Longitude & Latitude 
- Day Light Saving 
- Time Zone 
- Local Standard Time Meridian
- Date & Time
- Tilt Angle of Surface (Σ  | Sigma in °)
- Surface Azimuth (Surface Orientation - Ψ | psi in °)

#### Considerations
- Calculation of local standard time and apparent solar time
- Solar Angles
  - Sun's altitude angle (β | beta in °)
  - Solar azimuth angle (Φ | phi in °)
- Equation of Time [minutes] as dependent to the day in a year
- Sun's Declination [°] as dependent to the day in a year
- Solar Hour Angle [°] as dependent to the time
- Relative air mass
- Beam optical depth (τ_b | tau_b)
- Diffuse optical depth (τ_d | tau_d)
- Air mass exponents (ab and ad)
- Extraterrestrial normal irradiance as dependent to the day in a year
  - Beam Normal Irradiance
  - Diffuse Normal Irradiance
  - Ground-Reflected Component
- Solar Heat Gain Factor
  - Coefficients for DSA glass for calculation of transmittance and absorptance
  - Transmitted Solar Heat Gain Factor (TSHGF) 
  - Absorbed Solar Heat Gain Factor (ASHGF) 
 
NOTE: you can get the values of beam and diffuse optical depth (τ_b | tau_b & τ_d | tau_d) according to the location of your case study via the reference [2]
 
## License
You are free to use, modify and distribute the code as long as authorship is properly acknowledged.

## Acknowledgement
Praise and thank to the Almighty Allah (SWT). In memory of my mother Esma Tol and my father Bekir Tol.

We would like to acknowledge all of the open-source minds in general for their willing of share (as apps or comments/answers in forums), which has encouraged our department to publish our tools developed.

## How2Cite


## References
1. ASHRAE Handbook - Fundamentals (SI Edition). 2009. ISBN: 978-1-933742-55-7. ISSN: 1523-282. 
2. ASHRAE CLIMATIC DESIGN CONDITIONS 2009/2013/2017. http://ashrae-meteo.info/v2.0/
3. Spindler, Henry C. | Residential Building Energy Analysis: Development and Uncertainty Assessment of a Simplified Model, M.Sc. Thesis, Massachusetts Institute of Technology
4. Inao Charlton, Chapter 4 | Solar Radiation in HVAC, https://www.slideshare.net/CharltonInao/chap4-solar-radiation-in-hvac
5. Oh, John Kie-Whan, An Effective Algorithm for Transmitted Solar Radiation Calculation through Window Glazing on a Clear Day, KIEAE Journal, 35-45
6. Hensen, Jan LM & Lamberts, Roberto. | Building Performance Simulation for Design and Operation. 
