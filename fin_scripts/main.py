import os
import time
import sys
import argparse
from gs import gs
from exc import exc
from ase import Atoms
from ase.parallel import parprint
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

	parser.add_argument('-num','--number',type=int,nargs=1,help='file number')

#	parser.add_argument('-procs','--nproc',type=int,nargs=1,help='total cores')	

	parser.add_argument('-index','--ind',type=int,nargs=1,help='Index tbc')

	args = parser.parse_args()
  
	path=args.path[0]
	outpath=args.path2[0]
#	cores=args.nproc[0]
	index=args.ind[0]

	a=10.0

	name=args.name[0]
	molecule=io.read(path+name)
	#print(molecule.get_atomic_numbers())
	molecule.cell=(a,a,a)
	
	#es_1=4000.234
	es_1=exc(name,molecule,outpath,index)
	parprint("Excited state has been done")
	parprint(f'Excited state energy : {es_1:.4f} eV')

	es=np.round(es_1,4)
	time.sleep(int(index)*2.0)
	df=pd.read_csv(outpath+name[:-4]+'.csv')
	print(df.head())
	#df.reset_index(drop=True,inplace=True)  
	df2=pd.DataFrame({'State':[index],'Energy':[es]})
	#df2.set_index('State', inplace=True, drop=True)

	#print(df2.head())
	df = pd.concat([df,df2],ignore_index=True,axis=0)
	#df.reset_index(drop=True, inplace=True) 
	#print(df.head())
	df.to_csv(outpath+name[:-4]+'.csv',index=False)
