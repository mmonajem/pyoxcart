import re

import matplotlib
import numpy as np
import pandas as pd
from faker import Factory

from pyccapt.calibration.data_tools import data_tools


def fix_parentheses(c):
    """
    Fix parentheses in a given string by expanding the elements inside them.

    Args:
        c (str): Input string containing parentheses.

    Returns:
        str: String with expanded elements inside parentheses.
    """
    index = []
    for i in range(len(c)):
        if c[i] == '(':
            index.append(i + 1)
        if c[i] == ')':
            index.append(i)
            index.append(int(c[i + 1]))
    index = list(chunks(index, 3))
    list_parentheses = []
    for i in range(len(index)):
        tmp = c[index[i][0]:index[i][1]]
        tmp = re.findall('[A-Z][^A-Z]*', tmp)
        for j in range(len(tmp)):
            if tmp[j].isalpha():
                tmp[j] = tmp[j] + str(index[i][-1])
            elif not tmp[j].isalpha():
                dd = int(re.findall(r'\d+', tmp[j])[0]) * index[i][-1]
                tmp[j] = ''.join([p for p in tmp[j] if not p.isdigit()]) + str(dd)
        list_parentheses.append("".join(tmp))

    for i in range(len(list_parentheses)):
        gg = list_parentheses[i]
        c = list(c)
        c[index[i][0] - 1 - (2 * i):index[i][1] + 2] = list_parentheses[i]

    return ''.join(c)


def create_formula_latex(aa, num_charge=0):
    """
    Create a LaTeX representation of a chemical formula.

    Args:
        aa (str): The chemical formula.
        num_charge (int): The number of charges associated with the formula.

    Returns:
        str: The LaTeX representation of the chemical formula.

    """
    aa = list(aa)
    for i in range(len(aa)):
        if aa[i] == ')':
            if i + 1 == len(aa):
                aa.insert(i + 1, '1')
            else:
                if not aa[i + 1].isnumeric():
                    aa.insert(i + 1, '1')
    aa = ''.join(aa)
    aa = re.findall('(\d+|[A-Za-z]+)', aa)
    for i in range(int(len(aa) / 3)):
        if aa[i * 3 + 2].isnumeric():
            aa[i * 3 + 2] = int(aa[i * 3 + 2])
    for i in range(len(aa)):
        if aa[i] == '1':
            aa[i] = ' '
    for i in range(int(len(aa) / 3)):
        if i == 0:
            bb = '{}^{%s}%s_{%s}' % (aa[(i * 3) + 1], aa[(i * 3)], aa[(i * 3) + 2])
        else:
            bb += '{}^{%s}%s_{%s}' % (aa[(i * 3) + 1], aa[(i * 3)], aa[(i * 3) + 2])
    if num_charge == 0:
        bb = r'$' + bb + '$'
    else:
        bb = r'$(' + bb + ')^{%s+}' % num_charge + '$'
    return bb


