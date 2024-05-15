import csv

def read_contacts_from_csv(csv_file):
    contacts = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if exists
        for row in reader:
            if len(row) >= 2:  # Ensure both name and phone number are present
                contacts.append({'name': row[0], 'phone': row[1]})
    return contacts

def create_vcard_file(contact):
    vcard = f"BEGIN:VCARD\nVERSION:3.0\nN:{contact['name']}\nFN:{contact['name']}\nTEL;TYPE=CELL:{contact['phone']}\nCATEGORIES:Groups,Umping\nEND:VCARD"
    file_name = f"{contact['name']}.vcf"
    with open(file_name, 'w') as vcard_file:
        vcard_file.write(vcard)
    print(f"vCard file created for '{contact['name']}'")

def main():
    csv_file = 'contacts.csv'  # Update with your CSV file name and path
    contacts = read_contacts_from_csv(csv_file)
    
    for contact in contacts:
        create_vcard_file(contact)

    print("vCard files created successfully!")

if __name__ == "__main__":
    main()
