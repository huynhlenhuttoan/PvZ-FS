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

#Plants Data: [0]: Amino Acids Code, [1]: Male:Famale ratio, [2]: Plant Rating (PR)
Plants = {
    "Peashooter": (["DB"], [60,40], 1),
    "Sunflower": (["DS"], [40,60], 1),
    "Wall-nut": (["DF"], [50,50], 1),
    "Pea Sunflower": (["DBS","DSB"], [50,50], 2), #Peashooter x Sunflower
    "Solar-nut": (["DSF","DFS"], [30,70], 2), #Sunflower x Wall-nut
    "Pea-nut": (["DGF","DBF"],[70,30], 2)  #Peashooter x Wall-nut
}

#DNA to RNA
def DNA_to_RNA(DNA):
    return DNA.replace('T','U')

#RNA to DNA
def RNA_to_DNA(RNA):
    return RNA.replace('U','T')

#Separate RNA into codons
def RNA_to_Condons(RNA):
    codons = [RNA[i:i+3] for i in range(0, len(RNA) - len(RNA) % 3, 3)]
    return codons

#Translate codons to Amino Acids code
def Codons_to_AA_code(codons):
    print("DB:", codons)
    Protein_Codes = []
    start_pos = [i for i, codon in enumerate(codons) if codon == "AUG"]
    stop_pos = [i for i, codon in enumerate(codons) if codon in AminoAcids["END"]["components"]]

    if not start_pos or not stop_pos or all(stop < start for stop in stop_pos for start in start_pos):
        return []  # No valid coding region


    for start in start_pos:
        nearest_stop = next((stop for stop in stop_pos if stop > start), None) #Find nearest stop after this start codon

        if nearest_stop and nearest_stop > start + 1: #Exist valid stop codon(s)
            protein_code = ""
            #Collect the codons between chosen start and stop codons
            for i in range(start, nearest_stop):
                codon = codons[i]
                for key, value in AminoAcids.items():
                    if "code" in value and codon in value.get("components",[]):
                        protein_code += value["code"]

            Protein_Codes.append(protein_code)
            stop_pos = [stop for stop in stop_pos if stop > nearest_stop] #Update stop codons
        
        else: #No valid stop codon found after this start codon, skip this start codon
            continue

    return Protein_Codes

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
    protein_codes = Codons_to_AA_code(codons)

    highest_PR = -1
    best_plant_type = []

    for protein_code in protein_codes:
        for plant, values in Plants.items():
            if protein_code in values[0]: #If Protein code is valid
                plant_PR = values[2] #Get plant's PR
                if plant_PR > highest_PR:
                    highest_PR = plant_PR #Update new highest PR
                    best_plant_type = [plant] #Reset best plant type list if new higher PR was found
                elif plant_PR == highest_PR:
                    best_plant_type.append(plant)

    if best_plant_type:
        return random.choice(best_plant_type)

    return None #After checking all plants

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

    if should_mutate(max(plant_1["IR"], plant_2["IR"]), userdata["pity"]):
        mutated_DNA = mutate_DNA(child_DNA)
        if mutated_DNA:
            child_DNA = mutated_DNA
            print("Mutation happened!")
            userdata["pity"] = 0 #Pity became 0 if mutation happened
        else:
            print("Breeding failed due to corrupted mutation..")
            userdata["pity"] += 1 #Increase pity if mutation failed
            return None

    return {
        "DNA": child_DNA,
        "Protein": Codons_to_AA_name(RNA_to_Condons(DNA_to_RNA(child_DNA))),
        "type": get_plant_type(child_DNA),
        "gender": get_random_gender(get_plant_type(child_DNA)),
        "PR": Plants[get_plant_type(child_DNA)][2],
        "IR": Plants[get_plant_type(child_DNA)][2], #For now, PR = IR
    }

#Check if mutation happens
def should_mutate(IR, pity):
    if random.randint(1, 100) <= IR + pity:
        return True #Mutation happens
    return False #No mutation

