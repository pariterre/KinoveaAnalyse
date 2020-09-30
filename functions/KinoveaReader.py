import os
from datetime import datetime

import xml.etree.ElementTree as ElementTree
import numpy as np
from scipy.interpolate import interp1d


# Read the XML file
def read_xml_file(xml_path, reperes_anato):
    # Note to the programmer
    # The structure given by the XML file in Kinovea is a 5 level where
    #   the 1st iterate on structure (3 is the actual Worksheet)
    #   the 3rd iterate on lines
    #   the 4th iterate on columns
    ws = 3  # worksheet
    tree = ElementTree.parse(xml_path)
    root = tree.getroot()[ws][0]  # We don't mind the first 2 columns of root
    data = {}
    data_to_stack = np.ndarray((3, 1))  # Declare data stacker that keeps being updated (Time, X, Y)
    for repere in reperes_anato:
        repere_found = False
        data_tp = np.ndarray((3, 0))  # Append all data
        # Find the data for each reperes
        for i in range(len(root)):
            # If we haven't reach the repere so far
            if not repere_found:
                if root[i][0][0].text is not None and len(root[i]) > 1 and root[i][1][0].text == repere:
                    repere_found = True
            # If we finished the repere
            elif len(root) <= i+2 or root[i+2][0][0].text is None:
                break
            # Otherwise add data
            else:
                if os.name == 'nt':
                    # Windows, timestamp fails if year is inferior of 1971
                    d = datetime.strptime(root[i + 2][2][0].text, "%H:%M:%S:%f")
                    data_to_stack[0, 0] = \
                        datetime.timestamp(datetime(1971, 1, 1, d.hour, d.minute, d.second, d.microsecond)) \
                        - datetime.timestamp(datetime(1971, 1, 1))
                else:
                    data_to_stack[0, 0] = datetime.timestamp(
                        datetime.strptime(root[i+2][2][0].text, "%H:%M:%S:%f")
                    )
                data_to_stack[1, 0] = root[i+2][0][0].text
                data_to_stack[2, 0] = root[i+2][1][0].text
                data_tp = np.hstack((data_tp, data_to_stack))

        # If we get here and haven't found the repere, raise an error
        if not repere_found:
            raise LookupError(repere + " n'a pas été trouvé dans le document")
        data[repere] = data_tp  # Save the data

    # Filter the data (this also align time stamps)
    # Find the most probable dt
    dt = np.ndarray((0,))
    for _, d in data.items():
        dt = np.concatenate((dt, d[0, 1:] - d[0, :-1]))
    dt = np.around(np.median(dt), 3)

    # Find what is the first and last time stamp
    first_frame, last_frame = -np.inf, np.inf
    for _, d in data.items():
        first_frame = np.max((first_frame, d[0, 0]))
        last_frame = np.min((last_frame, d[0, -1]))
    shared_time = np.arange(first_frame, last_frame, dt)

    # Interpolate
    for k, d in data.items():
        _, idx = np.unique(d[0, :], return_index=True)
        data[k] = interp1d(d[0, idx], d[1:3, idx], kind='cubic')(shared_time) * 0.01  # From cm to m

    # Return data
    time = shared_time - shared_time[0]
    return data, time


def convert_to3d(data):
    n_frame = data[list(data.keys())[0]].shape[1]
    new_data = np.ndarray((2, len(data), n_frame))
    for i, m in enumerate(data.values()):
        new_data[:, i, :] = m
    return new_data


def dispatch_dict(data):
    new_data = np.ndarray((data[list(data.keys())[0]].shape[0], len(data), data[list(data.keys())[0]].shape[2]))
    for i, m in enumerate(data.values()):
        new_data[:, i, :] = m[:, 0, :]
    return new_data


def to_degree(data):
    return data * 180/np.pi
