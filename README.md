# Running Python Scripts and Generating CSV Files

This repository contains two Python scripts, `Deduce.py` and `Deidentify.py`, which are used to generate two CSV files, `deduce_result.csv` and `deidentify_result.csv`, respectively. The scripts need to be run in separate conda environments.

## Create conda env

1. Deduce:

```
conda create -n deduce python=3.11
conda activate deduce
pip install deduce==2.0.3 pandas scikit-learn
conda deactivate
```

2. Deidentify:

Mac is currently not supported. Make sure you have `cmake` installed in your system. Then run:

```
conda create -n deidentify python=3.10
conda activate deidentify
pip install deduce==1.0.8
pip install deidentify
conda deactivate
```

## Before Running the Scripts

In each script, you should find the load data part of the code and change the data file path to your dataset path:

```
# Load data from the .jsonl file
with open('4_annotated_by_gpt_4.jsonl', 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(line)
        texts.append(data['text'])
        true_labels.append({(span['start'], span['end']): span['label'] \
	                           for span in data['spans']})
```

## Running the Scripts

1. Before running `Deduce.py`, activate the `deduce` environment by running the command:

conda activate deduce

2. Before running `Deidentify.py`, activate the `deidentify` environment by running the command:

conda activate deidentify

## Dependency Versions

Please note that when running 'Deidentify.py', you may need to change the version of the 'flair' library. If any of the script fails to run, it is likely due to version compatibility issues with the dependencies in the env. I will provide the respective dependency versions for each environment below. (Using GPT-4 to repeatedly ask or investigate the problematic dependency version is also an option.)

### Deduce Environment

