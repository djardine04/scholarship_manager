from Scholarship_Recorder import Scholarship, Academic, Federal_Grant, Need_Based, Athletic, Minority, Creative_Arts, Community_Service, Scholarship_Manager


def get_optional_string(prompt: str) -> str:
    value = input(prompt)
    return value if value != "" else None

def get_required_string(prompt: str, field_name: str) -> str:
    while True:
        value = input(prompt)
        if value != "":
            return value.strip()
        else:
            print(f"The {field_name} is required.")

def get_optional_float(prompt: str, min_value: float = None, max_value: float = None) -> float:
    while True:
        value = input(prompt)
        if value == "":
            return None
        try:
            float_value = float(value)
            if (min_value is not None and float_value < min_value) or (max_value is not None and float_value > max_value):
                print(f"Please enter a value between {min_value} and {max_value}.")
                continue
            else:
                return float_value
        except ValueError:
            print("Please enter a valid number.")

def get_required_float(prompt: str, field_name: str, min_value: float = 0, max_value: float = None) -> float:
    while True:
        value = input(prompt)
        if value != "":
            try:
                float_value = float(value)             
                if (min_value is not None and float_value < min_value) or (max_value is not None and float_value > max_value):
                    print(f"Please enter a value between {min_value} and {max_value}.")
                    continue
                else:
                    return float_value
            except ValueError:
                print(f"The {field_name} is required and must be a valid number.")
        else:
            print(f"The {field_name} is required.")

def get_optional_int(prompt: str, min_value: int = 0, max_value: int = None) -> int:
    while True:
        value = input(prompt)
        if value == "":
            return None
        try:
            int_value = int(value)
            if (min_value is not None and int_value < min_value) or (max_value is not None and int_value > max_value):
                print(f"Please enter a value between {min_value} and {max_value}.")
                continue
            else:
                return int_value
        except ValueError:
            print("Please enter a valid integer.")

def get_required_int(prompt: str, field_name: str, min_value: int = 0, max_value: int = None) -> int:
    while True:
        value = input(prompt)
        if value != "":
            try:
                int_value = int(value)
                if (min_value is not None and int_value < min_value) or (max_value is not None and int_value > max_value):
                    print(f"Please enter a value between {min_value} and {max_value}.")
                    continue
                else:
                    return int_value
            except ValueError:
                print(f"The {field_name} is required and must be a valid integer.")
        else:
            print(f"The {field_name} is required.")

def get_yes_no_required(prompt: str) -> bool:
    while True:
        value = input(prompt).strip().lower()
        if value != "":
            if value in ['y', 'yes']:
                return True
            elif value in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")
                continue
        else:
            print("This field is required.")

def get_yes_no_optional(prompt: str) -> bool:
    while True:
        value = input(prompt).strip().lower()
        if value == "":
            return None
        if value in ['y', 'yes']:
            return True
        elif value in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes, 'n' for no, or press Enter to skip.")

def get_date_required(prompt: str, field_name: str) -> str:
    while True:
        value = input(prompt)
        if value != "":
            if Scholarship.validate_date_format(value):
                return value
            else:
                print("Invalid date format. Please use YYYY-MM-DD (e.g., 2025-12-31).")
                continue
        else:
            print(f"The {field_name} is required.")

def get_date_optional(prompt: str) -> str:
    while True:
        value = input(prompt)
        if value == "":
            return None
        if Scholarship.validate_date_format(value):
            return value
        else:
            print("Invalid date format. Please use YYYY-MM-DD (e.g., 2025-12-31).")

