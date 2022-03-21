import ipywidgets as widgets

from apt_pyanalysis.tools  import variables

# Stores values currently selected element in dropdown.
elementDict = {}
# Stores values currently selected charge in dropdown. 
chargeDict = {}
elementWithChargeDict = {}


def dropdownWidget(elementsList, dropdownLabel):
    '''
    This function creates a dropdown widget which offers selection of different elements.

    Attributes:
        elementsList: List of element with its correponding mass/weight [list]
                      For eg: [('H',1.01),('He',3.02)]
    Returns:
        dropdown: object for the created widget [object]

    '''
    dropdown = widgets.Dropdown(options=elementsList, description=dropdownLabel, disabled=False)

    # Setup default values of elements and charge
    if dropdownLabel == "Charge":
        chargeDict['charge'] = elementsList[0][1]
    elif dropdownLabel == "Elements":
        elementDict['element'] = elementsList[0][1]
    return dropdown


def buttonWidget(buttonText):
    """
    This function creates a button widget.

    Attributes:
        buttonText:  Text to be displayed on the button [string]
    Returns:
        button: object for the created widget [object]
    """
    button = widgets.Button(
        description=buttonText,
        disabled=False,
        button_style='',
        tooltip=buttonText,
        icon='check'
    )
    return button


def onClickAdd(b):
    """
    This is a callback function when the ADD button is clicked/pressed.
    It adds the selected element in dropdown in to a list.

    Attributes:
        Accepts only a internal object as an argument
    Returns:
        Does not return anything
    """
    if 'element' in elementWithChargeDict:
        elementMass = elementWithChargeDict['element']
        if elementMass not in variables.listMaterial:
            variables.listMaterial.append(elementMass)
            print("Updated List : ", variables.listMaterial, ''.ljust(40), end='\r')
    else:
        print("Please select the charge before adding", end='\r')


def onClickDelete(b):
    """
    This is a callback function when the DELETE button is clicked/pressed.
    It deletes the selected element in the dropdown from the list.

    Attributes:
        Accepts only a internal object as an argument
    Returns:
        Does not return anything
    """
    if 'element' in elementWithChargeDict:
        elementMass = elementWithChargeDict['element']
        if elementMass in variables.listMaterial:
            variables.listMaterial.remove(elementMass)
            print("Updated List : ", variables.listMaterial, ''.ljust(40), end='\r')
        else:
            print("Nothing Deleted. Choose carefully(Enter right combination of element and charge)", end='\r')
    else:
        print("Please select the element with the right combination of charge to efficiently delete", end='\r')


def onClickReset(b):
    """
    This is a callback function when the RESET button is clicked/pressed.
    It clears the list and deletes all the elements from the list.

    Attributes:
        Accepts only a internal object as an argument
    Returns:
        Does not return anything
    """
    variables.listMaterial.clear()
    print("Updated List : ", variables.listMaterial, ''.ljust(40), end='\r')


def on_change(change):
    """
    This is a callback fucntion which observes change in the dropdown widget.
    It updates the element and its corresponding weight/mass based on the selection from the dropdown.
    Updates the selected value in a global dict. [This dict could be replaced by a single variable]
    Atrributes:
        Accepts only a internal object as an argument
    Returns:
        Does not return anything
    """
    if change['type'] == 'change' and change['name'] == 'value':
        print("Mass of selected element: to %s" % change['new'], ''.ljust(40), end='\r')
        elementWithChargeDict.clear()
        print("Now please select the appropriate charge", ''.ljust(40), end='\r')
        elementDict['element'] = change['new']
        compute_element_isotope_values_according_to_selected_charge()
        

def on_change_charge(change):
    """
    This is a callback function which observes change in the dropdown widget.
    It updates the element and its corresponding weight/mass based on the selection from the dropdown.
    Updates the selected value in a global dict. [This dict could be replaced by a single variable]
    Attributes:
        Accepts only a internal object as an argument
    Returns:
        Does not return anything
    """
    if change['type'] == 'change' and change['name'] == 'value':
        print("Selected charge : to %s" % change['new'], ''.ljust(40), end='\r')
        selectedElement = elementDict['element']
        updatedCharge = change['new']
        chargeDict['charge'] = updatedCharge
        compute_element_isotope_values_according_to_selected_charge()
        

def compute_element_isotope_values_according_to_selected_charge():
    selectedElement = elementDict['element']
    charge = chargeDict['charge']
    elementWithCharge = round(float(selectedElement) / int(charge), 2)
    elementWithChargeDict['element'] = elementWithCharge
    