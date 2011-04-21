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
// Module: EvtGen/EvtPythia.hh
//
// Description:
//Class to handle generic phase space decays not done
//in other decay models.
//
// Modification history:
//
//    DJL/RYD     August 11, 1998         Module created
//
//------------------------------------------------------------------------

#ifndef EVTPYTHIA_HH
#define EVTPYTHIA_HH

#include "EvtGenBase/EvtDecayIncoherent.hh"

class EvtParticle;
class EvtAbsExternalGen;
class EvtDecayBase;

class EvtPythia: public  EvtDecayIncoherent  {

public:
  
  EvtPythia();
  virtual ~EvtPythia();

  std::string getName();

  EvtDecayBase* clone();

  void initProbMax();

  void init();

  void decay(EvtParticle *p); 

protected:

  EvtAbsExternalGen* _pythiaEngine;

};

#endif

