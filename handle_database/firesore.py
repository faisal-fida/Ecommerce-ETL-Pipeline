

def upload_data(db, dataJson):
    print("Uploading Data to Firestore DB.")
    for i in dataJson:
        i["Platform"] = "thredup"
        db.collection('products').document(f'thredup_{i["ItemID"]}').set(i)
    print("Data Uploaded.")
    
def retrieve_data(db):
    print("Retrieving Data from Firestore DB.")
    docs = db.collection('products').where('Platform', '==', 'thredup').select(['ItemID', 'Price']).get()
    docs = [doc.to_dict() for doc in docs]
    return docs

def delete_data(db, document):
    # Get reference to the document you want to delete
    doc_ref = db.collection('products').document(document)

    # Delete the document
    doc_ref.delete()
    print("Deleted", document)