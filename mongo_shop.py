import pymongo


class MongoShop:
    def __init__(self, mongohost):
        self.client = pymongo.MongoClient(mongohost)
        db_name = 'Shop'
        collection_name = 'Info'
        self.info_client = self.client[db_name][collection_name]
        self.service_client = self.client[db_name]['Services']

    def insert_info(self, shop_data):
        print 'Inside insert_data', shop_data
        x = self.info_client.insert_one(shop_data)

    def insert_services(self, services_data):
        return self.service_client.insert_one(services_data)

    def get_services(self, shop_id):
        return self.service_client.find_one({"_id": shop_id})
