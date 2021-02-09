# pymaxion
Multi-purpose projective solver for geometric and structural problems. Written in Cython to go wicked fast. Currently only tested against Python3. Based on ideas from [ShapeOp](https://shapeop.org/) and [Dynamic Relaxation](https://en.wikipedia.org/wiki/Dynamic_relaxation).

## Build Instructions
Pymaxion utilizes Cython, so it must be compiled before running test cases. A minimal Dockerfile is provided that avoids any OS/missing compiler issues if you want to get up and running quickly!

## Linux/Mac Build Instructions
To compile with OpenMP for parallelism, you must first install ```gcc```, (I did this using Homebrew). To compile from terminal, make sure to alias the correct gcc, as Apple's default CLang may not support OpenMP.

```python
cd pymaxion
pip3 install -r requirements.txt
python3 setup.py build_ext --inplace
```

Once you've built the package, you should be able to import modules with the same hierarchy as you would any Python package by adding ```~/pymaxion/src``` to your ```$PYTHONPATH```.
