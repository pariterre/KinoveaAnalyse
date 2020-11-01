import sys

import numpy as np
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from . import KinoveaReader


def show(time, data, com, com_dot, com_ddot, com_i, grf, angles, stick):
    qapp = QtWidgets.QApplication(sys.argv)
    app = QtWidgets.QMainWindow()
    app.setWindowTitle("Analyse biomécanique de Kinovea")

    _main = QtWidgets.QWidget()
    app.setCentralWidget(_main)
    main_layout = QtWidgets.QHBoxLayout(_main)

    # Body position column
    body_position_widget = QtWidgets.QWidget()
    main_layout.addWidget(body_position_widget)
    body_position_layout = QtWidgets.QVBoxLayout(body_position_widget)

    # Show model
    body_position_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    body_position_layout.addWidget(body_position_canvas)
    body_position_ax = body_position_canvas.figure.subplots()

    time_idx = 0
    body_position_ax.set_title(f"Position du corps à l'instant {time[time_idx]:.2f} s")
    body_position_ax.set_ylabel("Axe vertical (m)")
    body_position_ax.set_xlabel("Axe frontal (m)")
    body_position_ax.axis('equal')
    body_position_ax.set_xlim(np.min(data[0, :, :]), np.max(data[0, :, :]))
    body_position_ax.set_ylim(np.min(data[1, :, :]) - (np.max(data[1, :, :]) - np.min(data[1, :, :]))*0.1 ,
                              np.max(data[1, :, :]) + (np.max(data[1, :, :]) - np.min(data[1, :, :]))*0.1 )
    body_position_text = body_position_ax.text(
        0.5, 0.99,
        f"CoM = [{str(np.round(com[0, 0, time_idx], 2))}; {str(np.round(com[1, 0, time_idx], 2))}]",
        fontsize=12,
        horizontalalignment='center',
        verticalalignment='top',
        transform=body_position_ax.transAxes
    )

    stick_plot = body_position_ax.plot(data[0, stick, time_idx], data[1, stick, time_idx], 'r')
    comi_plot = body_position_ax.plot(com_i[0, :, time_idx], com_i[1, :, time_idx], 'k.')
    com_plot = body_position_ax.plot(com[0, 0, time_idx], com[1, 0, time_idx], 'k.', markersize=20)

    def move_stick_figure(time_idx):
        body_position_ax.set_title(f"Position du corps à l'instant {time[time_idx]:.2f} s")

        body_position_text.set_text(f"CoM = [{str(np.round(com[0, 0, time_idx], 2))}; {str(np.round(com[1, 0, time_idx], 2))}]")

        stick_plot[0].set_data(data[0, stick, time_idx], data[1, stick, time_idx])
        comi_plot[0].set_data(com_i[0, :, time_idx], com_i[1, :, time_idx])
        com_plot[0].set_data(com[0, 0, time_idx], com[1, 0, time_idx])

    time_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    body_position_layout.addWidget(time_slider)

    # Trajectory column
    trajectory_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    main_layout.addWidget(trajectory_canvas)
    buffer = (time[-1]-time[0])*0.005
    xlim = (time[0]-buffer, time[-1]+buffer)

    ax_height = trajectory_canvas.figure.add_subplot(411)
    ax_height.set_title("Hauteur du CoM")
    ax_height.set_ylabel("Hauteur (m)")
    ax_height.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax_height.plot(time, com[1, 0, :])
    ylim = ax_height.get_ylim()
    height_vbar = ax_height.plot((time[time_idx], time[time_idx]), ylim, 'r')
    ax_height.set_xlim(xlim)
    ax_height.set_ylim(ylim)

    ax_velocity = trajectory_canvas.figure.add_subplot(412)
    ax_velocity.set_title("Vitesse verticale")
    ax_velocity.set_ylabel("Vitesse (m/s)")
    ax_velocity.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax_velocity.plot(time, com_dot[1, 0, :])
    ylim = ax_velocity.get_ylim()
    velocity_vbar = ax_velocity.plot((time[time_idx], time[time_idx]), ylim, 'r')
    ax_velocity.set_xlim(xlim)
    ax_velocity.set_ylim(ylim)

    ax_acceleration = trajectory_canvas.figure.add_subplot(413)
    ax_acceleration.set_title("Accélération verticale")
    ax_acceleration.set_ylabel("Accélération (m/s²)")
    ax_acceleration.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax_acceleration.plot(time, com_ddot[1, 0, :])
    ylim = ax_acceleration.get_ylim()
    acceleration_vbar = ax_acceleration.plot((time[time_idx], time[time_idx]), ylim, 'r')
    ax_acceleration.set_xlim(xlim)
    ax_acceleration.set_ylim(ylim)

    ax_grf = trajectory_canvas.figure.add_subplot(414)
    ax_grf.set_title("GRF")
    ax_grf.set_ylabel("GRF (N)")
    ax_grf.set_xlabel("Temps (s)")
    ax_grf.plot(time, grf[1, 0, :])
    ylim = ax_grf.get_ylim()
    grf_vbar = ax_grf.plot((time[time_idx], time[time_idx]), ylim, 'r')
    ax_grf.set_xlim(xlim)
    ax_grf.set_ylim(ylim)

    trajectory_canvas.figure.tight_layout(h_pad=-0.5, w_pad=-6)

    # Angles column
    angles_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    main_layout.addWidget(angles_canvas)
    ax_angles = angles_canvas.figure.subplots()
    ax_angles.set_title("Angles articulaire au cours du temps")
    ax_angles.set_ylabel("Angle (°)")
    ax_angles.set_xlabel("Temps (s)")
    for joint in angles.values():
        ax_angles.plot(time, KinoveaReader.to_degree(joint))
    ylim = ax_angles.get_ylim()
    angles_vbar = ax_angles.plot((time[time_idx], time[time_idx]), ylim, 'r')
    ax_angles.set_xlim(xlim)
    ax_angles.set_ylim(ylim)
    ax_angles.legend(angles.keys())

    def change_time():
        time_idx = time_slider.value()

        move_stick_figure(time_idx)
        body_position_canvas.draw()

        height_vbar[0].set_xdata([time[time_idx], time[time_idx]])
        velocity_vbar[0].set_xdata([time[time_idx], time[time_idx]])
        acceleration_vbar[0].set_xdata([time[time_idx], time[time_idx]])
        grf_vbar[0].set_xdata([time[time_idx], time[time_idx]])
        trajectory_canvas.draw()

        angles_vbar[0].set_xdata([time[time_idx], time[time_idx]])
        angles_canvas.draw()

    time_slider.setMinimum(0)
    time_slider.setMaximum(time.shape[0] - 1)
    time_slider.setPageStep(1)
    time_slider.setValue(0)
    time_slider.valueChanged.connect(change_time)
    body_position_canvas.mpl_connect(body_position_canvas.resize_event, change_time)

    # app.showMaximized()
    app.show()
    qapp.exec_()
