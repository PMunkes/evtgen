// A factory type method to create engines for external physics
// generators like Pythia. Unfortunately, this needs to be yet another
// static factory method, since decay models are implemented in
// EvtGenModels, which EvtParticles then have to know about when decay models 
// are "cloned". The problem is that particles are defined in the EvtGenBase 
// directory, which cannot depend on EvtGenModel classes. 
// What should happen is that the particle-decay_model link should be done 
// within classes that use both EvtGenModels and EvtGenBase classes, in an 
// "EvtGenDecay" directory, but this will involve significant redesign of EvtGen 
// itself. These class interface problems explains why static variables/methods 
// are used, and are indeed needed, all over the place in order to pass info to 
// and from the particles and decay models.

#include "EvtGenBase/EvtPatches.hh"
#include <stdlib.h>
#include "EvtGenModels/EvtExternalGenFactory.hh"

#include "EvtGenModels/EvtPythiaEngine.hh"

#include <iostream>
using std::cout;
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

  int genId = EvtExternalGenFactory::PythiaGenId;

  EvtAbsExternalGen* pythiaGenerator = new EvtPythiaEngine(xmlDir, convertPhysCodes);
  _extGenMap[genId] = pythiaGenerator;

}

EvtAbsExternalGen* EvtExternalGenFactory::getGenerator(int genId) {

  EvtAbsExternalGen* theGenerator(0);

  ExtGenMap::iterator iter;

  if ((iter = _extGenMap.find(genId)) != _extGenMap.end()) {

    // Retrieve the external generator engine
    theGenerator = iter->second;

  } else {

    cout<<"EvtAbsExternalGen::getGenerator: could not find generator for genId = "<<genId<<endl;

  }

  return theGenerator;

}
