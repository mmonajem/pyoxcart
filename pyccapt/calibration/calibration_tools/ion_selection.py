import itertools
import math
import re

import numpy as np
import pandas as pd

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


def find_close_element(target_elem, num_c, abundance_threshold=1, charge=4):
    """
    Find the closest elements to a target element.

    Args:
        target_elem (float): Target element.
        num_c (int): Number of closest elements to find.
        abundance_threshold (float): Abundance threshold for filtering elements.
        charge (int): Charge value.

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

    element_c = element_c[index_sort]
    element_weights_c = element_weights_c[index_sort]
    abundance_c = abundance_c[index_sort]

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

    if abundance_threshold < 1.0:
        element_c = element_c[abundance_c < abundance_threshold]
        element_weights_c = element_weights_c[abundance_c < abundance_threshold]
        abundance_c = abundance_c[abundance_c < abundance_threshold]

    df = pd.DataFrame({'element': element_c, 'weight': element_weights_c, 'abundance': abundance_c})
    return df


def find_close_molecule(target_mole, num_c, abundance_threshold=1, charge=4):
    """
    Find the closest molecules to a target molecule.

    Args:
        target_mole (float): Target molecule.
        num_c (int): Number of closest molecules to find.
        abundance_threshold (float): Abundance threshold for filtering molecules.
        charge (int): Charge value.

    Returns:
        pandas.DataFrame: DataFrame containing closest molecules and their properties.
    """
    data_table = '../../../files/molecule_table.h5'
    dataframe = data_tools.read_hdf5_through_pandas(data_table)

    elements = dataframe['molecule'].to_numpy()
    weight_number = dataframe['weight'].to_numpy()
    abundance = dataframe['abundance'].to_numpy()
    element_abundance = np.repeat(abundance, charge)

    element_weights = np.zeros((len(elements), charge))
    elements_w = weight_number
    for i in range(charge):
        element_weights[:, i] = elements_w / (i + 1)
    element_weights = element_weights.flatten()

    elem = elements
    element_list = np.zeros(len(elem) * charge).astype('U')
    for i in range(len(elem)):
        for j in range(charge):
            element_list[i + j + ((charge - 1) * i)] = elem[i] + '+' * (j + 1)

    idxs = find_nearest(np.copy(element_weights), target_mole, num_c)

    element_c = element_list[idxs]
    element_weights_c = element_weights[idxs]
    abundance_c = element_abundance[idxs]

    index_sort = np.argsort(abundance_c)
    index_sort = np.flip(index_sort)

    element_c = element_c[index_sort]
    element_weights_c = element_weights_c[index_sort]
    abundance_c = abundance_c[index_sort]

    # Make the formula in LaTeX format
    for i in range(len(element_c)):
        ff = element_c[i]
        num_charge = ff.count('+')
        ff = ff.replace('+', '')
        element_c[i] = create_formula_latex(ff, num_charge)

    if abundance_threshold < 1.0:
        element_c = element_c[abundance_c < abundance_threshold]
        element_weights_c = element_weights_c[abundance_c < abundance_threshold]
        abundance_c = abundance_c[abundance_c < abundance_threshold]

    df = pd.DataFrame({'molecule': element_c, 'weight': element_weights_c, 'abundance': abundance_c})
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
            bb = '{}^{{{}}}_{{{}}}'.format(aa[(i * 3) + 1], aa[(i * 3)], aa[(i * 3) + 2])
        else:
            bb += '{}^{{{}}}_{{{}}}'.format(aa[(i * 3) + 1], aa[(i * 3)], aa[(i * 3) + 2])
    if num_charge == 0:
        bb = r'${}$'.format(bb)
    else:
        bb = r'${}^{{{}}+}$'.format(bb, num_charge)
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


def molecule_isotope_list(dataframe, target_element, latex=True):
    """
    Generate a list of isotopes for a given target element.

    Args:
        dataframe (pd.DataFrame): The input DataFrame containing isotope data.
        target_element (str): The target element to find isotopes for.
        latex (bool, optional): Whether to generate LaTeX representation of formulas. Defaults to True.

    Returns:
        pd.DataFrame: A DataFrame containing the list of isotopes with their weights and abundances.

    """
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
                    for k in range(number_of_elem):
                        abundance_i = abundance_i * abundance_i
                elem_abundance_tmp.append(abundance_i)

            elem_compo.append(elem_compo_temp)
            elem_weights.append(elem_weights_tmp)
            elem_abundance.append(elem_abundance_tmp)

    list_elem_compo = list(itertools.product(*elem_compo))
    list_elem_weights = list(itertools.product(*elem_weights))
    list_elem_abundance = list(itertools.product(*elem_abundance))

    list_elem_compo = [''.join(item) for item in list_elem_compo]
    if latex:
        for i in range(len(list_elem_compo)):
            list_elem_compo[i] = create_formula_latex(list_elem_compo[i])
    list_elem_weights = [sum(item) for item in list_elem_weights]
    list_elem_abundance = [math.prod(item) for item in list_elem_abundance]
    list_elem_abundance = [item * 100 for item in list_elem_abundance]
    df = pd.DataFrame({'molecule': list_elem_compo, 'weight': list_elem_weights, 'abundance': list_elem_abundance})
    return df
