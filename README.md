Significances of the B anomalies
=================================

Forked from Patrick Koppenburg, https://gitlab.cern.ch/pkoppenb/bllsplots on Jan 6, 2022. Also, "Flavour Anomalies", https://www.nikhef.nl/~pkoppenb/anomalies.html

Set of plots of `b -> s l l` and `b -> c tau nu` observables that have shown discrepancies from the Standard Model.

author: Manuel Franco Sevilla based on code by Patrick Koppenburg and Tom Blake

Please report any mistakes.

**Documentation**
- `BllXs/AnomaliesPlot.*` : Pulls of observables of interest. The theory prediction is shifted to zero and then teh experimental value scaled by the quadratic sume of theory and experimental uncertainty. That gives a naïve pull. When significances are given in the original publication, that is used instead. See [Anomalies.md](BllsXs/Anomalies.md) for a list of references.
- `BllXs/B2llKstar-*` : Observables in B->K*ll decays versus q^2. 
- `BllXs/B2llKstar-*-average` : My own averages of B->K*ll decays versus q^2. 
- `BllXs/B2llKstar-*-with-average` : The data with my own averages of B->K*ll decays versus q^2. 
- `BllXs/Bd2llKstar-*` : As above, but only with B0 
- `BllXs/Bu2llKstar-*` : As above, but only with B+ 
- `RX/Blls-R*` : RX plots versus q^2. Wide bins are displayed in dotted lines.
- `RX/Blls-R*-NoDerived` : RX plots versus q^2 excluding wide bins.
- `RX/Error_on_*` : My own prediction on how the uncertainties will scale in the future. 
- `TomBlake/*` : Original plots by Tom Blake.
