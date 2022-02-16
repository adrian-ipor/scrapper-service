from ethereum.connection_manager import ConnectionManager
from mathematics import maths

RAY_UNIT = maths.ray_unit


class AssetContractDto:

    def __init__(self, asset, reserve_data, block_number, _configuration):
        configuration = _configuration
        decimal_currency = configuration['io.ipor.scrapper']['ethereum']['currencies'][asset]['decimals']
        connection_manager = ConnectionManager(_configuration)

        self.blockNumber = block_number
        self.timestamp = connection_manager.get_timestamp(block_number)
        self.indexTimestamp = connection_manager.get_timestamp(
            connection_manager.get_latest_block_number()
        )
        self.asset = asset
        self.indexSource = "ipor-oracle-scrapper-aave"
        self.borrowRate = maths.to_percent(maths.to_decimal(RAY_UNIT, reserve_data[6]))
        self.supplyRate = maths.to_percent(maths.to_decimal(RAY_UNIT, reserve_data[4]))
        self.totalBorrowsUT = maths.to_decimal(decimal_currency, (reserve_data[2] + reserve_data[3]))
        self.totalSupplyUT = maths.to_decimal(
            decimal_currency,
            connection_manager.get_total_supply(asset, block_number)
        )
        self.utilizationRate = maths.to_percent(
            maths.to_decimal(decimal_currency, reserve_data[8])
        )
        self.availableLiquidityRaw = reserve_data[1]
        self.totalStableDebtRaw = reserve_data[2]
        self.totalVariableDebtRaw = reserve_data[3]
        self.liquidityRateRaw = reserve_data[4]
        self.variableBorrowRateRaw = reserve_data[5]
        self.stableBorrowRateRaw = reserve_data[6]
        self.averageStableBorrowRateRaw = reserve_data[7]
        self.liquidityIndexRaw = reserve_data[9]
        self.variableBorrowIndexRaw = reserve_data[10]
        self.lastUpdateTimestamp = reserve_data[12]
        self.totalSupplyRaw = connection_manager.get_total_supply(asset, block_number)
        self.stableBorrowRate = maths.to_percent(maths.to_decimal(RAY_UNIT, reserve_data[6]))
        self.availableLiquidity = maths.to_decimal(decimal_currency, reserve_data[1])
        self.totalStableDebt = maths.to_decimal(decimal_currency, reserve_data[2])
        self.totalVariableDebt = maths.to_decimal(decimal_currency, reserve_data[3])
        self.averageStableBorrowRate = maths.to_percent(
            maths.to_decimal(decimal_currency, reserve_data[7])
        )
        self.liquidityIndex = maths.to_decimal(decimal_currency, reserve_data[9])
        self.variableBorrowIndex = maths.to_decimal(decimal_currency, reserve_data[10])
