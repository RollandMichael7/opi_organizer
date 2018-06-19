# opi_organizer
A python script that converts a flat directory of AreaDetector Control System Studio OPI files into a hierarchical structure, sub-dividing by plugin and version. Aditionally, updates the cross-references of plugin OPIs so that they don't break in the new directory.

If the user has CS Studio installed, the script also uses the adl2boy feature to convert MEDM adl files into opi files and places them in their appropriate place in the new directory.
