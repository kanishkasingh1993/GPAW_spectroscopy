import sys
import numpy as np
from gpaw import GPAW, setup_paths
from gpaw.xas import XAS
import matplotlib.pyplot as plt
import pandas as pd
from ase import Atoms
from gpaw.xas import RecursionMethod

setup_paths.insert (0,'.')




def specmake(mol,spec_path,calc_name,dks,index) :
	sys.setrecursionlimit (10000)
	file_name=mol
	name = calc_name
	print(name)



	dks_energy = dks  # from dks calcualtion

	calc = GPAW(calc_name)

	xas = XAS(calc, mode='xas')
	x, y = xas.get_spectra(fwhm=0.5, linbroad=[4.5, -1.0, 5.0])
	x_s, y_s = xas.get_spectra(stick=True)

	shift = dks_energy - x_s[0]  # shift the first transition

	y_tot = y[0] + y[1] + y[2]
	y_tot_s = y_s[0] + y_s[1] + y_s[2]

#	plt.plot(x + shift, y_tot)
#	plt.bar(x_s + shift, y_tot_s, width=0.05)
	#plt.savefig('xas_h2o_spectrum.png')

#	plt.savefig (spec_path+file_name+"_"+str(index)+"_spectrum.png")
	#spec_array=np.column_stack((x_s+shift,y_tot_s))
	#np.savetxt(spec_path+file_name+"_"+str(index)+'.csv', spec_array, delimiter=',')
#	plt.close()
	df=pd.DataFrame({'Energy':x_s+shift,'Intensity':y_tot_s})
	x_min=min(x_s+shift)
	x_max=max(x_s+shift)
	return df,x_min,x_max 
