import pandas as pd

from pyccapt.calibration.calibration_tools import data_tools, ion_selection


def molecule_dataframe():
    isotopeTableFile = '../../../files/isotopeTable.h5'
    dataframe = data_tools.read_hdf5_through_pandas(isotopeTableFile)
    molecul_list_file = '../../../files/list_of_chemical.csv'
    molecule_dataframe = pd.read_csv(molecul_list_file, encoding='utf-8', header=0)
    molecule_dataframe = molecule_dataframe[molecule_dataframe['Chemical formula'].notna()]
    molecule_dataframe = molecule_dataframe.reset_index(drop=True)
    ff = molecule_dataframe['Chemical formula']
    for i in range(len(ff)):
        #     print(i, ff[i])
        if i == 0:
            df2 = ion_selection.molecule_isotop_list(dataframe, ff[i], latex=False)
        else:
            df3 = ion_selection.molecule_isotop_list(dataframe, ff[i], latex=False)
            df2 = pd.concat([df2, df3], ignore_index=True)
    return df2


if __name__ == "__main__":
    df = molecule_dataframe()
    print(len(df))
    # df2.to_hdf('molecule_table.h5', 'df', mode='w')