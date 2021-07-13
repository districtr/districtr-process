#!/usr/bin/env bash

# Usage: bash run.sh [args]
# [args] are whatever args you would normally pass to "python3 -m districtr_process"

docker run -it --env-file .env.list --rm -v $(pwd):/districtr-process innovativeinventor/districtr-process python3 -m districtr_process "$@"
