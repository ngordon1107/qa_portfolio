import pytest, json
from PyQt6.QtGui import QAction
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMessageBox, QApplication

import emp_tracker

# Fixtures ----------------------------------------
# Opening/Closing Main Window
@pytest.fixture
def app(qtbot):
    test_window = emp_tracker.Main()
    qtbot.addWidget(test_window)
    return test_window

# Creating a New Supervisor Window
@pytest.fixture
def add_supervisor_window(app) -> QtWidgets.QMainWindow:
    # Arrange elements
    create_supervisor_action = app.input_supervisor_menu_item
    original_windows_open = set(QApplication.topLevelWidgets())
    supervisor_window = None

    # Act on trigger components
    create_supervisor_action.trigger()  # trigger the input supervisor button
    current_windows_open = set(QApplication.topLevelWidgets())  # capture currently open windows in a set
    newly_opened_windows = current_windows_open - original_windows_open  # create a set of only newly opened windows
    # isolate the actual window and set it equal to supervisor_window
    for window in newly_opened_windows:
        if isinstance(window, QtWidgets.QMainWindow) and window.windowTitle() == "Add Supervisor":
            supervisor_window = window
            break
    return supervisor_window

@pytest.fixture
def add_a_supervisor(add_supervisor_window, captured_popup, qtbot):
    def _params(name = employee_data["supervisors"]["name"], emp_num = employee_data["supervisors"]["emp_num"], shift = employee_data["supervisors"]["shift"],
                salary = employee_data["supervisors"]["salary"], max_workers = employee_data["supervisors"]["max_workers"]):
        """Receives a trigger item, saves the popup, replaces the 'exec' method used with mock_exec, triggers the popup, and returns the popup object."""
        # Arrange -- defining all empty fields
        supervisor_window = add_supervisor_window
        name_input = supervisor_window.supervisor_name_input
        emp_num_input = supervisor_window.supervisor_emp_num_input
        shift_dropdown_menu = supervisor_window.supervisor_shift_dropdown
        salary_input = supervisor_window.supervisor_salary_input
        max_workers_input = supervisor_window.supervisor_max_workers_input
        submit_button = supervisor_window.enter_supervisor

        # Act
        name_input.setText(name)
        emp_num_input.setText(emp_num)
        shift_index = shift_dropdown_menu.findText(shift)
        shift_dropdown_menu.setCurrentIndex(shift_index)
        salary_input.setText(salary)
        max_workers_input.setText(max_workers)
        # swap out the exec function for the popup and dismiss popup
        popup = captured_popup(submit_button)
        qtbot.wait(300)

        # Assert
        assert popup is not None
        assert "Successfully added all of the Supervisor details" in popup.text()
    return _params

@pytest.fixture
def add_worker_window(app, monkeypatch, mock_load):
    # Arrange elements
    create_worker_action = app.input_worker_menu_item
    original_windows_open = set(QApplication.topLevelWidgets())
    worker_window = None
    load_menu_option = app.file_load_menu_item

    # Act on trigger components
    with monkeypatch.context() as m:
        m.setattr(QAction, 'triggered', mock_load)
        load_menu_option.trigger()
    create_worker_action.trigger()  # trigger the input worker button
    current_windows_open = set(QApplication.topLevelWidgets())  # capture currently open windows in a set
    newly_opened_windows = current_windows_open - original_windows_open  # create a set of only newly opened windows
    # isolate the actual window and set it equal to worker_window
    for window in newly_opened_windows:
        if isinstance(window, QtWidgets.QMainWindow) and window.windowTitle() == "Add Production Worker":
            worker_window = window
            break
    return worker_window

