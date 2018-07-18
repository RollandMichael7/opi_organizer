#!/bin/bash

#BASE=/epics/base-7.0.1.1
#DETECTOR=/home/mrolland/Documents/epics/synAppsRelease/synApps/support/areaDetector-master
#EPICS=/home/mrolland/Documents/epics/synAppsRelease/synApps/support
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

if ! [ -z $1 ]; then
	TARGET=$1
fi

if ! [ -z $TARGET ]; then
	mkdir -p $TARGET

	HOME="$(pwd)"
	
	cd $DETECTOR
	AD_DIR="$(echo ${PWD##*/})"
	cd $HOME
	mkdir -p $TARGET/$AD_DIR
	AD_DIR=$TARGET/$AD_DIR

	cd $BASE
	BASE_DIR="$(echo ${PWD##*/})"
	cd $HOME
	mkdir -p $TARGET/$BASE_DIR
	cp -r -n $BASE/bin $TARGET/$BASE_DIR

	echo looking for ADCore...
	# CORE="$(ls $DETECTOR | grep -m 1 ADCore)"
	# if ! [ -z $CORE ]; then
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
	# else
	        # echo Not found
	# fi

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

	echo looking for ADSupport...
	SUPPORT="$(ls $DETECTOR | grep -m 1 ADSupport)"
	if ! [ -z $SUPPORT ]; then
	    echo copying $SUPPORT...
	    mkdir -p $AD_DIR/$SUPPORT
	    cp -r -n $DETECTOR/$SUPPORT/bin $AD_DIR/$SUPPORT
	    cp -r -n $DETECTOR/$SUPPORT/lib $AD_DIR/$SUPPORT
	    cp -r -n $DETECTOR/$SUPPORT/supportApp $AD_DIR/$SUPPORT
	    echo done.
	else
	    echo Not found.
	fi

	echo looking for asyn...
	ASYN="$(ls $EPICS | grep -m 1 asyn)"
	if ! [ -z $ASYN ]; then
	    echo copying $ASYN...
	    mkdir -p $TARGET/$ASYN
	    cp -r -n $EPICS/$ASYN/bin $TARGET/$ASYN
	    cp -r -n $EPICS/$ASYN/db $TARGET/$ASYN
	    cp -r -n $EPICS/$ASYN/opi $TARGET/$ASYN
	    cp -r -n $EPICS/$ASYN/lib $TARGET/$ASYN
	    echo done.
	else
	    echo Not found.
	fi

	echo looking for autosave...
	SAVE="$(ls $EPICS | grep -m 1 autosave)"
	if ! [ -z $SAVE ]; then
	    echo copying $SAVE...
	    mkdir -p $TARGET/$SAVE/asApp
	    cp -r -n $EPICS/$SAVE/asApp/Db $TARGET/$SAVE/asApp
	    cp -r -n $EPICS/$SAVE/asApp/op $TARGET/$SAVE/asApp
	    cp -r -n $EPICS/$SAVE/bin $TARGET/$SAVE
	    echo done.
	else
	    echo Not found.
	fi

	echo looking for busy...
	BUSY="$(ls $EPICS | grep -m 1 busy)"
	if ! [ -z $BUSY ]; then
	    echo copying $BUSY...
	    mkdir -p $TARGET/$BUSY/busyApp
	    cp -r -n $EPICS/$BUSY/busyApp/Db $TARGET/$BUSY/busyApp
	    cp -r -n $EPICS/$BUSY/busyApp/op $TARGET/$BUSY/busyApp
	    echo done.
	fi

	echo looking for calc...
	CALC="$(ls $EPICS | grep -m 1 calc)"
	if ! [ -z $CALC ]; then
	    echo copying $CALC...
	    mkdir -p $TARGET/$CALC/calcApp
	    cp -r -n $EPICS/$CALC/calcApp/Db $TARGET/$CALC/calcApp
	    cp -r -n $EPICS/$CALC/calcApp/op $TARGET/$CALC/calcApp
	    echo done.
	else
	    echo Not found.
	fi

	echo looking for devIocStats...
	DSTATS="$(ls $EPICS | grep -m 1 devIocStats)"
	if ! [ -z $DSTATS ]; then
	    echo copying $DSTATS...
	    mkdir -p $TARGET/$DSTATS
	    cp -r -n $EPICS/$DSTATS/bin $TARGET/$DSTATS
	    cp -r -n $EPICS/$DSTATS/lib $TARGET/$DSTATS
	    cp -r -n $EPICS/$DSTATS/db $TARGET/$DSTATS
	    cp -r -n $EPICS/$DSTATS/op $TARGET/$DSTATS
	    echo done.
	else
	    echo Not found.
	fi

	echo looking for iocStats...
	STATS="$(ls $EPICS | grep -m 1 iocStats)"
	if ! [ -z $STATS ]; then
	    echo copying $STATS...
	    mkdir -p $TARGET/$STATS
	    cp -r -n $EPICS/$STATS/bin $TARGET/$STATS
	    cp -r -n $EPICS/$STATS/lib $TARGET/$STATS
	    cp -r -n $EPICS/$STATS/db $TARGET/$STATS
	    cp -r -n $EPICS/$STATS/op $TARGET/$STATS
	    echo done.
	else
	    echo Not found.
	fi

	echo looking for sscan...
	SCAN="$(ls $EPICS | grep -m 1 sscan)"
	if ! [ -z $SCAN ]; then
	    echo copying $SCAN...
	    mkdir -p $TARGET/$SCAN/sscanApp
	    cp -r -n $EPICS/$SCAN/sscanApp/Db $TARGET/$SCAN/sscanApp
	    cp -r -n $EPICS/$SCAN/sscanApp/op $TARGET/$SCAN/sscanApp
	    echo done.
	else
	    echo Not found.
	fi

	echo looking for seq...
	SEQ="$(ls $EPICS | grep -m 1 seq)"
	if ! [ -z $SEQ ]; then
	    echo copying $SEQ...
	    mkdir -p $TARGET/$SEQ
	    cp -r -n $EPICS/$SEQ/lib $TARGET/$SEQ
	    cp -r -n $EPICS/$SEQ/bin $TARGET/$SEQ
	    echo done.
	else
	    echo Not found.
	fi

	echo creating envPaths file...
	cd $TARGET/$ASYN
	ASYN_DIR="$(pwd)"
	cd $HOME
	cd $TARGET/$BUSY
	BUSY_DIR="$(pwd)"
	cd $HOME
	cd $TARGET/$SAVE
	SAVE_DIR="$(pwd)"
	cd $HOME
	cd $TARGET/$CALC
	CALC_DIR="$(pwd)"
	cd $HOME
	cd $TARGET/$SEQ
	SEQ_DIR="$(pwd)"
	cd $HOME
	cd $TARGET/$SCAN
	SCAN_DIR="$(pwd)"
	cd $HOME
	if ! [ -z $STATS ]; then
	    cd $TARGET/$STATS
	    STATS_DIR="$(pwd)"
	    cd $HOME
	else
	    cd $TARGET/$DSTATS
	    STATS_DIR="$(pwd)"
	    cd $HOME
	fi
	cd $TARGET
	SUPPORT_DIR="$(pwd)"
	cd $HOME
	cd $AD_DIR
	AD_DIR="$(pwd)"
	cd $HOME
	cd $TARGET/$BASE_DIR
        BASE_DIR="$(pwd)"
	cd $HOME
	
	#echo $IOC_DIR
	#echo $ASYN_DIR
	#echo $BUSY_DIR
	#echo $SAVE_DIR
	#echo $CALC_DIR
	#echo $SEQ_DIR
	#echo $SCAN_DIR
	#echo $STATS_DIR
	#echo $EPICS_DIR
	#echo $AD_DIR

	cd $TARGET
	echo \# put this file in IOC folders to use this deployment. > envPaths
	echo \# plugins added with fullDeploy.sh will automatically have this file with appropriate paths copied in. >> envPaths
	echo >> envPaths
	echo epicsEnvSet\(\"SUPPORT\", \"$SUPPORT_DIR\"\) >> envPaths
	echo epicsEnvSet\(\"ASYN\", \"$ASYN_DIR\"\) >> envPaths
	echo epicsEnvSet\(\"AREA_DETECTOR\", \"$AD_DIR\"\) >> envPaths
	echo epicsEnvSet\(\"ADSUPPORT\", \"$AD_DIR/$SUPPORT\"\) >> envPaths
	echo epicsEnvSet\(\"ADCORE\", \"$AD_DIR/ADCore\"\) >> envPaths
	echo epicsEnvSet\(\"AUTOSAVE\", \"$SAVE_DIR\"\) >> envPaths
	echo epicsEnvSet\(\"BUSY\", \"$BUSY_DIR\"\) >> envPaths
	echo epicsEnvSet\(\"CALC\", \"$CALC_DIR\"\) >> envPaths
	echo epicsEnvSet\(\"SNSEQ\", \"$SEQ_DIR\"\) >> envPaths
	echo epicsEnvSet\(\"SSCAN\", \"$SCAN_DIR\"\) >> envPaths
	echo epicsEnvSet\(\"DEVIOCSTATS\", \"$STATS_DIR\"\) >> envPaths
	echo epicsEnvSet\(\"EPICS_BASE\", \"$BASE_DIR\"\) >> envPaths
	echo \# epicsEnvSet\(\"TOP\", \"\<path to plugin/iocs/pluginIOC\>\"\) >> envPaths
	echo \# epicsEnvSet\(\"IOC\", \"\<iocPlugin\>\"\) >> envPaths
	echo \# epicsEnvSet\(\"\<PLUGIN_NAME\>\", \"\<path to plugin\>\"\) >> envPaths
	cd $HOME
	
	echo done.

	if ! [ -z $2 ]; then
	    PLUGIN=$2
	else
	    echo Enter name of an AD plugin to add or \"done\" to exit:
	    read PLUGIN
	fi
	while ! [ $PLUGIN = done ]; do
	    PLUGIN="$(ls $DETECTOR | grep -m 1 $PLUGIN)"
	    if [ -z $PLUGIN ]; then
		echo Invalid plugin name.
	    else
		echo copying $PLUGIN...
		APP="$(ls $DETECTOR/$PLUGIN | grep App)"

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
		echo done.

		echo making envPaths file...
		
		cd $AD_DIR/$PLUGIN
		PLUG_ABSPATH=$(pwd)
		cd $HOME
		IOC_DIR="$(ls -d1 $PLUG_ABSPATH/iocs/** | grep -m 1 IOC)" # iocs/prosilicaIOC
		IOC_DIR="$(ls -d1 $IOC_DIR/iocBoot/** | grep -m 1 ioc)" # iocBoot/iocProsilica
		# echo $IOC_DIR

		cd $TARGET
		cp envPaths $IOC_DIR
		cd $IOC_DIR/../..
		TOP=$(pwd)
		cd $IOC_DIR
		PLUGIN_UPPER="$(echo $PLUGIN | tr a-z A-Z)"
		echo epicsEnvSet\(\"IOC\", \"ioc$PLUGIN\"\) >> envPaths
	        echo epicsEnvSet\(\"TOP\", \"$TOP\"\) >> envPaths
		echo epicsEnvSet\(\"$PLUGIN_UPPER\", \"$TOP/../..\"\) >> envPaths
		echo done.
		cd $HOME
	    fi
	    echo Name of AD plugin to add:
	    read PLUGIN
	done
else
    echo Invalid TARGET. Did you set one?
fi





