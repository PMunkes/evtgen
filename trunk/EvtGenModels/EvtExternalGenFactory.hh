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

#ifndef EVTEXTERNALGENFACTORY_HH
#define EVTEXTERNALGENFACTORY_HH

#include "EvtGenModels/EvtAbsExternalGen.hh"

#include <map>

class EvtExternalGenFactory {

public:
  
  enum genId {PythiaGenId = 0};

  static EvtExternalGenFactory* getInstance();

  EvtAbsExternalGen* getGenerator(int genId = 0);

  void definePythiaGenerator(std::string xmlDir, bool convertPhysCodes);

protected:

  EvtExternalGenFactory();
  ~EvtExternalGenFactory();

  typedef std::map<int, EvtAbsExternalGen*> ExtGenMap;

private:

  EvtExternalGenFactory(const EvtExternalGenFactory&) {};

  ExtGenMap _extGenMap;

};

#endif
