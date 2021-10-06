# Magnetic-Field Project

This project consists of two parts, both are preordained for calculation magnetic field between two coils. You can find more detailed description in Russian in "Краткое руководство.pdf".

## _MagPyLib coil project_

This project uses python library MagPyLib to calculate the magnetic field distribution between two coils. Parameters of rectangular/circle coils are passing through corresponding YAML configure files. Also the project provides an opportunity for pseudo-sinusoidal current supply implementation (works as permanent current coils but the values of permanent current are changing corresponding to the number of iterations in cycle).

The example of possible calculations output is represented below:

![N|Solid](https://user-images.githubusercontent.com/63719570/136214517-1443c283-f3b4-409e-bb7c-cb305b95cad8.png)

## _OpenEMS code example_

Provides an example of code used to calculate the distribution of magnetic field between two rectangular coils using openEMS free software for calculation and ParaView for visualization.

![N|Solid](https://user-images.githubusercontent.com/63719570/136210584-c164fdfd-1ccb-416e-a8f4-ab8c34149117.png)

![N|Solid](https://user-images.githubusercontent.com/63719570/136210479-8596de61-8cf1-424f-9b6c-d4201fce7b7d.png) 
