#!/bin/bash

# This script installs EvtGen with all external dependencies. The variable VERSION specifies
# the tag of EvtGen you want to use. The list of available tags can be found using either the
# command "svn ls -v http://svn.cern.ch/guest/evtgen/tags" or by going to the url
# http://svn.cern.ch/guest/evtgen/tags in a web browser. Note that some earlier EvtGen versions
# will not be compatible with all external depedency versions given below, owing to C++
# interface differences; see the specific tagged version of the EvtGen/README file for guidance

VERSION=R01-05-00

mkdir -p EvtGen
cd EvtGen

INSTALL_BASE=`pwd`

echo Will setup EvtGen $VERSION in $INSTALL_BASE

echo Downloading EvtGen from SVN
svn export http://svn.cern.ch/guest/evtgen/tags/$VERSION

echo Downloading external dependencies
mkdir -p external
cd external

# Minimum required versions of the external packages. Later versions should be OK as well,
# assuming their C++ interfaces do not change
wget http://home.thep.lu.se/~torbjorn/pythia8/pythia8180.tgz
wget http://photospp.web.cern.ch/photospp/resources/PHOTOS.3.54/PHOTOS.3.54.tar.gz
wget http://tauolapp.web.cern.ch/tauolapp/resources/TAUOLA.1.1.4/TAUOLA.1.1.4.tar.gz
wget http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-2.06.08.tar.gz

echo Extracting external dependencies
tar -xzf PHOTOS.3.54.tar.gz 
tar -xzf HepMC-2.06.08.tar.gz 
tar -xzf pythia8180.tgz
tar -xzf TAUOLA.1.1.4.tar.gz 

echo Installing HepMC in $INSTALL_BASE/external/HepMC/
mkdir -p HepMC
cd HepMC/
cmake -DCMAKE_INSTALL_PREFIX=$INSTALL_BASE/external/HepMC/ $INSTALL_BASE/external/HepMC-2.06.08/ -Dmomentum:STRING=MEV -Dlength:STRING=MM
make
make install

echo Installing pythia8 in $INSTALL_BASE/external/pythia8180/
cd ../pythia8180/
./configure --with-hepmc=$INSTALL_BASE/external/HepMC/ --with-hepmcversion=2.06.08 --enable-shared
make

echo Installing TAUOLA in $INSTALL_BASE/external/TAUOLA/
cd ../TAUOLA/
./configure --with-hepmc=$INSTALL_BASE/external/HepMC/
make

echo Installing PHOTOS in $INSTALL_BASE/external/PHOTOS/
cd ../PHOTOS/
./configure --with-hepmc=$INSTALL_BASE/external/HepMC/
make

echo Building EvtGen
cd $INSTALL_BASE/$VERSION
./configure --hepmcdir=$INSTALL_BASE/external/HepMC/ --photosdir=$INSTALL_BASE/external/PHOTOS/ --pythiadir=$INSTALL_BASE/external/pythia8180/ --tauoladir=$INSTALL_BASE/external/TAUOLA/
make

echo Setup done.
echo To complete, add the following command to your .bashrc file or run it in your terminal before running any programs that use the EvtGen library:
echo LD_LIBRARY_PATH=$INSTALL_BASE/external/HepMC/lib:$INSTALL_BASE/external/pythia8180/lib:$INSTALL_BASE/external/PHOTOS/lib:$INSTALL_BASE/external/TAUOLA/lib:$INSTALL_BASE/$VERSION/lib:\$LD_LIBRARY_PATH
echo Also set the Pythia8 data path:
echo PYTHIA8DATA=$INSTALL_BASE/external/pythia8180/xmldoc
