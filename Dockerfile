FROM python:3.6.12-buster

COPY . /code

RUN apt-get update
RUN apt-get -y install sudo

RUN pip install -r /code/requirements.txt

ENV PATH=$PATH:/code/src
ENV PYTHONPATH "${PYTHONPATH}:/code/src"

RUN cd /code/src && python setup.py build_ext --inplace

WORKDIR /code/tests/open_mp_tests

# RUN sudo py-spy record -o profile.svg -- python cython_test.py --native
