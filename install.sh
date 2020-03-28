#!/usr/bin/env bash

MODULE_DIR=$(realpath $(dirname $0))

ENV_PATH="missing"
HELP_MSG="Usage: install.sh --env=/path/to/python/env"

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
      ENV_PATH=${param#*=}
      shift
      ;;
    --help)
      echo ${HELP_MSG}
      exit
  esac
done

if [[ ${ENV_PATH} == "missing" ]]; then
  err "Not found --env argument!"
fi

${ENV_PATH}/bin/pip install -r ${MODULE_DIR}/requirements.txt

function run_tests {
    echo "${ENV_PATH}/bin/python -m unittest discover -s ${TESTS_DIR} -t ${TESTS_DIR} -v"
}

# This way source code will be importable from tests
export PYTHONPATH=${MODULE_DIR}/src:${PYTHONPATH}

TESTS_DIR=${MODULE_DIR}/tests

echo "Run tests in ${TESTS_DIR} ..."
TESTS_OUTPUT=$($(run_tests) 2>&1 | tee /dev/tty)

if [[ ${TESTS_OUTPUT} =~ "FAILED" ]]; then
    echo "Tests failed!"
    exit 1
fi

${ENV_PATH}/bin/pip install ${MODULE_DIR}
