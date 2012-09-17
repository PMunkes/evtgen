include ../config.mk

TMPDIR=../tmp

sources := $(shell find . -type 'f' -name '*.cpp')
sources += $(shell find . -type 'f' -name '*.[Ff]')
objects := $(shell echo $(sources) | sed 's,\./,$(TMPDIR)/,g;s,\.cpp,\.o,g;s,\.F,\.o,g;')
mkfiles := $(shell echo $(sources) | sed 's,\./,$(TMPDIR)/,g;s,\.cpp,\.mk,g;s,\.F,\.mk,g;s,\.f,\.mk,g;')

default: all

all: lib_shared lib_archive

lib_shared: $(LIB_SHARED)

lib_archive: $(LIB_ARCHIVE)

evtgenExclude=EVTGEN_PHOTOS

allShLibs=-L$(HEPMCSHLIBDIR) $(HEPMCLIBLIST)

allIncDir=-I$(INCLUDEDIR)
allIncDir+=-I$(HEPMCINCDIR)

ifeq ($(EVTGEN_PHOTOS),1)
	allShLibs+=-L$(PHOTOSSHLIBDIR) $(PHOTOSLIBLIST)
	allIncDir+=-I$(PHOTOSINCDIR)
endif
ifeq ($(EVTGEN_TAUOLA),1)
	allShLibs+=-L$(TAUOLASHLIBDIR) $(TAUOLALIBLIST)
	allIncDir+=-I$(TAUOLAINCDIR)
endif
ifeq ($(EVTGEN_PYTHIA),1)
	allShLibs+=-L$(PYTHIASHLIBDIR) $(PYTHIALIBLIST)
	allIncDir+=-I$(PYTHIAINCDIR)
endif

$(LIB_SHARED) : $(objects)
	mkdir -p $(LIBDIR_SHARED)
	@echo creating the shared library $@
	$(CXX) $(LDFLAGSSHARED) $(objects) -o $@ -shared -Wl,-soname,$(notdir $@) $(FLIBS) \
	$(allShLibs)

$(LIB_ARCHIVE) : $(objects)
	ar cru $(LIB_ARCHIVE) $(objects)

#---- The following is for dependency checking:

$(TMPDIR)/%.mk: %.cpp
	echo $(allIncDir)
	$(CXX) -MM $(CXXFLAGS) $(EXTRAFLAGS) $< $(allIncDir) | sed 's,[^ ]*\.o:,$(TMPDIR)/&,' > $@

$(TMPDIR)/%.mk: %.F
	$(FC) $(FFLAGS) -c $< -I$(INCLUDEDIR) | sed 's,[^ ]*\.o:,$(TMPDIR)/&,' > $@


ifneq ($(MAKECMDGOALS),clean)
 ifneq ($(mkfiles),)
  -include $(mkfiles)
 endif
endif

#----

$(TMPDIR)/%.o : %.cpp $(TMPDIR)/%.mk
	$(CXX) $(CXXFLAGS) $(CXXFLAGSSHARED) $(EXTRAFLAGS) -c -o $@ $< $(allIncDir)

$(TMPDIR)/%.o: %.F $(TMPDIR)/%.mk
	$(FC) $(FFLAGS) $(FFLAGSSHARED) -c -o $@ $< -I$(INCLUDEDIR)

$(TMPDIR)/%.o: %.f $(TMPDIR)/%.mk
	$(FC) $(FFLAGS) $(FFLAGSSHARED) -c -o $@ $< -I$(INCLUDEDIR)

.PHONY: clean

clean:
	rm -f *~
	rm -f $(objects) $(mkfiles)
	rm -f $(LIB_SHARED) 
	rm -f $(LIB_ARCHIVE)
