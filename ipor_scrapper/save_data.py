# from configuration.properties.config import ProductionConfig
from loguru import logger
from elasticsearch import Elasticsearch
import pathlib
import random as r

parent_path = pathlib.Path(__file__).parent.resolve()


class SaveData:

    def __init__(self, _configuration):
        self.configuration = _configuration
        self.data_configuration = self.configuration['io.ipor.scrapper']
        self.save_to_file = self.data_configuration['save-data']['file']['enable']
        self.save_to_elasticsearch = self.data_configuration['save-data']['elasticsearch']

        if self.save_to_file:
            self.output_file = self.creating_output_file()

        if self.save_to_elasticsearch['enable']:
            es_host = self.save_to_elasticsearch['host-name']
            es_port = self.save_to_elasticsearch['port']
            self.output_elasticsearch = Elasticsearch(
                [es_host],
                port=es_port
            )
            logger.info("Creating instance of Elasticsearch")
        else:
            self.output_elasticsearch = False

    @staticmethod
    def generate_uuid():
        random_string = ''
        random_str_seq = "RFMsVkw4ITObx58U9QVJv7KfUCYSYgwQPF5Vo8HCb7OEphrlneCEgIDt"
        uuid_format = [8, 4, 4, 4, 12]
        for n in uuid_format:
            for i in range(0, n):
                random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])
            if n != 12:
                random_string += '-'
        return random_string

    def creating_output_file(self):
        output_file = {}  # creating dictionary of output
        for asset in self.data_configuration['ethereum']['currencies']:
            output_file[asset] = open(f"{parent_path}/output/stable_coin_{asset}", "a")
            logger.info("creating output file stable_coin_{}", asset)
        return output_file

    def save_dto_to_file(self, send_data, asset):
        self.output_file[asset].write(str(send_data) + "\n")

    def save_dto_to_elasticsearch(self, send_data, asset):
        asset = asset.lower()  # change from upper to low case
        es_id = self.generate_uuid()
        logger.info("Elasticsearch id = {}", es_id)
        self.output_elasticsearch.index(f"{asset}-aave-v1", id=es_id, document=send_data)
        return es_id

    def close_output_file(self):
        for asset in self.data_configuration['currencies']:
            self.output_file[asset].close()
            logger.info("close output file stable_coin_{}", asset)

    def save_data(self, send_data, asset):
        if self.save_to_file:
            self.save_dto_to_file(send_data, asset)
            logger.info("Save data to file: {}", asset)

        if self.save_to_elasticsearch['enable']:
            self.save_dto_to_elasticsearch(send_data, asset)
            logger.info("Save data to elasticsearch: {}", asset)
