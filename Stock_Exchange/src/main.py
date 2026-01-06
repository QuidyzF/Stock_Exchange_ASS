from src.exchange import Exchange
from src.parser import Parser

def main():
    core = Exchange()
    parser = Parser(core)
    parser.run()

if __name__ == "__main__":
    main()