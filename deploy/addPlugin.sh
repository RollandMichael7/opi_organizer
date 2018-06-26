#!/bin/bash
DETECTOR=/epics/support4c/areaDetector
TARGET=

if [ -z $TARGET ]; then
	TARGET=$1
fi

if ! [ -z $TARGET ]; then
	echo name of AD plugin to add:
	read plugin
	if [ -d $DETECTOR/$plugin ]; then
		app="$(ls $DETECTOR/$plugin | grep App)"
		mkdir -p $TARGET/areaDetector/$plugin
		mkdir -p $TARGET/areaDetector/$plugin/$app
	
		cp -r -n $DETECTOR/$plugin/bin $TARGET/areaDetector/$plugin
		cp -r -n $DETECTOR/$plugin/db $TARGET/areaDetector/$plugin
		cp -r -n $DETECTOR/$plugin/documentation $TARGET/areaDetector/$plugin
		cp -r -n $DETECTOR/$plugin/iocs $TARGET/areaDetector/$plugin
		cp -r -n $DETECTOR/$plugin/$app/Db $TARGET/areaDetector/$plugin/$app
		cp -r -n $DETECTOR/$plugin/$app/op $TARGET/areaDetector/$plugin/$app
	else
		echo Invalid name
	fi
else
	echo Invalid TARGET. Did you set one?
fi
