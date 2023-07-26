import itertools
import math
import re

import matplotlib
import numpy as np
import pandas as pd
from faker import Factory

from pyccapt.calibration.data_tools import data_tools


def find_nearest(a, a0, num):
    """
    Find the indices of the num closest elements in array a to the scalar value a0.

    Args:
        a (numpy.ndarray): Input array.
        a0 (float): Target scalar value.
        num (int): Number of closest values to find.

    Returns:
        list: Indices of the num closest elements.
    """
    idx = []
    for i in range(num):
        idx.append(np.abs(a - a0).argmin())
        a[idx] = -200  # some dummy negative value
    return idx


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


def find_close_element(target_elem, num_c, abundance_threshold=0.0, charge=4, variables=None):
    """
    Find the closest elements to a target element.

    Args:
        target_elem (float): Target element.
        num_c (int): Number of closest elements to find.
        abundance_threshold (float): Abundance threshold for filtering elements.
        charge (int): Charge value.
        variables (object): object containing the variables.

    Returns:
        pandas.DataFrame: DataFrame containing closest elements and their properties.
    """
    data_table = '../../../files/isotopeTable.h5'
    dataframe = data_tools.read_hdf5_through_pandas(data_table)

    elements = dataframe['element'].to_numpy()
    isotope_number = dataframe['isotope'].to_numpy()
    abundance = dataframe['abundance'].to_numpy()
    element_abundance = np.repeat(abundance, charge)

    element_weights = np.zeros((len(elements), charge))
    elements_w = dataframe['weight'].to_numpy()
    for i in range(charge):
        element_weights[:, i] = elements_w / (i + 1)
    element_weights = element_weights.flatten()

    elem = np.core.defchararray.add(elements.astype('U'), isotope_number.astype('U'))
    element_list = np.zeros(len(elem) * charge).astype('U')
    for i in range(len(elem)):
        for j in range(charge):
            element_list[i + j + ((charge - 1) * i)] = elem[i] + '+' * (j + 1)

    idxs = find_nearest(np.copy(element_weights), target_elem, num_c)

    element_c = element_list[idxs]

    element_weights_c = element_weights[idxs]
    abundance_c = element_abundance[idxs]

    index_sort = np.argsort(abundance_c)
    index_sort = np.flip(index_sort)

    element_weights_c = element_weights_c[index_sort]
    abundance_c = abundance_c[index_sort]
    isotope_number_c = []
    element_simbol_c = []
    charge_c = []
    num_c = []

    # Make the formula in LaTeX format
    for i in range(len(element_c)):
        num_plus = element_c[i].count('+')
        cc = re.findall('(\d+|[A-Za-z]+)', element_c[i])
        if num_plus == 1:
            cc.append('+')
        else:
            cc.append('%s+' % num_plus)
        for j in range(len(cc)):
            if cc[j].isnumeric():
                cc[j] = int(cc[j])
        element_c[i] = '$${}^{%s}%s^{%s}$$' % (cc[1], cc[0], cc[2])
        isotope_number_c.append(cc[1])
        element_simbol_c.append(cc[0])
        charge_c.append(cc[2])
        num_c.append(1)
    df = pd.DataFrame({'ion': element_c, 'mass': element_weights_c, 'element': element_simbol_c,
                       'complex': num_c, 'isotope': isotope_number_c, 'charge': charge_c, 'abundance': abundance_c, })
    if variables is not None:
        variables.range_data_backup = df.copy()
    # Filter the DataFrame based on the "abundance" column
    abundance_threshold = abundance_threshold * 100
    df = df[df['abundance'] > abundance_threshold]
    return df


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


