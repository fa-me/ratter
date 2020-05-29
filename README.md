# ratter

*ratter* is a python tool to calculate the optical response -- most importantly *R*eflection and *T*ransmission -- of a stack of layers of different materials. For this is uses the fresnel formalae and transfer matrix calculations.

It provides classes to define a stack of materials, while giving all, some or no numeric values. With *ratter* you can calculate the optical properties of this
stack as numerical values or as functions - formulae or algorithms. With the power of [numpy](https://numpy.org) and [sympy](https://www.sympy.org), *ratter* gives numeric and symbolic calculations as a mixture and allows you to jump between the two freely.

If you give all values that are necessary to calculate the reflectance of a stack, *ratter* will just calculate and return that value. If you leave numerical values unset and give a symbol instead, for example a *d* as the thickness of an interlayer, *ratter* will return the reflection as a sympy formula with free symbol *d*. This formula can then be turned into an algorithmic function with *d* as an argument. This function will be a numpy function and vectorized, such that it can be applied to an array of *d*'s. This enables fast numeric calculations of the dependencies of the optical properties of a stack from any free parameter.

## Example 1: general symbolic calculations

In a stack of multiple layers, the two outer layers are considered infinite half-spaces.

```python
from ratter import *

# define three materials
m1 = Material('1')
m2 = Material('2')
m3 = Material('3')

# define three layers
l1 = Layer('l1', m1)
l2 = Layer('l2', m2)
l3 = Layer('l3', m3)

# define the order of the layers
stack = Layerstack([l1,l2,l3])

# calculate the (complex) reflectance amplitude
r = stack.reflectance_amplitude().simplify()
```
<img src="/docs/three_materials_r.png" width="320"/>

```
stack.transmittance_amplitude().simplify()
```
<img src="/docs/three_materials_t.png" width="320"/>


## Example 2: numeric calculation of a double layer coating
```python
from ratter import *
from sympy import conjugate

wavelength = 600 # length units: nm

# define materials with their refractive index at the wavelength
Si = Material('Si', refractive_index_value=3.9400+0.019934j)  # Green 2008
air = Material('air', refractive_index_value=1.00027698) # Ciddor 1996
SiO2 = Material('SiO2', refractive_index_value=1.4580) # Malitson 1965
AlOx = Material('Al2O3', refractive_index_value=1.7675) # Malitson and Dodge 1972

# define the layers
environment = Layer('env', air)
coating1 = Layer('coat1', SiO2)
coating2 = Layer('coat2', AlOx)
bulk = Layer('bulk', Si)

# define the order of materials
stack = Layerstack([environment, coating1, coating2, bulk])

# calculate absolute reflectivity R
r = stack.reflectance_amplitude()
R = conjugate(r)*r

# substitute symbols with numbers
R_ = R.subs(LAMBDA_VAC, wavelength)

# create a vectorized numpy function out of symbolic definition
R_of_coating_thickness = as_function_of(R_, [coating1.thickness_symbol, 
                                             coating2.thickness_symbol])
```
**Plot** using the fast vectorized function
```python
import numpy as np
import matplotlib.pyplot as plt

d1 = np.arange(0,500)

for d2 in [50,200,500]:
    reflectivity_values = np.real(R_of_coating_thickness(d1, d2))
    plt.plot(d1, reflectivity_values, label='{}'.format(d2))

plt.legend(title='$Al_2O_3$ thickness (nm)')
plt.ylabel('reflectivity')
plt.xlabel('$SiO_2$ thickness (nm)')
```
<img src="/docs/example_plot.png" width="320"/>


## Installation

*ratter* is written for Python 3, tested in Python 3.7. It depends on [numpy](https://numpy.org) and [sympy](https://www.sympy.org). To run the tests, you will also need [scipy](https://www.scipy.org) and [tmm](https://pypi.org/project/tmm/).

To install use `pip`

```pip install ratter```

## Theoretical background

The theory behind the formulae used by *ratter* are the Fresnel Formulae. *ratter* assumes incoming light as a plane wave, described by its complex field amplitude and phase. The interaction with a material layer leads to a change in phase and amplitude (dependent on the refractive index of the material), which can be expressed as a transfer matrix. The consecutive propagation through the layers can be described as a consecutive application of the matrices. Thus a stack of layers can be described as one single transfer matrix. *ratter* calculates that matrix symbolically using [sympy](https://www.sympy.org).

For a detailed description, I recommend the explanations of Steven J. Byrnes: [arXiv:1603.02720 [physics.comp-ph]](https://arxiv.org/abs/1603.02720)

## Limitations

* As of now, *ratter* does not support an angle of incidence other than 0, meaning perfectly normal incidence. It does not consider polarization at all.
* It does not support incoherent light and thus gives unrealistic results for thick layers which do not maintain coherence.
* The calculation of spatially resolved absorption is also not included.

All of these above can and hopefully will be implemented in future versions.

## Similar tools

If it is required to numerically calculate the reflectance, absorption or transmission, other python tools give very complete solutions:

* [tmm](https://pypi.org/project/tmm/)
* [OpenTMM](https://pypi.org/project/openTMM/)
* [PyTMM](https://github.com/kitchenknif/PyTMM)

*ratter* is tested to give the same results as [tmm](https://pypi.org/project/tmm/).