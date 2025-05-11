#!/bin/bash
#SBATCH -J orb
#SBATCH --partition=Jotunn-GPU
#SBATCH --nodes=1 
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=01:00:00
#SBATCH --mail-user=real@mail.address
#SBATCH --mail-type=end

module load Python/3.11.3
source ../orb_env/bin/activate

python inference.py --csv ./data.csv --image_dir ./output_images/ --name output_inference
