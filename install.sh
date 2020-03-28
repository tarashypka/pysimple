#!/usr/bin/env bash

MODULE_DIR=$(realpath $(dirname $0))
PYTHON_VERSION=3.7

ANACONDA_PATH="missing"
ENV_NAME="missing"
HELP_MSG="Usage: install.sh --conda=/path/to/anaconda --env=env_name"

err() {
    echo
    echo ${1}
    echo
    echo ${HELP_MSG}
    echo
    exit
}

for param in $@; do
  case ${param} in
    --env=*)
      ENV_NAME=${param#*=}
      shift
      ;;
    --conda=*)
      ANACONDA_PATH=${param#*=}
      shift
      ;;
    --help)
      echo ${HELP_MSG}
      exit
  esac
done

if [[ ${ANACONDA_PATH} == "missing" ]]; then
  err "Not found --conda argument!"
fi

if [[ ${ENV_NAME} == "missing" ]]; then
  err "Not found --env argument!"
fi

echo ENV=${ENV_NAME}
echo ANACONDA=${ANACONDA_PATH}

export PATH=${ANACONDA_PATH}/bin:$PATH
export PYTHONPATH=${MODULE_DIR}/src:${PYTHONPATH}

ENV_PATH=${ANACONDA_PATH}/envs/${ENV_NAME}
ENV_INSTALLED=0
if [[ ! -d ${ENV_PATH} ]]; then
    echo "Create new environment at ${ENV_PATH} ..."
    conda create -n ${ENV_NAME} python=${PYTHON_VERSION}
    ENV_INSTALLED=1
fi
conda activate ${ENV_NAME}

PIP=${ENV_PATH}/bin/pip

cd ${MODULE_DIR}

${PIP} install -r requirements.txt

TESTS_DIR=${MODULE_DIR}/tests
if [[ -d ${TESTS_DIR} ]]; then
    echo "Run tests in ${TESTS_DIR} ..."
    function run_tests
    {
        echo "${ENV_PATH}/bin/python -m unittest discover -s ${TESTS_DIR} -t ${TESTS_DIR} -v"
    }
    TESTS_OUTPUT=$($(run_tests) 2>&1 | tee /dev/tty)
    echo "Run tests in ${TESTS_DIR} ..."
    if [[ ${TESTS_OUTPUT} =~ "FAILED" ]]; then
        echo "Tests failed!"
        if [[ ${ENV_INSTALLED} == 1 ]]; then
            echo "Remove created at ${ENV_PATH} environment ..."
            rm -rf ${ENV_PATH}
        fi
        exit
    fi
fi

${PIP} install ${MODULE_DIR}