@pytest.fixture
def add_a_worker(add_worker_window, captured_popup, qtbot):
    """Fixture returns the _params function. The _params function returns the function to add a worker with the given parameters."""
    def _params(name = employee_data["workers"]["name"], emp_num = employee_data["workers"]["emp_num"], shift = employee_data["workers"]["shift"], pay = employee_data["workers"]["pay_rate"],
                hours = employee_data["workers"]["hours_worked"], assigned_supervisor = employee_data["workers"]["assigned_supervisor"]):
        """Receives a trigger item, saves the popup, replaces the 'exec' method used with mock_exec, triggers the popup, and returns the popup object."""
        # Arrange -- defining all empty fields
        worker_window = add_worker_window
        name_input = worker_window.worker_name_input
        emp_num_input = worker_window.worker_emp_num_input
        shift_dropdown_menu = worker_window.worker_shift_dropdown
        hours_input = worker_window.worker_hours_worked_input
        payrate_input = worker_window.worker_payrate_input
        assign_supervisor_dropdown_menu = worker_window.worker_assign_supervisor_dropdown
        submit_button = worker_window.enter_worker

        # Act
        name_input.setText(name)
        emp_num_input.setText(emp_num)
        shift_index = shift_dropdown_menu.findText(shift)
        shift_dropdown_menu.setCurrentIndex(shift_index)

        payrate_input.setText(pay)
        hours_input.setText(hours)
        assigned_supervisor_index = assign_supervisor_dropdown_menu.findText(f"{assigned_supervisor} ({shift})")
        print(f"Assigned supervisor index: {assigned_supervisor_index}")
        assign_supervisor_dropdown_menu.setCurrentIndex(assigned_supervisor_index)
        print(f"Current supervisor: {assign_supervisor_dropdown_menu.currentText()}")
        if name == employee_data["workers"]["name"]:
            employee_data["supervisors"]["employees_in_shift"] = name

        # swap out the exec function for the popup and dismiss popup
        popup = captured_popup(submit_button)
        qtbot.wait(300)

        # Assert
        assert popup is not None
        assert "Successfully added all of the Production Worker details" in popup.text()
        print(f"Add worker popup text: {popup.text()}")
    return _params

# Safely Capturing and Dismissing Popup
@pytest.fixture
def captured_popup(app, qtbot, monkeypatch):
    """Fixture returns the _params function. The _params function returns the captured popup."""
    def _params(trigger_item):
        """Receives a trigger item, saves the popup, replaces the 'exec' method used with mock_exec, triggers the popup, and returns the popup object."""
        # Arrange
        captured_popup = []

        def mock_exec(self):
            """Saves the popup to the list, shows it non-modally, and returns Ok to simulate user click."""
            captured_popup.append(self)
            self.show()  # Show non-modally to prevent the test from stalling out
            qtbot.addWidget(self)  # Let qtbot manage the popup
            return QMessageBox.StandardButton.Ok

        monkeypatch.setattr(QMessageBox, 'exec', mock_exec)

        # Act
        # if the trigger item is a QAction/top menu object
        if isinstance(trigger_item, QAction):
            # use the trigger method to trigger the popup
            trigger_item.trigger()
        # if the trigger item is any other type of object such as a button
        else:
            # use a mouse click method on the item to trigger the popup
            qtbot.mouseClick(trigger_item, QtCore.Qt.MouseButton.LeftButton)

        # Wait for the popup to be displayed/saved before attempting to return the item
        qtbot.wait(300)

        return captured_popup[0]
    return _params

