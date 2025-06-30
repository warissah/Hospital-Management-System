# Hotel Management project covers content from Data Structure
import heapq


patient_heap=[]

action_stack=[] #lastin-firstout

check_in_queue = []

class person:

    def __init__(self, name , person_ID, age):
        self.name = name
        self.id = person_ID
        self. age = age



#doctor

class Doctor(person):
    def __init__(self, name, age, person_ID, specialty):
        # Repeating name, age to pass to Person
        super().__init__(name, age, person_ID) 
        self.specialty = specialty

#methods for doctor

    def list_patient(self,patients):
        for p in patients:
            print(f"Dr.{self.name}'s patients:" )
            if p["doctor_id"]== self.id:
                show_patient_by_id(p["patients_id"], patients)
    
    
                

    def update_specialty(self, doctors, doctor_ID):
        doctor_ID = input("Enter Doctor Id: ")
        for d in doctors:
            if d["doctor_id"]==doctor_ID:
                old_specialty = d["specialty"]
                new_specialty = input("Enter new specialty: ")
                d["specialty"] = new_specialty
                print("Specialty Updated.")
                action_stack.append(("update_specialty", {"id": doctor_ID, "old": old_specialty}))
                return 
        print("Doctor not found.")



#nurse
class Nurse(person):
    def __init__(self, name, age, person_ID, shift, department):
        # Repeating name, age to pass to Person
        super().__init__(name, age, person_ID) 
        self.shift = shift
        self.department = department

#methods for nurse
    def assign_shift(self, new_shift):
        self.shift = new_shift
        print(f"Shift updated to {new_shift} for Nurse {self.name}")

    def assist_doctor(self, doctor_id, doctors, patients):
        for d in doctors:
            if d["doctor_id"] == doctor_id:
                print(f"Nurse {self.name} is assisting Dr.{d['name']} (Specialty: {d['specialty']})")
                print("Here are Dr.{0}'s patients:".format(d['name']))
                for p in patients:
                    if p["doctor_id"] == doctor_id:
                        print(f"- {p['name']} (ID: {p['patients_id']}, Ailment: {p['ailment']})")
                return
        print("Doctor not found.")





#patient
class Patient(person):
    def __init__(self, name, age, person_ID, ailment, priority_level, admitted=False):
        # Repeating name, age to pass to Person
        super().__init__(name, age, person_ID) 
        self.ailment = ailment
        self.priority_level = priority_level
        self.admitted = admitted 

#methods for patient



    def admit(self, patients, doctor):
        patient_name = input("Enter patient's name: ")
        patient_id = input("Enter patient's ID: ")
        patient_age = input("Enter patient's age: ")
        patient_ailment = input("Enter patient's ailment: ")
        while True:
            priority_input = input("Enter priority level (1=Critical, 4=Low): ")
            if priority_input.isdigit() and 1 <= int(priority_input) <= 4:
                patient_priority_lvl = int(priority_input)
                break
            else:
                print("Please enter a number between 1 and 4.")
        patient_admit = True  # patient is being admitted
        doctor_id = input("Enter Doctor ID: ")  # doctor assigning the patient

        new_patient = {
            "name": patient_name,
            "age": int(patient_age),
            "patients_id": patient_id,
            "ailment": patient_ailment,
            "priority": patient_priority_lvl,
            "admitted": patient_admit,
            "doctor_id": doctor_id}
        
        for d in doctor:
            if doctor_id == d["doctor_id"]:
                print(f'{patient_name} has been admitted and assigned to Dr.{d["name"]}')

        

        patients.append(new_patient)
        heapq.heappush(patient_heap, (int(patient_priority_lvl), patient_id, new_patient))
        

        if patient_priority_lvl > 1:
            check_in_queue.append(new_patient)
            print(f"{patient_name} added to check-in queue for general consultation.")

        


    def discharge(self, patients):
        patient_id = input("Enter patient ID to discharge: ")
        for i, p in enumerate(patients):
            if p["patients_id"] == patient_id:
                print(f"Discharging patient: {p['name']} (ID: {patient_id})")
                patients.pop(i)  # remove from list using index
                print("Patient successfully discharged and removed.")
                return
        print("Patient not found.")

        

    def update_ailment(self,patients, action_stack):
        patient_ID = input("Enter patient Id: ")
        for p in patients:
            if p["patients_id"]== patient_ID:
                new_ailment = input("Enter new specialty: ")
                old_ailment = p["ailment"] 
                p["ailment"] = new_ailment
                action_stack.append(("update_ailment", {"id": patient_ID, "old": old_ailment}))
                print("Ailment Updated.")
                return 
        print("Patient not found.")


    def update_priority(self, new_priority_lvl, action_stack):
        old_priority = self.priority_level
        self.priority_level = new_priority_lvl
        update_priority_in_heap(patient_heap, self.id, new_priority_lvl)
        print(f"Priority level updated to {new_priority_lvl} for patient {self.name}")
        action_stack.append(("update_priority", {"id": self.id, "old": old_priority}))


    def update_doctor(patients,action_stack):
        patient_ID = input("Enter patient Id: ")
        for p in patients:
            if p["patients_id"]== patient_ID:
                old_doctor = p["doctor_id"]
                new_Doc_ID = input("Enter new Doctor ID: ")
                p["doctor_id"] = new_Doc_ID
                print("Doctor updated.")
                action_stack.append(("update_doctor", {"id": patient_ID, "old": old_doctor}))
                return
        print("Patient not found.")








