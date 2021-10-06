#!/bin/bash 

# Скрипт, собирающий изображения в ПДФ-ки в XY, XZ и YZ в MagneticField/pic/fields/
# Следует запускать только из MagneticField/bash-scripts/

# Обрабатываем директорию XY
cd ../pic/fields/XY
convert *.png XY.pdf
cd ../../../bash-scripts
# Обрабатываем директорию XZ
cd ../pic/fields/XZ
convert *.png XZ.pdf
cd ../../../bash-scripts
# Обрабатываем директорию YZ
cd ../pic/fields/YZ
convert *.png YZ.pdf
cd ../../../bash-scripts
