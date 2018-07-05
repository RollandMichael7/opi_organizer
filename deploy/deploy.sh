#!/bin/bash
TARGET=
BASE=/epics/base-7.0.1.1
# DETECTOR=/home/mrolland/Documents/epics/synAppsRelease/synApps/support/areaDetector-3-3-1
DETECTOR=
# EPICS=/home/mrolland/Documents/epics/synAppsRelease/synApps/support
EPICS=

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
	mkdir -p iocStats
	mkdir -p sscan
	mkdir -p sscan/sscanApp
	
	cp --parents -r -n $BASE/bin $TARGET/base

	echo copying ADCore...
	cp -r -n $DETECTOR/ADCore/bin $TARGET/areaDetector/ADCore
	cp -r -n $DETECTOR/ADCore/lib $TARGET/areaDetector/ADCore
	cp -r -n $DETECTOR/ADCore/db $TARGET/areaDetector/ADCore
	cp -r -n $DETECTOR/ADCore/documentation $TARGET/areaDetector/ADCore
	cp -r -n $DETECTOR/ADCore/iocBoot $TARGET/areaDetector/ADCore
	cp -r -n $DETECTOR/ADCore/Viewers $TARGET/areaDetector/ADCore
	cp -r -n $DETECTOR/ADCore/ADApp/Db $TARGET/areaDetector/ADCore/ADApp
	cp -r -n $DETECTOR/ADCore/ADApp/op $TARGET/areaDetector/ADCore/ADApp

	echo copying ADSupport...
	cp -r -n $DETECTOR/ADSupport/bin $TARGET/areaDetector/ADSupport
	
	echo copying asyn...
	cp -r -n $EPICS/asyn/bin $TARGET/asyn
	cp -r -n $EPICS/asyn/db $TARGET/asyn
	cp -r -n $EPICS/asyn/opi $TARGET/asyn
	cp -r -n $EPICS/asyn/lib $TARGET/asyn

	echo copying autosave...
	cp -r -n $EPICS/autosave/asApp/Db $TARGET/autosave/asApp
	cp -r -n $EPICS/autosave/asApp/op $TARGET/autosave/asApp
	cp -r -n $EPICS/autosave/bin $TARGET/autosave

	echo copying busy...
	cp -r -n $EPICS/busy/busyApp/Db $TARGET/busy
	cp -r -n $EPICS/busy/busyApp/op $TARGET/busy

	echo copying calc...
	cp -r -n $EPICS/calc/calcApp/Db $TARGET/calc/calcApp
	cp -r -n $EPICS/calc/calcApp/op $TARGET/calc/calcApp

	echo copying devIocStats...
	cp -r -n $EPICS/devIocStats/bin $TARGET/devIocStats
	cp -r -n $EPICS/devIocStats/lib $TARGET/devIocStats
	cp -r -n $EPICS/devIocStats/db $TARGET/devIocStats
	cp -r -n $EPICS/devIocStats/op $TARGET/devIocStats

	echo copying iocStats...
	cp -r -n $EPICS/iocStats/bin $TARGET/iocStats
	cp -r -n $EPICS/iocStats/lib $TARGET/iocStats
	cp -r -n $EPICS/iocStats/db $TARGET/iocStats
	cp -r -n $EPICS/iocStats/op $TARGET/iocStats

	echo copying sscan...
	cp -r -n $EPICS/sscan/sscanApp/Db $TARGET/sscan/sscanApp
	cp -r -n $EPICS/sscan/sscanApp/op $TARGET/sscan/sscanApp

	echo done.
else
	echo invalid TARGET. Did you set one?
fi





