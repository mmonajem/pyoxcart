import pandas as pd

from pyccapt.calibration.calibration_tools import ion_selection
from pyccapt.calibration.data_tools import data_tools


def molecule_dataframe():
    """
    Retrieve a dataframe of molecules and their isotopic information.

    Reads an isotope table file and a list of chemical formulas file,
    selects the isotopic information for each molecule, and returns
    a combined dataframe containing the isotopic details for all molecules.

    Returns:
        pandas.DataFrame: The dataframe containing the isotopic information for molecules.
    """
    isotope_table_file = '../../../files/isotopeTable.h5'
    dataframe = data_tools.read_hdf5_through_pandas(isotope_table_file)

    molecule_list_file = '../../../files/list_of_chemical.csv'
    molecule_dataframe = pd.read_csv(molecule_list_file, encoding='utf-8', header=0)
    molecule_dataframe = molecule_dataframe[molecule_dataframe['Chemical formula'].notna()]
    molecule_dataframe = molecule_dataframe.reset_index(drop=True)

    chemical_formulas = molecule_dataframe['Chemical formula']
    df2 = None

    for i, formula in enumerate(chemical_formulas):
        if i == 0:
            df2 = ion_selection.molecule_isotop_list(dataframe, formula, latex=False)
        else:
            df3 = ion_selection.molecule_isotop_list(dataframe, formula, latex=False)
            df2 = pd.concat([df2, df3], ignore_index=True)

    return df2


if __name__ == "__main__":
    df = molecule_dataframe()
    print(len(df))
    # df2.to_hdf('molecule_table.h5', 'df', mode='w')