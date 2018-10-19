#!/bin/bash
HOME=$(pwd)
echo Running convert_and_organize_ad.py
python3 $HOME/organize_components/convert_and_organize_ad.py $@
echo Running convert_and_organize_epics.py
python3 $HOME/organize_components/convert_and_organize_epics.py $@
echo Running update_references.py
python3 $HOME/organize_components/update_references.py $@
