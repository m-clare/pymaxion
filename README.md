# Pymaxion
Multi-purpose projective solver for geometric and structural problems. Written in Cython to go wicked fast. Currently only tested against Python3. Based on ideas from [ShapeOp](https://shapeop.org/) and [Dynamic Relaxation](https://en.wikipedia.org/wiki/Dynamic_relaxation).

## General Build Instructions
Pymaxion utilizes Cython, so it must be compiled before running test cases. A minimal Dockerfile is provided that avoids any OS/missing compiler issues if you want to get up and running quickly!

## Linux/Mac Build Instructions
To compile with OpenMP for potential parallelism, you must first install ```gcc```, (I did this using Homebrew). To compile from terminal, make sure to alias the correct gcc, as Apple's default CLang may not support OpenMP.

```python
cd pymaxion/src
pip3 install -r requirements.txt
python3 setup.py build_ext --inplace
```

Once you've built the package, you should be able to import modules with the same hierarchy as you would any Python package by adding ```./pymaxion/src``` to your ```$PYTHONPATH```.

## More Information
The initial development of this project, touching on Cython performance, profiling Cython, and developing [Blender](https://www.blender.org/) add-ons using C-extensions generated from Cython, was presented at [Pycon 2022](https://www.youtube.com/watch?v=TE3M3XfwSN4).

Other relevant development information and process documentation can be found in the following blog posts:
- [Performance Comparison Across Three Languages](https://mclare.blog/posts/performance-comparison-across-three-languages)
- [Further Adventures in Cython Profiling](https://mclare.blog/posts/further-adventures-in-cython-profiling)
- [Dynamic Menu Creation in Blender](https://mclare.blog/posts/dynamic-menu-creation-in-blender)
