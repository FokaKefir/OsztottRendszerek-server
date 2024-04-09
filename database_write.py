import firebase_admin
from firebase_admin import credentials, firestore

# load credentials for firebase
cred = credentials.Certificate('forms_key.json')
firebase_admin.initialize_app(cred)

# get firestore

db = firestore.client()

def register_user(email: str, name: str, password: str, phone: str, role: str = "user"):
    pass


if __name__ == '__main__':
    user_ref = db.collection('users').document('user1')
    docSnapshot = user_ref.get()
    print(docSnapshot.to_dict())