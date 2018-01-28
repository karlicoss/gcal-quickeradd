#!/bin/bash
RES=0
python3.6 -mmypy quickeradd || RES=$?
python3.6 -mpylint -E quickeradd/*.py || RES=$?
exit "$RES"
