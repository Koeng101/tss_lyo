# TSST-KCM lyo competent cells

Much derived from https://binomicalabs.notion.site/c2974334797c4e45964668338d28a790?v=5d843a3dc7b44c198534ece39f175ad3&p=62561320d8314ff982150a3f2a0c20ec&pm=s and https://doi.org/10.1128/spectrum.02497-22

### References
=> https://doi.org/10.1128/spectrum.02497-22 [1] An Optimized Transformation Protocol for Escherichia coli BW3KD with Supreme DNA Assembly Efficiency
=> https://doi.org/10.1006/cryo.1993.1052 [2] Protection of freeze-dried Escherichia coli by trehalose upon exposure to environmental conditions
=> https://doi.org/10.1016/j.ab.2004.05.021 [3] Trehalose increases chemical-induced transformation efficiency of Escherichia coli
=> https://patents.google.com/patent/US7648832B2/en [4] Methods for lyophilizing competent cells

## Materials

### TSST

* 20mM MgSO4
* 10% PEG 3350
* 140mM MnCl2
* 200mM trehalose
* LB 

Or per 100mL:

* 0.5g MgSO4 heptahydrate
* 2.77g MnCl2 tetrahydrate

* 10g PEG 3350
* 6.846g trehalose
* 2.5g LB powder

Autoclave the MgSO4+MnCl2 and the PEG+trehalose+LB separately. This is to prevent precipitation.

Addition of 140mM MnCl2 increases transformation efficiency by approximately 2x (Fig S1J of [1]). MgSO4 is used rather than MgCl2 so that no wash step is required (Fig S1H of [1]). 100mM trehalose protects the cells against lyophilization (Fig 3 of [2]), but 200mM trehalose actually increases transformation efficiency (Fig 1 of [3]) in TSS. Thusly, 200mM of trehalose is used. TSS is renamed TSST to denote the added trehalose.

DMSO is the main chemical preventing autoclaving of normal TSS, since it can degrade in the autoclave. This recipe doesn't use DMSO, so we just autoclave the entire thing.

### 5x KCM

* 0.5M KCl
* 150mM CaCl2
* 250mM MgCl2

or per 200mL:

* 7.46g KCl
* 3.33g CaCl2
* 10.17g MgCl2 hexahydrate

KCM during the transformation step has been shown to increased transformation by approximately 10x (Fig 1B of [1]).

## Protocol

Before the protocol:
* Make sure you have pre-frozen tubes at -80c for cell aliquots
* Make sure your TSS is ice cold

* Streak E.coli turbo onto an LB agar plate
* Pick one colony into an erlenmeyer flask and shake overnight. Try to keep at about a 5x to 10x reduction: ie, ~20mL in a 125mL flask or ~100mL in 1L. These aren't hard numbers, and the optimal varies by lab
* Centrifuge down. This is not done yet at a cold temperature. Resuspend in 10x reduction of TSS. For example, 20mL of cells should be resuspended in 2mL of TSS. 50x does show a higher transformation efficiency (Fig S1C of [1]), but I still need to test this.
* Immediately aliquot into pre-frozen -80c tubes on ice. You want to freeze the cells as quickly as possible.
* Freeze cells in -80c overnight, along with a lyophilization tray in the -20c overnight

### Lyophilization
* The next day, lyophilize the cells. [more here later from [4]]

### Transformation
