import sys
from src.optional_arguments import get_optional_arguments
from src.GIFCreator import GIFCreator
from src.STLHandler import STLHandler

def main(argv):
  options = get_optional_arguments(argv)
  stl_handler = STLHandler(options)
  gif_creator = GIFCreator(options)
  gif_creator.create(stl_handler)
  print("Done!")

if __name__ == "__main__":
  print("Started")
  main(sys.argv[1:])
