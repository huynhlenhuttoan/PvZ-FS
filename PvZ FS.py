import random, json, time, os

#Amino Acids Data
AminoAcids = {
    "Phe": {"name": "Phenylalanine", "code": "A", "components": ['UUU','UUC']},
    "Leu": {"name": "Leucine", "code": "B", "components": ['UUA','UUG','CUU','CUC','CUA','CUG']},
    "Ile": {"name": "Isoleucine", "code": "C", "components": ['AUU','AUC','AUA']},
    "Met": {"name": "Methionine", "code": "D", "components": ['AUG']},
    "Val": {"name": "Valine", "code": "E", "components": ['GUU','GUC','GUA','GUG']},
    "Ser": {"name": "Serine", "code": "F", "components": ['UCU','UCC','UCA','UCG','AGU','AGC']},
    "Pro": {"name": "Proline", "code": "G", "components": ['CCU','CCC','CCA','CCG']},
    "Thr": {"name": "Threonine", "code": "H", "components": ['ACU','ACC','ACA','ACG']},
    "Ala": {"name": "Alanine", "code": "I", "components": ['GCU','GCC','GCA','GCG']},
    "Tyr": {"name": "Tyrosine", "code": "J", "components": ['UAU','UAC']},
    "His": {"name": "Histidine", "code": "K", "components": ['CAU','CAC']},
    "Gln": {"name": "Glutamine", "code": "L", "components": ['CAA','CAG']},
    "Asn": {"name": "Asparagine", "code": "M", "components": ['AAU','AAC']},
    "Lys": {"name": "Lysine", "code": "N", "components": ['AAA','AAG']},
    "Asp": {"name": "Aspartic acid", "code": "O", "components": ['GAU','GAC']},
    "Glu": {"name": "Glutamic acid", "code": "P", "components": ['GAA','GAG']},
    "Cys": {"name": "Cysteine", "code": "Q", "components": ['UGU','UGC']},
    "Trp": {"name": "Tryptophan", "code": "R", "components": ['UGG']},
    "Arg": {"name": "Arginine", "code": "S", "components": ['CGU','CGC','CGA','CGG','AGA','AGG']},
    "Gly": {"name": "Glycine", "code": "T", "components": ['GGU','GGC','GGA','GGG']},
    "END": {"components": ['UAA','UAG','UGA']}
}

#Plants Data: [1]: Amino Acids Code, [2]: Male:Famale ratio
Plants = {
    "Peashooter": (["DB"], [60,40]),
    "Sunflower": (["DS"], [40,60]),
    "Wall-nut": (["DF"], [50,50]),
    "Pea Sunflower": (["DBS","DSB"], [50,50]), #Peashooter x Sunflower
    "Solar-nut": (["DSF","DFS"], [30,70]), #Sunflower x Wall-nut
    "Pea-nut": (["DGF","DBF"],[70,30])  #Peashooter x Wall-nut
}

#DNA to RNA
def DNA_to_RNA(DNA):
    return DNA.replace('T','U')

#RNA to DNA
def RNA_to_DNA(RNA):
    return RNA.replace('U','T')

#Separate RNA into codons
def RNA_to_Condons(RNA):
    codons = [RNA[i:i+3] for i in range(0,len(RNA),3)]
    #codons = [codon for codon in codons if len(codon) == 3]
    return codons

#Translate codons to Amino Acids code
def Codons_to_AA_code(codons):
    ProteinCode = ""

    for codon in codons:
        found = False
        for key, value in AminoAcids.items():
            if codon in value.get("components",[]):
                ProteinCode += value["code"]
                found = True
                break

            if not found and codon in AminoAcids["END"]["components"]:
                break

    return ProteinCode

#Translate codons to Amino Acids names
def Codons_to_AA_name(codons):
    protein_names = []

    for codon in codons:
        found = False

        if not found and codon in AminoAcids["END"]["components"]:
            break # Stop translation if a stop codon is encountered

        for key, value in AminoAcids.items():
            if codon in value.get("components", []):
                protein_names.append(key) #Get short Amino Acids names
                found = True
                break
    
    return "-".join(protein_names)

#Determine plant type base on DNA
def get_plant_type(DNA):
    RNA = DNA_to_RNA(DNA)
    codons = RNA_to_Condons(RNA)
    protein_code = Codons_to_AA_code(codons)
    for plant, values in Plants.items():
        if protein_code in values[0]:
            return plant

    return "Unknown" #After checking all plants

#Get possible DNA strings (for randomizing new game starter)
def get_possible_DNA_strings(plant_name):
    if plant_name not in Plants:
        return []

    AA_codes = Plants[plant_name][0]
    possible_DNA_strings = []

    for AA_code in AA_codes:
        possible_DNA = [""]
        for code in AA_code:
            new_possible_DNA = []
            for key, value in AminoAcids.items():
                if "code" not in value:
                    continue
                if value["code"] == code:
                    for codon in value["components"]:
                        RNA_codon = RNA_to_DNA(codon)
                        for DNA in possible_DNA:
                            new_possible_DNA.append(DNA + RNA_codon)
            possible_DNA = new_possible_DNA

        possible_DNA_strings.extend(possible_DNA)

    return possible_DNA_strings

#Translate and choose random stop codons
def get_random_stop_codon():
    stop_codons = AminoAcids["END"]["components"]
    return RNA_to_DNA(random.choice(stop_codons))

#Random plant's gender
def get_random_gender(plant_name):
    if plant_name not in Plants:
        return "Unknown"
    male_ratio, female_ratio = Plants[plant_name][1]
    return "Male" if random.randint(1,100) <= male_ratio else "Female"


