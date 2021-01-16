from settings import DEBUG

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

class phrases:
    PLACED = colors.PLACED + "PLACED " + colors.END
    FILLED = colors.FILLED + "FILLED " + colors.END
    BUY = colors.BUY + "BUY " + colors.END
    SELL = colors.SELL + "SELL " + colors.END
    ERROR = colors.ERROR + "ERROR " + colors.END
    WARNING = colors.WARNING + "WARNING " + colors.END
    DEBUG = "(test) " if DEBUG else ""