def update_priority_in_heap(patient_heap, patient_id, new_priority):
    for i, item in enumerate(patient_heap):
        if item[1] == patient_id:
            patient_data = item[2]
            patient_data["priority"] = new_priority
            del patient_heap[i]
            heapq.heapify(patient_heap)  # re-heapify after deletion
            heapq.heappush(patient_heap, (new_priority, patient_id, patient_data))
            break











def check_next_patient(self, check_in_queue):
    if check_in_queue:
        current_patient = check_in_queue.pop(0)
        print(f"Now treating: {current_patient['name']} (ID: {current_patient['patients_id']})")
    else:
        print("No patients in the check-in queue.")







def load_patients():
    patients = []
    try:
        with open("patients.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) < 7:
                    continue
                patients.append({
                    "name": parts[0].strip(),
                    "age": int(parts[1].strip()),
                    "patients_id": parts[2].strip(),
                    "ailment": parts[3].strip(),
                    "priority": parts[4].strip(),
                    "admitted": parts[5].strip().lower() == "true",
                    "doctor_id": parts[6].strip()
                })
    except FileNotFoundError:
        pass
    return patients

def save_patients(patients):
    with open("patients.txt", "w") as file:
        for p in patients:
            line = ",".join([
                p["name"],
                str(p["age"]),
                p["patients_id"],
                p["ailment"],
                p["priority"],
                str(p["admitted"]),
                p["doctor_id"]
            ])
            file.write(line + "\n")



#dont forget to load at the start

def load_doctor():
    doctors = []
    try:
        with open("doctor.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) < 4:
                    continue
                doctors.append({
                    "name": parts[0].strip(),
                    "age": int(parts[1].strip()),
                    "doctor_id": parts[2].strip(),
                    "specialty": parts[3].strip(),
                })
    except FileNotFoundError:
        pass  # no file yet
    return doctors

def save_doctor(doctors):
    with open("doctor.txt", "w") as file:
        for d in doctors:
            line = ",".join([
                d["name"],
                str(d["age"]),
                d["doctor_id"],
                d["specialty"],
            ])
            file.write(line + "\n")



def show_patient_by_id(patient_id, patients):
    for p in patients:
        if p["patients_id"] == patient_id:
            print("Patient Information:")
            print(f"Name: {p['name']}")
            print(f"Age: {p['age']}")
            print(f"ID: {p['patients_id']}")
            print(f"Ailment: {p['ailment']}")
            print(f"Priority: {p['priority']}")
            print(f"Admitted: {p['admitted']}")
            print(f"Doctor ID: {p['doctor_id']}")
            return
    print("Patient not found.")



def load_nurse():
    nurse = []
    try:
        with open("nurse.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) < 5:
                    continue
                nurse.append({
                    "name": parts[0].strip(),
                    "age": int(parts[1].strip()),
                    "nurse_id": parts[2].strip(),
                    "shift": parts[3].strip(),
                    "doctor_id": parts[4].strip(),
                })
    except FileNotFoundError:
        pass  # no file yet
    return nurse

def save_nurse(nurse):
    with open("nurse.txt", "w") as file:
        for n in nurse:
            line = ",".join([
                n["name"],
                str(n["age"]),
                n["nurse_id"],
                n["shift"],
                n["doctor_id"],
                
            ])
            file.write(line + "\n")




def show_most_urgent(patient_heap):
    if not patient_heap:
        print("No patients in the heap.")
        return
    patient = patient_heap[0][2]  # Access the patient dictionary in the tuple
    print(f"Most urgent patient:")
    print(f"Name: {patient['name']}")
    print(f"Ailment: {patient['ailment']}")
    print(f"ID: {patient['patients_id']}")

def treat_urgent_patient(patients,patient_heap):
    if not patient_heap:
        print("No patients in the heap.")
        return
    
    urgent_patient = patient_heap[0][2]
    heapq.heappop(patient_heap)
    print(f"Treating patient {urgent_patient['name']} (ID: {urgent_patient['patients_id']}) with ailment: {urgent_patient['ailment']}")

    patient_id = urgent_patient['patients_id']
    for i, p in enumerate(patients):
        if p["patients_id"] == patient_id:
            print(f"Discharging patient: {p['name']} (ID: {patient_id})")
            patients.pop(i)  # remove from list using index
            print("Patient successfully discharged and removed.")
            return
    print("Patient not found.")


def sort_patients(patients):
    # Sort by age first, then by name
    patients.sort(key=lambda p: (p["age"], p["name"].lower()))
    print("Patients sorted by age and name:")
    for p in patients:
        print(f"{p['name']} - Age: {p['age']}")


def search_patient_wname(patients):
    need = input("Enter part of the patient's name: ").lower()
    found = False
    for p in patients:
        if need in p["name"].lower():
            print("Match found:")
            print(f"Name: {p['name']}, ID: {p['patients_id']}, Ailment: {p['ailment']}")
            found = True
    if not found:
        print("No patient found with that name part.")




def main():
    patients = load_patients()
    doctors = load_doctor()
    nurse = load_nurse()

    # your program logic here

    save_patients(patients)
    save_doctor(doctors)
    save_nurse(nurse)

if __name__ == "__main__":
    main()
