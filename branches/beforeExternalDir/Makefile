include ./config.mk

default: lib_shared lib_archive

lib_shared:  
	$(MAKE) -C $(SRCDIR) lib_shared

lib_archive: 
	$(MAKE) -C $(SRCDIR) lib_archive

distclean: clean
	rm -rf  tmp/ bin/ lib/
	rm -f config.mk fort.*

clean: 
	$(MAKE) -C $(SRCDIR) clean

help:
	@echo "A list of targets to make:"
	@echo ""
	@echo "lib_shared:  compiles EvtGen as a shared library and puts it into ./lib"
	@echo "lib_archive: compiles EvtGen as an archive library and puts it into ./lib/archive"
	@echo "default:     lib_shared lib_archive"
	@echo "clean:       removes all libraries, executables and objects"
	@echo "distclean:   same as 'clean' plus removing ./config.mk, tmp/ and lib/ directories"
	@echo ""

.PHONY: examples distclean clean	

