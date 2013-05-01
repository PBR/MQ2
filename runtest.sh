#!/bin/bash
PYTHONPATH=MQ2 nosetests --with-coverage --cover-erase --cover-package=MQ2 $*

