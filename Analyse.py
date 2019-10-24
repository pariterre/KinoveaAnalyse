# Ce script analyse des données de position fournies par le logiciel Kinovea (export XML)
# Pour l'utiliser, assurez-vous que les labels utilisés dans Kinovea correspondent à ceux
# inscrits dans la variable "reperes_anato" du présent logiciel
# Le script retourne les graphiques de centre de masse, ainsi que les angles entre les segments
import numpy as np
import matplotlib.pyplot as plt

from functions import KinoveaReader
from functions import BiomechanicsComputation
from functions import GUI

ask_info_by_popup = True

if ask_info_by_popup:
    masse, time_idx, xml_path, model_name = GUI.get_info()
else:
    time_idx = 0
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

# Kinogramme
plt.figure("Kinogramme du mouvement")
plt.ylabel("Axe vertical (m)")
plt.xlabel("Axe frontal (m)")
couleurs = np.linspace(0.88, 0, data.shape[2])
for i in range(data.shape[2]):
    plt.plot(data[0, stick, i], data[1, stick, i], color=[couleurs[i], couleurs[i], couleurs[i]])
plt.axis('equal')

# Output
plt.figure("Analyse biomécanique de Kinovea")

# Show model
plt.subplot(131)
plt.title("Position du corps à l'instant " + str(time_idx))
plt.ylabel("Axe vertical (m)")
plt.xlabel("Axe frontal (m)")
plt.plot(data[0, stick, time_idx], data[1, stick, time_idx], 'r')
plt.plot(com_i[0, :, time_idx], com_i[1, :, time_idx], 'k.')
plt.plot(com[0, 0, time_idx], com[1, 0, time_idx], 'k.', markersize=20)
plt.axis('equal')

# Show some calculation
plt.subplot(432)
plt.title("Hauteur du CoM")
plt.ylabel("Hauteur (m)")
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.plot(time, com[1, 0, :])

plt.subplot(435)
plt.title("Vitesse verticale")
plt.ylabel("Vitesse (m/s)")
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.plot(time, com_dot[1, 0, :])

plt.subplot(438)
plt.title("Accélération verticale")
plt.ylabel("Accélération (m/s²)")
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.plot(time, com_ddot[1, 0, :])

plt.subplot(4, 3, 11)
plt.title("GRF")
plt.ylabel("GRF (N)")
plt.xlabel("Temps (s)")
plt.plot(time, grf[1, 0, :])

plt.subplot(1, 3, 3)
plt.title("Angles articulaire au cours du temps")
plt.ylabel("Angle (°)")
plt.xlabel("Temps (s)")
for joint in angles.values():
    plt.plot(time, KinoveaReader.to_degree(joint))
plt.legend(angles.keys())

plt.show()
print("Fin du script")