import firebase_admin
from firebase_admin import credentials, db
cred = credentials.Certificate('../Account_management/credentials.json')
firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/%22%7D"})
class Product:
    def __init__(self, image, title, description, price, seller_name, rating, condition):
        self.__image__ = image
        self.__title__ = title
        self.__description__ = description
        self.__price__ = price
        self.__seller_name__ = seller_name
        self.__rating__ = rating
        self.__condition__ = condition

    def get_image(self):
        return self.__image__

    def get_title(self):
        return self.__title__

    def get_description(self):
        return self.__description__

    def get_price(self):
        return self.__price__

    def get_seller_name(self):
        return self.__seller_name__

    def get_rating(self):
        return self.__rating__

    def get_condition(self):
        return self.__condition__

    def set_image(self, image):
        self.__image__ = image

    def set_title(self, title):
        self.__title__ = title

    def set_description(self, description):
        self.__description__ = description

    def set_price(self, price):
        self.__price__ = price

    def set_seller_name(self, seller_name):
        self.__seller_name__ = seller_name

    def set_rating(self, rating):
        self.__rating__ = rating

    def set_condition(self, condition):
        self.__condition__ = condition


class Product:
    def __init__(self, image, title, description, price, seller_name, rating, condition):
        self.__image__ = image
        self.__title__ = title
        self.__description__ = description
        self.__price__ = price
        self.__seller_name__ = seller_name
        self.__rating__ = rating
        self.__condition__ = condition

    def get_image(self):
        return self.__image__

    def get_title(self):
        return self.__title__

    def get_description(self):
        return self.__description__

    def get_price(self):
        return self.__price__

    def get_seller_name(self):
        return self.__seller_name__

    def get_rating(self):
        return self.__rating__

    def get_condition(self):
        return self.__condition__

    def read_data_from_firebase(document_id):
        try:
            ref = db.reference(f'products/{document_id}')  # Reference to the RTDB document
            data = ref.get()
            if data:
                return data
            else:
                print(f"Document '{document_id}' does not exist in the database.")
                return None
        except Exception as e:
            print("Error reading data from Firebase:", e)
            return None

    def update_data_in_firebase(document_id, data_to_update):
        try:
            ref = db.reference(f'products/{document_id}')  # Reference to the RTDB document
            ref.update(data_to_update)
            print(f"Document '{document_id}' successfully updated in the database.")
            return True
        except Exception as e:
            print("Error updating data in Firebase:", e)
            return False

    def delete_data_from_firebase(document_id):
        try:
            ref = db.reference(f'products/{document_id}')  # Reference to the RTDB document
            ref.delete()
            print(f"Document '{document_id}' successfully deleted from the database.")
            return True
        except Exception as e:
            print("Error deleting data from Firebase:", e)
            return False

def test_add_and_read_from_firebase():
    # Test data for product
    product_data = {
        "image": "product_image.jpg",
        "title": "Test Product",
        "description": "This is a test product.",
        "price": 99.99,
        "seller_name": "Test Seller",
        "rating": 4.2,
        "condition": "New"
    }

    # Add data to Firebase
    try:
        db.reference('products/test_product').set(product_data)
        print("Data added to Firebase.")
    except Exception as e:
        print("Error adding data to Firebase:", e)
        return

    # Read data from Firebase
    print("\nReading data from Firebase:")
    data = Product.read_data_from_firebase("test_product")
    if data:
        print("Data read from Firebase:", data)

if __name__ == "__main__":
    test_add_and_read_from_firebase()



