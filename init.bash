#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd "$DIR"

echo "export PYTHONPATH=$DIR:PYTHONPATH" >> ~/.bashrc
echo "export KA_HELPERS_REPO=$DIR" >> ~/.bashrc

echo "KA_HELPERS_REPO=$DIR" >> env.ide