from scrapper_service import Scrapper
from configuration.properties.config import ProductionConfig


config = ProductionConfig()
# configuration = config.import_configuration()
scrapper = Scrapper(config)


class TestScrapper:

    def test_scrape_reserve_data_for_latest_block_number_less_then_start_block_number(self):
        # Given
        scrapper.start_block_number = 14004723
        scrapper.latest_block_number = 14004722
        # When & Then
        assert not scrapper.scrape_reserve_data()

    def test_scrape_reserve_data_for_latest_block_number_equal_then_start_block_number(self):
        # Given
        scrapper.start_block_number = 14004723
        scrapper.latest_block_number = 14004723
        # When & Then
        assert scrapper.scrape_reserve_data()

    def test_scrape_reserve_data_for_latest_block_number_greater_then_start_block_number(self):
        # Given
        scrapper.start_block_number = 14004523
        scrapper.latest_block_number = 14004723
        # When & Then
        assert scrapper.scrape_reserve_data()
