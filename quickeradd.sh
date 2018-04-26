#!/bin/bash
DIR=$(dirname "$(readlink -f "$0")")

x-terminal-emulator -e "bash -c \"$DIR/quickeradd/quickeradd.py; read -p 'press any key to close'\""
