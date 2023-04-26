
import pandas as pd
import numpy as np
import math
import itertools
import re

# Local module and scripts
from data_tools import data_tools


def find_nearest(a, a0, num):
    # Element in nd array that is closest to the scalar value a0
    # num define the number of the closest value that we are looking for
    idx = []
    for i in range(num):
        idx.append(np.abs(a - a0).argmin())
        a[idx] = -200  # some dummy negative value
    return idx


def find_close_element(target_elem, num_c, aboundance_threshold=1, charge=4):
    data_table = '../../../files/isotopeTable.h5'
    dataframe = data_tools.read_hdf5_through_pandas(data_table)

    elements = dataframe['element'].to_numpy()
    isotope_number = dataframe['isotope'].to_numpy()
    abundance = dataframe['abundance'].to_numpy()
    element_abundance = np.repeat(abundance, charge)

    element_wights = np.zeros((len(elements), charge))
    elements_w = dataframe['weight'].to_numpy()
    for i in range(charge):
        element_wights[:, i] = elements_w / (i + 1)
    element_wights = element_wights.flatten()

    elem = np.core.defchararray.add(elements.astype('U'), isotope_number.astype('U'))
    element_list = np.zeros(len(elem) * charge).astype('U')
    for i in range(len(elem)):
        for j in range(charge):
            element_list[i + j + ((charge - 1) * i)] = elem[i] + '+' * (j + 1)

    idxs = find_nearest(np.copy(element_wights), target_elem, num_c)

    element_c = element_list[idxs]
    element_wights_c = element_wights[idxs]
    abundance_c = element_abundance[idxs]

    index_sort = np.argsort(abundance_c)
    index_sort = np.flip(index_sort)

    element_c = element_c[index_sort]
    element_wights_c = element_wights_c[index_sort]
    abundance_c = abundance_c[index_sort]
    # make the formula in latex format
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

    if aboundance_threshold < 1.0:
        element_c = element_c[abundance_c < aboundance_threshold]
        element_wights_c = element_wights_c[abundance_c < aboundance_threshold]
        abundance_c = abundance_c[abundance_c < aboundance_threshold]

    df = pd.DataFrame({'element': element_c, 'weight': element_wights_c, 'abundance': abundance_c})
    return df


def find_close_molecule(target_mole, num_c, aboundance_threshold=1, charge=4):
    data_table = '../../../files/molecule_table.h5'
    dataframe = data_tools.read_hdf5_through_pandas(data_table)

    elements = dataframe['molecule'].to_numpy()
    weight_number = dataframe['weight'].to_numpy()
    abundance = dataframe['abundance'].to_numpy()
    element_abundance = np.repeat(abundance, charge)

    element_wights = np.zeros((len(elements), charge))
    elements_w = weight_number
    for i in range(charge):
        element_wights[:, i] = elements_w / (i + 1)
    element_wights = element_wights.flatten()
    elem = elements
    #     elem = np.core.defchararray.add(elements.astype('U'), weight_number.astype('U'))
    element_list = np.zeros(len(elem) * charge).astype('U')
    for i in range(len(elem)):
        for j in range(charge):
            element_list[i + j + ((charge - 1) * i)] = elem[i] + '+' * (j + 1)

    idxs = find_nearest(np.copy(element_wights), target_mole, num_c)

    element_c = element_list[idxs]
    element_wights_c = element_wights[idxs]
    abundance_c = element_abundance[idxs]

    index_sort = np.argsort(abundance_c)
    index_sort = np.flip(index_sort)

    element_c = element_c[index_sort]
    element_wights_c = element_wights_c[index_sort]
    abundance_c = abundance_c[index_sort]
    # make the formula in latex format
    for i in range(len(element_c)):
        ff = element_c[i]
        num_charge = ff.count('+')
        ff = ff.replace('+', '')
        element_c[i] = create_formula_latex(ff, num_charge)

    if aboundance_threshold < 1.0:
        element_c = element_c[abundance_c < aboundance_threshold]
        element_wights_c = element_wights_c[abundance_c < aboundance_threshold]
        abundance_c = abundance_c[abundance_c < aboundance_threshold]
    df = pd.DataFrame({'molecule': element_c, 'weight': element_wights_c, 'abundance': abundance_c})
    return df

