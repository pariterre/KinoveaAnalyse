# Ce script analyse des données de position fournies par le logiciel Kinovea (export XML)
# Pour l'utiliser, assurez-vous que les labels utilisés dans Kinovea correspondent à ceux
# inscrits dans la variable "reperes_anato" du présent logiciel
# Le script retourne les graphiques de centre de masse, ainsi que les angles entre les segments
import numpy as np
import matplotlib.pyplot as plt

from functions import KinoveaReader, BiomechanicsComputation, GUI, MainFigure

use_Qt_gui = True

if use_Qt_gui:
    masse, xml_path, model_name = GUI.get_info()
else:
    masse = 70  # kg
    xml_path = "example/box_jump.xml"
    model_name = "sagittal"

# Load the model
models = __import__("models." + model_name)
reperes_anato, stick, angle_seg, winter_table = getattr(models, model_name).model()

# Get the data
(data, time) = KinoveaReader.read_xml_file(xml_path, reperes_anato)

# Compute position of com and com_i
com_i = KinoveaReader.dispatch_dict(
    BiomechanicsComputation.compute_com_i(data, winter_table)
)
com = BiomechanicsComputation.compute_com(data, winter_table)

# Compute angle between segment
angles = BiomechanicsComputation.compute_angles(data, angle_seg)

# Convert data into 3d data so they are easy to print
data = KinoveaReader.convert_to3d(data)

# Derivative of com and com_i to get velocity and accelerations
com_dot = BiomechanicsComputation.derivative(com, time)
com_ddot = BiomechanicsComputation.derivative(com_dot, time)
com_i_dot = BiomechanicsComputation.derivative(com_i, time)
com_i_ddot = BiomechanicsComputation.derivative(com_i_dot, time)

# Compute GRF
grf = BiomechanicsComputation.compute_grf(com_ddot, masse)

# Output
MainFigure.show(time, data, com, com_dot, com_ddot, com_i, grf, angles, stick)
