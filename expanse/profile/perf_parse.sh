#!/bin/bash

set -e

for name in "$@"
do
  echo "Parsing $name"
  perf report --stdio -i $name > $name.txt
done