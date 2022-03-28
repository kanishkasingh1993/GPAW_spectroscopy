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

setup_paths.insert(0, '.')


def dks(file_name,mol,outpath):
	name = file_name
	path=outpath
	f_name=outpath+name+'.txt'
	exc_name=outpath+name+'_exc.txt'
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

	calc1 = GPAW(h=0.2,
             txt=f_name,
             xc='PBE',mixer=Mixer(0.02, 5, 100),eigensolver=Davidson(3))
	atoms.calc = calc1
	e1 = atoms.get_potential_energy() + calc1.get_reference_energy()

	calc2 = GPAW(h=0.2,
             txt=exc_name,
             xc='PBE',
             charge=-1,
             spinpol=True,
             occupations=FermiDirac(0.0, fixmagmom=True),
             setups={0: 'fch1s'},mixer=Mixer(0.02, 5, 100),eigensolver=Davidson(3))
	atoms[0].magmom = 1
	atoms.calc = calc2
	e2 = atoms.get_potential_energy() + calc2.get_reference_energy()

	#with paropen('dks.result', 'w') as fd:
    	#	print('Energy difference:', e2 - e1, file=fd)
	dks=e2-e1

	return dks
