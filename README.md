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
