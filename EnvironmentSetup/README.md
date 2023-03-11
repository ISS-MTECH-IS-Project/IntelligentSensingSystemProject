# Installation Guide

## Install Anaconda (Optional)

If you have Python 3.9 environment ready, you can activate it and skip this step.

- Install Anaconda

https://www.anaconda.com/products/distribution
Follow the guide to complete the installation.

- Create a new python 3.9.12 environment

```bash
conda create --name py39 python=3.9.12
```

- Activate the environment

```bash
conda activate py39
```

## Setup the application

- Download the code repository from github and save the code under ~/PRMLS_Project https://github.com/TeamEightIS04/PRMLS_Poject
- Go to the SystemCode folder

```bash
cd ~/PRMLS_Project/SystemCode
```

- Install the dependencies (make sure the py39 environment is activated)

```bash
pip install tensorflow==2.9.0 Flask flask-cors Pillow
```

- Start the application

```bash
flask run
```

- Open the application in browser http://localhost:5000
