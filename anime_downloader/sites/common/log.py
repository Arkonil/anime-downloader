from .const import COLORS


class console:
    level = 0

    @classmethod
    def log(cls, msg, verbose=True):
        if verbose and cls.level < 1:
            print(f"{COLORS.WHITE}{msg}{COLORS.RESET}")

    @classmethod
    def info(cls, msg, verbose=True):
        if verbose and cls.level < 2:
            print(f"{COLORS.GREEN}{msg}{COLORS.RESET}")


    @classmethod
    def warning(cls, msg, verbose=True):
        if verbose and cls.level < 3:
            print(f"{COLORS.YELLOW}{msg}{COLORS.RESET}")

    @classmethod
    def error(cls, msg, verbose=True):
        if verbose and cls.level < 4:
            print(f"{COLORS.RED}{msg}{COLORS.RESET}")


if __name__ == '__main__':
    console.log("log")
    console.info("info")
    console.warning("warning")
    console.error("Error")

    console.level = 1
    console.log("log")
    console.info("info")
    console.warning("warning")
    console.error("Error")

    console.level = 2
    console.log("log")
    console.info("info")
    console.warning("warning")
    console.error("Error")

    console.level = 3
    console.log("log")
    console.info("info")
    console.warning("warning")
    console.error("Error")