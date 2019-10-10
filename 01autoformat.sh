#!/usr/bin/env bash

cd "$(dirname $0)" || exit 1
python3 autoformat.py --pre | js wikificator.js | js node_modules/eyo/bin/cli.js --stdin | python3 autoformat.py --post
