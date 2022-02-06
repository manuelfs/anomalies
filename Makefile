pyfiles = $(wildcard *.py)
jsonfiles = $(wildcard */*.json)

all : Anomalies RX BllX

Anomalies : Anomalies/AnomaliesPlot.png
RX : RX/Blls-RK.png RX/Error_on_R_K.png
BllX : BllXs/Bd2llKstar-P5prime.png BllXs/Bu2llKstar-P5prime.png BllXs/B2llKstar-P5prime.png BllXs/B2llKstar-P5prime-average.png BllXs/Bs2llPhi-dBrdq2.png


RX/Blls-RK.png : RK.py Utilities.py $(jsonfiles)
	python3 RK.py 

BllXs/Bd2llKstar-P5prime.png : B2llKstar.py Utilities.py $(jsonfiles)
	python3 B2llKstar.py Bd

BllXs/Bu2llKstar-P5prime.png : B2llKstar.py Utilities.py $(jsonfiles)
	python3 B2llKstar.py Bu

BllXs/B2llKstar-P5prime.png : B2llKstar.py Utilities.py $(jsonfiles)
	python3 B2llKstar.py Both

BllXs/B2llKstar-P5prime-average.png : B2llKstar.py Utilities.py $(jsonfiles)
	python3 B2llKstar.py average

BllXs/Bs2llPhi-dBrdq2.png : B2llKstar.py Utilities.py $(jsonfiles)
	python3 B2llKstar.py Bs

RX/Error_on_R_K.png : RKproj.py Utilities.py
	python3 RKproj.py

Anomalies/AnomaliesPlot.png :  AnomaliesPlot.py Utilities.py $(jsonfiles)
	python3 AnomaliesPlot.py

clean :
	rm -f RX/*.png RX/*.pdf BllXs/*.pdf BllXs/*.png 
