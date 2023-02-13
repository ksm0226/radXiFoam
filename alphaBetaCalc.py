# Order: H2, O2, N2, H2O

H2_vf = float(input("H2 volume fraction: "))
H2O_vf = float(input("H2O volume fraction: "))
O2_vf = (1-(H2_vf+H2O_vf))*0.21
N2_vf = (1-(H2_vf+H2O_vf))*0.79

mm = [2, 32, 28, 18]

vf = [H2_vf, O2_vf, N2_vf, H2O_vf]

mf = []
mTot = 0

for i in range(4):
	mTot = mTot + (mm[i] * vf[i])

for i in range(4):
	mf.append((mm[i] * vf[i]) / mTot)
	
H2_ratio = mf[0] / mf[1]
H2_eq_ratio = H2_ratio / 0.125 # 0.125 = stoichiometry H2/O2 mass ratio

H2_alpha = 2.18 - (0.8 * (H2_eq_ratio - 1))


H2_beta = -0.16 + 0.22 * (H2_eq_ratio - 1)


print("===============================================")
print("H2 mass fraction: ", mf[0])
print("H2O mass fraction: ", mf[3])
print("N2 mass fraction: ", mf[2])
print("equivalence ratio: ", H2_eq_ratio)
print("H2 alpha: ", H2_alpha)
print("H2 beta: ", H2_beta)
print("===============================================")

'''
How to use
In terminal, type
	python alphaBetaCalc.py
'''
