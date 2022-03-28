import sys
import argparse
import numpy as np
import pickle
from spectra import specmake
import pandas as pd
from numpy import genfromtxt
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

from os import listdir
from os.path import isfile, join

def spectrum(E,osc,sigma,x):
    gE=[]
    for Ei in x:
        tot=0
        for Ej,os in zip(E,osc):
            tot+=os*np.exp(-((((Ej-Ei)/sigma)**2)))
        gE.append(tot)
    return gE


#ARGS
parser = argparse.ArgumentParser(description='For input files')
parser.add_argument('-inp', '--inpath', metavar='dir', type=str, nargs=1,
                        help='path where inp files are  (default ./)')
parser.add_argument('-spec','--spectpath',metavar='dir',type=str,nargs=1,
                        help='path where script will be saved')
#parser.add_argument('-f','--inpfile',metavar='str',type=str,nargs=1,
#                       help='name of input xyz file')

#Declaring variables for ase calc

args = parser.parse_args()

ase_inp=args.inpath[0]
og_spec_path=args.spectpath[0]
input_file_arr= [f for f in listdir(ase_inp) if isfile(join(ase_inp, f))]
#input_file_arr=['Methane.xyz']

for input_file  in input_file_arr :
	molname=input_file[:-4]
#index=[1,2,3]
	spec_path=og_spec_path+molname+'/'


#calc_path="/home/singhk93/output_files/acrolei/acrolein_2_xas.gpw"

## retreive df with energies and get index/dks values

	df_spec=pd.read_csv(spec_path+molname+'.csv',index_col=False)
	print(df_spec.head())
	df_spec['dks'] = df_spec['Energy']
	print(df_spec.head())
	gs_energy=df_spec.loc[df_spec['State'] == -1, 'Energy'].item()
	print(gs_energy)

	df_spec['dks']=df_spec['dks']-gs_energy
	print(df_spec.head())
	index=df_spec['State'].tolist()
	dks=df_spec['dks'].tolist()
	index.pop(0)
	dks.pop(0)
	print(index)
	print(dks)
	#dks=[283.1307,283.3986,284.7049]
	df_dict={}
	df_list=[]

######## spectra utils ###########
	x_min=[]
	x_max=[]
	calc_path=spec_path+molname+'_'

	for i in range(len(dks)):
		print(dks[i],index[i])
		new_calc_path=calc_path+str(index[i])+"_xas.gpw"
		#calc_path="/home/singhk93/output_files/acrolei/acrolein_"+str(index[i])+"_xas.gpw"
		xyz_name=molname+'.xyz'
		df,x_mini,x_maxi=specmake(molname,spec_path,new_calc_path,dks[i],index[i])
	#x_mini=min(df['Energy'])
	#x_maxi=max(df['Energy'])
		df_dict[i]=df
		df_list.append(df)
		x_min.append(x_mini)
		x_max.append(x_maxi)

	spec_combine=pd.concat(df_list)
	print(spec_combine.head())
	df_dict['Total']=spec_combine

#########################For making spectra dynamically ######################
	min_x=np.floor(min(x_min))-1
	max_x=np.ceil(max(x_max))+1

	x=np.linspace(min_x,max_x, num=500, endpoint=True)
	gE_arr=[]
	sigma=0.5
	keys=list(df_dict.keys())
	print(keys)
	for i in range(len(keys)):
		df=df_dict.get(keys[i])
		temp=spectrum(df['Energy'],df['Intensity'],sigma,x)
		gE_arr.append(temp)

	color = iter(cm.rainbow(np.linspace(0, 1, len(dks))))

	
	for i in range(len(keys)-1):
		
		plt.plot(x,gE_arr[i],'k',label=f'C{i+1}')
		plt.savefig(spec_path+molname+'_'+str(i)+'.png')
		plt.close()

	for i in range(len(keys)-1):
		c = next(color)
		plt.fill(x,gE_arr[i],c=c,label=f'C{i+1}')
	plt.plot(x,gE_arr[-1],"k",label='Total')
	plt.legend()
	plt.savefig(spec_path+molname+'.png')
	plt.close()

	f = open(spec_path+molname+'.pkl',"wb")
	pickle.dump(df_dict,f)
	f.close()
