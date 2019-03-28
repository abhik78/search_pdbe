
#! /usr/bin/env python

from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import Draw



import csv
import sys


compound_smiles_list = []
compound_het_list = []
template_smiles_list = []
template_name_list = []
final_list = set()
compound_dict = {}
with open(sys.argv[1]) as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        compound_smiles_list.append(row['smiles'])
        compound_het_list.append(row['hetcode'])
        compound_dict[row['hetcode']] = row['smiles']
        #print(compound_smiles_list)

with open(sys.argv[2]) as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        template_smiles_list.append(row['smiles1'])
        template_name_list.append(row['hetcode1'])

for template_smiles, template_name in zip(template_smiles_list, template_name_list):
    patt = Chem.MolFromSmarts('%s' % template_smiles)

    for compound_smiles, compound_hetcode in zip(compound_smiles_list, compound_het_list):
        try:
            m = Chem.MolFromSmiles('%s' % compound_smiles)
            result = m.HasSubstructMatch(patt, useChirality = True)
            print(compound_hetcode, result, template_name)
            if result == True:
                final_list.add(compound_hetcode)

            else:
                None
        except:
            pass
smiles_list_image = []
print(final_list)
#print(compound_dict)

for item in final_list:
    for het2, smiles3 in compound_dict.items():
        if het2 == item:
            smiles_list_image.append(smiles3)
            #print(smiles_list_image)
htmlfile = open("interesting_sugar.html", "w")
htmlfile.write("<html>\n")
htmlfile.write("<body>\n")
htmlfile.write("<figure>\n")

for smiles4, item, template_smiles in zip(smiles_list_image, final_list, template_smiles_list):
    mol_for_image = Chem.MolFromSmiles('%s' % smiles4)
    #print(mol_for_image.GetNumAtoms(), item)
    Draw.MolToFile(mol_for_image,'/homes/abhik/work2/find_similar_sugar/images_test/{}.png'.format(item))
    str='<img src ="/homes/abhik/work2/find_similar_sugar/images_test/{0}.png" alt ="sugar">\n'.format(item)
    print(item)

    htmlfile.write(str)
    htmlfile.write("<figcaption>\n")
    #'{}.o.png'.format(item)
    htmlfile.write('{}'.format(item))
    htmlfile.write("</figcaption>\n")
htmlfile.write("</figure>\n")

htmlfile.write("</body>\n")

htmlfile.write("</html>\n")
htmlfile.close()


