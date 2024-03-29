# radXiFoam
CFD simulation solver for flamelet progress variable (FPV) combustion model with radiation heat transfer.

## Overview
radXiFoam is an open source simulation tool for studying premixed flames. The solver is based on the XiFoam code developed by [OpenCFD Ltd.](http://openfoam.com/). 
The following models have been added.
* powerLaw (constant/combustionProperties/laminarFlameSpeedCorrelation) - for laminar flame speed
* vaporInhomogeneousMixture (constant/thermophysicalProperties/mixture) - for calculation of mixture fraction after combustion
* vaporGreyMeanAbsorptionEmission (constant/radiationProperties/absorptionEmissionModel) - for calculating the radiative absorption coefficient of water vapor  
* radiation heat transfer

radXiFoam can be used for:
* premixed flame in confined/unconfined spaces 
* deflagration explosion

## Installation
- Unzip SRC.zip
- Source OpenFOAM v2112
- Execute "Allwmake.sh" to compile the solver and source codes

## Usage
- radXiFoam takes inputs based on mass fraction.
- The alphaBetaCalc.py tool allows the determination of the mass fraction of fuel (0/ft), water vapor (0/wv), nitrogen (0/n2), equivalence ratio  (constant/combustionProperties/equivalenceRatio), and alpha, beta (constant/combustionProperties/powerLawCoeffs).
- alphaBetaCalc.py is written based on the hydrogen fuel. If other fuels are used, please calculate the mass fraction accordingly.
- It was confirmed that the p1 radiation model works normally (constant/radiationProperties/radiationModel). 
  - If you desire to exclude the calculation of radiative heat transfer, you can set the radiation model to "none".

- Hope the following tutorial case will help you to use radXiFoam.

## Tutorial case
The tutorial case simulated the SRI-402 experiment. This is an experiment to study the effect of a barrier when a tent filled with hydrogen gas explodes.
Details related to this experiment can be found in ref. 2.

- Unzip tutorial.zip
- Source OpenFOAM v2112
- Run 'blockMesh'
- If you want to change the composition of a gas, run 'phthon alphaBetaCalc.py'
  - Enter the alphaBetaCalc.py results (ft, wv and n2) in system/setFieldsDict
    - system/setFieldsDict/defaultFieldValues is for the initial condition outside the tent
    - system/setFieldsDict/regions/boxToCell is for the initial condition inside the tent
    - system/setFieldsDict/regions/sphereToCell is for the ignitin condition
  - Enter equivalence ratio, alpha and beta in constant/combustionProperties
  - The w value in constant/combustionProperties/powerLawCoeff is the Su0 (reference laminar flame speed). 
    - In general, it is set by referring to the paper of the laminar flame speed test result for each type of fuel. (ref. 3)
- Set the number of cores (#) to use for compute in system/decomposeParDict/numberOfSubdomains.
  - Since the mesh in the tutorial case consists of 1.2 million cells, it is recommended to run in parallel.  
- Run 'decomposePar'
- Run 'mpirun -np # radXiFoam -parallel'

## Algorithm
XiFoam calculates the laminar flame speed (Su) value according to the ambient temperature and pressure, and the fuel to oxidizer ratio. Calculate the flame wrinkling (Xi) value according to the turbulence intensity and Reynolds number to derive the turbulent flame speed (St) value. In the compressible turbulent combustion model, the value of St controls the propagation of the regress variable (b). Instead of the progress variable (c) used in general FPV models, XiFoam uses the regress variable (b, b = 1 - c).
The mass fraction of the compositions within a computational cell before and after combustion is determined by the value of b. As the mass fraction changes, the values of Cp and h in the cell are altered, resulting in a change in temperature.

This code discretizes the momentum, energy, and continuity conservation equations of a compressible gas in the FVM method and is solved according to the following algorithm.

 1. Initialize simulation data, turbulent, combustion and radiation model
 2. WHILE t < t_end DO
 - 1.	Update Δt for stability (CFL condition)
 - 2.	Solve rho equation
 - 3.	Do pressure-velocity PIMPLE corrector loop
   * 1. Solve momentum (U) equation
   * 2. Solve transport (ft, wv, n2) equation
   * 3. Solve transport (b) equation
    *  - Calculate combustion properties (Xi, Su)
   * 4. Solve energy (Eau, Ea) equations
    *  - Update T
   * 5. Do pressure PISO corrector loop
    *  - Solve p equation
    *  - Correct p
   * 6. LOOP
 - 4.	Correct U
 - 5.	LOOP
 3. LOOP

## References
1. Kim, S., & Kim, J. (2022). Effect of radiation model on simulation of water vapor-hydrogen premixed flame using flamelet combustion model in OpenFOAM. Nuclear Engineering and Technology, 54(4), 1321-1335.
2. Kang, H. S., Kim, S. M., & Kim, J. (2022). Safety issues of a hydrogen refueling station and a prediction for an overpressure reduction by a barrier using OpenFOAM software for an SRI explosion test in an open space. Energies, 15(20), 7556.
3. Konnov, A. A., Mohammad, A., Kishore, V. R., Kim, N. I., Prathap, C., & Kumar, S. (2018). A comprehensive review of measurements and data analysis of laminar burning velocities for various fuel+ air mixtures. Progress in Energy and Combustion Science, 68, 197-267.