def mutate_DNA(DNA):
    mutation_type = random.choice(["Point", "Substitution", "Inversion", "Insertion", "Deletion"])
    DNA_list = list(DNA)
    length = len(DNA_list)

    if mutation_type == "Point": #Change a nucleotide into another one
        how_many = random.randint(1, max(1, length // 3))
        step = 1
        temp = []
        while step <= how_many:
            index = random.randint(0, length - 1)
            if index not in temp:
                DNA_list[index] = random.choice(["A","T","C","G"])
                temp.append(index)
                step += 1

    elif mutation_type == "Substitution": #Change a nucleotide section into another one, with the same length
        start = random.randint(0, length - 2)
        end = random.randint(start + 1, length)
        for i in range(start, end):
            DNA_list[i] = random.choice(["A","T","C","G"])

    elif mutation_type == "Inversion": #Reverse a nucleotide section
        start = random.randint(0, length - 2)
        end = random.randint(start + 1, length)
        DNA_list[start:end] = reversed(DNA_list[start:end])

    elif mutation_type == "Insertion": #Insert nucleotide(s) or a nucleotide section
        how_many = random.randint(1, max(1,length // 3))
        insert_type = random.choice(["Group", "Individual"])
        if insert_type == "Group":
            index = random.randint(0, length)
            insertion = random.choices(["A","T","C","G"],k=random.randint(1, how_many))
            DNA_list = DNA_list[:index] + insertion + DNA_list[index:]

        if insert_type == "Individual":
            step = 1
            while step <= how_many:
                index = random.randint(0, length)
                base = random.choice(["A","T","C","G"])
                DNA_list = DNA_list[:index] + base + DNA_list[index:]
                step += 1

        elif mutation_type == "Deletion": #Delete nucleotide(s) or a nucleotide section
            delete_type = random.choice("Group", "Individual")
            if delete_type == "Group":
                start = random.randint(0, length - 2)
                end = random.randint(start + 1, length)
                del DNA_list[start:end]

            if delete_type == "Individual":
                how_many = random.randint(1, max(1, length // 3))
                step = 1
                while step <= how_many:
                    if length == 0:
                        break
                    index = random.randint(0, length - 1)
                    del DNA_list[index]
                    step += 1

    mutated_DNA = ''.join(DNA_list)
    
    #Validate the mutated DNA
    if not is_valid_DNA(mutated_DNA):
        return None #Mutation Failed
    
    print(mutated_DNA)
    return mutated_DNA

def is_valid_DNA(DNA):
    RNA = DNA_to_RNA(DNA)
    codons = RNA_to_Condons(RNA)

    # Ensure there is a start codon
    if "AUG" not in codons:
        return False

    try: # Ensure there is a stop codon
        start_index = codons.index("AUG")
    except ValueError:
        return False  # No start codon found
    
    for i in range(start_index + 1, len(codons)):
        if codons[i] in AminoAcids["END"]["components"]:
            if i - start_index > 1: # Ensure at least one codon between start and stop
                is_a_plant = get_plant_type(DNA)
                if is_a_plant:
                    return True
                else:
                    return False
            break

    return False  # No valid protein-coding region found

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
        choice = input("Save file is corrupted, do you want to start a new game?\nY: Yes; N: No\n").strip().upper()
        print(f"User input after strip and lower: '{choice}'")
        if choice == "Y":
            return create_new_userdata(userdata_path)
        
        else:
            raise SystemExit("Exiting due to corrupted save file.")

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
            "pity": 0, #Mutation Pity

            1: {  # Peashooter
                "DNA": random_Peashooter_DNA,
                "Protein": Codons_to_AA_name(RNA_to_Condons(DNA_to_RNA(random_Peashooter_DNA))),
                "type": get_plant_type(random_Peashooter_DNA),
                "gender": peashooter_gender,
                "PR": 1,
                "IR": 1
            },
            2: {  # Sunflower
                "DNA": random_Sunflower_DNA,
                "Protein": Codons_to_AA_name(RNA_to_Condons(DNA_to_RNA(random_Sunflower_DNA))),
                "type": get_plant_type(random_Sunflower_DNA),
                "gender": sunflower_gender,
                "PR": 1,
                "IR": 1
            },
            3: {  # Wall-nut
                "DNA": random_Wallnut_DNA,
                "Protein": Codons_to_AA_name(RNA_to_Condons(DNA_to_RNA(random_Wallnut_DNA))),
                "type": get_plant_type(random_Wallnut_DNA),
                "gender": get_random_gender("Wall-nut"),
                "PR": 1,
                "IR": 1
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
        print("Invalid input. Please enter valid order numbers!")

    except KeyboardInterrupt:
        print("\nExiting game...")
        break
