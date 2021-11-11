import os

class GIFCreator:
  def __init__(self, options):
    self.background_color = options['background_color'].get_value()
    self.duration_frame = options['duration_frame'].get_value()
    self.edge_color = options['edge_color'].get_value()
    self.elevation = options['elevation'].get_value()
    self.frames = options['frames'].get_value()
    self.init_angle = options['init_angle'].get_value()
    self.line_width = options['line_width'].get_value()
    self.model_color = options['model_color'].get_value()
    self.outputfile = options['outputfile'].get_value()
    self.path = options['path'].get_value()

  def __createFrames(self, mesh_handler):
    """
    Creates frames for the gif
    """
    from mpl_toolkits import mplot3d
    import matplotlib.pyplot as plt
    import shutil

    # Create a new plot
    figure = plt.figure()
    axes = mplot3d.Axes3D(figure)

    # Set the background color
    figure.patch.set_facecolor(self.background_color)
    axes.patch.set_facecolor(self.background_color)

    # Add STL vectors to the plot
    vectors = mesh_handler.get_vectors()
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(vectors,color=self.model_color))
    axes.add_collection3d(mplot3d.art3d.Line3DCollection(vectors,color=self.edge_color,linewidth=self.line_width))
    axes.view_init(elev=35.0, azim=-45)

    # Auto scale to the mesh size
    scale = mesh_handler.get_flattened_points()
    axes.auto_scale_xyz(scale, scale, scale)

    # Deactivate Axes
    plt.axis('off')

    # Delete folder containing frames from previous runs
    if os.path.exists(self.path):
        shutil.rmtree(self.path)

    # Create a folder to contain the frames
    try: 
        os.makedirs(self.path)
    except OSError:
        if not os.path.isdir(self.path):
            raise

    for i in range(self.frames):
        # Rotate the view
        axes.view_init(elev=self.elevation, azim=self.init_angle + 360/self.frames*i)
    
        # Save frame
        frame_i = "frame_" + str(i) + ".png"
        print("Saved frames: " + str(i+1) + "/" + str(self.frames))
        plt.savefig(os.path.join(self.path, frame_i))

  def __createGif(self):
    """
    Creates a gif from the frames
    """
    import imageio, re

    images = []
    files = os.listdir(self.path)
    ordered_files = sorted(files, key=lambda x: (int(re.sub('\D','',x)),x))
    for file_name in ordered_files:
        if file_name.endswith('.png'):
            file_path = os.path.join(self.path, file_name)
            images.append(imageio.imread(file_path))
    imageio.mimsave(self.outputfile, images, duration = self.duration_frame)

  def create(self, mesh_handler):
    print("Creating frames")
    self.__createFrames(mesh_handler)

    print("Creating GIF")
    self.__createGif()