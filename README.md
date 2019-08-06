# `ratter`

`ratter` is a python tool to calculate the optical properties -- most importantly *R*eflection and *T*ransmission -- of a stack of layers of different materials. For this is uses the fresnel formalae and transfer matrix calculations.

It provides classes to define a stack of materials, while giving all, some or no numeric values. With `ratter` you can calculate the optical properties of this
stack as numerical values or as functions - formulae or algorithms. With the power of `numpy` and `sympy`, `ratter` gives numeric and symbolic calculations as a mixture and allows you to jump between the two freely.

If you give all values that are necessary to calculate the reflectance of a stack, `ratter` will just calculate and return that value. If you leave numerical values unset and give a symbol instead, for example a *d* as the thickness of an interlayer, `ratter` will return the reflection as a sympy formula with free symbol *d*. This formula can then be turned into an algorithmic function with *d* as an argument. This function will be a numpy function and vectorized, such that it can be applied to an array of *d*'s. This enables fast numeric calculations of the dependencies of the optical properties of a stack from any free parameter.

## Example

Todo

## Installation

`ratter` is written for Python 3, tested in Python 3.7. It depends on `sympy` and `numpy`. To run the tests, you will also need `scipy` and `tmm`.

## Theoretical background

The theory behind the formulae used by `ratter` are the Fresnel Formulae. `ratter` assumes incoming light as a plane wave, described by its complex field amplitude and phase. The interaction with a material layer leads to a change in phase and amplitude (dependent on the refractive index of the material), which can be expressed as a transfer matrix. The consecutive propagation through the layers can be described as a consecutive application of the matrices. Thus a stack of layers can be described as one single transfer matrix. `ratter` calculates that matrix symbolically using `sympy`.

For a detailed description, I recommend the publication of Steven J. Byrnes: [arXiv:1603.02720 [physics.comp-ph]](https://arxiv.org/abs/1603.02720)

## Limitations

* As of now, `ratter` does not support an angle of incidence other than 0, meaning perfectly normal incidence. Hence it does not consider polarization at all.
* It does not support incoherent light and thus gives unrealistic results for thick layers (Thick meaning much thicker than the wavlength)
* The calculation of spatially resolved absorption is also not included.

All of these above can and hopefully will be implemented in future versions.

## Similar tools

If it is required to numerically calculate the reflectance, absorption or transmission, other python tools give very complete solutions:

* `PyTMM`
* `tmm`

We try to test `ratter` to give the same results as `tmm`.