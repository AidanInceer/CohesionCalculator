from src.core.directory_parser import DirectoryParser

if __name__ == "__main__":
    path = "./data/"
    directory_parser = DirectoryParser(path)
    directory_parser.parse_directory()
