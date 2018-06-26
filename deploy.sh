#!/bin/bash
TARGET=./test
BASE=/epics/base
CORE=/epics/support4c/areaDetector/ADCore
EPICS=/epics/support4c

mkdir -p $TARGET
cd $TARGET
mkdir -p areaDetector
mkdir -p areaDetector/ADCore
mkdir -p areaDetector/ADCore/ADApp
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

cp -r -n $CORE/bin ./areaDetector/ADCore
cp -r -n $CORE/db ./areaDetector/ADCore
cp -r -n $CORE/documentation ./areaDetector/ADCore
cp -r -n $CORE/iocBoot ./areaDetector/ADCore
cp -r -n $CORE/Viewers ./areaDetector/ADCore
cp -r -n $CORE/ADApp/Db ./areaDetector/ADCore/ADApp
cp -r -n $CORE/ADApp/op ./areaDetector/ADCore/ADApp

cp -r -n $EPICS/asyn/bin ./asyn
cp -r -n $EPICS/asyn/db ./asyn
cp -r -n $EPICS/asyn/opi ./asyn

cp -r -n $EPICS/autosave/asApp/Db ./autosave/asApp
cp -r -n $EPICS/autosave/asApp/op ./autosave/asApp
cp -r -n $EPICS/autosave/bin ./autosave

cp -r -n $EPICS/busy/busyApp/Db ./busy
cp -r -n $EPICS/busy/busyApp/op ./busy

cp -r -n $EPICS/calc/calcApp/Db ./calc/calcApp
cp -r -n $EPICS/calc/calcApp/op ./calc/calcApp

cp -r -n $EPICS/devIocStats/bin ./devIocStats
cp -r -n $EPICS/devIocStats/db ./devIocStats
cp -r -n $EPICS/devIocStats/op ./devIocStats

cp -r -n $EPICS/sscan/sscanApp/Db ./sscan/sscanApp
cp -r -n $EPICS/sscan/sscanApp/op ./sscan/sscanApp





