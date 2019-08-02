#!/usr/bin/env bash

# без викификатора…

cd ~/PycharmProjects/txt_autoformat/ || exit 1
python3 autoformat.py --pre | js node_modules/eyo/bin/cli.js --stdin | python3 autoformat.py --post
