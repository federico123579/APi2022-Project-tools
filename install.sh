#!/bin/bash
python3 -m virtualenv .env
. .env/bin/activate
pip install -r requirements.txt
ln ./tools/test_tools/generator.py .env/bin/gentest
ln ./tools/test_tools/test_all.py .env/bin/testall
ln ./tools/test_tools/run_single.py .env/bin/testsingle
ln ./tools/test_tools/run_all.py .env/bin/runtest
deactivate
