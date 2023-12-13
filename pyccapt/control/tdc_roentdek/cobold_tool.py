import h5py
import numpy as np
import pandas as pd

def copy_xy_from_cobold_txt_to_hdf5(txt_path, save_path):
    """
    Copy x and y data from Cobold text file to an existing HDF5 file.

    Args:
        txt_path (str): Path to the Cobold text file.
        save_path (str): Path to the save file.

    Returns:
        None
    """
    # Read data from text file
    with open(txt_path, 'r') as f:
        data = np.loadtxt(f)

    xx = data[:, 6] / 10
    yy = data[:, 7] / 10

    with h5py.File(save_path, 'r+') as file:
        del file['dld/x']
        del file['dld/y']

        file.create_dataset('dld/x', data=xx)
        file.create_dataset('dld/y', data=yy)

    print('finish')


def cobold_txt_to_hdf5(txt_path, save_path):
    """
    Convert Cobold text data to an HDF5 file.

    Args:
        txt_path (str): Path to the Cobold text file.
        save_path (str): Path to the save file.
    Returns:
        None
    """
    with open(txt_path, 'r') as f:
        data = np.loadtxt(f)

    xx = data[:, 6] / 10
    yy = data[:, 7] / 10
    tof = data[:, 8]

    with h5py.File(save_path, "w") as f:
        f.create_dataset("dld/x", data=xx, dtype='f')
        f.create_dataset("dld/y", data=yy, dtype='f')
        f.create_dataset("dld/t", data=tof, dtype='f')
        f.create_dataset("dld/start_counter", data=np.zeros(len(xx)), dtype='i')
        f.create_dataset("dld/high_voltage", data=np.full(len(xx), 5300), dtype='f')
        f.create_dataset("dld/pulse", data=np.zeros(len(xx)), dtype='f')

    print('finish')


def convert_ND_angle_to_laser_intensity(file_path, ref_laser_intensity, ref_angle):
    with h5py.File(file_path, 'r+') as data:
        laser_intensity = data['dld/pulse'][:]
        OD = (laser_intensity - ref_angle) / 270
        scale = 10 ** OD
        dld_pulse = ref_laser_intensity * scale
        del data['dld/pulse']
        data.create_dataset("dld/pulse", data=dld_pulse, dtype='f')


def rename_a_category(file_path, old_name, new_name):
    with h5py.File(file_path, 'r+') as data:
        temp = data[old_name][:]
        del data[old_name]
        data.create_dataset(new_name, data=temp)


def pulse_energy_calculator_list(ref_angle, ref_laser_intensity, step_pulse_energy, output_file="output.xlsx"):
    # pulse energy = ref_laser_intensity * pulse duration * area
    pulse_ref_energy = ref_laser_intensity * 1e2 * 1e2 * 12e-15 * 4e-6 * 4e-6 * np.pi
    pulse_ref_energy = pulse_ref_energy * 1e12  # pJ
    print(
        f'Pulse energy at {ref_angle}°: {pulse_ref_energy:.2e} pJ , Laser intensity: {ref_laser_intensity:.2e} W/cm^2')

    data = {"Angle (degrees)": [ref_angle], "Pulse Energy (pJ)": [pulse_ref_energy],
            "Laser Intensity (W/cm^2)": [ref_laser_intensity]}

    for i in range(1, 25):
        pulse_energy = 10000 + i * step_pulse_energy
        angle = ref_angle + 270 * np.log10(pulse_energy / pulse_ref_energy)
        angle = round(angle, 2)
        laser_intensity = ref_laser_intensity * (10 ** ((angle - ref_angle) / 270))

        print(f'Pulse energy at {angle:.2f}°: {pulse_energy:.2e} pJ , Laser intensity: {laser_intensity:.2e} W/cm^2')

        # Append data to the dictionary
        data["Angle (degrees)"].append(angle)
        data["Pulse Energy (pJ)"].append(pulse_energy)
        data["Laser Intensity (W/cm^2)"].append(laser_intensity)

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(data)

    # Save DataFrame to Excel file
    df.to_excel(output_file, index=False)
    print(f'Data saved to {output_file}')


def pulse_energy_calculator(ref_angle, ref_laser_intensity, pulse_energy):
    # pulse energy = ref_laser_intensity * pulse duration * area
    pulse_ref_energy = ref_laser_intensity * 1e2 * 1e2 * 12e-15 * 4e-6 * 4e-6 * np.pi
    pulse_ref_energy = pulse_ref_energy * 1e12  # pJ
    angle = ref_angle + 270 * np.log10(pulse_energy / pulse_ref_energy)
    return angle

    # OD = (laser_intensity - ref_angle) / 270
    # scale = 10 ** OD
    # dld_pulse = ref_laser_intensity * scale
    # return dld_pulse

if __name__ == "__main__":
    # txt_path = '../../../tests/data/physics_experiment/data_130_Sep-19-2023_14-58_W_12fs.txt'
    # save_path = '../../../tests/data/physics_experiment/data_130_Sep-19-2023_14-58_W_12fs.h5'
    # copy_xy_from_cobold_txt_to_hdf5(txt_path, save_path)

    # file_path = '../../../tests/data/physics_experiment/data_130_Sep-19-2023_14-58_W_12fs.h5'
    # (at 242°) corresponds to an intensity of 1.4e13 W/cm^2.
    # 170 fs the highest intensity is at 3.4e13 W/cm^2
    # Energy per pulse (J) = Power Density (W/cm^2) * Area (cm^2) * Pulse Duration (s)
    # ref_angle = 242
    # ref_laser_intensity = 3.4e13 * 12e-15 * 4e-4 * 4e-4 * np.pi / 1e-12
    # # ref_laser_intensity = 1.4 * 12 * 4 * 4 * np.pi
    # print(ref_laser_intensity)
    # convert_ND_angle_to_laser_intensity(file_path, ref_laser_intensity, ref_angle)

    # rename_a_category(file_path, 'dld/AbsoluteTimeStamp', 'dld/start_counter')
    pulse_energy_calculator_list(242, 1.4e13, 5000)
    print('Done')
