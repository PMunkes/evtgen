//--------------------------------------------------------------------------
//
// Environment:
//      This software is part of the EvtGen package developed jointly
//      for the BaBar and CLEO collaborations.  If you use all or part
//      of it, please give an appropriate acknowledgement.
//
// Copyright Information: See EvtGen/COPYRIGHT
//      Copyright (C) 1998      Caltech, UCSB
//
// Module: EvtPythia.cc
//
// Description: Routine to decay a particle according th phase space
//
// Modification history:
//
//    RYD       January 8, 1997       Module created
//
//------------------------------------------------------------------------
//
#include "EvtGenBase/EvtPatches.hh"
#include <stdlib.h>
#include "EvtGenBase/EvtParticle.hh"

#include "EvtGenBase/EvtReport.hh"
#include "EvtGenModels/EvtPythia.hh"

#include "EvtGenModels/EvtExternalGenFactory.hh"
#include "EvtGenModels/EvtAbsExternalGen.hh"
#include "EvtGenBase/EvtDecayBase.hh"

#include <string>

#include <iostream>

EvtPythia::EvtPythia() {

  // Set the Pythia engine to a null pointer at first.
  // When we do the decay, we retrieve the pointer to the Pythia engine
  // and use that for all decays. All clones will use the same Pythia engine.
  _pythiaEngine = 0;

}

EvtPythia::~EvtPythia() {}

std::string EvtPythia::getName(){

  return "PYTHIA";

}

EvtDecayBase* EvtPythia::clone(){

  return new EvtPythia();

}


void EvtPythia::init(){

  // Do not check for any arguments. The PythiaEngine will check
  // to see if there is an integer specifying the decay physics,
  // otherwise it just uses phase-space.

}

void EvtPythia::initProbMax(){

  noProbMax();

}

void EvtPythia::decay( EvtParticle *p ){

  // We have to initialise the Pythia engine after the decay.dec files have been read in,
  // since we will be modifying Pythia data tables, and that is only possible once we have
  // defined all Pythia-type decays we want to use. 
  // We check to see if the engine has been created before doing the decay.
  // This should only create the full Pythia engine once, and all clones will point to the same engine.

  if (_pythiaEngine == 0) {
    _pythiaEngine = EvtExternalGenFactory::getInstance()->getGenerator(EvtExternalGenFactory::PythiaGenId);
  }
    
  if (_pythiaEngine != 0) {
    _pythiaEngine->doDecay(p);
  }

}