class ScholarshipPrompt:

    @staticmethod
    def prompt_scholarship():
        print("\nPlease enter the following scholarship information (If non-required information is unknown or not applicable, press Enter):\n\n")
        args = {} #create empty dictionary to hold arguments allowing for default values if user skips input

        args['name'] = get_required_string("Enter the name of the scholarship: ", "scholarship name")
        args['pay_amount'] = get_required_float("Enter the pay amount: ", "pay amount", min_value=0)
        deadline = get_date_optional("Enter the application deadline (YYYY-MM-DD): ")
        if deadline is not None:
            args['deadline'] = deadline
        essay_count = get_optional_int("Enter the number of essays required: ", min_value=0)
        if essay_count is not None:
            args['essay_count'] = essay_count
        args['organization'] = get_required_string("Enter the organization offering the scholarship: ", "organization")
        while True:
            additional_materials = get_optional_string("Enter short description of any additional required materials (if none then press Enter): ")
            if additional_materials is None:
                break
            elif additional_materials is not None:
                other_addtional_materials = get_optional_string("Are there any other additional required materials? (if none then press Enter): ")
                additional_materials = additional_materials + "," + other_addtional_materials if other_addtional_materials is not None else additional_materials    
                args['additional_required_materials'] = [material.strip() for material in additional_materials.split(',')]
                break
        args['URL'] = get_required_string("Enter the URL for the scholarship application page: ", "URL")

        return args
    @staticmethod
    def user_prompt_other_scholarship():
        args = ScholarshipPrompt.prompt_scholarship()
        scholarship_type = get_optional_string("Enter the type of scholarship (if unsure then press Enter): ")
        if scholarship_type is not None:
            args['scholarship_type'] = scholarship_type

        return Scholarship(**args)

    
    @staticmethod
    def user_prompt_academic():
        args = ScholarshipPrompt.prompt_scholarship()
        gpa = get_optional_float("Enter the minimum GPA requirement (if none then press Enter): ", min_value=0.0, max_value=5.0)
        if gpa is not None:
            args['GPA_requirement'] = gpa
        transcript_required = get_yes_no_optional("Is a transcript required? (y/n, press Enter if unsure): ")
        if transcript_required is not None:
            args['transcript_required'] = transcript_required
        letters_of_recommendation = get_optional_int("Enter the number of letters of recommendation required (if none then press Enter): ", min_value=0)
        if letters_of_recommendation is not None:
            args['letters_of_recommendation'] = letters_of_recommendation
        standardized_test_required = get_yes_no_optional("Is standardized test scores required? (y/n, press Enter if unsure): ")
        if standardized_test_required is not None:
            args['standardized_testing_required'] = standardized_test_required

        return Academic(**args)
    
    @staticmethod
    def user_prompt_federal():
        args = ScholarshipPrompt.prompt_scholarship()
        fafsa_required = get_yes_no_required("Is FAFSA required? (y/n): ")
        args['FAFSA_required'] = fafsa_required
        enrollment = get_optional_string("Enter the required enrollment status (e.g., full-time, part-time) (if unsure then press Enter): ")
        if enrollment is not None:
            args['enrollment_status'] = enrollment
        args["income_threshold"] = get_required_float("Enter your yearly income. If you are under the age of 24, not married, or have no dependants of your own, enter your parents' income. (e.g., 50000)", "income threshold", min_value=0.0)

        return Federal_Grant(**args)

    @staticmethod
    def user_prompt_need_based():
        args = ScholarshipPrompt.prompt_scholarship()
        fafsa_required = get_yes_no_required("Is FAFSA required? (y/n): ")
        args['FAFSA_required'] = fafsa_required
        enrollment = get_optional_string("Enter the required enrollment status (e.g., full-time, part-time) (if unsure then press Enter): ")
        if enrollment is not None:
            args['enrollment_status'] = enrollment

        return Need_Based(**args)

    @staticmethod
    def user_prompt_athletic():
        args = ScholarshipPrompt.prompt_scholarship()
        args['sport'] = get_required_string("Enter the sport associated with the scholarship: ", "sport")
        args['competition_level'] = get_required_string("Enter the competition level (e.g., Division I, Division II, etc.): ", "competition level")
        coach_recommendation = get_yes_no_required("Is a coach recommendation required? (y/n): ")
        args['coach_recommendation'] = coach_recommendation
        if coach_recommendation:
            contact_info = ["Name", "Cell Phone", "Work Phone", "Email"]
            contact = []
            for item in contact_info:
                info = get_optional_string(f"Enter the coach's {item}: ")
                contact.append(f"{item}: {info}")
            args['coach_contact_info'] = contact
        args['athletic_resumes_required'] = get_yes_no_required("Are athletic resumes required? (y/n): ")

        return Athletic(**args)

    @staticmethod
    def user_prompt_Minority():
        args = ScholarshipPrompt.prompt_scholarship()
        args['target_demographic'] = get_required_string("Enter the target demographic for the scholarship: ", "target demographic")
        community_involvement = get_yes_no_optional("Is community involvement required? (y/n, press Enter if unsure): ")
        if community_involvement is not None:
            args['community_involvement_required'] = community_involvement
        diversity_statement = get_yes_no_optional("Is a diversity statement required? (y/n, press Enter if unsure): ")
        if diversity_statement is not None:
            args['diversity_statement_required'] = diversity_statement
        
        return Minority(**args)
    
    @staticmethod
    def user_prompt_arts():
        args = ScholarshipPrompt.prompt_scholarship()
        while True:
            art_mediums = get_optional_string("Enter the art mediums accepted (comma-separated) (if unsure then press Enter): ")
            if art_mediums is None:
                break
            elif art_mediums is not None:
                other_mediums = get_optional_string("Are there any other art mediums accepted? (if none then press Enter): ")
                art_mediums = art_mediums + "," + other_mediums if other_mediums is not None else art_mediums    
                args['art_mediums_accepted'] = [medium.strip() for medium in art_mediums.split(',')]
                break   
        args['art_portfolio_required'] = get_yes_no_required("Is an art portfolio required? (y/n): ")
        args['audition_required'] = get_yes_no_required("Is an audition required? (y/n): ")

        return Creative_Arts(**args)
    
    @staticmethod
    def user_prompt_service():
        args = ScholarshipPrompt.prompt_scholarship()
        args['service_hours_required'] = get_required_int("Enter the number of service hours required: ", "service hours", min_value=0)
        service_type = get_optional_string("Enter the type of service required (if unsure then press Enter): ")
        if service_type is not None:
            args['type_of_service'] = service_type
        recommendation_letters = get_optional_int("Enter the number of recommendation letters required (if none then press Enter): ", min_value=0)
        if recommendation_letters is not None:
            args['recommendation_letters_required'] = recommendation_letters

        return Community_Service(**args)


