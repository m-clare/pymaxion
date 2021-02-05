import os
import sys
import numpy
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Compiler.Main import default_options
from Cython.Distutils import build_ext

# Helper functions
def scandir(dir, files=[]):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if os.path.isfile(path) and path.endswith("pyx"):
            files.append(path.replace(os.path.sep, ".")[:-4])
        elif os.path.isdir(path):
            scandir(path, files)
    return files

def makeExtension(extName):
    extPath = extName.replace(".", os.path.sep) + ".pyx"
    print(extName)
    return Extension(
        name=extName,
        sources=[extPath],
        include_dirs=[numpy_include, ".", geo_include],
        extra_compile_args=["-fopenmp"],
        extra_link_args=["-fopenmp"],
        language="c++",
    )

# Find all includes
numpy_include = numpy.get_include()

# Add includes for C++ only libraries (no .pyx wrapped)
geo_include = os.path.abspath("./pymaxion/geometry")

extNames = scandir("pymaxion")


# build up set of Extension objects
extensions = [makeExtension(name) for name in extNames]

# Create a dictionary of arguments for setup
setup_args = {
    "name": "pymaxion",
    "packages": ["pymaxion", "pymaxion.goals", "pymaxion.geometry"],
    "py_modules": [],
    "ext_modules": cythonize(extensions, emit_linenums=True, compiler_directives={'language_level': 3}),
    "requires": [],
    "cmdclass": {"build_ext": build_ext},
}

setup(**setup_args)
