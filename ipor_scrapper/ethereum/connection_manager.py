from web3 import Web3
import json
import pathlib

# import env
# from configuration.properties.config import ProductionConfig

parent_path = pathlib.Path(__file__).parent.resolve().parent


class ConnectionManager:

    def __init__(self, _configuration):
        # self.env_config = _configuration
        self.configuration = _configuration
        self.ethereum_configuration = self.configuration['io.ipor.scrapper']['ethereum']
        self.aave_v1_configuration = self.ethereum_configuration['contracts']["aave"]["v1"]

    def get_web3(self):
        abi_dir = self.ethereum_configuration['node']
        web3 = Web3(Web3.HTTPProvider(abi_dir))
        return web3

    def get_timestamp(self, block_number):
        timestamp = self.get_web3().eth.get_block(block_number).get('timestamp')
        return timestamp

    def get_latest_block_number(self):
        latest_block_number = self.get_web3().eth.get_block('latest').number
        return latest_block_number

    def get_contract_from_arch_node(self, abi_file_path, smart_contract_address):  # TODO: will change name of metod
        file = open(f"{parent_path}/{abi_file_path}")
        abi = json.loads(file.read())
        file.close()
        contract = self.get_web3().eth.contract(address=smart_contract_address, abi=abi)
        return contract

    def get_reserve_data(self, stable_coin_address, block_number) -> object:
        lending_pool_address = self.aave_v1_configuration["lending-pool"]["address"]
        lending_pool_abi_path = self.aave_v1_configuration["lending-pool"]["abi-path"]
        contract = self.get_contract_from_arch_node(lending_pool_abi_path, lending_pool_address)
        reserve_data = contract.functions.getReserveData(stable_coin_address).call(block_identifier=block_number)
        return reserve_data

    def get_total_supply(self, asset, block_number):
        token_contract = self.get_contract_from_arch_node(
            self.aave_v1_configuration["lending-pool"]["aave-v1-token-abi-path"],
            self.aave_v1_configuration['a-tokens'][asset]['address']
        )

        total_supply = token_contract.functions.totalSupply().call(block_identifier=block_number)
        return total_supply
