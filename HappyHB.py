class Atom:

    def __init__(self, AtomLineType, AtomPdbNumber, AtomTypeExtended, ResidueName, Chain, ResidueNumber, Xcoordinate, Ycoordinate, Zcoordinate, AtomType):
        self.AtomLineType = AtomLineType
        self.AtomPdbNumber = AtomPdbNumber
        self.AtomTypeExtended = AtomTypeExtended
        self.ResidueName = ResidueName
        self.Chain = Chain
        self.ResidueNumber = ResidueNumber
        self.Xcoordinate = Xcoordinate
        self.Ycoordinate = Ycoordinate
        self.Zcoordinate = Zcoordinate
        self.AtomType = AtomType

        self.Hybridisation = None
    
        self.AtomBonds = []
        self.BondPartners = []

    def	VdWRadius(self):
        if self.AtomType == 'C':
            return float(1.70)
        elif self.AtomType == 'O':
            return float(1.52)
        elif self.AtomType == 'N':
            return float(1.55)
        elif self.AtomType == 'H':
            return float(1.09)
        elif self.AtomType == 'S':
            return float(1.80)
        elif self.AtomType == 'P':
            return float(1.80)
        elif self.AtomType == 'F':
            return float(1.47)
        elif self.AtomType == 'Br':
            return float(1.85)
        elif self.AtomType == 'I':
            return float(1.98)
        elif self.AtomType == 'X':
            return float(2.00)
        else:    #otherwise - if the above conditions don't satisfy(are not True)
            print("Atom's VdV radius not found")
            return False

    def AddBondPartner(self, Partner):
        self.BondPartners.append(Partner)

    def	SetHybridisation(self,Hybridisation):
        self.Hybridisation = Hybridisation

    def IsDonor(self):
        DonorAtoms = ['H']
       
        if self.AtomType in DonorAtoms:
            for PartnerinHB in self.BondPartners:
                
                if PartnerinHB.AtomType == 'N' or PartnerinHB.AtomType == 'O' or PartnerinHB.AtomType == 'S':
                    return True
                else:
                    return False 
        else:
            return False

    def IsAcceptor(self):
        AcceptorAtoms = ['O','N','S']
        
        if self.AtomType in AcceptorAtoms:
            if self.Hybridisation == 1 or self.Hybridisation == 2:
                return True
            else:
                return False

        else:
            return False

class Residue():
    AtomsInResidue =[]

    def __init__(self, AtomList):
        self.AtomsInResidue.append(AtomList)

def ReadPbdFile(PdbFile):
    AtomsList = []

    with open(PdbFile) as f:
        Lines = f.readlines()

    for Line in Lines:
        LineType = Line[0:6].replace(" ", "")

        if LineType == 'ATOM' or LineType == 'HETATM':
            AtomLineType = LineType
            AtomPdbNumber = int(Line[6:11].replace(" ", ""))
            AtomTypeExtended = Line[12:16].replace(" ", "")
            ResidueName = Line[17:20].replace(" ", "")
            Chain = Line[21].replace(" ", "")
            ResidueNumber = int(Line[22:31].replace(" ", ""))
            Xcoordinate = float(Line[30:38].replace(" ", ""))
            Ycoordinate = float(Line[38:46].replace(" ", ""))
            Zcoordinate = float(Line[46:54].replace(" ", ""))
            AtomType = Line[76:78].replace(" ", "")

            AtomsList.append(Atom(AtomLineType, AtomPdbNumber, AtomTypeExtended, ResidueName, Chain, ResidueNumber, Xcoordinate, Ycoordinate, Zcoordinate, AtomType))

    return AtomsList

def AtomsDistance(Atom1, Atom2):
    Distance = ((Atom1.Xcoordinate - Atom2.Xcoordinate)**2 + (Atom1.Ycoordinate - Atom2.Ycoordinate)**2 + (Atom1.Zcoordinate - Atom2.Zcoordinate)**2) ** (1./2.)

    return Distance

def Bonded(Atom1, Atom2):

    if (AtomsDistance(Atom1, Atom2) < (Atom1.VdWRadius() + Atom2.VdWRadius()) * 0.528):
        return True
    else:
        return False    

def CreateConnectivityMatrix(AtomList):
    i = 0
    for Atom1Instancece in AtomList:
        i = i + 1
        # print(i)
        for Atom2Instancece in AtomList[i:]:
            
            
            if Bonded(Atom1Instancece, Atom2Instancece) == True:
                Atom1Instancece.AddBondPartner(Atom2Instancece)
                Atom2Instancece.AddBondPartner(Atom1Instancece)

def AssignHybridisation(AtomList):

    for Atom1Instancece in AtomList:
        
        NumberOfPartners = len(Atom1Instancece.BondPartner())
        Atom1Instancece.SetHybridisation(NumberOfPartners)

