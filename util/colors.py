from settings import DEBUG
from binance.enums import SIDE_BUY, SIDE_SELL

# Adapted from Blender source code
class Colors:
    RED = ERROR = "\u001b[31m"
    GREEN = FILLED = "\u001b[32m"
    YELLOW = PLACED = "\u001b[33m"
    BLUE = THRESHOLD = "\u001b[34m"
    MAGENTA = SELL = "\u001b[35m"
    CYAN = BUY = "\u001b[36m"
    WHITE = "\u001b[37m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = INFO = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

    def warn(input: str) -> str:
        return Colors.WARNING + input + Colors.END

    def info(input: str) -> str:
        return Colors.INFO + input + Colors.END

    def fail(input: str) -> str:
        return Colors.FAIL + input + Colors.END
    def buy(input: str) -> str:
        return Colors.BUY + input + Colors.END
    def sell(input: str) -> str:
        return Colors.SELL + input + Colors.END

class phrases:
    PLACED = Colors.PLACED + "PLACED " + Colors.END
    FILLED = Colors.FILLED + "FILLED " + Colors.END
    BUY = Colors.BUY + "BUY " + Colors.END
    SELL = Colors.SELL + "SELL " + Colors.END
    ERROR = Colors.ERROR + "ERROR " + Colors.END
    WARNING = Colors.WARNING + "WARNING " + Colors.END
    THRESHOLD = Colors.THRESHOLD + "THRESHOLD " + Colors.END

    def debug() -> str:
        return (Colors.WARNING + "(test) " + Colors.END) if DEBUG else ""

    def buyOrSell(side: SIDE_BUY or SIDE_SELL) -> str:
        return (phrases.BUY if side == SIDE_BUY else phrases.SELL) + phrases.debug()

    def filledOrPlaced(filled: bool):
        return phrases.FILLED if filled else phrases.PLACED
    def thresholdPricedOrNot(cancelThreshold: bool):
        return phrases.THRESHOLD + str(cancelThreshold) if not cancelThreshold == None else "(no threshold)"
    def cancelled(cancelled: bool):
        return Colors.fail("CANCELLED ") if cancelled else ""