# Changes db filename to test_data.json to avoid overriding local db's
@pytest.fixture
def mock_save():
    """Saves data to the JSON database and returns boolean"""
    def __params(self):
        class NoInputError(Exception):
            """Exception raised when the user attempts to save an empty database"""
            pass

        try:
            print("Attempting to save data to file...")
            # generate employee dictionaries (results in tuple)
            data = self.generate_dictionaries()
            # if data exists and the dictionaries are not empty save the file
            if data and (data["supervisors"] != {} or data["workers"] != {}):
                # changing name of the file to test_data.json to avoid overriding local databases
                with open("test_data.json", "w") as file:
                    json.dump(data, file)
            else:  # else raise a value error
                raise NoInputError
        # remaining exceptions will be raised if processing fails
        except MemoryError:
            print("MemoryError: Not enough disk space to save data!")
            self.file_status_indicator.setText("Error: Not enough memory on "
                                               "the disk to save file! Please "
                                               "free up some memory on your "
                                               "device before proceeding!")
            self.file_status_indicator.adjustSize()
            return False
        except PermissionError:
            print("PermissionError: No permission to save file!")
            self.file_status_indicator.setText("Error: You do not have "
                                               "the correct file permissions "
                                               "to save this file!")
            self.file_status_indicator.adjustSize()
            return False
        except NoInputError:
            print("NoInputError (Custom): No data available to save!")
            self.file_status_indicator.setText("Error: No data to save! "
                                               "Please add employees before "
                                               "attempting to save!")
            self.file_status_indicator.adjustSize()
        except Exception as e:
            print("Exception: ", e)
            self.file_status_indicator.setText("Error: Something went wrong!")
            self.file_status_indicator.adjustSize()
        else:  # if no errors, set the status indicator to "Data saved!"
            self.file_status_indicator.setText("Data saved!")
            self.file_status_indicator.adjustSize()
            # adding console message for tracking
            print("Successfully saved data to JSON file!")
            return True
    return __params

@pytest.fixture
def save_fixture(app, monkeypatch, mock_save):
    def _save():
        # Arrange
        save_menu_item = app.file_save_menu_item
        status_indicator = app.file_status_indicator

        # Act
        monkeypatch.setattr(QAction, "triggered", mock_save(app))
        save_menu_item.trigger()

        # Assert
        assert status_indicator.text() == "Data saved!"
    return _save

# Loads test db (named test_data.json
@pytest.fixture
def mock_load():
    """Loads data from the JSON database and returns boolean"""
    def __params(self):
        """Loads data from the JSON database, converts complex structures
        back to original form (classes, enums, etc) and returns boolean"""
        # reset lists
        self.workers_array = []
        self.supervisors_array = []
        # reset dropdown options
        self.reset_dropdown_options()
        # reset display box
        self.display_box.clear()

        try:
            print("Attempting to load data from file...")
            with (open("test_data.json", "r") as file):
                data = json.load(file)
                for key, value in data.items():
                    if key == "supervisors":
                        for supervisor_subkey, subvalue in value.items():
                            name = supervisor_subkey
                            for subkey_detail_key, sub_detail_value in \
                                    subvalue.items():
                                if subkey_detail_key == "emp_num":
                                    emp_num = sub_detail_value
                                elif subkey_detail_key == "shift":
                                    shift = sub_detail_value
                                    # temp object
                                    temp = self.Employee()
                                    temp.set_shift_name_to_enum(shift)
                                elif subkey_detail_key == "salary":
                                    salary = sub_detail_value
                                elif subkey_detail_key == "max_workers":
                                    max_workers = sub_detail_value
                                elif subkey_detail_key == "array_of_prod_workers":
                                    array_of_prod_workers = sub_detail_value

                            self.supervisors_array.append(
                                self.ShiftSupervisor(name, emp_num, salary,
                                                temp.shift, max_workers))
                            # temporarily adding list of strings to the
                            # supervisor
                            self.supervisors_array[-1].array_of_prod_workers \
                                = array_of_prod_workers
                            # add the last supervisors_array item to the main
                            # dropdown
                            self.set_supervisor_dropdown_options()
                    if key == "workers":
                        # traverse the worker's value (subdictionary) for
                        # specific employee details
                        for worker_subkey, subvalue in value.items():
                            name = worker_subkey
                            # traverse sub_detail values and assign worker
                            # details
                            for subkey_detail_key, sub_detail_value in \
                                    subvalue.items():
                                if subkey_detail_key == "emp_num":
                                    emp_num = sub_detail_value
                                elif subkey_detail_key == "shift":
                                    shift = sub_detail_value
                                    temp = self.Employee()  # temp object
                                    temp.set_shift_name_to_enum(shift)
                                elif subkey_detail_key == "pay_rate":
                                    pay_rate = sub_detail_value
                                elif subkey_detail_key == "hours_worked":
                                    hours_worked = sub_detail_value
                                # the assigned supervisor will be handled in
                                # load_assigned_employees function below,
                                # default will be set automatically when
                                # constructing the class object in the meantime

                            # reconstruct the worker object
                            self.workers_array.append(
                                self.ProductionWorker(name, emp_num,
                                                 temp.shift, pay_rate,
                                                 hours_worked))

                            # add the last workers_array item to the main
                            # dropdown
                            self.set_workers_dropdown_options()

                # reconnecting the assigned worker to the supervisor
                # object
                self.load_assigned_employees(
                    self.supervisors_array, self.workers_array)



        except FileNotFoundError:
            print("FileNoneFoundError: No file found!")
            self.file_status_indicator.setText("Error: File not found! Please "
                                               "save data before continuing!")
            self.file_status_indicator.adjustSize()
            return False
        except json.JSONDecodeError:
            print("json.JSONDecodeError: Syntax Error in JSON file!")
            self.file_status_indicator.setText("Error: Something went wrong "
                                               "while trying to load the data!")
            self.file_status_indicator.adjustSize()
            return False
        except Exception as err:
            print(f"Exception: {err}")
            return False
        else:
            print("File loaded successfully!")
            self.file_status_indicator.setText("Data loaded!")
            self.file_status_indicator.adjustSize()
            return True
    return __params