def InvolvedInHB(Atom1, AtomList):

    Closest = None
    AtomNeighbours={}

    for Neighbour in AtomList:
        Distance = AtomsDistance(Atom1, Neighbour)
        AtomNeighbours[Neighbour] = Distance

    ClosestSorted = sorted(AtomNeighbours.items(), key=lambda x: x[1], reverse=False)

    for ClosestFound, Distance in ClosestSorted:

        if Atom1.ResidueNumber != ClosestFound.ResidueNumber:
            Closest = ClosestFound
            break

    if Closest == None:
        return False

    if Atom1.IsDonor():
        if Closest.IsAcceptor() and (AtomsDistance(Atom1, Closest) < float(3.00)):
            return True
        else:
            return False
    if Atom1.IsAcceptor():
        if Closest.IsDonor() and (AtomsDistance(Atom1, Closest) < float(3.00)):
            return True
        else:
            return False
    else:
        return False

def GenerateResidueList(AtomList):
    ResidueList = []
    tmpResidueNumber = AtomList[0].ResidueNumber
    for Atom1 in AtomList:
        tmpResidueList = []
        if tmpResidueNumber == Atom1.ResidueNumber:
            tmpResidueList.append(Atom1)
        else:
            ResidueList.append(Residue(tmpResidueList))
            tmpResidueNumber = Atom1.ResidueNumber

    return ResidueList

def AddWater(Atom1, AtomList):
    partner = Atom1.BondPartner()[0]
    vector = [Atom1.Xcoordinate() - partner.Xcoordinate(), Atom1.Ycoordinate() - partner.Ycoordinate(), Atom1.Zcoordinate() - partner.Zcoordinate()]
    
    Xcoordinate = Atom1.Xcoordinate() + 2 * vector[0]
    Ycoordinate = Atom1.Ycoordinate() + 2 * vector[1]
    Zcoordinate = Atom1.Zcoordinate() + 2 * vector[2]

    AtomList.append(Atom('HETATM', '1', 'X', 'X', 'X', 'X', Xcoordinate, Ycoordinate, Zcoordinate, 'O'))
    AtomList.append(Atom('HETATM', '1', 'X', 'X', 'X', 'X', Xcoordinate + (1/2**(1/2)), Ycoordinate + (1/2**(1/2)), Zcoordinate, 'H'))
    AtomList.append(Atom('HETATM', '1', 'X', 'X', 'X', 'X', Xcoordinate - (1/2**(1/2)), Ycoordinate + (1/2**(1/2)), Zcoordinate, 'H'))

    return AtomList

def main(path, file):

    AtomList = ReadPbdFile(path + file)

    ResidueList = GenerateResidueList(AtomList)

    CreateConnectivityMatrix(AtomList)
    AssignHybridisation(AtomList)

    for Atom1Instancece in AtomList:
        if Atom1Instancece.IsDonor() and not InvolvedInHB(Atom1Instancece,AtomList) and Atom1Instancece.ResidueName() == 'UNK':
            AtomList = AddWater(Atom1Instancece, AtomList)

    CreateConnectivityMatrix(AtomList)
    AssignHybridisation(AtomList)
            
    n = 0
    for AtomInstance1 in AtomList:
        if AtomInstance1.AtomType() == 'X':
            if AtomInstance1.Hybridisation() != 0:
                n = n +1
    print('Found', n, 'Unhappy HB donors')

    for AtomInstance1 in AtomList:
        file_object = open('HOH_' + file, 'a')
        header = 'HETATM'.rjust(6)
        AtomPdbNumber = str(AtomInstance1.AtomPdbNumber).rjust(5)
        AtomTypeExtended = str(AtomInstance1.AtomTypeExtended).rjust(4)
        ResidueName = str(AtomInstance1.ResidueName).rjust(3)
        Chain = str(AtomInstance1.Chain).rjust(1)
        ResidueNumber = str(AtomInstance1.ResidueNumber).rjust(4)
        Xcoordinate = str(round(AtomInstance1.Xcoordinate, 3)).rjust(8)
        Ycoordinate = str(round(AtomInstance1.Ycoordinate, 3)).rjust(8)
        Zcoordinate = str(round(AtomInstance1.Zcoordinate, 3)).rjust(8)
        AtomType = str(AtomInstance1.AtomType).rjust(2)
        Line = header + AtomPdbNumber + ' ' + AtomTypeExtended + ' ' + ResidueName + ' ' + Chain + ResidueNumber + '    ' + Xcoordinate + Ycoordinate + Zcoordinate + '                     ' + AtomType + '\n'
        file_object.write(Line)

    file_object.close()

    return n
