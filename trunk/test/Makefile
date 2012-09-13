CXX = g++
CXXFLAGS = -g -Wall -fPIC
LD = g++
LDFLAGS = -g
SOFLAGS = -shared

# Base directory where the EvtGen libraries are
BASEDIR = ../

# Read in the config.mk file in the base directory to extract where
# the external libraries are, as well as setting compiler flags etc..

include ${BASEDIR}/config.mk
include extraConfig.mk

# Need to first add EvtGen libraries, then HepMC, then Photos, Tauola and Pythia,
# since Photos depends on HepMC etc..                                            

allLibDir=-L$(HEPMCLIBDIR)
allLibs=$(HEPMCLIBLIST)   

ifeq ("$(EVTGEN_PHOTOS)", "1")
        allLibDir+=-L$(PHOTOSLIBDIR)
        allLibs+=$(PHOTOSLIBLIST)   
endif

ifeq ("$(EVTGEN_PYTHIA)", "1")
        allLibDir+=-L$(PYTHIALIBDIR)
        allLibs+=$(PYTHIALIBLIST)
endif

ifeq ("$(EVTGEN_TAUOLA)", "1")
        allLibDir+=-L$(TAUOLALIBDIR)
        allLibs+=$(TAUOLALIBLIST)
endif

GENLIBS = -L${BASEDIR}/lib/archive ${allLibDir} -lEvtGen -lgfortran ${allLibs}

INCLUDEDIR = ${BASEDIR}

CXXFLAGS      += $(ROOTCFLAGS)
LIBS           = $(ROOTLIBS)
NGLIBS         = $(ROOTGLIBS)
NGLIBS        += -lMinuit
GLIBS          = $(filter-out -lNew, $(NGLIBS))

.SUFFIXES: .cc

# ================================================================================
default: evtgenlhc_test1 evt_dalitz example1

evtgenlhc_test1: evtgenlhc_test1.o
	$(CXX) $(CXXFLAGS) -o evtgenlhc_test1 evtgenlhc_test1.o $(GENLIBS) $(LIBS)

evt_dalitz: evt_dalitz.o
	$(CXX) $(CXXFLAGS) -o evt_dalitz evt_dalitz.o $(GENLIBS) $(LIBS)

example1: example1.o
	$(CXX) $(CXXFLAGS) -o example1 example1.o $(GENLIBS) $(LIBS)

.cc.o:
	$(CXX) $(CXXFLAGS) -c -o $@ $< -I$(INCLUDEDIR) -I$(HEPMCINCDIR)

clean:
	rm -f evtgenlhc_test1 evt_dalitz example1 *.o
