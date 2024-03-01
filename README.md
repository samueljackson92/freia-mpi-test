# MPI & Dask Examples on Freia

This repo contains examples of running multi-process, multi-node jobs on Freia. It contains two examples:

 - mpi-example.py - an example using the mpi4py library
 - dask-example.py - an example using the dask_mpi library


## Installation
First, load the python module:

```sh
module load python/3.9
```

Then create a new venv environment locally
```sh
/usr/local/depot/Python-3.9/bin/python3 -m venv mpi-test
```

Activate the environment
```sh
source mpi-test/bin/activate
```

Install the requirements
```sh
pip install -r requirements.txt
```

## Running

To submit a multi node MPI job using mpi4py run:
```sh
qsub submit-mpi.job
```

To submit a multi-node MPI job using dask run:
```sh
qsub submit-dask.job
```