def main():
    p = ScholarshipPrompt()
    manager = Scholarship_Manager()
    manager.import_from_saved_file("SR_cache.pkl")

# Set of example scholarships for testing purposes. Uncomment to add them to your records. Once you run the program once with these uncommented, they will be saved to your SR_cache.pkl file and loaded automatically on subsequent runs. 
    # # --- BASIC SCHOLARSHIP ---
    # scholarship_example = Scholarship(
    #     name="General Excellence Award",
    #     pay_amount=1000,
    #     deadline="2025-05-01",
    #     scholarship_type="Other",
    #     essay_count=1,
    #     organization="Community Foundation",
    #     additional_required_materials=["Transcript"],
    #     URL="https://example.com/general-excellence"
    # )

    # # --- ACADEMIC ---
    # academic_example = Academic(
    #     name="Academic Honors Scholarship",
    #     pay_amount=5000,
    #     deadline="2025-06-15",
    #     essay_count=2,
    #     organization="University Board",
    #     GPA_requirement=3.8,
    #     transcript_required=True,
    #     letters_of_recommendation=2,
    #     standardized_testing_required=True,
    #     additional_required_materials=["Transcript", "Letter of Recommendation"],
    #     URL="https://example.com/academic-honors"
    # )

    # # --- FEDERAL GRANT ---
    # federal_example = Federal_Grant(
    #     name="Pell Grant",
    #     pay_amount=7395,
    #     deadline=None,   # federal grants do not usually have individual deadlines
    #     essay_count=0,
    #     organization="Federal Student Aid",
    #     FAFSA_required=True,
    #     enrollment_status="Full-Time",
    #     income_threshold=35000,
    #     URL="https://example.com/pell-grant"
    # )

    # # --- NEED-BASED ---
    # need_based_example = Need_Based(
    #     name="Low-Income Student Assistance Fund",
    #     pay_amount=2000,
    #     deadline="2025-08-30",
    #     organization="Helping Hands Org",
    #     FAFSA_required=True,
    #     enrollment_status="Part-Time",
    #     additional_required_materials=["Proof of Income"],
    #     URL="https://example.com/need-based"
    # )

    # # --- ATHLETIC ---
    # athletic_example = Athletic(
    #     name="Student Athlete Achievement Scholarship",
    #     pay_amount=3000,
    #     deadline="2025-07-01",
    #     essay_count=1,
    #     organization="National Sports League",
    #     sport="Basketball",
    #     competition_level="State Level",
    #     coach_recommendation=True,
    #     coach_contact_info=["Coach John Doe", "coach@example.com"],
    #     athletic_resumes_required=True,
    #     additional_required_materials=["Athletic Resume"],
    #     URL="https://example.com/athletic"
    # )

    # # --- MINORITY ---
    # minority_example = Minority(
    #     name="Diversity Leadership Scholarship",
    #     pay_amount=4000,
    #     deadline="2025-09-01",
    #     organization="Diversity Fund",
    #     target_demographic="Underrepresented Students",
    #     community_involvement_required=True,
    #     diversity_statement_required=True,
    #     additional_required_materials=["Diversity Statement"],
    #     URL="https://example.com/minority"
    # )

    # # --- CREATIVE ARTS ---
    # creative_arts_example = Creative_Arts(
    #     name="Artistic Talent Grant",
    #     pay_amount=2500,
    #     deadline="2025-04-15",
    #     organization="Arts Council",
    #     art_portfolio_required=True,
    #     audition_required=False,
    #     art_mediums_accepted=["Painting", "Sculpture", "Digital Art"],
    #     additional_required_materials=["Portfolio"],
    #     URL="https://example.com/creative-arts"
    # )

    # # --- COMMUNITY SERVICE ---
    # community_service_example = Community_Service(
    #     name="Community Hero Scholarship",
    #     pay_amount=1500,
    #     deadline="2025-03-20",
    #     organization="Volunteer Network",
    #     service_hours_required=100,
    #     type_of_service="Community Clean-Up / Local Outreach",
    #     recommendation_letters_required=1,
    #     additional_required_materials=["Service Log"],
    #     URL="https://example.com/community-service"
    # )
    # manager.add_scholarship(scholarship_example)
    # manager.add_scholarship(academic_example)
    # manager.add_scholarship(federal_example)
    # manager.add_scholarship(need_based_example)
    # manager.add_scholarship(athletic_example)
    # manager.add_scholarship(minority_example)
    # manager.add_scholarship(creative_arts_example)
    # manager.add_scholarship(community_service_example)


