# magcoilcalc - Axisymmetric circular current loops (coils) magnetic field calculator
## Introduction
Highly uniform magnetic field with minimal lateral field gradient is required for the generation and preservation of the spin-polarized state of <sup>3</sup>He and <sup>129</sup>Xe gasses and other noble gas species with non-zero nuclear spin. `magcoilcalc` is designed to be useful in the design, simulation and optimization of magnet systems used to generate an uniform magnetic field intended to support such systems.
## Installation
`pip install magcoilcalc`. Requires Python >= 3.4,  `numpy` and `matplotlib`.
## Limitations
Before you get your hopes up, `magcoilcalc` is only for circular axisymmetric current loops with no support for non-unity relative permeability. This geometry is versatile and useful, but this package won't get you very far for problems other than building spin-polarizer magnets. For proper 2D EM FEM software check [FEMM](https://www.femm.info/wiki/HomePage) out. `magcoilcalc` is useful for quickly mapping out a large parameter space, or for getting a quick answer typing on one hand while holding that magnet wire mid-winding with the other.

Support for infinitely thin cylindrical current sheets are also being worked on. You can spawn one with `magcoilcalc.CurrentSheet` with the usual parameters, but these are not vectorized so can be slow on a large mesh. 

## Mu-metal shielding
`magcoilcalc` in incapable of dealing with non-unity relative permeability. Simulate mu-metal shields in `FEMM` upon your finished design in `magcoilcalc`.

## Usage
Users are encouraged to refer to cookbook examples for usage examples with line-by-line comments.

## Found a bug?
The author still discovers yet another misconception in his understanding of elementary electromagnetism once in a while. If you find something not quite right, you are probably right - open an issue or drop me an email!