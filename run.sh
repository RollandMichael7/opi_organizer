#!/bin/bash
echo Running convert_and_organize_ad.py
python3 ./organize_components/convert_and_organize_ad.py
echo Running convert_and_organize_epics.py
python3 ./organize_components/convert_and_organize_epics.py
echo Running update_references.py
python3 ./organize_components/update_references.py

