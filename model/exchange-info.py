class ExchangeInformation():
    def ___init___(self):
        self.baseAsset: str = None
        self.baseAssetPrecision: int = None
        self.quoteAsset: str = None
        self.quoteAssetPrecision: int = None
        self.filters: list = []
        self.minPrice: float = 0
        self.maxPrice: float = 0
        self.tickSize: float = 0
        self.stepSize: float = 0