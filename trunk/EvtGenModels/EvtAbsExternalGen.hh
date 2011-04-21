// Abstract pure base class interface for external physics generators

#ifndef EVTABS_EXTERNALGEN_HH
#define EVTABS_EXTERNALGEN_HH

#include "EvtGenBase/EvtParticle.hh"

class EvtAbsExternalGen {

public:

  EvtAbsExternalGen() {};
  virtual ~EvtAbsExternalGen() {};

  virtual bool doDecay(EvtParticle* theMother) = 0;

protected:

  virtual void initialise() = 0;

private:

};

#endif