#Breeding
def breed(plant1, plant2):
    RNA_1 = DNA_to_RNA(plant1["DNA"])
    RNA_2 = DNA_to_RNA(plant2["DNA"])
    codons_1 =  RNA_to_Condons(RNA_1)
    codons_2 = RNA_to_Condons(RNA_2)
    print(codons_1)
    print(codons_2)

    child_codons = []

    if len(codons_1) == len(codons_2): #Parents' RNA length is equal
        for i in range(len(codons_1)):
            child_codons.append(random.choice([codons_1[i],codons_2[i]])) #Random choice codons orderly

    else: #Parents' RNA length is not equal
        shorter, longer = (codons_1,codons_2) if len(codons_1) < len(codons_2) else (codons_2, codons_1)
        child_length = random.choice([len(codons_1),len(codons_2)]) #Random choice child's RNA length among parents' RNA lengths
        for i in range(child_length):
            if i < len(shorter):
                child_codons.append(random.choice([codons_1[i],codons_2[i]])) #Random choice codons orderly
            else:
                child_codons.append(longer[i]) #Take longer's residuals

        if child_length == len(shorter) and not any(codon in AminoAcids["END"]["components"] for codon in child_codons):
            return #Stop the breed, do not update data

    child_RNA = ''.join(child_codons)
    child_DNA = RNA_to_DNA(child_RNA) 

    return {
        "DNA": child_DNA,
        "Protein": Codons_to_AA_name(RNA_to_Condons(DNA_to_RNA(child_DNA))),
        "type": get_plant_type(child_DNA),
        "gender": get_random_gender(get_plant_type(child_DNA))
    }

#Load json file
def load_userdata(userdata_path):
    if not os.path.exists(userdata_path):
        print("No save files found, starting new game..")
        return create_new_userdata(userdata_path)
    
    try:
        with open(userdata_path,'r') as user_file:
            userdata = json.load(user_file)
            return {int(k) if k.isdigit() else k: v for k, v in userdata.items()}
    
    except (json.JSONDecodeError, ValueError):
        print("Save file is corrupted, do you want to start a new game?")
        return create_new_userdata(userdata_path)

#Create new userdata   
def create_new_userdata(userdata_path): #Give 3 starter plants
    Peashooter_DNA = get_possible_DNA_strings("Peashooter")
    Sunflower_DNA = get_possible_DNA_strings("Sunflower")
    Wallnut_DNA = get_possible_DNA_strings("Wall-nut")
    random_Peashooter_DNA = random.choice(Peashooter_DNA) + get_random_stop_codon()
    random_Sunflower_DNA = random.choice(Sunflower_DNA) + get_random_stop_codon()
    random_Wallnut_DNA = random.choice(Wallnut_DNA) + get_random_stop_codon()

    # Make sure the gender of Peashooter and Sunflower is opposite
    peashooter_gender = get_random_gender("Peashooter")
    sunflower_gender = "Female" if peashooter_gender == "Male" else "Male"

    starting_data = {
            "order_number": 4, #Already gave 3 starter plants, so the next plant will have the order number of 4

            1: {  # Peashooter
                "DNA": random_Peashooter_DNA,
                "Protein": Codons_to_AA_name(RNA_to_Condons(DNA_to_RNA(random_Peashooter_DNA))),
                "type": get_plant_type(random_Peashooter_DNA),
                "gender": peashooter_gender
            },
            2: {  # Sunflower
                "DNA": random_Sunflower_DNA,
                "Protein": Codons_to_AA_name(RNA_to_Condons(DNA_to_RNA(random_Sunflower_DNA))),
                "type": get_plant_type(random_Sunflower_DNA),
                "gender": sunflower_gender
            },
            3: {  # Wall-nut
                "DNA": random_Wallnut_DNA,
                "Protein": Codons_to_AA_name(RNA_to_Condons(DNA_to_RNA(random_Wallnut_DNA))),
                "type": get_plant_type(random_Wallnut_DNA),
                "gender": get_random_gender("Wall-nut")
            }
        }
    
    with open(userdata_path,'w') as userdata: #Import 3 starter plants
        json.dump(starting_data,userdata,indent=4)

    return starting_data

#Main game loop
userdata = 'userdata.json'
player_data = load_userdata(userdata)

while True:
    print("\n---PVZ Fusion Simluator---")

    #Show current plants
    print("Your plants:")
    for order, plant in player_data.items():
        if isinstance(order, int):
            print(f"{order}. {plant['type']} ({plant['gender']} - DNA: {plant['DNA']})")

    #Select breeders
    try:
        plant_1_id = int(input("Enter the order number of the first plant: "))
        plant_2_id = int(input("Enter the order number of the second plant: "))

        if plant_1_id not in player_data or plant_2_id not in player_data:
            print("Invalid plant order number.")
            continue

        plant_1 = player_data[plant_1_id]
        plant_2 = player_data[plant_2_id]

        if plant_1["gender"] == plant_2["gender"]:
            print("Both plants must have different genders!")
            continue

        #Start breeding
        child_plant = breed(plant_1, plant_2)
        if not child_plant:
            print("Breeding failed..")
            continue

        print("\nBreeding Successful!")
        print(f"Child Plant Type: {child_plant['type']}")
        print(f"Child Plant DNA: {child_plant['DNA']}")
        print(f"Child Plant Gender: {child_plant['gender']}")

        #Add to userdata
        order_number = player_data["order_number"]
        player_data[order_number] = child_plant
        player_data["order_number"] += 1

        #Save new userdata
        with open(userdata,'w') as user_file:
            json.dump(player_data,user_file,indent=4)

    except ValueError:
        print("Invalid input. Please enter numbers!")

    except KeyboardInterrupt:
        print("\nExiting game...")
        break
