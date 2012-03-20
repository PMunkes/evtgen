#!/usr/bin/python
import sys

comments = True

def main(inFile, outFile, extraFiles):
  #open our files
  fh1 = open(inFile,"r")
  fh2 = open(outFile, "w")
  data = fh1.readlines()

  allowedParticles = []
  particleData = {}

  #open extra files to get aliases
  firstWordIsAlias = False
  for file in extraFiles:
    extrafh = open(file,"r")
    extradata = extrafh.readlines()
    for line in extradata:
      words = line.split()
      if len(words) == 0:
        continue
      if firstWordIsAlias:
        allowedParticles.append(words[0])
        firstWordIsAlias = False
      for x in range(len(words)-1):
        if words[x][0] == '#':
          break
        elif words[x] == "Alias":
          allowedParticles.append(words[x+1])
      if words[len(words)-1] == "Alias":
        firstWordIsAlias = True
    extrafh.close()

  #assemble particles list
  fhPDL = open("evt.pdl","r")
  pdlData = fhPDL.readlines()
  for line in pdlData:
    words = line.split()
    if words[0] == "add" and words[2] == "Particle":
      allowedParticles.append(words[3])
  fhPDL.close()

  #keep count of some things
  count = 0
  countComment = 0
  countDec = 0
  countParticle = 0
  countAlias = 0
  countModelAlias = 0
  countDef = 0
  countConj = 0
  countConjDecay = 0
  countLineShapePW = 0
  countPhotos = 0
  countBad = 0
  countCopyDec = 0
  countRemoveDec = 0
  countPythia6 = 0

  #flags to figure out if we're in a decay block
  inDecay = False
  inRemoveDecay = False
  #store unused tokens from previous lines
  previousLine=""
  getMore=True

  #first print the top
  fh2.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
  fh2.write("<?xml-stylesheet href=\"DECAY.XSL\" type=\"text/xsl\" ?>\n")
  fh2.write("<data>\n")
  fh2.write("\t<Title>"+outFile+"</Title>\n")
  fh2.write("\t<Details>XML Decay File for EvtGen - automatically generated by convertDecayFile.py</Details>\n")
  fh2.write("\t<Author>convertDecayFile.py</Author>\n")
  fh2.write("\t<Version>1.0</Version>\n")

  for line in data:
  #add in anything we had previously
    if previousLine:
      line = " ".join([previousLine,line])
    previousLine = ""
    getMore = False
    line = line.strip(" \t")
    while line and not getMore:
      line = line.strip(" \t")
      line = line.lstrip("\n")
      if not line:#catch any lines that were just whitespace here
        continue
    #check if we have a comment
      if line[0] == '#':
        countComment += 1
        if line.find('\n')!=-1:
          comment = line.split('\n',1)[0]
          line = line.split('\n',1)[1]
        else:
          comment = line
          line = ""
        if comments:
          comment = comment.strip("#")
          while comment.find("--") != -1:#illegal sequence in XML comments
            comment = comment.replace("--","-")
          if comment and comment != "-":#ignore empty comments
            comment = "<!--"+comment+" -->\n"
          fh2.write(comment)
        continue
      count += 1
    #split the line into words and check it's not empty
      words = line.split()
      if len(words) == 0:
        fh2.write(line)
        getMore = True
        continue
    #are we currently parsing a decay?
      if inDecay:
        if words[0] == "Enddecay":
          fh2.write("\t</decay>\n")
          inDecay = False
          if len(words) > 1:
            line = " ".join(words[1:])
          else:
            getMore = True
        else:
          br = words[0]
          daughtersList = []
          model = ""
          paramsList = []

    #various flags to deal with the evil format
          photos = False
          summary = False
          verbose = False
          stage = 0 ## 0 - daughters, 1 - PSV/model, 2 - params
          semicolonDetected = False

    #precheck for a semicolon to save ourselves a bit of work
          for word in words:
            if word[-1] == ';':
              semicolonDetected = True
              break

          if not semicolonDetected:  #we're missing some of this line so wait til we have it all
            previousLine = line
            getMore = True
            continue

          semicolonDetected = False

          for x in range(1,len(words)):
            if not semicolonDetected and words[x][-1] == ';':
              semicolonDetected = True
              words[x] = words[x][:-1]

            if stage == 0:
              allowed = set(allowedParticles)
              if words[x] in allowed:
                daughtersList.append(words[x])
              else:
                stage = 1 #fall through into stage 1
            if stage == 1:
              if words[x] == "PHOTOS":
                photos = True
              elif words[x] == "SUMMARY":
                summary = True
              elif words[x] == "VERBOSE":
                verbose = True
              else:
                model = words[x]
                stage = 2 #don't fall through on this lap
            elif stage == 2:
              paramsList.append(words[x])

            if semicolonDetected:
              if len(words) > x+1:
                line = " ".join(words[x+1:])
              else:
                getMore = True
              break

          daughters = " ".join(daughtersList)
          params = " ".join(paramsList)

          toWrite = "\t\t<channel br=\""+br+"\" daughters=\""+daughters+"\" model=\""+model
          if params:
            toWrite += "\" params=\""+params
          if photos:
            toWrite += "\" photos=\"true"
          if summary:
            toWrite += "\" summary=\"true"
          if verbose:
            toWrite += "\" verbose=\"true"
          toWrite += "\"/>\n"
          fh2.write(toWrite)
        continue
    #are we currently parsing a removeDecay?
      if inRemoveDecay:
        if words[0] == "Enddecay":
          fh2.write("\t</removeDecay>\n")
          inRemoveDecay = False
          if len(words) > 1:
            line = " ".join(words[1:])
          else:
            getMore = True
        else:
          semicolonDetected = False
          daughtersList = []
  #precheck for a semicolon to save ourselves a bit of work
          for word in words:
            if word[-1] == ';':
              semicolonDetected = True
              break

          if not semicolonDetected:  #we're missing some of this line so wait til we have it all
            previousLine = line
            getMore = True
            continue

          for x in range(len(words)):
            if words[x][-1] == ';':
              daughtersList.append(words[x][:-1])
              if len(words) > x+1:
                print words[x+1:]
                line = " ".join(words[x+1:])
              else:
                getMore = True
              break
            else:
              daughtersList.append(words[x])
          daughters = " ".join(daughtersList)
          fh2.write("\t\t<channel daughters=\""+daughters+"\"/>\n");
        continue
    #otherwise lets figure out what this line does!
  #######DECAY##################
      if words[0] == "Decay":
        if len(words) < 2:
          previousLine = line
          getMore = True
          continue
        countDec += 1
        parent = words[1]
        fh2.write("\t<decay name=\""+parent+"\">\n")
        if len(words) > 2:
          line = " ".join(words[2:])
        else:
          getMore = True
        inDecay = True
  #######ALIAS##################
      elif words[0] == "Alias":
        if len(words) < 3:
          previousLine = line
          getMore = True
          continue
        countAlias += 1
        alias = words[1]
        particle = words[2]
        fh2.write("\t<alias name=\""+alias+"\" particle=\""+particle+"\"/>\n")
        if len(words) > 3:
          line = " ".join(words[3:])
        else:
          getMore = True
        allowedParticles.append(alias)
  #######MODELALIAS#############
      elif words[0] == "ModelAlias":
        semicolonDetected = False

    #precheck for a semicolon to save ourselves a bit of work
        if len(words) < 3:
          previousLine = line
          getMore = True
          continue
        for word in words[1:]:
          if word[-1] == ';':
            semicolonDetected = True
            break

        if not semicolonDetected:  #we're missing some of this line so wait til we have it all
          previousLine = line
          getMore = True
          continue

        countModelAlias += 1
        alias = words[1]
        paramsList = []
        if words[2][-1] == ';':
          model = words[2][:-1]
        else:
          model = words[2]
          for x in range(3,len(words)):
            if word[x][-1] == ';':
              paramsList.append(word[x][:-1])
              if len(words) > x+1:
                line = " ".join(word[x+1:])
              else:
                getMore = True
              break
            else:
              paramsList.append(word[x])
          params = " ".join(paramsList)
          fh2.write("\t<modelAlias name=\""+name+"\" model=\""+value+"\" params=\""+params+"\"/>\n")
  #######DEFINE#################
      elif words[0] == "Define":
        if len(words) < 3:
          previousLine = line
          getMore = True
          continue
        countDef += 1
        name = words[1]
        value = words[2]
        fh2.write("\t<define name=\""+name+"\" value=\""+value+"\"/>\n")
        if len(words) > 3:
          line = " ".join(words[3:])
        else:
          getMore = True
  #######CHARGECONJ#############
      elif words[0] == "ChargeConj":
        if len(words) < 3:
          previousLine = line
          getMore = True
          continue
        countConj += 1
        particle = words[1]
        conjugate = words[2]
        fh2.write("\t<chargeConj particle=\""+particle+"\" conjugate=\""+conjugate+"\"/>\n")
        if len(words) > 3:
          line = " ".join(words[3:])
        else:
          getMore = True
  #######CDECAY#################
      elif words[0] == "CDecay":
        if len(words) < 2:
          previousLine = line
          getMore = True
          continue
        countConjDecay += 1
        particle = words[1]
        fh2.write("\t<conjDecay particle=\""+particle+"\"/>\n")
        if len(words) > 2:
          line = " ".join(words[2:])
        else:
          getMore = True
  #######LINESHAPEPW############
      elif words[0] == "SetLineshapePW":
        if len(words) < 5:
          previousLine = line
          getMore = True
          continue
        countLineShapePW += 1
        parent = words[1]
        daug1 = words[2]
        daug2 = words[3]
        pw = words[4]
        fh2.write("\t<lineShapePW parent=\""+parent+"\" daug1=\""+daug1+"\" daug2=\""+daug2+"\" pw=\""+pw+"\"/>\n")
        if len(words) > 5:
          line = " ".join(words[5:])
        else:
          getMore = True
  #######PHOTOS#################
      elif words[0] == "yesPhotos":
        countPhotos += 1
        fh2.write("\t<photos usage=\"always\"/>\n")
        if len(words) > 1:
          line = " ".join(words[1:])
        else:
          getMore = True
      elif words[0] == "noPhotos":
        countPhotos += 1
        fh2.write("\t<photos usage=\"never\"/>\n")
        if len(words) > 1:
          line = " ".join(words[1:])
        else:
          getMore = True
      elif words[0] == "normalPhotos":
        countPhotos += 1
        fh2.write("\t<photos usage=\"normal\"/>\n")
        if len(words) > 1:
          line = " ".join(words[1:])
        else:
          getMore = True
  #######PARTICLE###############
      elif words[0] == "Particle":
        if len(words) < 4:
          previousLine = line
          getMore = True
          continue
        particle = words[1]
        mass = words[2]
        width = words[3]

        if particle in particleData:
          particleDatum = particleData[particle]
        else:
          particleDatum = {}
        particleDatum["mass"] = mass
        particleDatum["width"] = width
        particleData[particle] = particleDatum
        if len(words) > 4:
          line = " ".join(words[4:])
        else:
          getMore = True
  #######CHANGEMASSMIN##########
      elif words[0] == "ChangeMassMin":
        if len(words) < 3:
          previousLine = line
          getMore = True
          continue
        particle = words[1]
        massMin = words[2] 

        if particle in particleData:
          particleDatum = particleData[particle]
        else:
          particleDatum = {}
        particleDatum["massMin"] = massMin
        particleData[particle] = particleDatum
        if len(words) > 3:
          line = " ".join(words[3:])
        else:
          getMore = True
  #######CHANGEMASSMAX##########
      elif words[0] == "ChangeMassMax":
        if len(words) < 3:
          previousLine = line
          getMore = True
          continue
        particle = words[1]
        massMax = words[2]
      
        if particle in particleData:
          particleDatum = particleData[particle]
        else:
          particleDatum = {}
        particleDatum["massMax"] = massMax
        particleData[particle] = particleDatum
        if len(words) > 3:
          line = " ".join(words[3:])
        else:
          getMore = True
  #######BIRTHFACTOR############
      elif words[0] == "IncludeBirthFactor":
        if len(words) < 3:
          previousLine = line
          getMore = True
          continue
        particle = words[1]
        birthFactor = words[2]
      
        if particle in particleData:
          particleDatum = particleData[particle]
        else:
          particleDatum = {}
        particleDatum["birthFactor"] = birthFactor
        particleData[particle] = particleDatum
        if len(words) > 3:
          line = " ".join(words[3:])
        else:
          getMore = True
  #######DECAYFACTOR############
      elif words[0] == "IncludeDecayFactor":
        if len(words) < 3:
          previousLine = line
          getMore = True
          continue
        particle = words[1]
        decayFactor = words[2]
      
        if particle in particleData:
          particleDatum = particleData[particle]
        else:
          particleDatum = {}
        particleDatum["decayFactor"] = massMin
        particleData[particle] = particleDatum
        if len(words) > 3:
          line = " ".join(words[3:])
        else:
          getMore = True
  #######BLATTWEISSKOPF#########
      elif words[0] == "BlattWeisskopf":
        if len(words) < 3:
          previousLine = line
          getMore = True
          continue
        particle = words[1]
        decayFactor = words[2]

        if particle in particleData:
          particleDatum = particleData[particle]
        else:
          particleDatum = {}
        particleDatum["blattWeisskopf"] = massMin
        particleData[particle] = particleDatum
        if len(words) > 3:
          line = " ".join(words[3:])
        else:
          getMore = True
  #######LSNONRELBW#############
      elif words[0] == "LSNONRELBW":
        if len(words) < 2:
          previousLine = line
          getMore = True
          continue
        particle = words[1]

        if particle in particleData:
          particleDatum = particleData[particle]
        else:
          particleDatum = {}
        particleDatum["lineShape"] = "NONRELBW"
        particleData[particle] = particleDatum
        if len(words) > 2:
          line = " ".join(words[2:])
        else:
          getMore = True
  #######SP8LSFIX###############
      elif words[0] == "SP8LSFIX" or words[0] == "SP6LSFIX":
        if len(words) < 2:
          previousLine = line
          getMore = True
          continue
        particle = words[1]

        if particle in particleData:
          particleDatum = particleData[particle]
        else:
          particleDatum = {}
        particleDatum["fixLS"] = "yes"
        particleData[particle] = particleDatum
        if len(words) > 2:
          line = " ".join(words[2:])
        else:
          getMore = True
  #######LSFLAT#################
      elif words[0] == "LSFLAT":
        if len(words) < 2:
          previousLine = line
          getMore = True
          continue
        particle = words[1]

        if particle in particleData:
          particleDatum = particleData[particle]
        else:
          particleDatum = {}
        particleDatum["lineShape"] = "FLAT"
        particleData[particle] = particleDatum
        if len(words) > 2:
          line = " ".join(words[2:])
        else:
          getMore = True
  #######LSMANYDELTAFUNC########
      elif words[0] == "LSMANYDELTAFUNC":
        if len(words) < 2:
          previousLine = line
          getMore = True
          continue
        particle = words[1]

        if particle in particleData:
          particleDatum = particleData[particle]
        else:
          particleDatum = {}
        particleDatum["lineShape"] = "MANYDELTAFUNC"
        particleData[particle] = particleDatum
        if len(words) > 2:
          line = " ".join(words[2:])
        else:
          getMore = True
  #######COPYDECAY##############
      elif words[0] == "CopyDecay":
        if len(words) < 3:
          previousLine = line
          getMore = True
          continue
        countCopyDec += 1
        particle = words[1]
        copy = words[2]
        fh2.write("\t<copyDecay particle=\""+particle+"\" copy=\""+copy+"\"/>\n")
        if len(words) > 3:
          line = " ".join(words[3:])
        else:
          getMore = True
  #######REMOVEDECAY############
      elif words[0] == "RemoveDecay":
        if len(words) < 2:
          previousLine = line
          getMore = True
          continue
        countRemoveDec += 1
        parent = words[1]
        fh2.write("\t<removeDecay particle=\""+parent+"\">\n")
        if len(words) > 2:
          line = " ".join(words[2:])
        else:
          getMore = True
        inRemoveDecay = True
  #######PYTHIA6################
      elif words[0] == "JetSetPar":
        if len(words) < 2:
          previousLine = line
          getMore = True
          continue
        s1 = words[1].find("(")
        s2 = words[1].find(")")
        s3 = words[1].find("=")
        if s1 == -1 or s2 == -1 or s3 == -1:
          countBad += 1
          print "bad line: "+words[0]+" "+words[1]+" copied as comment, please fix manually!\n"
          fh2.write("\t<!--TODO "+words[0]+" "+words[1]+" -->\n")
        else:
          countPythia6 += 1
          fh2.write("\t<pythia6Param generator=\"BOTH\" module=\""+ words[1][:s1] +"\" param=\""+ words[1][s1+1:s2] +"\" value=\""+ words[1][s3+1:] +"\"/>\n")
        module = words[1].split("(")[0]
        if len(words) > 2:
          line = " ".join(words[2:])
        else:
          getMore = True
  #######END####################
      elif words[0] == "End":
        for particle in particleData.keys():
          countParticle += 1
          mass = particleData[particle].get("mass","")
          width = particleData[particle].get("width","")
          massMax = particleData[particle].get("massMax","")
          massMin = particleData[particle].get("massMin","")
          birthFactor = particleData[particle].get("birthFactor","")
          decayFactor = particleData[particle].get("decayFactor","")
          lineShape = particleData[particle].get("lineShape","")
          blattWeisskopf = particleData[particle].get("blattWeisskopf","")
          fixLS = particleData[particle].get("fixLS","")

          toWrite = "<particle name=\""+particle+"\""
          if mass:
            toWrite += " mass=\""+mass+"\""
          if width:
            toWrite += " width=\""+width+"\""
          if massMax:
            toWrite += " massMax=\""+massMax+"\""
          if massMin:
            toWrite += " massMin=\""+massMin+"\""
          if birthFactor:
            toWrite += " includeBirthFactor=\""+birthFactor+"\""
          if decayFactor:
            toWrite += " includeDecayFactor=\""+decayFactor+"\""
          if lineShape:
            toWrite += " lineShape=\""+lineShape+"\""
          if blattWeisskopf:
            toWrite += " blattWeisskopfFactor=\""+blattWeisskopf+"\""
          if fixLS:
            toWrite += " fixLS=\""+fixLS+"\""
          toWrite += "/>\n"
          fh2.write(toWrite)
        fh2.write("</data>")
        break
      else:
        countBad += 1
        print "bad line: "+line+"copied as comment, please fix manually!\n"
        fh2.write("<!--TODO "+line[:-1]+"-->\n")
        getMore = True
  if comments:
    print str(countComment)+" commented lines copied without modification"
  else:
    print str(countComment)+" commented lines ignored"
  print str(count)+" other lines converted including:"
  print str(countDec)+" decays"
  print str(countParticle)+" modified particles"
  print str(countAlias)+" aliases"
  print str(countModelAlias)+" model aliases"
  print str(countDef)+" definitions"
  print str(countConj)+" conjugates"
  print str(countConjDecay)+" conjugate decays"
  print str(countLineShapePW)+" line shape PWs"
  print str(countPhotos)+" PHOTOS lines"
  print str(countCopyDec)+" copied decays"
  print str(countRemoveDec)+" removed decays"
  print str(countPythia6)+" pythia commands"
  print str(countBad)+" bad lines!"

  fh1.close()
  fh2.close()

##################
args = sys.argv
extraFiles = []
if len(args) == 1:
  inFile = "DECAY.DEC"
  outFile = "DECAY.XML"
elif len(args) == 2:
  inFile = args[1]
  outFile = inFile.rsplit(".",1)[0]+".XML"
elif len(args) == 3:
  inFile = args[1]
  outFile = args[2]
else:
  inFile = args[1]
  outFile = args[2]
  extraFiles = args[3:]

main(inFile,outFile,extraFiles)
