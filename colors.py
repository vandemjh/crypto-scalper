from settings import DEBUG
from binance.enums import SIDE_BUY, SIDE_SELL

# Adapted from Blender source code
class colors:
    RED = ERROR = "\u001b[31m"
    GREEN = FILLED = "\u001b[32m"
    YELLOW = PLACED = "\u001b[33m"
    BLUE = "\u001b[34m"
    MAGENTA = SELL = "\u001b[35m"
    CYAN = BUY = "\u001b[36m"
    WHITE = "\u001b[37m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = INFO = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

    def warn(input: str) -> str:
        return colors.WARNING + input + colors.END

    def info(input: str) -> str:
        return colors.INFO + input + colors.END

    def fail(input: str) -> str:
        return colors.FAIL + input + colors.END


class phrases:
    PLACED = colors.PLACED + "PLACED " + colors.END
    FILLED = colors.FILLED + "FILLED " + colors.END
    BUY = colors.BUY + "BUY " + colors.END
    SELL = colors.SELL + "SELL " + colors.END
    ERROR = colors.ERROR + "ERROR " + colors.END
    WARNING = colors.WARNING + "WARNING " + colors.END

    def debug() -> str:
        return (colors.WARNING + "(test) " + colors.END) if DEBUG else ""

    def buyOrSell(side: SIDE_BUY or SIDE_SELL) -> str:
        return (phrases.BUY if side == SIDE_BUY else phrases.SELL) + phrases.debug()

    def filledOrPlaced(filled: bool):
        return phrases.FILLED if filled else phrases.PLACED