def chunks(lst, n):
    """
    Yield successive n-sized chunks from a list.

    Args:
        lst (list): The input list.
        n (int): The chunk size.

    Yields:
        list: Successive n-sized chunks from the input list.

    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def find_closest_elements(target_elem, num_elements, abundance_threshold=0.0, charge=4,
                          data_table='../../../files/isotopeTable.h5', variables=None):
    """
    Find the closest elements to a target element.

    Args:
        target_elem (float): Target element.
        num_elements (int): Number of closest elements to find.
        abundance_threshold (float): Abundance threshold for filtering elements (as a percentage).
        charge (int): Charge value.
        data_table (str): Path to the data table (HDF5 file).
        variables (object): Object containing the variables.

    Returns:
        pd.DataFrame: DataFrame containing closest elements and their properties.
    """
    # Read data from the HDF5 file
    dataframe = pd.read_hdf(data_table)

    # Expand elements based on charge
    elements = dataframe['element'].to_numpy()
    isotope_number = dataframe['isotope'].to_numpy()
    weight = dataframe['weight'].to_numpy()
    abundance = dataframe['abundance'].to_numpy()

    elements = np.repeat(elements, charge)
    isotope_number = np.repeat(isotope_number, charge)
    weights = np.repeat(weight, charge)
    abundance = np.repeat(abundance, charge)
    charge_list = np.array([i % charge + 1 for i in range(len(weights))])

    weights = weights / charge_list

    # Filter elements by abundance threshold
    abundance_threshold *= 100
    mask_abundanc = (abundance > abundance_threshold)
    elements = elements[mask_abundanc]
    isotope_number = isotope_number[mask_abundanc]
    weights = weights[mask_abundanc]
    abundance = abundance[mask_abundanc]

    # Find closest elements
    idxs = np.argsort(np.abs(weights - target_elem))[:num_elements]

    selected_elements = elements[idxs]
    selected_isotope_number = isotope_number[idxs]
    selected_weights = weights[idxs]
    selected_abundance = abundance[idxs]
    selected_charge_list = charge_list[idxs]
    # Create LaTeX formatted element symbols
    element_symbols = []
    for i in range(len(idxs)):
        element_symbols.append(
            r"${}^{%s}%s_{%s}$" % (selected_isotope_number[i], selected_elements[i], selected_charge_list[i]))

    # Create DataFrame
    df = pd.DataFrame({
        'ion': element_symbols,
        'mass': selected_weights,
        'element': selected_elements,
        'complex': np.ones(len(idxs), dtype=int),
        'isotope': selected_isotope_number,
        'charge': selected_charge_list,
        'abundance': selected_abundance,
    })

    # Sort DataFrame
    df = df.sort_values(by=['abundance', 'mass'], ascending=[False, True])
    df.reset_index(drop=True, inplace=True)

    # Backup data if variables provided
    if variables is not None:
        variables.range_data_backup = df.copy()

    return df


def molecule_manual(target_element, charge, latex=True, variables=None):
    """
    Generate a list of isotopes for a given target element.

    Args:
        target_element (str): The target element to find isotopes for.
        charge (int): The charge of the target element.
        aboundance_threshold (float): The abundance threshold for filtering isotopes.
        latex (bool, optional): Whether to generate LaTeX representation of formulas. Defaults to True.
        variables (object, optional): The variables object. Defaults to None.

    Returns:
        pd.DataFrame: A DataFrame containing the list of isotopes with their weights and abundances.

    """
    isotopeTableFile = '../../../files/isotopeTable.h5'
    dataframe = data_tools.read_hdf5_through_pandas(isotopeTableFile)
    target_element = fix_parentheses(target_element)

    elements = dataframe['element'].to_numpy()
    isotope_number = dataframe['isotope'].to_numpy()
    abundance = dataframe['abundance'].to_numpy()
    weight = dataframe['weight'].to_numpy()

    # Extract numbers enclosed in curly braces and store them in a list
    isotope_list = [int(match.group(1)) for match in re.finditer(r'{(\d+)}', target_element)]

    # Extract uppercase letters and store them in a list
    element_list = re.findall(r'[A-Z][a-z]*', target_element)

    # Extract numbers that follow the uppercase letters and store them in a list
    complexity_list = [int(match[1]) for match in re.findall(r'([A-Z][a-z]*)(\d+)', target_element)]

    total_weight = 0
    abundance_c = 0
    for i, isotop in enumerate(isotope_list):
        index = np.where(isotope_number == isotop)
        total_weight += weight[index] * complexity_list[i]
        abundance_c *= abundance[index] ** complexity_list[i]

    total_weight = total_weight / charge
    if latex:
        formula = ''
        for i in range(len(isotope_list)):
            isotope = isotope_list[i]
            element = element_list[i]
            comp = complexity_list[i]

            formula += '{}^'
            formula += '{%s}' % isotope
            formula += '%s' % element
            if comp != 1:
                formula += '_{%s}' % comp
        if charge > 1:
            formula = r'$(' + formula + ')^{%s+}$' % charge
        else:
            formula = r'$' + formula + '$'
    else:
        formula = target_element

    df = pd.DataFrame({'ion': [formula], 'mass': [total_weight], 'element': [element_list],
                       'complex': [complexity_list], 'isotope': [isotope_list], 'charge': [charge],
                       'abundance': [abundance_c], })

    if variables is not None:
        variables.range_data_backup = df.copy()
    return df
    # molecule_formula = re.findall('(\d+|[A-Za-z]+)', target_element)
    # molecule_formula = [re.split('(?<=.)(?=[A-Z])', item) for item in molecule_formula]
    # molecule_formula = list(itertools.chain(*molecule_formula))
    #
    # elem_weights = []
    # elem_abundance = []
    # elem_compo = []
    #
    # for i in range(len(molecule_formula)):
    #     if not molecule_formula[i].isnumeric():
    #         idx_element = np.where(elements == molecule_formula[i])
    #         elem_compo_temp = []
    #         elem_weights_tmp = []
    #         elem_abundance_tmp = []
    #         for j in range(len(idx_element[0])):
    #             if i + 1 < len(molecule_formula):
    #                 if molecule_formula[i + 1].isnumeric():
    #                     number_of_elem = int(molecule_formula[i + 1])
    #                     elem_compo_temp.append(
    #                         elements[idx_element[0][j]] + '(' + str(isotope_number[idx_element[0][j]]) + ')' + str(
    #                             number_of_elem))
    #                 else:
    #                     number_of_elem = 1
    #                     elem_compo_temp.append(
    #                         elements[idx_element[0][j]] + '(' + str(isotope_number[idx_element[0][j]]) + ')')
    #             else:
    #                 number_of_elem = 1
    #                 elem_compo_temp.append(
    #                     elements[idx_element[0][j]] + '(' + str(isotope_number[idx_element[0][j]]) + ')')
    #
    #             elem_weights_tmp.append(weight[idx_element[0][j]] * number_of_elem)
    #
    #             abundance_i = abundance[idx_element[0][j]] / 100
    #             if number_of_elem > 1:
    #                 abundance_i = abundance_i ** number_of_elem
    #
    #             elem_abundance_tmp.append(abundance_i)
    #         elem_compo.append(elem_compo_temp)
    #         elem_weights.append(elem_weights_tmp)
    #         elem_abundance.append(elem_abundance_tmp)
    #
    # list_elem_compo = list(itertools.product(*elem_compo))
    # list_elem_weights = list(itertools.product(*elem_weights))
    # list_elem_abundance = list(itertools.product(*elem_abundance))
    #
    # list_elem_compo = [''.join(item) for item in list_elem_compo]
    # num_element = len(list_elem_compo)
    #
    # list_elem_weights = [sum(item) for item in list_elem_weights]
    # list_elem_abundance = [math.prod(item) for item in list_elem_abundance]
    # list_elem_abundance = [item * 100 for item in list_elem_abundance]
    #
    # # duplicate the list base on the charge
    # list_elem_compo = [item for item in list_elem_compo for _ in range(charge)]
    # list_elem_weights = [val / (charge / x) for val in list_elem_weights for x in range(charge, 0, -1)]
    # list_elem_abundance = [item for item in list_elem_abundance for _ in range(charge)]
    # list_elem_charge = [x for x in range(1, charge + 1)] * num_element
    # if latex:
    #     for i in range(len(list_elem_compo)):
    #         list_elem_compo[i] = create_formula_latex(list_elem_compo[i], list_elem_charge[i])
    #
    # df = pd.DataFrame({'molecule': list_elem_compo, 'weight': list_elem_weights, 'abundance': list_elem_abundance})
    # # df = pd.DataFrame({'ion': element_c, 'mass': element_weights_c, 'element': element_simbol_c,
    # #                    'complex': num_c, 'isotope': isotope_number_c, 'charge': charge_c, 'abundance': abundance_c,})
    # # Filter the DataFrame based on the "abundance" column
    # abundance_threshold = abundance_threshold * 100
    # df = df[df['abundance'] > abundance_threshold]
    # df = df.sort_values(by=['weight', 'abundance'], ascending=[False, True])
    # # Accessing the index of the sorted DataFrame
    # df.reset_index(drop=True, inplace=True)
    # if variables is not None:
    #     variables.range_data_backup = df.copy()
    # return df


def molecule_create(element_list, complexity, charge, latex=True):
    isotopeTableFile = '../../../files/isotopeTable.h5'
    dataframe = data_tools.read_hdf5_through_pandas(isotopeTableFile)
    elements = dataframe['element'].to_numpy()
    isotope_number = dataframe['isotope'].to_numpy()
    abundance = dataframe['abundance'].to_numpy()
    weight = dataframe['weight'].to_numpy()

    indices_elements = [np.where(elements == element)[0] for element in element_list]


def ranging_dataset_create(variables, row_index, mass_unknown):
    """
    This function is used to create the ranging dataset

        Arg:
            variables (class): The class of the variables
            row_index (int): The index of the selected row
            mass_unknown (float): The mass of the unknown element

        Returns:
            None
    """
    if row_index >= 0:
        selected_row = variables.range_data_backup.iloc[row_index].tolist()
        selected_row = selected_row[:-1]
    else:
        selected_row = ['unranged', mass_unknown, 'unranged', 0, 0, 0]
    fake = Factory.create()
    data_table = '../../../files/color_scheme.h5'
    dataframe = data_tools.read_hdf5_through_pandas(data_table)
    element_selec = selected_row[2]
    try:
        color_rgb = dataframe[dataframe['ion'].str.contains(element_selec, na=False)].to_numpy().tolist()
        color = matplotlib.colors.to_hex([color_rgb[0][1], color_rgb[0][2], color_rgb[0][3]])
    except Exception as e:
        print(f"An error occurred: {e}")
        print('The element is not color list')
        color = fake.hex_color()

    print(selected_row)
    mass = selected_row[1]
    if not variables.h_line_pos:
        print('The h_line_pos is empty')
        print('first do the ranging then add the selected ion to the ranging dataset')
        range = [0, 0]
    else:
        range = sorted(variables.h_line_pos, key=lambda x: abs(x - mass))[:2]
        mc = sorted(variables.peak, key=lambda x: abs(x - mass))[:1]
        index_mc = [index for index, value in enumerate(variables.peak) if value == mc]
        mc_peak_height = variables.peak_y[index_mc[0]]
    selected_row.insert(2, mc[0])
    selected_row.insert(3, range[0])
    selected_row.insert(4, range[1])
    selected_row.insert(5, color)
    selected_row.insert(6, int(mc_peak_height))

    # Add the row to the DataFrame using the .loc method

    variables.range_data.loc[len(variables.range_data)] = selected_row

def display_color(color):
    """
    This function is used to display the color in the table

        Arg:
            color (str): The color in hex format

        Returns:
            str: The color in hex format
    """
    return f'background-color: {color}; width: 50px; height: 20px;'