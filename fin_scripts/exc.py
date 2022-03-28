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


def exc(file_name,mol,outpath,index):
	name = file_name
	path=outpath
	f_name=outpath+name+'.txt'
	exc_name=outpath+name+'_exc'+str(index)+'.txt'
	#a = 12.0  # use a large cell

	#d = 0.9575
	#t = pi / 180 * 104.51
	#atoms = Atoms('OH2',
        #      [(0, 0, 0),
        #       (d, 0, 0),
        #       (d * cos(t), d * sin(t), 0)],
        #      cell=(a, a, a))
	convergence = {'energy': 0.001}
	atoms=mol
	atoms.center()
	#atoms.set_pbc(True)
	#calc1 = GPAW(h=0.2,
        #     txt=f_name,
        #     xc='PBE',mixer=Mixer(0.02, 5, 100),eigensolver=Davidson(3))
	#atoms.calc = calc1
	#e1 = atoms.get_potential_energy() + calc1.get_reference_energy()

	calc2 = GPAW(h=0.2,
             txt=exc_name,
             xc='PBE',
             charge=-1,
             spinpol=True,
             occupations=FermiDirac(0.05,fixmagmom=True),
             setups={(index): 'fch1s'},mixer=MixerDif(0.02, 3, 100),eigensolver=Davidson(3),convergence=convergence)
	atoms[0].magmom = 1
	atoms.calc = calc2
	e2 = atoms.get_potential_energy() + calc2.get_reference_energy()

	#with paropen('dks.result', 'w') as fd:
    	#	gggg = {'energy': Energy(tol=0.0005, n_old=4)}Energy difference:', e2 - e1, file=fd)
	#dks=e2-e1

	return e2
