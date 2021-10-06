#!/bin/bash 

# Скрипт, очищающий директории XY, XZ и YZ в MagneticField/pic/fields/
# Следует запускать только из MagneticField/bash-scripts/

# Обрабатываем директорию XY
cd ../pic/fields/XY
rm *.png *.pdf
cd ../../../bash-scripts
# Обрабатываем директорию XZ
cd ../pic/fields/XZ
rm *.png *.pdf
cd ../../../bash-scripts
# Обрабатываем директорию YZ
cd ../pic/fields/YZ
rm *.png *.pdf
cd ../../../bash-scripts 
