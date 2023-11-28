class Atom:

    def __init__(self, atom_line_type, atom_pdb_number, atom_type_extended, residue_name, chain, residue_number, x_coordinate, y_coordinate, z_coordinate, atom_type):
        self.atom_line_type = atom_line_type
        self.atom_pdb_number = atom_pdb_number
        self.atom_type_extended = atom_type_extended
        self.residue_name = residue_name
        self.chain = chain
        self.residue_number = residue_number
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.z_coordinate = z_coordinate
        self.atom_type = atom_type

        self.Hybridisation = None
    
        self.AtomBonds = []
        self.BondPartners = []

    def	vdw_radius(self):
        if self.atom_type == 'C':
            return float(1.70)
        elif self.atom_type == 'O':
            return float(1.52)
        elif self.atom_type == 'N':
            return float(1.55)
        elif self.atom_type == 'H':
            return float(1.09)
        elif self.atom_type == 'S':
            return float(1.80)
        elif self.atom_type == 'P':
            return float(1.80)
        elif self.atom_type == 'F':
            return float(1.47)
        elif self.atom_type == 'Br':
            return float(1.85)
        elif self.atom_type == 'I':
            return float(1.98)
        elif self.atom_type == 'X':
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
       
        if self.atom_type in DonorAtoms:
            for PartnerinHB in self.BondPartners:
                
                if PartnerinHB.atom_type == 'N' or PartnerinHB.atom_type == 'O' or PartnerinHB.atom_type == 'S':
                    return True
                else:
                    return False 
        else:
            return False

    def IsAcceptor(self):
        AcceptorAtoms = ['O','N','S']
        
        if self.atom_type in AcceptorAtoms:
            if self.Hybridisation == 1 or self.Hybridisation == 2:
                return True
            else:
                return False

        else:
            return False

class Residue:
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
            atom_line_type = LineType
            atom_pdb_number = int(Line[6:11].replace(" ", ""))
            atom_type_extended = Line[12:16].replace(" ", "")
            residue_name = Line[17:20].replace(" ", "")
            chain = Line[21].replace(" ", "")
            residue_number = int(Line[22:31].replace(" ", ""))
            x_coordinate = float(Line[30:38].replace(" ", ""))
            y_coordinate = float(Line[38:46].replace(" ", ""))
            z_coordinate = float(Line[46:54].replace(" ", ""))
            atom_type = Line[76:78].replace(" ", "")

            AtomsList.append(Atom(atom_line_type, atom_pdb_number, atom_type_extended, residue_name, chain, residue_number, x_coordinate, y_coordinate, z_coordinate, atom_type))

    return AtomsList

def AtomsDistance(Atom1, Atom2):
    Distance = ((Atom1.x_coordinate - Atom2.x_coordinate)**2 + (Atom1.y_coordinate - Atom2.y_coordinate)**2 + (Atom1.z_coordinate - Atom2.z_coordinate)**2) ** (1./2.)

    return Distance

def Bonded(Atom1, Atom2):

    if (AtomsDistance(Atom1, Atom2) < (Atom1.vdw_radius() + Atom2.vdw_radius()) * 0.528):
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
        
        NumberOfPartners = len(Atom1Instancece.BondPartners)
        Atom1Instancece.SetHybridisation(NumberOfPartners)

def InvolvedInHB(Atom1, AtomList):

    Closest = None
    AtomNeighbours={}

    for Neighbour in AtomList:
        Distance = AtomsDistance(Atom1, Neighbour)
        AtomNeighbours[Neighbour] = Distance

    ClosestSorted = sorted(AtomNeighbours.items(), key=lambda x: x[1], reverse=False)

    for ClosestFound, Distance in ClosestSorted:

        if Atom1.residue_number != ClosestFound.residue_number:
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
    tmpResidueNumber = AtomList[0].residue_number
    for Atom1 in AtomList:
        tmpResidueList = []
        if tmpResidueNumber == Atom1.residue_number:
            tmpResidueList.append(Atom1)
        else:
            ResidueList.append(Residue(tmpResidueList))
            tmpResidueNumber = Atom1.residue_number

    return ResidueList

def AddWater(Atom1, AtomList):
    partner = Atom1.BondPartners[0]
    vector = [Atom1.x_coordinate - partner.x_coordinate, Atom1.y_coordinate - partner.y_coordinate, Atom1.z_coordinate - partner.z_coordinate]
    
    x_coordinate = Atom1.x_coordinate + 2 * vector[0]
    y_coordinate = Atom1.y_coordinate + 2 * vector[1]
    z_coordinate = Atom1.z_coordinate + 2 * vector[2]

    AtomList.append(Atom('HETATM', '1', 'X', 'X', 'X', 'X', x_coordinate, y_coordinate, z_coordinate, 'O'))
    AtomList.append(Atom('HETATM', '1', 'X', 'X', 'X', 'X', x_coordinate + (1/2**(1/2)), y_coordinate + (1/2**(1/2)), z_coordinate, 'H'))
    AtomList.append(Atom('HETATM', '1', 'X', 'X', 'X', 'X', x_coordinate - (1/2**(1/2)), y_coordinate + (1/2**(1/2)), z_coordinate, 'H'))

    return AtomList

def main(path, file):

    AtomList = ReadPbdFile(path + file)

    ResidueList = GenerateResidueList(AtomList)

    CreateConnectivityMatrix(AtomList)
    AssignHybridisation(AtomList)

    for Atom1Instancece in AtomList:
        if Atom1Instancece.IsDonor and not InvolvedInHB(Atom1Instancece,AtomList) and Atom1Instancece.residue_name == 'UNK':
            AtomList = AddWater(Atom1Instancece, AtomList)

    CreateConnectivityMatrix(AtomList)
    AssignHybridisation(AtomList)
            
    n = 0
    for AtomInstance1 in AtomList:
        if AtomInstance1.atom_type == 'X':
            if AtomInstance1.Hybridisation != 0:
                n = n +1
    print('Found', n, 'Unhappy HB donors')

    for AtomInstance1 in AtomList:
        file_object = open('HOH_' + file, 'a')
        header = 'HETATM'.rjust(6)
        atom_pdb_number = str(AtomInstance1.atom_pdb_number).rjust(5)
        atom_type_extended = str(AtomInstance1.atom_type_extended).rjust(4)
        residue_name = str(AtomInstance1.residue_name).rjust(3)
        chain = str(AtomInstance1.chain).rjust(1)
        residue_number = str(AtomInstance1.residue_number).rjust(4)
        x_coordinate = str(round(AtomInstance1.x_coordinate, 3)).rjust(8)
        y_coordinate = str(round(AtomInstance1.y_coordinate, 3)).rjust(8)
        z_coordinate = str(round(AtomInstance1.z_coordinate, 3)).rjust(8)
        atom_type = str(AtomInstance1.atom_type).rjust(2)
        Line = header + atom_pdb_number + ' ' + atom_type_extended + ' ' + residue_name + ' ' + chain + residue_number + '    ' + x_coordinate + y_coordinate + z_coordinate + '                     ' + atom_type + '\n'
        file_object.write(Line)

    file_object.close()

    return n
