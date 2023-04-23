import sys

import numpy as np
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
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
    body_position_layout = QtWidgets.QVBoxLayout()
    main_layout.addLayout(body_position_layout)

    # Show model
    body_position_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    body_position_layout.addWidget(body_position_canvas)
    body_position_ax = body_position_canvas.figure.subplots()

    time_idx = 0
    body_position_ax.set_ylabel("Axe vertical (m)")
    body_position_ax.set_xlabel("Axe frontal (m)")
    body_position_text = body_position_ax.text(
        0.5, 0.99, "", fontsize=12, horizontalalignment='center', verticalalignment='top', transform=body_position_ax.transAxes
    )

    kino_n_image = 5
    kino_pre_plot = []
    kino_post_plot = []
    kino_colors = np.linspace(0.88, 0, kino_n_image)
    for i in range(kino_n_image):
        i2 = kino_n_image - 1 - i
        kino_pre_plot.append(
            body_position_ax.plot(np.nan, np.nan, color=[kino_colors[i2], kino_colors[i2], kino_colors[i2]])
        )
        kino_post_plot.append(
            body_position_ax.plot(np.nan, np.nan, color=[kino_colors[i2], kino_colors[i2], kino_colors[i2]])
        )

    stick_plot = body_position_ax.plot(np.nan, np.nan, 'r')
    comi_plot = body_position_ax.plot(np.nan, np.nan, 'k.')
    com_plot = body_position_ax.plot(np.nan, np.nan, 'k.', markersize=20)

    def move_stick_figure(time_idx):
        body_position_ax.set_title(f"Position du corps à l'instant {time[time_idx]:.2f} s")

        body_position_text.set_text(f"CoM = [{str(np.round(com[0, 0, time_idx], 2))}; {str(np.round(com[1, 0, time_idx], 2))}]")

        for i in range(kino_n_image):
            if time_idx - i - 1 >= 0 and kino_pre_check.isChecked():
                kino_pre_plot[i][0].set_data(data[0, stick, time_idx - i - 1], data[1, stick, time_idx - i - 1])
            else:
                kino_pre_plot[i][0].set_data(np.nan, np.nan)
            if time_idx + i + 1 < data.shape[2] and kino_post_check.isChecked():
                kino_post_plot[i][0].set_data(data[0, stick, time_idx + i + 1], data[1, stick, time_idx + i + 1])
            else:
                kino_post_plot[i][0].set_data(np.nan, np.nan)

        stick_plot[0].set_data(data[0, stick, time_idx], data[1, stick, time_idx])
        comi_plot[0].set_data(com_i[0, :, time_idx], com_i[1, :, time_idx])
        com_plot[0].set_data(com[0, 0, time_idx], com[1, 0, time_idx])

    # Force axis equal with min and max data
    body_position_ax.plot(
        [np.min(data[0, :, :]), np.max(data[0, :, :])],
        [np.min(data[1, :, :]) - (np.max(data[1, :, :]) - np.min(data[1, :, :]))*0.1 ,
                              np.max(data[1, :, :]) + (np.max(data[1, :, :]) - np.min(data[1, :, :]))*0.1 ], 'w.'
    )
    body_position_ax.axis('equal')

    time_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    body_position_layout.addWidget(time_slider)

    kinogram_layout = QtWidgets.QHBoxLayout()
    body_position_layout.addLayout(kinogram_layout)
    kino_pre_check = QtWidgets.QCheckBox()
    kino_pre_check.setText("Kinogramme pre")
    kinogram_layout.addWidget(kino_pre_check)
    kino_post_check = QtWidgets.QCheckBox()
    kino_post_check.setText("Kinogramme post")
    kinogram_layout.addWidget(kino_post_check)

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
    height_vbar = ax_height.plot((np.nan, np.nan), ylim, 'r')
    ax_height.set_xlim(xlim)
    ax_height.set_ylim(ylim)

    ax_velocity = trajectory_canvas.figure.add_subplot(412)
    ax_velocity.set_title("Vitesse verticale")
    ax_velocity.set_ylabel("Vitesse (m/s)")
    ax_velocity.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax_velocity.plot(time, com_dot[1, 0, :])
    ylim = ax_velocity.get_ylim()
    velocity_vbar = ax_velocity.plot((np.nan, np.nan), ylim, 'r')
    ax_velocity.set_xlim(xlim)
    ax_velocity.set_ylim(ylim)

    ax_acceleration = trajectory_canvas.figure.add_subplot(413)
    ax_acceleration.set_title("Accélération verticale")
    ax_acceleration.set_ylabel("Accélération (m/s²)")
    ax_acceleration.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax_acceleration.plot(time, com_ddot[1, 0, :])
    ylim = ax_acceleration.get_ylim()
    acceleration_vbar = ax_acceleration.plot((np.nan, np.nan), ylim, 'r')
    ax_acceleration.set_xlim(xlim)
    ax_acceleration.set_ylim(ylim)

    ax_grf = trajectory_canvas.figure.add_subplot(414)
    ax_grf.set_title("GRF")
    ax_grf.set_ylabel("GRF (N)")
    ax_grf.set_xlabel("Temps (s)")
    ax_grf.plot(time, grf[1, 0, :])
    ylim = ax_grf.get_ylim()
    grf_vbar = ax_grf.plot((np.nan, np.nan), ylim, 'r')
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
    angles_vbar = ax_angles.plot((np.nan, np.nan), ylim, 'r')
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
    # body_position_canvas.mpl_connect(body_position_canvas.resize_event, change_time)
    kino_pre_check.stateChanged.connect(change_time)
    kino_post_check.stateChanged.connect(change_time)

    # app.showMaximized()
    change_time()
    app.show()
    qapp.exec_()