@pytest.fixture
def display_fixture(app, qtbot):
        def _params(display_button, emp_dropdown, emp_type):
            # Arrange -- defining all empty fields
            button = display_button
            dropdown = emp_dropdown

            # Act
            # adds Test Employee details and confirms success popup
            qtbot.mouseClick(dropdown, QtCore.Qt.MouseButton.LeftButton)
            qtbot.wait(300)
            dropdown.setCurrentIndex(dropdown.findText(employee_data[emp_type]["name"]))
            qtbot.mouseClick(button, QtCore.Qt.MouseButton.LeftButton)
            return app.display_box.text()
        return _params

@pytest.fixture
def load_fixture(app):
    def _load():
        load_menu = app.file_load_menu_item
        status_indicator = app.file_status_indicator

        # Act - triggering error
        load_menu.trigger()  # clicking the load menu option
        return status_indicator.text()
    return _load


# Resources (test data) ----------------------------------------
employee_data = {"supervisors":{
    "name": "Test Supervisor",
    "emp_num": "123",
    "shift": "DAY",
    "salary": "51000",
    "max_workers": "2",
    "employees_in_shift": []
}, "workers":{
    "name": "Test Worker",
    "emp_num": "456",
    "shift": "DAY",
    "pay_rate": "10",
    "hours_worked": "10",
    "assigned_supervisor": "Test Supervisor"
}}

# Tests ----------------------------------------
# Main Window Test cases
def test_app_initializes_with_correct_title(app):
    # Arrange
    title = app.windowTitle()
    # Assert
    assert title == "Employee Management App"

def test_add_worker_with_no_supervisor_creates_warning(app, captured_popup):
    # Arrange / Act
    popup = captured_popup(app.input_worker_menu_item)

    # Assert
    assert popup is not None
    assert isinstance(popup, QMessageBox)
    assert "Unable to add any Production Workers because there are no \nSupervisors!" in popup.text()

def test_load_data_before_adding_employees_without_database_data_warning(app, monkeypatch):
    # Arrange
    load_menu = app.file_load_menu_item
    status_indicator = app.file_status_indicator

    # Act - triggering error
    monkeypatch.chdir("/") # changing the current working directory to the root directory to simulate clicking the loading button when there is no database present
    load_menu.trigger() # clicking the load menu option

    #Assert
    assert status_indicator.text() == "Error: File not found! Please save data before continuing!"

def test_add_supervisor_window_is_opened(add_supervisor_window, app):
    # Arrange elements
    supervisor_window = add_supervisor_window # the supervisor window also covers Act and triggers the menu item to open
    # Assert that the name of the window is correct
    assert supervisor_window.windowTitle() == "Add Supervisor"

