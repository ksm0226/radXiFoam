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
The tutorial case and alphaBetaCalc.py are written based on the hydrogen flame.
If other fuels are used, please calculate the mass fraction accordingly.

It was confirmed that the p1 radiation model works normally.(constant/radiationProperties/radiationModel)
If you desire to exclude the calculation of radiative heat transfer, you can set the radiation model to "none".

Hope the following tutorial case will help you to use radXiFoam.

## Tutorial case
- Unzip tutorial.zip
- Source OpenFOAM v2112
- 
