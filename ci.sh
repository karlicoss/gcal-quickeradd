#!/bin/bash

cd "$(this_dir)" || exit

. ~/bash_ci

ci_run python3.6 -mmypy quickeradd
ci_run python3.6 -mpylint -E quickeradd/*.py

ci_report_errors
