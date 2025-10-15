import addressbook_pb2

# Create a new Person object
person = addressbook_pb2.Person()
person.name = "John Doe"
person.id = 1234
person.email = "johndoe@example.com"

# Serialize to binary
serialized_data = person.SerializeToString()

# Deserialize from binary
new_person = addressbook_pb2.Person()
new_person.ParseFromString(serialized_data)

print(f"Name: {new_person.name}, ID: {new_person.id}, Email: {new_person.email}")
