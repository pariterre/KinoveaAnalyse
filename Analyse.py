# Ce script analyse des données de position fournies par le logiciel Kinovea
# Pour l'utiliser, assurez-vous que les labels utilisés dans Kinovea correspondent à ceux
# inscrits dans la variable "reperes_anato" du présent logiciel
# Le script retourne les graphiques de centre de masse, ainsi que les angles entre les segments
import KinoveaReader
import BiomechanicsComputation
import matplotlib.pyplot as plt

time_idx = 0
masse = 70  # kg
show_model_position = False
show_com_height_over_time = False
show_com_upward_velocity = False
show_com_upward_acceleration = False
show_grf_forces = False
show_joint_angles = True


xml_path = "/home/pariterre/ownCloud/Documents/Enseignement/KIN2024/2018/cours9/media/" \
           "PropositionEtudiants/BoxJump.xml"
reperes_anato = ("Hanche", "Genou", "Malleole", "Pied", "Epaule", "Coude", "Main", "Tete")
angle_seg = {
    # Articulation  # dist          # prox      # center
    "Cheville":     ("Pied",        "Genou",    "Malleole"),
    "Genou":        ("Malleole",    "Hanche",   "Genou"),
    "Hanche":       ("Genou",       "Epaule",   "Hanche"),
    "Epaule":       ("Hanche",      "Coude",    "Epaule"),
    "Coude":        ("Epaule",      "Main",     "Coude")
}
stick = [3, 2, 1, 0, 4, 7, 4, 5, 6]
winter_table_lateral = {
    # Membre:   Seg_prox,    Seg_dist,   Masse,  CM_Prox, CM_Dist,  nb_seg
    "TT":       ("Epaule",   "Hanche",   0.578,  0.66,    0.34,     1),
    "Bras":     ("Epaule",   "Coude",    0.028,  0.436,   0.564,    2),
    "AvBras":   ("Coude",    "Main",     0.016,  0.43,    0.57,     2),
    "Cuisse":   ("Hanche",   "Genou",    0.1,    0.433,   0.567,    2),
    "Jambe":    ("Genou",    "Malleole", 0.0465, 0.433,   0.567,    2),
    "Pied":     ("Malleole", "Pied",     0.0145, 0.5,     0.5,      2)
}

# Get the data
(data, time) = KinoveaReader.read_xml_file(xml_path, reperes_anato)

# Compute position of com and com_i
com_i = KinoveaReader.dispatch_dict(
    BiomechanicsComputation.compute_com_i(data, winter_table_lateral)
)
com = BiomechanicsComputation.compute_com(data, winter_table_lateral)

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
