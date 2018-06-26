#!/bin/bash
DETECTOR=/epics/support4c/areaDetector
TARGET=./test/areaDetector

echo name of AD plugin to add:
read plugin
if [ -d $DETECTOR/$plugin ]; then
	app="$(ls $DETECTOR/$plugin | grep App)"
	mkdir -p $TARGET/$plugin
	mkdir -p $TARGET/$plugin/$app

	cp -r -n $DETECTOR/$plugin/bin $TARGET/$plugin
	cp -r -n $DETECTOR/$plugin/db $TARGET/$plugin
	cp -r -n $DETECTOR/$plugin/documentation $TARGET/$plugin
	cp -r -n $DETECTOR/$plugin/iocs $TARGET/$plugin
	cp -r -n $DETECTOR/$plugin/$app/Db $TARGET/$plugin/$app
	cp -r -n $DETECTOR/$plugin/$app/op $TARGET/$plugin/$app
else
	echo Invalid name
fi
