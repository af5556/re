#!/bin/bash

FILE_TO_EXPORT=$1
DATA_PROC_TAG=$2
CF_PYTHON_VERSION=$3
DDA_GCP_PROJECT=$4
DEFAULT_REGION=$5
echo "" > "$FILE_TO_EXPORT"

for dir in python/functions/*
  do
    echo """
$(basename ${dir}):
  stage: build
  tags:
  - '${DATA_PROC_TAG}'
  variables:
    FUNCTION_NAME: '$(basename ${dir})'
    FUNCTION_SOURCE: ${dir}
    CF_PYTHON_VERSION: '${CF_PYTHON_VERSION}'
    DDA_GCP_PROJECT: '${DDA_GCP_PROJECT}'
    DEFAULT_REGION: '${DEFAULT_REGION}'
  extends:
    - .common-deploy-cloudfunctions
""" >> "$FILE_TO_EXPORT"
  done