def create_formula_latex(aa, num_charge=0):
    aa = list(aa)
    # add one after parantezes if there is no higher number
    for i in range(len(aa)):
        if aa[i] == ')':
            if i+1 == len(aa):
                aa.insert(i+1, '1')
            else:
                if not aa[i+1].isnumeric():
                    aa.insert(i+1, '1')
    aa = ''.join(aa)
    aa = re.findall('(\d+|[A-Za-z]+)', aa)
    for i in range(int(len(aa)/3)):
        if aa[i*3+2].isnumeric():
            aa[i*3+2] = int(aa[i*3+2])
    # replace 1 with''
    for i in range(len(aa)):
        if aa[i]==1:
            aa[i] = ' '
    for i in range(int(len(aa)/3)):
        if i == 0:
            bb = '{}^{%s}%s_{%s}' %(aa[(i*3)+1], aa[(i*3)], aa[(i*3)+2])
        else:
            bb += '{}^{%s}%s_{%s}' %(aa[(i*3)+1], aa[(i*3)], aa[(i*3)+2])
    if num_charge == 0:
        bb = r'$' + bb + '$'
    else:
        bb = r'$(' + bb + ')^{%s+}' %num_charge + '$'
    return bb


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def fix_prantesis(c):
    index = []
    for i in range(len(c)):
        if c[i] == '(':
            index.append(i + 1)
        if c[i] == ')':
            index.append(i)
            index.append(int(c[i + 1]))
    index = list(chunks(index, 3))
    list_parantesis = []
    for i in range(len(index)):
        tmp = c[index[i][0]:index[i][1]]
        tmp = re.findall('[A-Z][^A-Z]*', tmp)
        for j in range(len(tmp)):
            if tmp[j].isalpha():
                tmp[j] = tmp[j] + str(index[i][-1])
            elif not tmp[j].isalpha():
                dd = int(re.findall(r'\d+', tmp[j])[0]) * index[i][-1]
                tmp[j] = ''.join([p for p in tmp[j] if not p.isdigit()]) + str(dd)
        list_parantesis.append("".join(tmp))

    for i in range(len(list_parantesis)):
        gg = list_parantesis[i]
        c = list(c)
        c[index[i][0] - 1 - (2 * i):index[i][1] + 2] = list_parantesis[i]

    return ''.join(c)


def molecule_isotop_list(dataframe, target_element, latex=True):
    target_element = fix_prantesis(target_element)

    elements = dataframe['element'].to_numpy()
    isotope_number = dataframe['isotope'].to_numpy()
    abundance = dataframe['abundance'].to_numpy()
    weight = dataframe['weight'].to_numpy()

    molecule_formula = re.findall('(\d+|[A-Za-z]+)', target_element)
    molecule_formula = [re.split('(?<=.)(?=[A-Z])', item) for item in molecule_formula]
    molecule_formula = list(itertools.chain(*molecule_formula))

    elem_wights = []
    elem_aboundance = []
    elem_compo = []

    for i in range(len(molecule_formula)):
        if not molecule_formula[i].isnumeric():
            idx_element = np.where(elements == molecule_formula[i])
            elem_compo_temp = []
            elem_wights_tmp = []
            elem_aboundance_tmp = []
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

                elem_wights_tmp.append(weight[idx_element[0][j]] * number_of_elem)
                aboundance_i = abundance[idx_element[0][j]] / 100
                if number_of_elem > 1:
                    for k in range(number_of_elem):
                        aboundance_i = aboundance_i * aboundance_i
                elem_aboundance_tmp.append(aboundance_i)

            elem_compo.append(elem_compo_temp)
            elem_wights.append(elem_wights_tmp)
            elem_aboundance.append(elem_aboundance_tmp)

    list_elem_compo = list(itertools.product(*elem_compo))
    list_elem_wights = list(itertools.product(*elem_wights))
    list_elem_aboundance = list(itertools.product(*elem_aboundance))

    list_elem_compo = [''.join(item) for item in list_elem_compo]
    if latex:
        for i in range(len(list_elem_compo)):
            list_elem_compo[i] = create_formula_latex(list_elem_compo[i])
    list_elem_wights = [sum(item) for item in list_elem_wights]
    list_elem_aboundance = [math.prod(item) for item in list_elem_aboundance]
    list_elem_aboundance = [item * 100 for item in list_elem_aboundance]
    df = pd.DataFrame({'molecule': list_elem_compo, 'weight': list_elem_wights, 'abundance': list_elem_aboundance})
    # df = df.style.set_properties(subset=['molecule'], **{'width': '300px'})
    return df

