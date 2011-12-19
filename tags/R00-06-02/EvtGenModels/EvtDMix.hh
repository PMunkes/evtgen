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
// Module: EvtGen/EvtPhsp.hh
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

#ifndef EVTDMIX_HH
#define EVTDMIX_HH

#include "EvtGenBase/EvtDecayIncoherent.hh"

class EvtParticle;

class EvtDMix:public  EvtDecayIncoherent  {

public:
  
  EvtDMix() {}
  virtual ~EvtDMix();

  std::string getName();

  EvtDecayBase* clone();

  void initProbMax();

  void init();

  void decay(EvtParticle *p); 

private:
  double _rd;
  double _xpr;
  double _ypr;

};

#endif