```
(deduce) jack@jack-xps:~/Desktop/PG/Thesis$ conda list
packages in environment at /home/jack/miniconda3/envs/deduce:

 Name                    Version                   Build  Channel
_libgcc_mutex             0.1                        main  
_openmp_mutex             5.1                       1_gnu  
blas                      1.0                         mkl  
brotli                    1.0.9                h166bdaf_7    conda-forge
brotli-bin                1.0.9                h166bdaf_7    conda-forge
bzip2                     1.0.8                h7b6447c_0  
ca-certificates           2023.5.7             hbcca054_0    conda-forge
certifi                   2023.5.7           pyhd8ed1ab_0    conda-forge
charset-normalizer        3.1.0              pyhd8ed1ab_0    conda-forge
deduce                    2.0.3                    pypi_0    pypi
deprecated                1.2.14                   pypi_0    pypi
docdeid                   0.1.6                    pypi_0    pypi
idna                      3.4                pyhd8ed1ab_0    conda-forge
intel-openmp              2023.1.0         hdb19cb5_46305  
joblib                    1.3.0              pyhd8ed1ab_1    conda-forge
ld_impl_linux-64          2.38                 h1181459_1  
libbrotlicommon           1.0.9                h166bdaf_7    conda-forge
libbrotlidec              1.0.9                h166bdaf_7    conda-forge
libbrotlienc              1.0.9                h166bdaf_7    conda-forge
libffi                    3.4.4                h6a678d5_0  
libgcc-ng                 11.2.0               h1234567_1  
libgfortran-ng            13.1.0               h69a702a_0    conda-forge
libgfortran5              13.1.0               h15d22d2_0    conda-forge
libgomp                   11.2.0               h1234567_1  
libstdcxx-ng              11.2.0               h1234567_1  
libuuid                   1.41.5               h5eee18b_0  
mkl                       2023.1.0         h6d00ec8_46342  
mkl-service               2.4.0           py311h5eee18b_1  
mkl_fft                   1.3.6           py311ha02d727_1  
mkl_random                1.2.2           py311ha02d727_1  
ncurses                   6.4                  h6a678d5_0  
numpy                     1.25.0          py311h08b1b3b_0  
numpy-base                1.25.0          py311hf175353_0  
openssl                   3.0.9                h7f8727e_0  
packaging                 23.1               pyhd8ed1ab_0    conda-forge
pandas                    2.0.3                    pypi_0    pypi
pip                       23.1.2          py311h06a4308_0  
platformdirs              3.8.0              pyhd8ed1ab_0    conda-forge
pooch                     1.7.0              pyha770c72_3    conda-forge
pysocks                   1.7.1              pyha2e5f31_6    conda-forge
python                    3.11.3               h955ad1f_1  
python-dateutil           2.8.2                    pypi_0    pypi
pytz                      2023.3                   pypi_0    pypi
rapidfuzz                 2.15.1                   pypi_0    pypi
readline                  8.2                  h5eee18b_0  
regex                     2022.10.31               pypi_0    pypi
requests                  2.31.0             pyhd8ed1ab_0    conda-forge
scikit-learn              1.2.2           py311h6a678d5_1  
scipy                     1.10.1          py311h08b1b3b_1  
setuptools                67.8.0          py311h06a4308_0  
six                       1.16.0                   pypi_0    pypi
sqlite                    3.41.2               h5eee18b_0  
tbb                       2021.8.0             hdb19cb5_0  
threadpoolctl             3.1.0              pyh8a188c0_0    conda-forge
tk                        8.6.12               h1ccaba5_0  
typing-extensions         4.7.1                hd8ed1ab_0    conda-forge
typing_extensions         4.7.1              pyha770c72_0    conda-forge
tzdata                    2023.3                   pypi_0    pypi
urllib3                   2.0.3              pyhd8ed1ab_0    conda-forge
wheel                     0.38.4          py311h06a4308_0  
wrapt                     1.15.0                   pypi_0    pypi
xz                        5.4.2                h5eee18b_0  
zlib                      1.2.13               h5eee18b_0  
(deduce) jack@jack-xps:~/Desktop/PG/Thesis$

### Deidentify Environment

(deidentify) jack@jack-xps:~/Desktop/PG/Thesis$ conda list
packages in environment at /home/jack/miniconda3/envs/deidentify:

 Name                    Version                   Build  Channel
_libgcc_mutex             0.1                        main  
_openmp_mutex             5.1                       1_gnu  
blis                      0.7.9                    pypi_0    pypi
bpemb                     0.3.4                    pypi_0    pypi
bzip2                     1.0.8                h7b6447c_0  
ca-certificates           2023.05.30           h06a4308_0  
catalogue                 1.0.2                    pypi_0    pypi
certifi                   2023.5.7                 pypi_0    pypi
charset-normalizer        3.1.0                    pypi_0    pypi
click                     8.1.3                    pypi_0    pypi
cmake                     3.26.4                   pypi_0    pypi
conllu                    4.5.3                    pypi_0    pypi
cymem                     2.0.7                    pypi_0    pypi
deduce                    1.0.8                    pypi_0    pypi
deidentify                0.7.3                    pypi_0    pypi
flair                     0.10                     pypi_0    pypi
fsspec                    2023.6.0                 pypi_0    pypi
ftfy                      6.1.1                    pypi_0    pypi
gdown                     3.12.2                   pypi_0    pypi
gensim                    4.3.1                    pypi_0    pypi
huggingface-hub           0.15.1                   pypi_0    pypi
idna                      3.4                      pypi_0    pypi
importlib-metadata        3.10.1                   pypi_0    pypi
janome                    0.5.0                    pypi_0    pypi
konoha                    4.6.5                    pypi_0    pypi
langdetect                1.0.9                    pypi_0    pypi
ld_impl_linux-64          2.38                 h1181459_1  
libffi                    3.4.4                h6a678d5_0  
libgcc-ng                 11.2.0               h1234567_1  
libgomp                   11.2.0               h1234567_1  
libprotobuf               3.20.3               he621ea3_0  
libstdcxx-ng              11.2.0               h1234567_1  
libuuid                   1.41.5               h5eee18b_0  
lit                       16.0.6                   pypi_0    pypi
loguru                    0.7.0                    pypi_0    pypi
more-itertools            8.8.0                    pypi_0    pypi
mpld3                     0.3                      pypi_0    pypi
mpmath                    1.3.0                    pypi_0    pypi
murmurhash                1.0.9                    pypi_0    pypi
nameparser                1.1.2                    pypi_0    pypi
ncurses                   6.4                  h6a678d5_0  
nl-core-news-sm           2.3.0                    pypi_0    pypi
nltk                      3.8.1                    pypi_0    pypi
nvidia-cublas-cu11        11.10.3.66               pypi_0    pypi
nvidia-cuda-cupti-cu11    11.7.101                 pypi_0    pypi
nvidia-cuda-nvrtc-cu11    11.7.99                  pypi_0    pypi
nvidia-cuda-runtime-cu11  11.7.99                  pypi_0    pypi
nvidia-cudnn-cu11         8.5.0.96                 pypi_0    pypi
nvidia-cufft-cu11         10.9.0.58                pypi_0    pypi
nvidia-curand-cu11        10.2.10.91               pypi_0    pypi
nvidia-cusolver-cu11      11.4.0.1                 pypi_0    pypi
nvidia-cusparse-cu11      11.7.4.91                pypi_0    pypi
nvidia-nccl-cu11          2.14.3                   pypi_0    pypi
nvidia-nvtx-cu11          11.7.91                  pypi_0    pypi
openssl                   3.0.9                h7f8727e_0  
overrides                 3.1.0                    pypi_0    pypi
pillow                    10.0.0                   pypi_0    pypi
pip                       23.1.2          py310h06a4308_0  
plac                      1.1.3                    pypi_0    pypi
preshed                   3.0.8                    pypi_0    pypi
protobuf                  3.20.3          py310h6a678d5_0  
py-dateinfer              0.4.5                    pypi_0    pypi
pyparsing                 3.1.0                    pypi_0    pypi
pysocks                   1.7.1                    pypi_0    pypi
python                    3.10.11              h955ad1f_3  
python-crfsuite           0.9.9                    pypi_0    pypi
pytz                      2023.3                   pypi_0    pypi
pyyaml                    6.0                      pypi_0    pypi
readline                  8.2                  h5eee18b_0  
requests                  2.31.0                   pypi_0    pypi
safetensors               0.3.1                    pypi_0    pypi
segtok                    1.5.11                   pypi_0    pypi
sentencepiece             0.1.95                   pypi_0    pypi
setuptools                67.8.0          py310h06a4308_0  
six                       1.16.0                   pypi_0    pypi
sklearn-crfsuite          0.3.6                    pypi_0    pypi
smart-open                6.3.0                    pypi_0    pypi
spacy                     2.3.9                    pypi_0    pypi
sqlite                    3.41.2               h5eee18b_0  
sqlitedict                2.1.0                    pypi_0    pypi
srsly                     1.0.6                    pypi_0    pypi
sympy                     1.12                     pypi_0    pypi
tabulate                  0.9.0                    pypi_0    pypi
thinc                     7.4.6                    pypi_0    pypi
tk                        8.6.12               h1ccaba5_0  
tokenizers                0.13.3                   pypi_0    pypi
torch                     1.13.1                   pypi_0    pypi
transformers              4.30.2                   pypi_0    pypi
triton                    2.0.0                    pypi_0    pypi
tzdata                    2023c                h04d1e81_0  
unidecode                 1.3.6                    pypi_0    pypi
urllib3                   2.0.3                    pypi_0    pypi
wasabi                    0.10.1                   pypi_0    pypi
wheel                     0.38.4          py310h06a4308_0  
wikipedia-api             0.6.0                    pypi_0    pypi
xz                        5.4.2                h5eee18b_0  
zipp                      3.15.0                   pypi_0    pypi
zlib                      1.2.13               h5eee18b_0  
(deidentify) jack@jack-xps:~/Desktop/PG/Thesis$
```