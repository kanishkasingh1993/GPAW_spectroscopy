#!/bin/bash 
#BATCH --job-name=test_GPAW_job                   # replace name 
#SBATCH --mail-user=singhk93@zedat.fu-berlin.de  # replace email address 
#SBATCH --mail-type=end 
#SBATCH --ntasks=1                             # replace with value for your job 
#SBATCH --mem-per-cpu=1024                      # replace with value for your job 
#SBATCH --time=02:00:00                         # replace with value for your job 
#SBATCH --qos=standard                          # replace with value for your job 
#SBATCH --cpus-per-task=4	
#SBATCH --array=0 


module add GPAW

PYTHDIR=/home/${USER}/fin_scripts
INPUTDIR=/home/${USER}/input_files/                      # replace with your directory 
OUTPUTDIR=/home/${USER}/output_files/Propane/
INPUT_FILES=Propane.xyz
FILE_PATH=/home/singhk93/input_files/Propane.xyz

cd $PYTHDIR
if [ ! -d $OUTPUTDIR ]; then
  	mkdir $OUTPUTDIR
	fi

mpiexec	--oversubscribe -np 4  python3  groundstate.py -p $INPUTDIR -p2 $OUTPUTDIR -name ${INPUT_FILES} 
	