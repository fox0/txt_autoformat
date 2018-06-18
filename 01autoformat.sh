#!/usr/bin/env bash

cd ~/PycharmProjects/txt_autoformat/
python3 autoformat.py --pre | js wikificator.js | js node_modules/eyo/bin/cli.js --stdin | python3 autoformat.py --post
