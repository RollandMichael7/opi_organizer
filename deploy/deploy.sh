#!/bin/bash

# BASE=/epics/base-7-0-1-1
# DETECTOR=/epics/synApps/support/areaDetector-3-2
# EPICS=/epics/synApps/support
TARGET=
BASE=
DETECTOR=
EPICS=

if [ -z $BASE ]; then
    echo No EPICS base path set. Exiting
    exit 1
fi

if [ -z $DETECTOR ]; then
    echo No areaDetector path set. Exiting
    exit 1
fi

if [ -z $EPICS ]; then
    echo No EPICS modules path set. Exiting
    exit 1
fi

if [ -z $TARGET ]; then
	TARGET=$1
fi

if ! [ -z $TARGET ]; then
	mkdir -p $TARGET

	AD_DIR="$(ls $DETECTOR/.. | grep -m 1 areaDetector)"
	mkdir -p $TARGET/$AD_DIR
	AD_DIR=$TARGET/$AD_DIR

	BASE_DIR="$(ls $BASE/.. | grep -m 1 base)"
	mkdir -p $TARGET/$BASE_DIR
	cp -r -n $BASE/bin $TARGET/$BASE_DIR

	# CORE="$(ls $DETECTOR | grep -m 1 ADCore)"
	# echo copying $CORE...
	# mkdir -p $TARGET/areaDetector/$CORE/ADApp
	# cp -r -n $DETECTOR/$CORE/bin $AD_DIR/$CORE
	# cp -r -n $DETECTOR/$CORE/lib $AD_DIR/$CORE
	# cp -r -n $DETECTOR/$CORE/db $AD_DIR/$CORE
	# cp -r -n $DETECTOR/$CORE/documentation $AD_DIR/$CORE
	# cp -r -n $DETECTOR/$CORE/iocBoot $AD_DIR/$CORE
	# cp -r -n $DETECTOR/$CORE/Viewers $AD_DIR/$CORE
	# cp -r -n $DETECTOR/$CORE/ADApp/Db $AD_DIR/$CORE/ADApp
	# cp -r -n $DETECTOR/$CORE/ADApp/op $AD_DIR/$CORE/ADApp

	echo copying ADCore...
	mkdir -p $AD_DIR/ADCore/ADApp
	cp -r -n $DETECTOR/ADCore/bin $AD_DIR/ADCore
	cp -r -n $DETECTOR/ADCore/lib $AD_DIR/ADCore
	cp -r -n $DETECTOR/ADCore/db $AD_DIR/ADCore
	cp -r -n $DETECTOR/ADCore/documentation $AD_DIR/ADCore
	cp -r -n $DETECTOR/ADCore/iocBoot $AD_DIR/ADCore
	cp -r -n $DETECTOR/ADCore/Viewers $AD_DIR/ADCore
	cp -r -n $DETECTOR/ADCore/ADApp/Db $AD_DIR/ADCore/ADApp
	cp -r -n $DETECTOR/ADCore/ADApp/op $AD_DIR/ADCore/ADApp

	SUPPORT="$(ls $DETECTOR | grep -m 1 ADSupport)"
	echo copying $SUPPORT...
	mkdir -p $AD_DIR/$SUPPORT
	cp -r -n $DETECTOR/$SUPPORT/bin $AD_DIR/$SUPPORT
	
	ASYN="$(ls $EPICS | grep -m 1 asyn)"
	echo copying $ASYN...
	mkdir -p $TARGET/$ASYN
	cp -r -n $EPICS/$ASYN/bin $TARGET/$ASYN
	cp -r -n $EPICS/$ASYN/db $TARGET/$ASYN
	cp -r -n $EPICS/$ASYN/opi $TARGET/$ASYN
	cp -r -n $EPICS/$ASYN/lib $TARGET/$ASYN

	SAVE="$(ls $EPICS | grep -m 1 autosave)"
	echo copying $SAVE...
	mkdir -p $TARGET/$SAVE/asApp
	cp -r -n $EPICS/$SAVE/asApp/Db $TARGET/$SAVE/asApp
	cp -r -n $EPICS/$SAVE/asApp/op $TARGET/$SAVE/asApp
	cp -r -n $EPICS/$SAVE/bin $TARGET/$SAVE

	BUSY="$(ls $EPICS | grep -m 1 busy)"
	echo copying $BUSY...
	mkdir -p $TARGET/$BUSY/busyApp
	cp -r -n $EPICS/$BUSY/busyApp/Db $TARGET/$BUSY/busyApp
	cp -r -n $EPICS/$BUSY/busyApp/op $TARGET/$BUSY/busyApp

	CALC="$(ls $EPICS | grep -m 1 calc)"
	echo copying $CALC...
	mkdir -p $TARGET/$CALC/calcApp
	cp -r -n $EPICS/$CALC/calcApp/Db $TARGET/$CALC/calcApp
	cp -r -n $EPICS/$CALC/calcApp/op $TARGET/$CALC/calcApp

	DSTATS="$(ls $EPICS | grep -m 1 devIocStats)"
	echo copying $DSTATS...
	mkdir -p $TARGET/$DSTATS
	cp -r -n $EPICS/$DSTATS/bin $TARGET/$DSTATS
	cp -r -n $EPICS/$DSTATS/lib $TARGET/$DSTATS
	cp -r -n $EPICS/$DSTATS/db $TARGET/$DSTATS
	cp -r -n $EPICS/$DSTATS/op $TARGET/$DSTATS

	STATS="$(ls $EPICS | grep -m 1 iocStats)"
	echo copying $STATS...
	mkdir -p $TARGET/$STATS
	cp -r -n $EPICS/$STATS/bin $TARGET/$STATS
	cp -r -n $EPICS/$STATS/lib $TARGET/$STATS
	cp -r -n $EPICS/$STATS/db $TARGET/$STATS
	cp -r -n $EPICS/$STATS/op $TARGET/$STATS

	SCAN="$(ls $EPICS | grep -m 1 sscan)"
	echo copying $SCAN...
	mkdir -p $TARGET/$SCAN/sscanApp
	cp -r -n $EPICS/$SCAN/sscanApp/Db $TARGET/$SCAN/sscanApp
	cp -r -n $EPICS/$SCAN/sscanApp/op $TARGET/$SCAN/sscanApp

	echo done.
else
	echo Invalid TARGET. Did you set one?
fi





