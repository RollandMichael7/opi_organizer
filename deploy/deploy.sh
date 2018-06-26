#!/bin/bash
TARGET=
BASE=/epics/base
DETECTOR=/epics/support4c/areaDetector/
EPICS=/epics/support4c

if [ -z $TARGET ]; then
	TARGET=$1
fi

if ! [ -z $TARGET ]; then
	mkdir -p $TARGET
	cd $TARGET
	mkdir -p areaDetector
	mkdir -p areaDetector/ADCore
	mkdir -p areaDetector/ADCore/ADApp
	mkdir -p areaDetector/ADSupport
	mkdir -p asyn
	mkdir -p autosave
	mkdir -p autosave/asApp
	mkdir -p base
	mkdir -p busy
	mkdir -p busy/busyApp
	mkdir -p calc
	mkdir -p calc/calcApp
	mkdir -p devIocStats
	mkdir -p sscan
	mkdir -p sscan/sscanApp
	
	cp --parents -r -n $BASE/bin ./base

	echo copying ADCore...
	cp -r -n $DETECTOR/ADCore/bin ./areaDetector/ADCore
	cp -r -n $DETECTOR/ADCore/lib ./areaDetector/ADCore
	cp -r -n $DETECTOR/ADCore/db ./areaDetector/ADCore
	cp -r -n $DETECTOR/ADCore/documentation ./areaDetector/ADCore
	cp -r -n $DETECTOR/ADCore/iocBoot ./areaDetector/ADCore
	cp -r -n $DETECTOR/ADCore/Viewers ./areaDetector/ADCore
	cp -r -n $DETECTOR/ADCore/ADApp/Db ./areaDetector/ADCore/ADApp
	cp -r -n $DETECTOR/ADCore/ADApp/op ./areaDetector/ADCore/ADApp

	echo copying ADSupport...
	cp -r -n $DETECTOR/ADSupport/bin ./areaDetector/ADSupport
	
	echo copying asyn...
	cp -r -n $EPICS/asyn/bin ./asyn
	cp -r -n $EPICS/asyn/db ./asyn
	cp -r -n $EPICS/asyn/opi ./asyn
	cp -r -n $EPICS/asyn/lib ./asyn

	echo copying autosave...
	cp -r -n $EPICS/autosave/asApp/Db ./autosave/asApp
	cp -r -n $EPICS/autosave/asApp/op ./autosave/asApp
	cp -r -n $EPICS/autosave/bin ./autosave

	echo copying busy...
	cp -r -n $EPICS/busy/busyApp/Db ./busy
	cp -r -n $EPICS/busy/busyApp/op ./busy

	echo copying calc...
	cp -r -n $EPICS/calc/calcApp/Db ./calc/calcApp
	cp -r -n $EPICS/calc/calcApp/op ./calc/calcApp

	echo copying devIocStats...
	cp -r -n $EPICS/devIocStats/bin ./devIocStats
	cp -r -n $EPICS/devIocStats/lib ./devIocStats
	cp -r -n $EPICS/devIocStats/db ./devIocStats
	cp -r -n $EPICS/devIocStats/op ./devIocStats

	echo copying sscan...
	cp -r -n $EPICS/sscan/sscanApp/Db ./sscan/sscanApp
	cp -r -n $EPICS/sscan/sscanApp/op ./sscan/sscanApp

	echo done.
else
	echo invalid TARGET. Did you set one?
fi





