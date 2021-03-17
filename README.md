# `coilcalc` - Axisymmetric circular coils calculator
## Introduction
Highly uniform magnetic field with minimal lateral field gradient is required for the generation and preservation of the spin-polarized state of <sup>3</sup>He and <sup>129</sup>Xe gasses. `coilcalc` is designed to be useful in the design, simulation and optimization of magnet systems used to generate an uniform magnetic field used support such systems.
## Limitations
Before you get your hopes up, `coilcalc` is only for circular axisymmetric current coils with no support for non-unity relative permeability. This geometry is surprisingly versatile and useful, but this package won't get you far for other problems other than building spin-polarizer magnets. For proper 2D EM FEM software check [FEMM](https://www.femm.info/wiki/HomePage) out. `coilcalc` is still going to be useful for quickly mapping out a large parameter space, or for getting a quick answer typing on one hand while holding that magnet wire mid-winding with the other. 

## Mu-metal shielding
`coilcalc` in incapable of dealing with non-unity relative permeability. Simulate mu-metal shields in `FEMM` upon your finished design in `coilcalc`. It is difficult to hit tight tolerances with metal sheets, so give it a wide berth to avoid souring your gradients.

## Usage
Users are encouraged to refer to cookbook examples for usage examples with line-by-line comments.
## Acknowledgements
B L A H