def test_add_supervisor_and_confirm_a_new_supervisor_is_created(add_a_supervisor, app):
    # Arrange and Act -- adds supervisor details and confirms success popup, defaults are for Test Supervisor
    add_a_supervisor()

    # Assert
    assert app.supervisors_dropdown.count() == 2
    assert app.supervisors_dropdown.findText(employee_data["supervisors"]["name"]) != -1

def test_display_supervisor_data(add_a_supervisor, app, display_fixture):
    # Arrange -- defining all empty fields
    button = app.display_supervisor_button
    supervisor_dropdown = app.supervisors_dropdown

    # Act
    # adds Test Supervisor details and confirms success popup
    add_a_supervisor()
    display_box = display_fixture(button, supervisor_dropdown, "supervisors")

    # Assert
    assert app.supervisors_dropdown.currentText() == app.supervisors_array[0].get_name()
    assert employee_data["supervisors"]["name"] in display_box
    assert employee_data["supervisors"]["emp_num"] in display_box
    assert employee_data["supervisors"]["shift"] in display_box
    assert employee_data["supervisors"]["salary"] in display_box
    assert employee_data["supervisors"]["max_workers"] in display_box
    assert str(len(employee_data["supervisors"]["employees_in_shift"])) in display_box

def test_save_data_after_adding_supervisor(app, add_a_supervisor, save_fixture, load_fixture):
    # Additional Arrange, Act and Assert steps are parameterized in the save_fixture function
    add_a_supervisor()
    save_fixture()
    # loading the data back in to verify contents
    status = load_fixture()

    # assert
    assert app.supervisors_dropdown.findText(employee_data["supervisors"]["name"]) != -1
    assert status == "Data loaded!"

def test_add_worker(app, captured_popup, add_a_worker):
    # Arrange & Act
    # adding worker --> this function handles adding default Test Worker, loading existing test db with a supervisor and handling/verifying the correct popup success message
    add_a_worker()

    # Assert
    # verify that 1 more worker was added to dropdown
    assert app.workers_dropdown.count() == 2
    # verify that the worker's name can be found in the app's homescreen dropdown for workers
    assert app.workers_dropdown.findText(employee_data["workers"]["name"]) != -1

def test_display_worker_data(app, add_a_worker, display_fixture):
    # Arrange
    dropdown = app.workers_dropdown
    button = app.display_worker_button

    # Act
    add_a_worker() # adding default worker back
    # selecting worker and grabbing updated display box text
    display_box = display_fixture(button, dropdown, "workers")

    # Assert
    assert employee_data["workers"]["name"] in display_box
    assert employee_data["workers"]["emp_num"] in display_box
    assert employee_data["workers"]["shift"] in display_box
    assert employee_data["workers"]["pay_rate"] in display_box
    assert employee_data["workers"]["hours_worked"] in display_box
    assert employee_data["workers"]["assigned_supervisor"] in display_box

def test_save_data_after_adding_both_employee_types(app, add_a_worker, save_fixture, load_fixture):
    # Arrange/Act
    add_a_worker()
    save_fixture()
    # loading the data back in to verify contents
    load_fixture()

    # assert
    assert app.workers_dropdown.findText(employee_data["workers"]["name"]) != -1

def test_display_supervisor_data_after_adding_employees(app, add_a_worker, display_fixture):
    # Arrange
    button = app.display_supervisor_button
    supervisor_dropdown = app.supervisors_dropdown

    # Act
    add_a_worker()
    display_box = display_fixture(button, supervisor_dropdown, "supervisors")

    # Assert
    assert employee_data["supervisors"]["name"] in display_box
    assert employee_data["supervisors"]["employees_in_shift"] in display_box

# other test ideas:
# stress testing
# add a bunch of employees and supervisors
# save the database and assert success message
# remove 2 supervisors
# assert supervisor dropdown does not have 2 supervisors
# check 2 employees that worked in their shift and assert supervisor = No one
# load the database and assert no duplicates in employee lists and assert success message
# remove 2 workers
# assert they don't exist in the worker dropdown and assert they are no longer in supervisor's list