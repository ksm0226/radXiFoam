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
radXiFoam takes inputs based on mass fraction.
The alphaBetaCalc.py tool allows the determination of the mass fraction of fuel (0/ft), water vapor (0/wv), nitrogen (0/n2), equivalence ratio  (constant/combustionProperties/equivalenceRatio), and alpha, beta (constant/combustionProperties/powerLawCoeffs).
alphaBetaCalc.py 의 사용 예시는 다음과 같습니다.



The tutorial case and alphaBetaCalc.py are written based on the hydrogen flame.
If other fuels are used, please calculate the mass fraction accordingly.

It was confirmed that the p1 radiation model works normally.(constant/radiationProperties/radiationModel)
If you desire to exclude the calculation of radiative heat transfer, you can set the radiation model to "none".

Hope the following tutorial case will help you to use radXiFoam.

## Tutorial case
tutorial case 는 SRI-402 실험을 모사 하였습니다. 수소가스로 가득찬 텐트가 폭발할때 방호벽 효과에 대한 연구한 실험 입니다. (ref.2)


- Unzip tutorial.zip
- Source OpenFOAM v2112
- run blockMesh
- run phthon alphaBetaCalc.py 
- Input the alphaBetaCalc.py results (ft, wv and n2) in system/setFieldsDict
  - system/setFieldsDict/defaultFieldValues is for the initial condition outside the tent
  - system/setFieldsDict/regions/boxToCell is for the initial condition inside the tent
  - system/setFieldsDict/regions/sphereToCell is for the ignitin condition

- Enter equivalence ratio, alpha and beta in constant/combustionProperties
- The w value in constant/combustionProperties/powerLawCoeff is the Su0 (reference laminar flame speed). 
 - In general, it is set by referring to the paper of the laminar flame speed test result for each type of fuel.



## Algorithm
XiFoam calculates the laminar flame speed (u) value according to the ambient temperature and pressure, and the fuel to oxidizer ratio. Calculate the flame wrinkling (Xi) value according to the turbulence intensity and Reynolds number to derive the turbulent flame speed (St) value. In the compressible turbulent combustion model, the value of St controls the propagation of the regress variable (b). Instead of the progress variable (c) used in general FPV models, XiFoam uses the regress variable (b, b = 1 - c).
The mass fraction of compositions in the computation cell before and after combustion is determined by the value of b. As much as the mass fraction changes, the Cp and h values in the cell change, that is, the temperature changes.
This code discretizes the momentum, energy, and continuity conservation equations of a compressible gas in the FVM method and is solved according to the following algorithm.

- 1. Initialize simulation data, turbulent, combustion and radiation model
- 2. WHILE t < tend DO
 - 1.	Update Δt for stability (CFL condition)
 - 2.	Solve rho equation
 - 3.	Do pressure-velocity PIMPLE corrector loop
  - 1. Solve U equation
  - 2. Solve ft equation (wv, n2 continuity eqns 여기에)
  - 3. Solve b equation
   - 1.	Calculate combustion properties (Xi, Su)
  - 4. Solve energy (Eau, Ea) equations
   - 1.	Update T
  - 5. Do pressure PISO corrector loop
   - 1. Solve p equation
   - 2. Correct p
  - 6. LOOP
 - 4.	Correct U
 - 5.	LOOP
- 3. LOOP

