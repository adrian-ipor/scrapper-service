import json
from loguru import logger
import pathlib

from ethereum.connection_manager import ConnectionManager
from save_data import SaveData
from dtos import AssetContractDto

parent_path = pathlib.Path(__file__).parent.resolve()
START_LIFE_STABILE_COIN_BLOCK_NUMBER = 9241200

class Scrapper:
    def __init__(self, _configuration):
        # self.env_config = _configuration
        self.configuration = _configuration
        self.connection_manager = ConnectionManager(_configuration)
        self.data_configuration_ethereum = self.configuration['io.ipor.scrapper']['ethereum']
        self.start_block_number = self.get_start_block_number()
        self.latest_block_number = self.get_end_block_number()

    def get_start_block_number(self):

        asset = list(self.data_configuration_ethereum['currencies'].keys())[0]
        logger.info("first asset in configuration {}", asset)

        try:
            file = open(f"output/stable_coin_{asset}")

            for last_line in file:
                pass
            one_line = json.loads(last_line)
            block_number = one_line["blockNumber"]+1
            logger.debug("block number from file is : {}", block_number)
        except:
            block_number = self.data_configuration_ethereum['start-block-number']
            logger.info("file not exist")
        if block_number >= START_LIFE_STABILE_COIN_BLOCK_NUMBER:
            return block_number
        else:
            raise ValueError("start block number is less then START_LIFE_STABILE_COIN_BLOCK_NUMBER")

    def get_end_block_number(self):
        from_conf_end_block_number_enable = self.data_configuration_ethereum['end-block-number']['enable']
        latest_block_number = self.connection_manager.get_web3().eth.get_block('latest').number
        if from_conf_end_block_number_enable:
            from_conf_end_block_number = self.data_configuration_ethereum['end-block-number']['number']
            if from_conf_end_block_number < latest_block_number:
                return from_conf_end_block_number
            else:
                raise ValueError("end block number is greater then current block number")
        else:
            return latest_block_number

    def scrape_reserve_data(self) -> bool:

        block_number = self.start_block_number
        end_block_number = self.latest_block_number
        # current_timestamp = 0
        output = SaveData(self.configuration)
        logger.info("Latest block number: {}", end_block_number)

        if block_number > end_block_number:
            raise ValueError("Start block number is less then latest block number")

        else:

            while block_number <= end_block_number:
                logger.info("current block number: {}", block_number)
                step = self.data_configuration_ethereum['read-block-number-step']
                for asset in self.data_configuration_ethereum['currencies']:
                    stable_coin_address = self.data_configuration_ethereum['currencies'][asset]['contract-address']
                    reserve_data = self.connection_manager.get_reserve_data(stable_coin_address, block_number)
                    dto = AssetContractDto(asset, reserve_data, block_number, self.configuration)

                    send_data = json.dumps(dto.__dict__)  # convert object to json object
                    output.save_data(send_data, asset)

                if block_number < end_block_number:
                    block_number += step
                else:
                    block_number += 1

            return True
