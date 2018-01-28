#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

x-terminal-emulator -e "bash -c \"$DIR/quickeradd/quickeradd.py; read -p 'press any key to close'\""
