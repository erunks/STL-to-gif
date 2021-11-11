import os, sys
from src.OptionalArgument import OptionalArgument

options = {
  'duration_frame' : {
    'short': 't',
    'long': 'duration',
    'default': 0.1,
    'description': 'Duration (in seconds) of display of each frame'
  },
  'frames' : {
    'short': 'n',
    'long': 'nframes',
    'default': 25,
    'description': 'Amount of frames to generate'
  },
  'init_angle' : {
    'short': 'a',
    'long': 'initangle',
    'default': 0,
    'description': 'Starting angle of the first frame'
  },
  'inputfile' : {
    'short': 'i',
    'long': 'ifile',
    'default': '',
    'description': 'Input the file to be get the frames for the gif'
  },
  'line_width' : {
    'short': 'l',
    'long': 'line_width',
    'default': 0.05,
    'description': 'Line width of the STL'
  },
  'outputfile' : {
    'short': 'o',
    'long': 'ofile',
    'default': 'output.gif',
    'description': 'Output filename of the gif'
  },
  'background_color' : {
    'short': 'b',
    'long': 'background_color',
    'default': '#f6f6f9',
    'description': 'Background color of the gif'
  },
  'elevation' : {
    'short': 'e',
    'long': 'elevation',
    'default': 10,
    'description': 'Elevation of the STL'
  },
  'path' : {
    'short': 'p',
    'long': 'path',
    'default': os.path.join(os.getcwd(), "frames"),
    'description': 'Folder in where the frames will be saved. If it doesn\'t exist, it will be created automatically'
  },
  'rotation_angle' : {
    'short': 'd',
    'long': 'rotation_angle',
    'default': 0,
    'description': 'Degrees to rotate the STL'
  },
  'rotation_axes' : {
    'short': 'r',
    'long': 'rotation_axis',
    'default': [1.0, 0.0, 0.0],
    'description': 'Specify the rotation axes of the STL'
  },
  'offset' : {
    'short': '',
    'long': 'offset',
    'default': [0, 0, 0],
    'description': 'Displaces the center from which the STL will revolve'
  },
  'model_color': {
    'short': 'c',
    'long': 'model_color',
    'default': '#437bc6',
    'description': 'Color of the STL when we render it'
  },
  'edge_color': {
    'short': '',
    'long': 'edge_color',
    'default': '#00000099',
    'description': 'Color of the edges on the STL when we render it'
  }
}

def get_short_ops():
  return ':'.join([option['short'] for option in options.values()])

def get_long_ops():
  return [("%s=" % option['long']) for option in options.values()]

def getList(strlist,separator=","):
  try:
    return list(map(float,strlist.split(separator)))
  except:
    print("Error: Input the values only separated by a comma (,) . I.e: 1,0,0")
    sys.exit(2)

def print_help():
  print("Usage: %s [options] <inputfile>" % os.path.basename(__file__))
  print("Options:")
  for option in options.keys():
    if options[option]['short']:
      print("  -%s, --%s=%s\n\t%s\n" % (options[option]['short'], options[option]['long'], options[option]['default'], options[option]['description']))
    else:
      print("  --%s=%s\n\t%s\n" % (options[option]['long'], options[option]['default'], options[option]['description']))

def get_optional_arguments(argv):
  import getopt

  optional_arguments = {}
  short_opts = "h"+get_short_ops()
  long_opts = ["help"]+get_long_ops()
  try:
    opts, _args = getopt.getopt(argv, short_opts, long_opts)
  except getopt.GetoptError:
    print('Error in args')
    sys.exit(2)

  for opt, arg in opts:
    if opt in ("-h", "--help"):
      print_help()
      sys.exit()
    else:
      for option in options.keys():
        if opt in ("-%s" % options[option]['short'], "--%s" % options[option]['long']):
          if arg:
            if (option == 'frames'):
              options[option]['value'] = max(0, int(arg))
            elif (option in ['background_color', 'edge_color', 'model_color', 'inputfile']):
              options[option]['value'] = arg
            elif (option == 'outputfile'):
              options[option]['value'] = "%s.gif" % arg
            elif (option == 'path'):
              options[option]['value'] = os.path.join(os.getcwd(), arg)
            elif (option == 'rotation_axes' or option == 'offset'):
              options[option]['value'] = getList(arg)
            else:
              options[option]['value'] = max(0.0, float(arg))
          else:
            print("Error: You must specify a value for %s" % option)
            sys.exit(2)
        optional_arguments[option] = OptionalArgument(option, options[option])

  if options['inputfile']['value'] == '':
    print("Error: You must specify an input file")
    sys.exit(2)

  return optional_arguments
