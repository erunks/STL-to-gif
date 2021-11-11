class STLHandler:
  def __init__(self, options):
    """
    Loads an STL file and returns a mesh object.
    """
    from stl import mesh

    filepath = options['inputfile'].get_value()

    self.mesh = mesh.Mesh.from_file(filepath)
    self.rotation_angle = options['rotation_angle'].get_value()
    self.rotation_axes = options['rotation_axes'].get_value()
    self.offset = options['offset'].get_value()

    self.__rotate_stl()
    self.__center_stl()
    print("STL: %s, loaded!" % filepath)

  def __center_stl(self):
    """
    Centers an STL mesh.
    """
    # Get the min and max coordinates of the mesh.
    x_min = self.mesh.vectors[:,:,0].min()
    x_max = self.mesh.vectors[:,:,0].max()
    y_min = self.mesh.vectors[:,:,1].min()
    y_max = self.mesh.vectors[:,:,1].max()
    z_min = self.mesh.vectors[:,:,2].min()
    z_max = self.mesh.vectors[:,:,2].max() 

    # Average the min and max values.
    x_center_offset = (x_max + x_min)/2.0
    y_center_offset = (y_max + y_min)/2.0
    z_center_offset = (z_max + z_min)/2.0

    # Center the mesh.
    self.mesh.vectors[:,:,0] = self.mesh.vectors[:,:,0] - x_center_offset - self.offset[0]
    self.mesh.vectors[:,:,1] = self.mesh.vectors[:,:,1] - y_center_offset - self.offset[1]
    self.mesh.vectors[:,:,2] = self.mesh.vectors[:,:,2] - z_center_offset - self.offset[2]

    return self.mesh

  def __rotate_stl(self):
    import math
    """
    Rotates an STL mesh by an angle.
    """
    return self.mesh.rotate(self.rotation_axes, math.radians(self.rotation_angle))

  def get_flattened_points(self):
    """
    Returns the flattened points of an STL mesh.
    """
    return self.mesh.points.flatten()

  def get_vectors(self):
    """
    Returns the vectors of an STL mesh.
    """
    return self.mesh.vectors
