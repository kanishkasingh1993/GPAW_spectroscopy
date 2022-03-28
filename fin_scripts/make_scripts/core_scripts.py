from ase import Atom
from ase.build import molecule
from ase import io
import os
import sys
import argparse

from os import listdir
from os.path import isfile, join


#ARGS 
parser = argparse.ArgumentParser(description='For input files')
parser.add_argument('-inp', '--inpath', metavar='dir', type=str, nargs=1,
                        help='path where inp files are  (default ./)')
parser.add_argument('-sp','--scriptpath',metavar='dir',type=str,nargs=1,
			help='path where script will be saved')
#parser.add_argument('-f','--inpfile',metavar='str',type=str,nargs=1,
#			help='name of input xyz file')

#Declaring variables for ase calc

args = parser.parse_args()

ase_inp=args.inpath[0]
script_path=args.scriptpath[0]
input_file_arr= [f for f in listdir(ase_inp) if isfile(join(ase_inp, f))]

for input_file in input_file_arr :

#Declaring all variables for bash
	python_path="/home/${USER}/fin_scripts"
#script_out="C:/Users/kanishk/Desktop/spectra/"
	input_path="/home/${USER}/input_files/"
	output_path="/home/${USER}/output_files/"
#script_path="/home/${USER}/input_files/input_scripts/"
#input_path="C:/Users/kanishk/Desktop/spectra/"
#output_path="C:/Users/kanishk/Desktop/spectra/"
#script_path="C:/Users/kanishk/Desktop/spectra/"
#input_file="acrolein.xyz"

	name=input_file[:-4]
	script_file=name+"_core.sh"
	output_path=output_path+name+"/"
	file_path=ase_inp+input_file

	#Process molecule info

	molecule=io.read(file_path)
	atom_list=molecule.get_chemical_symbols()

	#Get list of indexes for core-hole
	x=[i for i, j in enumerate(atom_list) if j == 'C']
	# Set number of resources for sarray
	s_array=len(x)-1

	#Sbatch string 
	sbatch_string='#!/bin/bash \n'\
	+'#BATCH --job-name=test_GPAW_job                   # replace name\n'\
	+'#SBATCH --mail-user=singhk93@zedat.fu-berlin.de  # replace email address\n'\
	+'#SBATCH --mail-type=end	\n'\
	+'#SBATCH --ntasks=1                             # replace with value for your job \n'\
	+'#SBATCH --mem-per-cpu=1024                      # replace with value for your job \n'\
	+'#SBATCH --time=02:00:00                         # replace with value for your job \n'\
	+'#SBATCH --qos=standard                          # replace with value for your job \n'\
	+'#SBATCH --cpus-per-task=4	\n'\
	+'#SBATCH --array=0-'+ str(s_array) +'\n'

	#modules PARAMS
	mods="""module add GPAW"""
	variables='PYTHDIR='+ python_path+'\n'\
	+'INPUTDIR='+input_path+ '                        # replace with your directory\n'\
	+'OUTPUTDIR='+output_path+'\n'\
	+'INPUT_FILES='+input_file+'\n'\
	+'FILE_PATH='+file_path +'\n'

	c_dir="cd $PYTHDIR"
	mk_dir="""if [ ! -d $OUTPUTDIR ]; then
  	mkdir $OUTPUTDIR
	fi"""

	t="("
	for i in range(len(x)):
    		t=t+str(x[i])+" "
	t=t[:-1]    
	t=t+")"

	#INDEX
	index_string='INDICES='+ t + '\n'\
	+'atom_index=${INDICES[${SLURM_ARRAY_TASK_ID}]} \n'
	exec_string="""mpiexec	--oversubscribe -np 4  python3  core_groundstate.py -p $INPUTDIR -p2 $OUTPUTDIR -name ${INPUT_FILES} -num ${SLURM_ARRAY_TASK_ID} -index ${atom_index} """

	with open(script_path+script_file, "a") as f:
		f.write(sbatch_string)
		f.write("\n\n")
		f.write(mods)
		f.write("\n\n")
		f.write(variables)
		f.write("\n")
		f.write(c_dir)
		f.write("\n")
		f.write(mk_dir)
		f.write("\n\n")
		f.write(index_string)
		f.write("\n\n")
		f.write(exec_string)
		f.close()
