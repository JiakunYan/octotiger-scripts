#!/usr/bin/env bash

jobname=lci-dim8
dirname=run-$jobname

mkdir -p $dirname
scp rostam:workspace/octotiger-scripts/rostam/analyize/${dirname}/octotiger_trace.${jobname}.0.log $dirname
scp rostam:workspace/octotiger-scripts/rostam/analyize/${dirname}/slurm_output.* $dirname
