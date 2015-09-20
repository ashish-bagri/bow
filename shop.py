from mongo_shop import MongoShop


class Shop:
    def __init__(self, config):
        mongohost = config.get("MONGO", "host")
        self.mongo_shop = MongoShop(mongohost)

    def get_services(self, shop_id):
        ret = {}
        data = self.mongo_shop.get_services(shop_id)
        if data is not None:
            ret['items'] = data['services'].values()
        return ret

    def insert_shop(self, shop_data):
        shop_data['_id'] = shop_data['id']
        self.mongo_shop.insert_info(shop_data)

    def insert_services(self, shop_id, services_list):
        services = {}
        i = 0
        for s in services_list:
            services[str(i)] = s
            i += 1

        services_data = {'id': shop_id, '_id': shop_id, 'services': services}
        self.mongo_shop.insert_services(services_data)
