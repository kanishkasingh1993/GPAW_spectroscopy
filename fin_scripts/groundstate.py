import os
import sys
import argparse
from gs import gs
from exc import exc
from recursion import recursion
from ase import Atoms
from ase.parallel import paropen
from ase.build import molecule
from ase.collections import g2
from ase import io
import gpaw.mpi as mpi
import numpy as np
import pandas as pd

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)


#print(os.environ['PYTHONPATH'])

if __name__ == '__main__':

	
	parser = argparse.ArgumentParser(description='For input files')
	parser.add_argument('-p', '--path', metavar='dir', type=str, nargs=1,
                        help='path where inp files are  (default ./)')
	
	parser.add_argument('-p2','--path2',metavar='dir',type=str,nargs=1, help='path where output files are')        

	parser.add_argument('-name','--name',type=str,nargs=1,help='xyz file name')

#	parser.add_argument('-num','--number',type=int,nargs=1,help='file number')

#	parser.add_argument('-procs','--nproc',type=int,nargs=1,help='total cores')	

#	parser.add_argument('-index','--ind',type=int,nargs=1,help='Index tbc')

	args = parser.parse_args()
  
	path=args.path[0]
	outpath=args.path2[0]
#	cores=args.nproc[0]
#	index=args.ind[0]

	a=10.0

	name=args.name[0]
	molecule=io.read(path+name)
	#print(molecule.get_atomic_numbers())
	molecule.cell=(a,a,a)
	
	df=pd.DataFrame(columns=['State','Energy'])
		
	#gs_1=4500.0300
	gs_1=gs(name,molecule,outpath)
	print("Ground state has been done")
	print(f'Ground state energy : {gs_1:.4f} eV')
	
	gs=np.round(gs_1,4)
	dicti={'State':'-1','Energy':gs}
	df = df.append(dicti, ignore_index = True)
	#df.set_index('State',inplace=True, drop=True)
	print(df.head())
	filepath=outpath+'/'+name[:-4]+'.csv'
	df.to_csv(filepath,index=False)  
	
	

