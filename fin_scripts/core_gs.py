import matplotlib.pyplot as plt
from math import pi, cos, sin
import numpy as np
import sys
from ase import Atoms
from ase.parallel import paropen
from gpaw import GPAW,FermiDirac
from gpaw.xas import RecursionMethod
from gpaw import Davidson
from gpaw import Mixer, MixerSum, MixerDif
from gpaw import setup_paths
#from gpaw.scf import Energy

setup_paths.insert(0, '.')


def core_gs(file_name,mol,index,outpath):
	name = file_name
	path=outpath
	new_name=name[:-4]+"_"+str(index)
	f_name=outpath+new_name+'.txt'
	calc_name=outpath+new_name+'_xas.gpw'

	convergence = {'energy': 0.001}

	#a = 12.0  # use a large cell

	#d = 0.9575
	#t = pi / 180 * 104.51
	#atoms = Atoms('OH2',
        #      [(0, 0, 0),
        #       (d, 0, 0),
        #       (d * cos(t), d * sin(t), 0)],
        #      cell=(a, a, a))
	
	atoms=mol
	atoms.center()
	#atoms.set_pbc(True)
	calc = GPAW(h=0.2,nbands=-30,
             txt=f_name,
             xc='PBE',mixer=Mixer(0.02, 3, 100),eigensolver=Davidson(3), setups={index: 'hch1s'},convergence=convergence)
	atoms.calc = calc
	e1 = atoms.get_potential_energy() + calc.get_reference_energy()
	calc.write(calc_name)
	
	return e1