def molecule_isotope_list(target_element, charge, abundance_threshold, latex=True):
    """
    Generate a list of isotopes for a given target element.

    Args:
        target_element (str): The target element to find isotopes for.
        charge (int): The charge of the target element.
        aboundance_threshold (float): The abundance threshold for filtering isotopes.
        latex (bool, optional): Whether to generate LaTeX representation of formulas. Defaults to True.

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

    molecule_formula = re.findall('(\d+|[A-Za-z]+)', target_element)
    molecule_formula = [re.split('(?<=.)(?=[A-Z])', item) for item in molecule_formula]
    molecule_formula = list(itertools.chain(*molecule_formula))

    elem_weights = []
    elem_abundance = []
    elem_compo = []

    for i in range(len(molecule_formula)):
        if not molecule_formula[i].isnumeric():
            idx_element = np.where(elements == molecule_formula[i])
            elem_compo_temp = []
            elem_weights_tmp = []
            elem_abundance_tmp = []
            for j in range(len(idx_element[0])):
                if i + 1 < len(molecule_formula):
                    if molecule_formula[i + 1].isnumeric():
                        number_of_elem = int(molecule_formula[i + 1])
                        elem_compo_temp.append(
                            elements[idx_element[0][j]] + '(' + str(isotope_number[idx_element[0][j]]) + ')' + str(
                                number_of_elem))
                    else:
                        number_of_elem = 1
                        elem_compo_temp.append(
                            elements[idx_element[0][j]] + '(' + str(isotope_number[idx_element[0][j]]) + ')')
                else:
                    number_of_elem = 1
                    elem_compo_temp.append(
                        elements[idx_element[0][j]] + '(' + str(isotope_number[idx_element[0][j]]) + ')')

                elem_weights_tmp.append(weight[idx_element[0][j]] * number_of_elem)

                abundance_i = abundance[idx_element[0][j]] / 100
                if number_of_elem > 1:
                    abundance_i = abundance_i ** number_of_elem

                elem_abundance_tmp.append(abundance_i)
            elem_compo.append(elem_compo_temp)
            elem_weights.append(elem_weights_tmp)
            elem_abundance.append(elem_abundance_tmp)

    list_elem_compo = list(itertools.product(*elem_compo))
    list_elem_weights = list(itertools.product(*elem_weights))
    list_elem_abundance = list(itertools.product(*elem_abundance))

    list_elem_compo = [''.join(item) for item in list_elem_compo]
    num_element = len(list_elem_compo)

    list_elem_weights = [sum(item) for item in list_elem_weights]
    list_elem_abundance = [math.prod(item) for item in list_elem_abundance]
    list_elem_abundance = [item * 100 for item in list_elem_abundance]

    # duplicate the list base on the charge
    list_elem_compo = [item for item in list_elem_compo for _ in range(charge)]
    list_elem_weights = [val / (charge / x) for val in list_elem_weights for x in range(charge, 0, -1)]
    list_elem_abundance = [item for item in list_elem_abundance for _ in range(charge)]
    list_elem_charge = [x for x in range(1, charge + 1)] * num_element
    if latex:
        for i in range(len(list_elem_compo)):
            list_elem_compo[i] = create_formula_latex(list_elem_compo[i], list_elem_charge[i])

    df = pd.DataFrame({'molecule': list_elem_compo, 'weight': list_elem_weights, 'abundance': list_elem_abundance})
    # df = pd.DataFrame({'ion': element_c, 'mass': element_weights_c, 'element': element_simbol_c,
    #                    'complex': num_c, 'isotope': isotope_number_c, 'charge': charge_c, 'abundance': abundance_c,})
    # Filter the DataFrame based on the "abundance" column
    abundance_threshold = abundance_threshold * 100
    df = df[df['abundance'] > abundance_threshold]
    return df


def molecule_create(formula, complexity, charge, abundance_threshold, latex=True):
    pass


def rangging_dataset_create(variables, row_index):
    """
    This function is used to create the rangging dataset

        Arg:
            variables (class): The class of the variables
            row_index (int): The index of the selected row

        Returns:
            None
    """
    selected_row = variables.range_data_backup.iloc[row_index].tolist()
    selected_row.pop()
    print(selected_row)
    fake = Factory.create()
    data_table = '../../../files/color_scheme.h5'
    dataframe = data_tools.read_hdf5_through_pandas(data_table)
    element_selec = selected_row[3]
    try:
        r = dataframe[dataframe['ion'] == re.sub(r'[0-9]', '', element_selec)]['r'].to_numpy()
        g = dataframe[dataframe['ion'] == re.sub(r'[0-9]', '', element_selec)]['g'].to_numpy()
        b = dataframe[dataframe['ion'] == re.sub(r'[0-9]', '', element_selec)]['b'].to_numpy()
        cc = matplotlib.colors.to_hex([r[0], g[0], b[0]])
        color = cc
    except:
        print('The element is not clor list')
        color = fake.hex_color()

    mass = selected_row[1]
    range = sorted(variables.h_line_pos, key=lambda x: abs(x - mass))[:2]
    print(range)
    print(color)
    selected_row.insert(2, range[0])
    selected_row.insert(3, range[1])
    selected_row.insert(4, color)
    print(selected_row)
    # Add the row to the DataFrame using the .loc method
    variables.range_data.loc[len(variables.range_data)] = selected_row
