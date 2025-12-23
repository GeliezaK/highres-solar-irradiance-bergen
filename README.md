# master_thesis

## Prepare conda environment 
Install conda, create environment in environment.yml. 

## test/
To run files in `test/` subfolder, add the working directory to `PYTHONPATH`: `export PYTHONPATH=$PWD` from the `master_thesis` root directory. This preserves the absolute imports.  

Linux/macOS:
```bash
export PYTHONPATH=$PWD
python -m unittest discover -s test -p "test_preprocessing.py"
```
