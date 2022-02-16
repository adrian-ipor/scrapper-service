import kwargs as kwargs
import pytest
import sys
import os
import requests
from expects import expect, raise_error
from testcontainers.elasticsearch import ElasticSearchContainer
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from save_data import SaveData
from scrapper_service import Scrapper
from configuration.properties.config import ProductionConfig


class TestScrapper:
    esc = ElasticSearchContainer(image="elasticsearch:7.16.2")
    esc.start()
    port = esc.get_exposed_port(esc.port_to_expose)
    config = ProductionConfig().import_configuration()
    scrapper = Scrapper(config)

    def setup_class(self):

        self.config["io.ipor.scrapper"]["save-data"]["elasticsearch"]["port"] = self.port
        file = open('migration/asset_mapping.json', 'r')
        data = file.read()
        headers = {'content-type': 'application/json'}

        for asset in self.config['io.ipor.scrapper']['ethereum']['currencies']:
            requests.put(f"http://localhost:{self.port}/{asset.lower()}-aave-v1")
            requests.put(f"http://localhost:{self.port}/{asset.lower()}-aave-v1/_mapping",
                         data=data, headers=headers)
        file.close()

    def teardown_class(self):
        self.esc.stop()

    def test_scrape_reserve_data_for_latest_block_number_less_then_start_block_number(self):
        # Given
        self.scrapper.start_block_number = 14004723
        self.scrapper.latest_block_number = 14004722
        # When and Then
        expect(lambda: self.scrapper.scrape_reserve_data()).to(raise_error(ValueError))

    def test_scrape_reserve_data_for_latest_block_number_equal_then_start_block_number(self):
        # Given
        self.scrapper.start_block_number = 14004723
        self.scrapper.latest_block_number = 14004723
        # When and Then
        assert self.scrapper.scrape_reserve_data()

    def test_scrape_reserve_data_for_latest_block_number_greater_then_start_block_number(self):
        # Given
        self.scrapper.start_block_number = 14004523
        self.scrapper.latest_block_number = 14004723
        # When and Then
        assert self.scrapper.scrape_reserve_data()

    def test_save_scraped_data_to_elasticsearch(self):
        # Given
        self.scrapper.start_block_number = 14004523
        self.scrapper.latest_block_number = 14004723
        # When and Then
        assert self.scrapper.scrape_reserve_data()

    def test_elasticsearch_compare_send_and_receive_data_expect_same(self):
        # Given
        save_data = SaveData(self.config)
        send_data = {"blockNumber": 14004824, "timestamp": 1642179365, "indexTimestamp": 1643616431, "asset": "DAI",
                     "indexSource": "ipor-oracle-scrapper-aave", "borrowRate": 8.273333864073507,
                     "supplyRate": 5.163423793313652, "totalBorrowsUT": 8610220.566438051,
                     "totalSupplyUT": 15747015.049619997, "utilizationRate": 63644589613.41474,
                     "availableLiquidityRaw": 4918377258982172125667916,
                     "totalStableDebtRaw": 6376553841639208822731725,
                     "totalVariableDebtRaw": 2233666724798841784775852, "liquidityRateRaw": 51634237933136516933042509,
                     "variableBorrowRateRaw": 65688895080857563755400770,
                     "stableBorrowRateRaw": 82733338640735054647486374,
                     "averageStableBorrowRateRaw": 86537849322085867329141916,
                     "liquidityIndexRaw": 1164333016411534713867770430,
                     "variableBorrowIndexRaw": 1284565388368158334606236877, "lastUpdateTimestamp": 1642170497,
                     "totalSupplyRaw": 15747015049619995901616438, "stableBorrowRate": 8.273333864073507,
                     "availableLiquidity": 4918377.258982173, "totalStableDebt": 6376553.841639209,
                     "totalVariableDebt": 2233666.724798842, "averageStableBorrowRate": 8653784932.20859,
                     "liquidityIndex": 1164333016.4115348, "variableBorrowIndex": 1284565388.3681586
                     }
        asset = 'DAI'
        # When
        es_id = save_data.save_dto_to_elasticsearch(send_data=send_data, asset=asset)
        response = requests.get(f"http://localhost:{self.port}/{asset.lower()}-aave-v1/_doc/{es_id}")
        reserve_data = response.json()['_source']
        # Then
        assert send_data == reserve_data
