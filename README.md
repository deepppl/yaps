[![Build Status](https://travis-ci.org/IBM/yaps.svg?branch=master)](https://travis-ci.org/IBM/yaps) [![PyPI version](https://badge.fury.io/py/yaps.svg)](https://badge.fury.io/py/yaps) [![Documentation Status](https://readthedocs.org/projects/yaps/badge/?version=latest)](https://yaps.readthedocs.io/en/latest/?badge=latest)

# YAPS

Yaps is a new surface language for [Stan](http://mc-stan.org/). It lets
users write Stan programs using Python syntax. For example, consider the
following Stan program, which models tosses `x` of a coin with bias `theta`:
```stan
data {
  int<lower=0,upper=1> x[10];
}
parameters {
  real<lower=0,upper=1> theta;
}
model {
  theta ~ uniform(0,1);
  for (i in 1:10)
    x[i] ~ bernoulli(theta);
}
```
It can be rewritten in Python has follows:
```python
import yaps
from yaps.lib import int, real, uniform, bernoulli

@yaps.model
def coin(x: int(lower=0, upper=1)[10]):
    theta: real(lower=0, upper=1) <~ uniform(0, 1)
    for i in range(1,11):
        x[i] <~ bernoulli(theta)
```

The `@yaps.model` decorator indicates that the function following it
is a Stan program.  While being syntactically Python, it is
semantically reinterpreted as Stan.

The argument of the function corresponds to the `data` block. The
type of the data must be declared. Here, you can see that `x` is an
array of 10 integers between `0` and `1` (`int(lower=0, upper=1)[10]`).

Parameters are declared as variables with their type in the body of
the function. Their prior can be defined using the sampling operator
`<~` (or `is`).

The body of the function corresponds to the Stan model. Python syntax
is used for the imperative constructs of the model, like the `for`
loop in the example. The operator `<~` is used to represent sampling
and `x.T[a,b]` for truncated distribution.

Note that Stan array are 1-based. The range of the loop is thus `range(1, 11)`,
that is 1,2, ... 10.

Other Stan blocks can be introduced using the `with` syntax of Python.
For example, the previous program could also be written as follows:
```python
@yaps.model
def coin(x: int(lower=0, upper=1)[10]):
    with parameters:
        theta: real(lower=0, upper=1)
    with model:
        theta <~ uniform(0, 1)
        for i in range(1,11):
            x[i] <~ bernoulli(theta)
```

The corresponding Stan program can be displayed using the `print` function:
```python
print(coin)
```

Finally, it is possible to launch Bayesian inference on the defined model applied to some data.
The communication with the Stan inference engine is based on on [PyCmdStan](https://pycmdstan.readthedocs.io/en/latest/).
```python
flips = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 1])
constrained_coin = coin(x=flips)
constrained_coin.sample(data=constrained_coin.data)
```
Note that arrays must be cast into numpy arrays (see pycmdstan documentation).

After the inference the attribute `posterior` of the constrained model is an object with fields for the latent model parameters:
```python
theta_mean = constrained_coin.posterior.theta.mean()
print("mean of theta: {:.3f}".format(theta_mean))
```

Yaps provides a lighter syntax to Stan programs. Since Yaps uses Python syntax, users can take advantage of Python tooling
for syntax highlighting, indentation, error reporting, ...

## Install

Yaps depends on the following python packages:
- astor
- graphviz
- antlr4-python3-runtime
- pycmdstan

To install Yaps and all its dependencies run:
```
pip install yaps
```

To install from source, first clone the repo, then:
```
pip install .
```

By default, communication with the Stan inference engine is based on [PyCmdStan](https://pycmdstan.readthedocs.io/en/latest/). To run inference, you first need to install [CmdStan](http://mc-stan.org/users/interfaces/cmdstan) and set the CMDSTAN environment variable to point to your CmdStan directory.

```
export CMDSTAN=/path/to/cmdstan
```

## Tools

We provide a tool to compile Stan files to Yaps syntax.
For instance, if `path/to/coin.stan` contain the Stan model presented at the beginning, then:
```
stan2yaps path/to/coin.stan
```
outputs:
```
# -------------
# tests/stan/coin.stan
# -------------
@yaps.model
def stan_model(x: int(lower=0, upper=1)[10]):
    theta: real
    theta is uniform(0.0, 1.0)
    for i in range(1, 10 + 1):
        x[(i),] is bernoulli(theta)
    print(x)
```

Compilers from Yaps to Stan and from Stan to Yaps can also be invoked programmatically using the following functions:
```python
yaps.from_stan(code_string=None, code_file=None)  # Compile a Stan model to Yaps
yaps.to_stan(code_string=None, code_file=None)    # Compile a Yaps model to Stan
```

## Documentation

The full documentation is available at https://yaps.readthedocs.io. You can find more details in the following [article](https://arxiv.org/abs/1812.04125):
```
@article{2018-yaps-stan,
  author = {Baudart, Guillaume and Hirzel, Martin and Kate, Kiran and Mandel, Louis and Shinnar, Avraham},
  title = "{Yaps: Python Frontend to Stan}",
  journal = {arXiv e-prints},
  year = 2018,
  month = Dec,
  url = {https://arxiv.org/abs/1812.04125},
}
```


## License

Yaps is distributed under the terms of the Apache 2.0 License, see
[LICENSE.txt](LICENSE.txt)



## Contributions

Yaps is still at an early phase of development and we welcome
contributions. Contributors are expected to submit a 'Developer's
Certificate of Origin', which can be found in [DCO1.1.txt](DCO1.1.txt).

