#!/bin/bash

# This script is used to run the program
programName="main.py"
thisDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd -P )"
programPath="$thisDir/$programName"

source ./make_env.sh ${thisDir} -f

python3 $programPath

