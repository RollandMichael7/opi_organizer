#!/bin/bash
echo Running convert_and_organize_ad.py
py -3.6 ./organize_components/convert_and_organize_ad.py $@
echo Running convert_and_organize_epics.py
py -3.6 ./organize_components/convert_and_organize_epics.py $@
echo Running update_references.py
py -3.6 ./organize_components/update_references.py $@
	
