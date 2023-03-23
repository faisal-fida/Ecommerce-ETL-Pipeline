import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('path/to/serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

batch = db.batch()

for i in range(100):
    product_ref = db.collection('products').document(f'thredup_{i}')
    batch.set(product_ref, {})

batch.commit()