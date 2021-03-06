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
// Module: EvtGen/EvtVSSMix.hh
//
// Description:
//
// Modification history:
//
//    DJL/RYD     August 11, 1998         Module created
//
//------------------------------------------------------------------------

#ifndef EVTVSSMIX_HH
#define EVTVSSMIX_HH

#include "EvtGenBase/EvtDecayAmp.hh"

class EvtParticle;

class EvtVSSMix:public  EvtDecayAmp  {

public:

  EvtVSSMix() {}
  virtual ~EvtVSSMix();

  std::string getName();
  EvtDecayBase* clone();

  void decay(EvtParticle *p); 
  void init();
  void initProbMax();

  std::string getParamName(int i);
};

#endif
