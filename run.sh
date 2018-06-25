#!/bin/bash
echo Running convert_and_organize_ad.py
python3 convert_and_organize_ad.py
echo Running convert_and_organize_epics.py
python3 convert_and_organize_epics.py
echo Running update_reference.py
python3 update_references.py