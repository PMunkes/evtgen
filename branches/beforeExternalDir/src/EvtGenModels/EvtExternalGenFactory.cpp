//--------------------------------------------------------------------------
//
// Environment:
//      This software is part of the EvtGen package. If you use all or part
//      of it, please give an appropriate acknowledgement.
//
// Copyright Information: See EvtGen/COPYRIGHT
//      Copyright (C) 2011      University of Warwick, UK
//
// Module: EvtExternalGenFactory
//
// Description: A factory type method to create engines for external physics
// generators like Pythia.
//
// Modification history:
//
//    John Back       April 2011            Module created
//
//------------------------------------------------------------------------------
//

#include "EvtGenBase/EvtPatches.hh"
#include "EvtGenModels/EvtExternalGenFactory.hh"
#include "EvtGenBase/EvtReport.hh"

#ifdef EVTGEN_PYTHIA
#include "EvtGenModels/EvtPythiaEngine.hh"
#endif

#ifdef EVTGEN_PHOTOS
#include "EvtGenModels/EvtPhotosEngine.hh"
#endif

#ifdef EVTGEN_TAUOLA
#include "EvtGenModels/EvtTauolaEngine.hh"
#endif

#include <iostream>
using std::endl;

EvtExternalGenFactory::EvtExternalGenFactory() {

  _extGenMap.clear();

}

EvtExternalGenFactory::~EvtExternalGenFactory() {

  ExtGenMap::iterator iter;
  for (iter = _extGenMap.begin(); iter != _extGenMap.end(); ++iter) {

    EvtAbsExternalGen* theGenerator = iter->second;
    delete theGenerator;

  }
  
  _extGenMap.clear();

}

EvtExternalGenFactory* EvtExternalGenFactory::getInstance() {

  static EvtExternalGenFactory* theFactory = 0;
  
  if (theFactory == 0) {
    theFactory = new EvtExternalGenFactory();
  }

  return theFactory;

}

void EvtExternalGenFactory::definePythiaGenerator(std::string xmlDir, bool convertPhysCodes) {

  // Only define the generator if we have the external ifdef variable set
#ifdef EVTGEN_PYTHIA

  int genId = EvtExternalGenFactory::PythiaGenId;

  report(INFO,"EvtGen")<<"Defining EvtPythiaEngine: data tables defined in "
		       <<xmlDir<<endl;

  if (convertPhysCodes == true) {
    report(INFO,"EvtGen")<<"Pythia 6 codes in decay files will be converted to Pythia 8 codes"<<endl;
  } else {
    report(INFO,"EvtGen")<<"Pythia 8 codes need to be used in decay files"<<endl;
  }

  EvtAbsExternalGen* pythiaGenerator = new EvtPythiaEngine(xmlDir, convertPhysCodes);
  _extGenMap[genId] = pythiaGenerator;

#endif

}

void EvtExternalGenFactory::definePhotosGenerator(std::string photonType) {

#ifdef EVTGEN_PHOTOS

  int genId = EvtExternalGenFactory::PhotosGenId;
  report(INFO,"EvtGen")<<"Defining EvtPhotosEngine using photonType = "<<photonType<<endl;
  EvtAbsExternalGen* photosGenerator = new EvtPhotosEngine(photonType);
  _extGenMap[genId] = photosGenerator;

#endif

}

void EvtExternalGenFactory::defineTauolaGenerator() {

#ifdef EVTGEN_TAUOLA

  int genId = EvtExternalGenFactory::TauolaGenId;
  report(INFO,"EvtGen")<<"Defining EvtTauolaEngine."<<endl;
  EvtAbsExternalGen* tauolaGenerator = new EvtTauolaEngine();
  _extGenMap[genId] = tauolaGenerator;

#endif

}

EvtAbsExternalGen* EvtExternalGenFactory::getGenerator(int genId) {

  EvtAbsExternalGen* theGenerator(0);

  ExtGenMap::iterator iter;

  if ((iter = _extGenMap.find(genId)) != _extGenMap.end()) {

    // Retrieve the external generator engine
    theGenerator = iter->second;

  }

  return theGenerator;

}

void EvtExternalGenFactory::initialiseAllGenerators() {

  ExtGenMap::iterator iter;
  for (iter = _extGenMap.begin(); iter != _extGenMap.end(); ++iter) {

    EvtAbsExternalGen* theGenerator = iter->second;
    if (theGenerator != 0) {
      theGenerator->initialise();
    }

  }
  
}
