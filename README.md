# radXiFoam
CFD simulation solver with flamelet progress variable combustion model with radiation heat transfer.

## Overview
radXiFoam is an open source simulation tool for studying premixed flames. The solver is based on the XiFoam code developed by [OpenCFD Ltd.](http://openfoam.com/). 
The following models have been added.
* powerLaw (constant/combustionProperties/laminarFlameSpeedCorrelation)
* vaporInhomogeneousMixture (constant/thermophysicalProperties/mixture)
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
- A usage example and result of alphaBetaCalc.py are as follows.


- alphaBetaCalc.py is written based on the hydrogen flame. If other fuels are used, please calculate the mass fraction accordingly.
- It was confirmed that the p1 radiation model works normally (constant/radiationProperties/radiationModel). If you desire to exclude the calculation of radiative heat transfer, you can set the radiation model to "none".

- Hope the following tutorial case will help you to use radXiFoam.

## Tutorial case
The tutorial case simulated the SRI-402 experiment. This is an experiment to study the effect of a barrier when a tent filled with hydrogen gas explodes.

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
- Run 'decomposepar'
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
1. 

