#!/bin/bash

#DETECTOR=/epics/synApps/support/areaDetector-3-2
DETECTOR=
TARGET=

if ! [ -z $1 ]; then
	TARGET=$1
fi

if [ -z $DETECTOR ]; then
    echo No areaDetector path set. Exiting
    exit 1
fi

if ! [ -z $TARGET ]; then
	echo name of AD plugin to add:
	read PLUGIN
	PLUGIN_DIR="$(ls $DETECTOR | grep -m 1 $PLUGIN)"
	if [ -z $PLUGIN_DIR ]; then
	    echo Invalid plugin name.
	else
	    PLUGIN=$PLUGIN_DIR
	    echo copying $PLUGIN_DIR...
	    APP="$(ls $DETECTOR/$PLUGIN | grep App)"

	    HOME="$(pwd)"
	    cd $DETECTOR
	    AD_DIR="$(echo ${PWD##*/})"
	    cd $HOME
	    mkdir -p $TARGET/$AD_DIR/$PLUGIN/$APP
	    AD_DIR=$TARGET/$AD_DIR
		
	    cp -r -n $DETECTOR/$PLUGIN/bin $AD_DIR/$PLUGIN
	    cp -r -n $DETECTOR/$PLUGIN/db $AD_DIR/$PLUGIN
	    cp -r -n $DETECTOR/$PLUGIN/documentation $AD_DIR/$PLUGIN
	    cp -r -n $DETECTOR/$PLUGIN/iocs $AD_DIR/$PLUGIN
	    cp -r -n $DETECTOR/$PLUGIN/lib $AD_DIR/$PLUGIN
	    cp -r -n $DETECTOR/$PLUGIN/$APP/Db $AD_DIR/$PLUGIN/$APP
	    cp -r -n $DETECTOR/$PLUGIN/$APP/op $AD_DIR/$PLUGIN/$APP
	fi
else
	echo Invalid TARGET. Did you set one?
fi
