#!/usr/bin/env bash

ENV_NAME=$1
MODULE_DIR=$(dirname $0)
PYTHON_VERSION=3.7
ANACONDA_PATH=${HOME}/miniconda3

export PATH=${ANACONDA_PATH}/bin:$PATH

if [[ ${ENV_NAME} == "" ]]; then
    ENV_PATH=${ANACONDA_PATH}
else
    ENV_PATH=${ANACONDA_PATH}/envs/${ENV_NAME}
    if [[ ! -d ${ENV_PATH} ]]; then
        conda create -n ${ENV_NAME} python=${PYTHON_VERSION}
    fi
    source ${ANACONDA_PATH}/etc/profile.d/conda.sh
    conda activate ${ENV_NAME}
fi

${ENV_PATH}/bin/pip install -r ${MODULE_DIR}/requirements.txt

function run_tests
{
    echo "${ENV_PATH}/bin/python -m unittest discover -s ${MODULE_DIR}/tests -t ${MODULE_DIR} -v"
}

TESTS_PASSED=$($(run_tests) 2>&1 | tee /dev/tty | tail -1)

if [[ ${TESTS_PASSED} != "OK" ]]; then
    exit
fi

${ENV_PATH}/bin/pip install -r ${MODULE_DIR}/requirements.txt
${ENV_PATH}/bin/pip install ${MODULE_DIR}
