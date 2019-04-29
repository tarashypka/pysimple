#!/bin/bash

ENV_NAME=$1
MODULE_DIR=$(dirname $0)
PYTHON_VERSION=3.7

git config --global credential.helper 'cache --timeout=600'

cd ${MODULE_DIR}

ANACONDA=/usr/local/anaconda
export PATH=${ANACONDA}/bin:$PATH
if [[ ${ENV_NAME} == "" ]]; then
    ENV_PATH=${ANACONDA}
else
    ENV_PATH=${ANACONDA}/envs/${ENV_NAME}
fi
if [[ ! -d ${ENV_PATH} ]]; then
    conda create -n ${ENV_NAME} python=${PYTHON_VERSION}
fi

PIP=${ENV_PATH}/bin/pip
${PIP} install -r requirements.txt
${PIP} install .