#greeting when main function is run
    print("\nWelcome to your Scholarship Recorder!")

#variable for scholarship type prompt
    prompt_scholarship_input = '\n'.join([
        "\n1. Academic",
        "2. Federal",
        "3. Need-Based",
        "4. Athletic",
        "5. Minority",
        "6. Creative Arts",
        "7. Community Service",
        "8. Other",
        "\nWhich type of scholarship would you like to add? (1-8, Enter for done): "])

#variable for general actions
    prompt_general_input = '\n'.join([
        "\n========== MAIN MENU ==========",
        "1. Add a Scholarship",
        "2. Delete a Scholarship",
        "3. List Scholarships",
        "4. Export Scholarships to Excel Sheet",
        "5. Open Scholarship URLs",
        "6. Mark a Scholarship as Applied",
        "7. View Scholarships Marked as Applied",
        "8. Exit",
        "\nEnter what you would like to do (1-8): "

    ])

#variable for excel viewing prompt
    prompt_excel_input = '\n'.join([
        "\n1. Academic",
        "2. Federal",
        "3. Need-Based",
        "4. Athletic",
        "5. Minority",
        "6. Creative Arts",
        "7. Community Service",
        "8. Other Scholarships",
        "9. All Scholarships",
        "10. Specific Scholarship (by Name)",
        "\nEnter which scholarships you would like to view in Excel (1-10, Enter for done): "
    ])

    while True:
        user_choice = input(f"\n{prompt_general_input}")

        match user_choice:
            case "1": # Add a Scholarship using prompts defined in ScholarshipPrompt
                while True:
                    scholarship_type = input(f"{prompt_scholarship_input}\n")
                    match scholarship_type:
                        case "1":
                            item = p.user_prompt_academic()
                            manager.add_scholarship(item)
                            # print(f'Scholarship "{item.name}" has been added to your records.')
                        case "2":
                            item = p.user_prompt_federal()
                            manager.add_scholarship(item)
                            # print(f'Scholarship "{item.name}" has been added to your records.')
                        case "3":
                            item = p.user_prompt_need_based()
                            manager.add_scholarship(item)
                            # print(f'Scholarship "{item.name}" has been added to your records.')
                        case "4":
                            item = p.user_prompt_athletic()
                            manager.add_scholarship(item)
                            # print(f'Scholarship "{item.name}" has been added to your records.')
                        case "5":
                            item = p.user_prompt_Minority()
                            manager.add_scholarship(item)
                            # print(f'Scholarship "{item.name}" has been added to your records.')
                        case "6":
                            item = p.user_prompt_arts()
                            manager.add_scholarship(item)
                            # print(f'Scholarship "{item.name}" has been added to your records.')
                        case "7":
                            item = p.user_prompt_service()
                            manager.add_scholarship(item)
                            # print(f'Scholarship "{item.name}" has been added to your records.')
                        case "8":
                            item = p.user_prompt_other_scholarship()
                            manager.add_scholarship(item)
                            print(f'Scholarship "{item.name}" has been added to your records.')
                        case '':
                            break
                        case _:
                            print("Invalid input. Please enter a choice from the menu (1-8) or Enter")

            case "2": # Delete a Scholarship after prompting user for scholarship name
                while True:
                    print("\nScholarships List:")
                    print(manager)
                    delete_prompt = input("Enter the name of the scholarship you want to delete (ALL to delete all scholarships, EXPIRED to delete expired scholarships that you have not applied for, or Enter to cancel): ")
                    if delete_prompt == "":
                        break
                    elif delete_prompt.upper() == "ALL":
                        while True:
                            confirm = input("Are you sure you want to delete ALL scholarships? This action cannot be undone. (yes/no): ")
                            if confirm.lower() == "yes":
                                manager.scholarships.clear()
                                print("All scholarships have been deleted from your records.")
                                break
                            elif confirm.lower() == "no":
                                print("Deletion of all scholarships canceled.")
                                break
                            else:
                                print("Invalid input. Please enter 'yes' or 'no'.")
                                continue
                    elif delete_prompt.strip() == "EXPIRED":
                        manager.auto_remove_expired_scholarships()
                        print("\nAll expired scholarships that you have not applied for have been deleted from your records.")
                    else:
                        for i in manager.scholarships:
                            if i.name.lower() == delete_prompt.lower():
                                manager.remove_scholarship(i)
                                print(f'Scholarship "{delete_prompt}" has been deleted from your records.')
                                break
                        else:
                            print(f'No scholarship found with the name "{delete_prompt}".')

            case "3": # List Scholarships
                print("\nScholarships List:")
                print(manager)

            
            case "4": # View Scholarships in Excel. First prompts users what scholarship type they want to view
                while True:
                    excel_choice = input(f"{prompt_excel_input}\n")
                    match excel_choice:
                        case "1":
                            count = 0
                            for i in manager.scholarships:
                                if i.scholarship_type == "Academic":
                                    i.add_to_sheet()
                                    count += 1
                            if count == 0:
                                print("No Academic scholarships found to export.")
                            else:
                                print(f"Exported {count} Academic scholarship(s) to Excel.")
                        case "2":
                            count = 0
                            for i in manager.scholarships:
                                if i.scholarship_type == "Federal Grant/Scholarship":
                                    i.add_to_sheet()
                                    count += 1
                            if count == 0:
                                print("No Federal Grant/Scholarship scholarships found to export.")
                            else:
                                print(f"Exported {count} Federal Grant/Scholarship scholarship(s) to Excel.")
                        case "3":
                            count = 0
                            for i in manager.scholarships:
                                if i.scholarship_type == "Need-Based":
                                    i.add_to_sheet()
                                    count += 1
                            if count == 0:
                                print("No Need-Based scholarships found to export.")
                            else:
                                print(f"Exported {count} Need-Based scholarship(s) to Excel.")
                        case "4":
                            count = 0
                            for i in manager.scholarships:
                                if i.scholarship_type == "Athletic":
                                    i.add_to_sheet()
                                    count += 1
                            if count == 0:
                                print("No Athletic scholarships found to export.")
                            else:
                                print(f"Exported {count} Athletic scholarship(s) to Excel.")
                        case "5": 
                            count = 0
                            for i in manager.scholarships:
                                if i.scholarship_type == "Minority":
                                    i.add_to_sheet()
                                    count += 1
                            if count == 0: 
                                print("No Minority scholarships found to export.")
                            else:
                                print(f"Exported {count} Minority scholarship(s) to Excel.")
                        case "6":
                            count = 0
                            for i in manager.scholarships:
                                if i.scholarship_type == "Creative Arts":
                                    i.add_to_sheet()
                                    count += 1
                            if count == 0:
                                print("No Creative Arts scholarships found to export.")
                            else:
                                print(f"Exported {count} Creative Arts scholarship(s) to Excel.")
                        case "7":
                            count = 0
                            for i in manager.scholarships:
                                if i.scholarship_type == "Community Service":
                                    i.add_to_sheet()
                                    count += 1
                            if count == 0:
                                print("No Community Service scholarships found to export.")
                            else:
                                print(f"Exported {count} Community Service scholarship(s) to Excel.")
                        case "8":
                            count = 0
                            for i in manager.scholarships:
                                if type(i) is Scholarship:
                                    i.add_to_sheet()
                                    count += 1
                            if count == 0:
                                print('No other scholarship types found to export.')
                            else:
                                print(f'Exported {count} other scholarship type(s) to Excel.')
                        case "9":
                            count = 0
                            for i in manager.scholarships:
                                i.add_to_sheet_all()
                                count += 1
                            if count == 0:
                                print("No scholarships found to export.")
                            else:
                                print(f"Exported {count} scholarship(s) to Excel.")
                        case "10":
                            print(manager)
                            name = input("\nEnter the name of the scholarship (or Enter to cancel): ")
                            scholarships = 0
                            if name == "":
                                continue
                            for i in manager.scholarships:
                                if i.name.lower() == name.lower():
                                    i.add_to_sheet()
                                    scholarships += 1
                            if scholarships == 0:
                                print(f'No scholarship found with the name "{name}".')
                            else:
                                print(f'Exported scholarship "{name}" to Excel.')
                        case '':
                            break
                        case _:
                            print("Invalid input. Please enter a choice from the menu (1-10) or Enter")   

            case "5": # Open Scholarship URLs after prompting user for scholarship name
                while True:
                    print(manager)
                    url_prompt = input("Enter the name of the scholarship you want to open the URL for (or Enter to cancel): ")
                    if url_prompt == "":
                        break
                    for scholarship in manager.scholarships:
                        if scholarship.name.lower() == url_prompt.lower():
                            if not scholarship.open_url():
                                print(f'No URL available for scholarship "{scholarship.name}".')
                            break
                    else:
                        print(f'No scholarship found with the name "{url_prompt}".')

            case "6": # Mark a Scholarship as Applied
                while True:
                    print("\nScholarships Available to Apply For:")
                    scholarship_count = 0
                    for i in manager.scholarships:
                        if not i.applied:
                            print(i)
                            scholarship_count += 1
                    if scholarship_count == 0:
                        print("None")
                    applied_prompt = input("\nEnter the name of the scholarship you have applied for (or Enter to cancel): ")
                    if applied_prompt == "":
                        break
                    for scholarship in manager.scholarships:
                        if scholarship.name.lower() == applied_prompt.lower():
                            scholarship.applied = True
                            print(f'Scholarship "{scholarship.name}" has been marked as applied.')
                            break
                    else:
                        print(f'No scholarship found with the name "{applied_prompt}".')
            
            case "7": # View applied for scholarships
                while True:
                    print("\nScholarships You Have Applied For:")
                    scholarship_count = 0
                    for i in manager.scholarships:
                        if i.applied:
                            print(i)
                            scholarship_count += 1
                    if scholarship_count == 0:
                        print("None")
                    value = input("\nIf you want to mark any scholarship as not applied, please type it's name (or Enter to return to the main menu): ")
                    if value == "":
                        break
                    for scholarship in manager.scholarships:
                        if scholarship.name.lower() == value.lower():
                            scholarship.applied = False
                            print(f'Scholarship "{scholarship.name}" has been marked as not applied.')
                            break
                    
            case "8": # Exit after saving scholarship information to a file
                print("\nExiting Scholarship Recorder. Goodbye!\n")
                manager.export_to_saved_file("SR_cache.pkl")
                break

if __name__ == "__main__":
    main()