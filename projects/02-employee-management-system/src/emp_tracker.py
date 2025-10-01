from enum import Flag, auto

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QMainWindow, QApplication, QPushButton,
                             QMessageBox, \
                             QLabel, QComboBox, \
                             QLineEdit)
from PyQt6 import uic
import sys
import json

# App logic ------------------------------------------------
# shift ENUM for Employee Class ------------------------
class Shift(Flag):
    """Provide valid shifts for Employee class."""
    DAY = auto()
    SWING = auto()
    NIGHT = auto()
    ALL_SHIFTS = DAY | SWING | NIGHT

# employee class ------------------------
class Employee:
    """
    A class to represent a single employee.
        ...
        Attributes
        ----------
        Instance
            name: str
                first and last name of the employee
            shift: enum
                assigned shift of employee
            emp_num: int
                identifying number of employees between 100 and 999
            benefits: bool
                employee benefits status (True if benefits are available, False if not)
        Class
            DEFAULT_NAME: str
                the default name of employee when there is no valid input
            DEFAULT_EMP_NUM: int
                the default employee id set when there is no valid employee id
            DEFAULT_SHIFT: enum
                the default shift used when an invalid shift enum is entered
            MIN_EMP_NUM: int
                the minimum employee id number allowed
            MAX_EMP_NUM: int
                the maximum employee id number allowed
            BENEFIT_CUTOFF: int
                the cutoff number for employee benefits (used to determine or
                not an employee receives benefits)
        Methods
        -------
        Mutators
            set_name(name):
                sets name if the name is a string and is not empty. Otherwise, defaults
                to "unidentified".
            set_emp_num(emp_num):
                sets emp_num if emp_num is an integer and is between 100 and 999.
                Otherwise, defaults to 999. Also sets benefits if emp_num is between
                100 and 500.
            set_shift(shift):
                takes an enum and checks if valid enum. If valid, sets the enum
                and returns true, otherwise, it returns false
            set_shift_name_to_enum(shift):
                takes a string and converts it to the shift enum equivalent and
                returns a boolean
                if it exists, otherwise returns False.
        Accessors
            get_name():
                grab the name and return it
            get_emp_num():
                grab the employee number and return it
            get_shift():
                grab shift and return it
            get_benefits():
                grab the employee benefits status
        Helpers (Instance/Class)
            determine_benefits():
                validates whether the employee number is between 100 and 500. If so,
                benefits are set to true. Otherwise, benefits are set to false.
            valid_emp_num(emp_num):
                validates whether the employee number is between 100 and 999. Returns
                boolean.
            min_emp_num(emp_num):
                validates whether the employee number is greater than or equal to 100.
                Returns boolean.
            max_emp_num(emp_num):
                validates whether the employee number is less than or equal to 999.
                Returns boolean.
        Display
            __str__
        """
    # static constants
    DEFAULT_NAME = "unidentified"
    DEFAULT_EMP_NUM = 999
    DEFAULT_SHIFT = Shift.DAY

    MIN_EMP_NUM = 100
    MAX_EMP_NUM = 999

    BENEFIT_CUTOFF = 500

    def __init__(self, name = DEFAULT_NAME, emp_num = DEFAULT_EMP_NUM,
                 shift = DEFAULT_SHIFT):
        # Values set in set functions. If set functions fail, fallback to the
        # default values
        if not self.set_name(name):
            self.name = self.DEFAULT_NAME
        if not self.set_emp_num(emp_num):
            self.emp_num = self.DEFAULT_EMP_NUM
            self.benefits = self.determine_benefits()
        if not self.set_shift(shift):
            self.shift = self.DEFAULT_SHIFT

    # mutators ------------------------
    def set_name(self, name):
        """Set name if valid string and returns true, otherwise, returns
        false"""
        if not (type(name) == str and name.strip()):
            return False
        # else
        self.name = name
        return True

    def set_emp_num(self, emp_num):
        """Set the employee number if valid and returns true, otherwise,
        returns false"""
        if not self.valid_emp_num(emp_num):
            return False
        # else
        self.emp_num = emp_num
        self.benefits = self.determine_benefits()
        return True

    def set_shift(self, shift):
        """Takes an enum and checks if valid enum. If valid, sets the enum
        and returns true, otherwise, it returns false """
        if not shift in Shift.ALL_SHIFTS:
            return False
        # else
        self.shift = shift
        return True

    def set_shift_name_to_enum(self, shift):
        """Takes a string and converts it to the shift enum equivalent and
            returns a boolean"""
        if shift.upper() == "DAY":
            self.shift = Shift.DAY
            return True
        elif shift.upper() == "NIGHT":
            self.shift = Shift.NIGHT
            return True
        elif shift.upper() == "SWING":
            self.shift = Shift.SWING
            return True
        else: # invalid shift fallback on defaults specified in class defaults
            return False

    # accessors ------------------------
    def get_name(self):
        """Grab the name and return it"""
        return self.name

    def get_emp_num(self):
        """Grab the employee number and return it"""
        return self.emp_num

    def get_shift(self):
        """Grab shift and return it"""
        return self.shift

    def get_benefits(self):
        """Grab benefit status and return it"""
        return self.benefits

    # instance and class helpers ------------------------
    def determine_benefits(self):
        """
        Determine if the employee is eligible for benefits based on employee
        number.

        Returns:
            bool: boolean evaluating whether the employee number is below the
            benefit cutoff.
        """
        if self.emp_num >= self.BENEFIT_CUTOFF:
            return False
        # else
        return True

    @classmethod
    def valid_emp_num(cls, emp_num):
        """Check if employee number is within valid range and returns
        boolean."""
        if cls.min_emp_num(emp_num) and cls.max_emp_num(emp_num):
            return True
        # else
        return False

    @classmethod
    def min_emp_num(cls, emp_num):
        """Check if the employee number is greater than a minimum and returns
        boolean."""
        if emp_num >= cls.MIN_EMP_NUM:
            return True
        # else
        return False

    @classmethod
    def max_emp_num(cls, emp_num):
        """Check if the employee number is lower than a maximum and returns
        boolean."""
        if emp_num <= cls.MAX_EMP_NUM:
            return True
        # else
        return False

    # display ------------------------
    def __str__(self):
        benefits = "Benefits"
        if not self.benefits:
            benefits = f"No {benefits.lower()}"
        output = f"""\n{self.name} #{self.emp_num} ({benefits})"""
        return output

class ProductionWorker(Employee):
    """A subclass that of the Employee class and tracks info related to
    work time/pay
        ...
        Attributes
        ----------
        Instance
            pay_rate: int
                the hourly pay rate for the employee
            hours_worked: int
                number amount of hours an employee worked for the week
            assigned_supervisor: object, None
                the associated supervisor object assigned to this worker
        Class
            DEFAULT_NAME: str
                the default name of employee when there is no valid input
            DEFAULT_EMP_NUM: int
                the default employee id set when there is no valid employee id
            DEFAULT_SHIFT: enum
                the default shift used when an invalid shift enum is entered
            MIN_EMP_NUM: int
                The minimum employee id number allowed
            MAX_EMP_NUM: int
                the maximum employee id number allowed
            BENEFIT_CUTOFF: int
                the cutoff number for employee benefits (used to
                determine or not an employee receives benefits)
            DEFAULT_PAY_RATE: float
                the default pay rate used when there is no valid input
            DEFAULT_HOURS_WORKED: int
                the default hours used when there is no valid input
            MAX_PAY_RATE: int
                the maximum pay rate allowed
            MIN_PAY_RATE: int
                the minimum pay rate allowed
            MAX_HOURS_WORKED: int
                the maximum hours allowed
            MIN_HOURS_WORKED: int
                the minimum hours allowed
            REMOVED_SUPERVISOR_FALLBACK: str
                the default assigned supervisor name when there is no valid
                supervisor available
        Methods
        ---------
        Mutators
            set_pay_rate(pay_rate):
                set pay rate if valid int/float and returns true, otherwise,
                returns false
            set_hours_worked(hours_worked):
                set shift if valid enum and returns true, otherwise, returns
                false
            set_assigned_supervisor_obj(assigned_supervisor):
                set the assigned supervisor object if it's an instance of
                ShiftSupervisor and under the 'max worker spots limit' then
                return True, otherwise return False
            set_assigned_supervisor_name(assigned_supervisor):
                sets and stores assigned supervisor name, returns True if
                successful and False the 'if get_name method' fails.
                Allows fallback to activate if supervisor is not present
        Accessors
            get_pay_rate():
                Grab pay rate and return it
            get_hours_worked():
                Grab hours worked and return it
            get_assigned_supervisor_obj():
                grab the assigned supervisor object and return it
        Helpers (Instance/Class)
            validate_pay_rate(rate):
                Validates pay rate is between 0-20 and returns boolean.
            validate_hours_worked(hours):
                Validates hours worked is between 0-40 and returns boolean.
            gross_pay():
                Calculates pay based on pay rate and hours worked
        Display
            __str__
    """
    DEFAULT_NAME = Employee.DEFAULT_NAME
    DEFAULT_EMP_NUM = Employee.DEFAULT_EMP_NUM
    DEFAULT_SHIFT = Employee.DEFAULT_SHIFT
    DEFAULT_PAY_RATE: float = 1.00
    DEFAULT_HOURS_WORKED = 0
    MAX_PAY_RATE = 20
    MIN_PAY_RATE = 1
    MAX_HOURS_WORKED: int = 40
    MIN_HOURS_WORKED: int = 0
    REMOVED_SUPERVISOR_FALLBACK = "No one"

    def __init__(self, name = DEFAULT_NAME,
                 emp_num = DEFAULT_EMP_NUM,
                 shift = DEFAULT_SHIFT,
                 pay_rate = DEFAULT_PAY_RATE,
                 hours_worked = DEFAULT_HOURS_WORKED, assigned_supervisor =
                 None):
        # Pulling name and emp_num handling from Employee parent class
        super().__init__(name, emp_num, shift)
        # Values set in set functions. If set functions fail, fallback to the
        # default values
        if not self.set_pay_rate(pay_rate):
            self.pay_rate = self.DEFAULT_PAY_RATE
        if not self.set_hours_worked(hours_worked):
            self.hours_worked = self.DEFAULT_HOURS_WORKED
        print("Initializing supervisor obj fallback")
        if not self.set_assigned_supervisor_obj(assigned_supervisor):
            self.assigned_supervisor = self.REMOVED_SUPERVISOR_FALLBACK
            print(f"self.assigned_supervisor: {self.assigned_supervisor}")
        print("Initializing supervisor name fallback")
        if not self.set_assigned_supervisors_name(assigned_supervisor):
            self.assigned_supervisor_name = self.REMOVED_SUPERVISOR_FALLBACK
            print(f"self.assigned_supervisor_name: {self.REMOVED_SUPERVISOR_FALLBACK}")
        print("Done: Production Worker Successfully Initialized")

    # mutators ------------------------
    def set_pay_rate(self, pay_rate):
        """Set pay rate if valid int/float and returns true, otherwise, returns
        false"""
        if type(pay_rate) == float or type(pay_rate) == int:
            if self.validate_pay_rate(pay_rate):
                self.pay_rate = float(pay_rate)
                return True
            return False
        # else
        return False

    def set_hours_worked(self, hours_worked: int):
        """Set shift if valid enum and returns true, otherwise, returns false"""
        if type(hours_worked) == int and self.validate_hours_worked(
                hours_worked):
            self.hours_worked = hours_worked
            return True
        # else
        return False

    def set_assigned_supervisor_obj(self, assigned_supervisor):
        """Set the assigned supervisor if it's an instance of ShiftSupervisor and
        under the 'max worker spots limit' then return True, otherwise return
        False"""
        if isinstance(assigned_supervisor, ShiftSupervisor):
            try:
                assigned_supervisor.add_prod_worker(self)
            except:
                return False
            else:
                print(f"Assigning supervisor to the worker {self.name}")
                self.assigned_supervisor = assigned_supervisor
                print(f"Completed supervisor assignment for {self.name}")
                return True
        #else
        return False

    def set_assigned_supervisors_name(self, assigned_supervisor):
        """Sets and stores assigned supervisor name, returns True if
        successful and False the 'if get_name method' fails. Allows fallback
        to activate if the supervisor is not present"""
        try:
            print(f"Attempting to grab supervisor name in "
                  f"set_assigned_supervisor_name function")
            self.assigned_supervisor_name = assigned_supervisor.get_name()
        except:
            return False
        else:
            return True

    # accessors  ------------------------
    def get_pay_rate(self):
        """Grab the pay rate and return it"""
        return self.pay_rate

    def get_hours_worked(self):
        """Grab hours worked and return it"""
        return self.hours_worked

    def get_assigned_supervisor_obj(self):
        """Grab the assigned supervisor and return it"""
        return self.assigned_supervisor

    # instance helpers ------------------------
    @classmethod
    def validate_pay_rate(cls, rate: float):
        """Validates pay rate is between 0 -- 20 and returns boolean."""
        if cls.MIN_PAY_RATE <= rate <= cls.MAX_PAY_RATE:
            return True
        # else
        return False

    @classmethod
    def validate_hours_worked(cls, hours: int):
        """Validates hours worked are between 0 -- 40 and returns boolean"""
        if cls.MIN_HOURS_WORKED <= hours <= cls.MAX_HOURS_WORKED:
            return True
        # else
        return False

    def gross_pay(self):
        """Calculates pay based on pay rate and hours worked"""
        return self.pay_rate * self.hours_worked

    def __str__(self):
        output_str = "WORKER:"
        output_str += super().__str__()
        output_str += f"""\nShift: {self.shift.name}
${self.pay_rate:.2f} per hour
{self.hours_worked} hours this week
Gross pay: ${self.gross_pay():.2f}
Assigned Supervisor: {self.assigned_supervisor_name}\n"""
        return output_str

class ShiftSupervisor(Employee):
    """
    A subclass that of the Employee class and tracks info related to
    supervisors
        ...
        Attributes
        ----------
        Instance
            annual_salary: int
                supervisor's annual salary/pay
            max_worker_spots: int
                the maximum amount of workers a supervisor can have in their shift
            array_of_prod_workers: list
                array of ProductionWorker objects that the supervisor is
                currently supervising on supervisor's shift
            current_spots_taken: int
                the active count of production workers currently working on
                supervisor's shift
        Class
            DEFAULT_NAME: str
                the default name of employee when there is no valid input
            DEFAULT_EMP_NUM: int
                the default employee id set when there is no valid employee id
            DEFAULT_SHIFT: enum
                the default shift used when an invalid shift enum is entered
            DEFAULT_ANNUAL_SALARY: int:
                the default annual salary set when there is no valid input
            MAX_ANNUAL_SALARY: int
                the highest allowed annual salary
            MIN_ANNUAL_SALARY: int
                the lowest allowed annual salary
            DEFAULT_MAX_WORKER_SPOTS: int
                the default maximum amount of workers a supervisor can have in
                their shift when no number is provided
            MIN_MAX_WORKER_SPOTS: int
                the minimum amount of workers a supervisor can have in their
                shift
            MIN_WORKERS_NEEDED_FOR_BONUS: int
                the minimum amount of workers a supervisor would need have in
                their shift to get a bonus
            SUPERVISOR_BONUS: int
                the of money awarded to a supervisor for meeting the
                minimum workers quota required for a bonus

        Methods
        ---------
        Mutators
            set_annual_salary(annual_salary):
                sets supervisor's annual salary if valid int and returns True,
                otherwise returns false
            set_max_worker_spots(max_worker_spots):
                Set the limit of workers a supervisor can accept on their shift
            add_prod_worker(prod_worker_obj):
                Validates and adds production workers to the array of workers if
                they are in the supervisor's shift and the shift is not full.
                boolean
            appends the message to the list of errors. Returns boolean
        Accessors
            get_annual_salary():
                Grab annual salary and return it
            get_max_worker_spots():
                grab max worker spots and return it
            get_array_of_prod_workers():
                grab current worker spots and return it
        Helpers (Instance/Class)
            valid_salary(salary):
                Checks if salary is valid and returns boolean
            shift_valid(prod_worker_obj):
                Checks if shift is valid and returns boolean
            bonus
                Validates if supervisor has enough workers in their shift to
                receive a bonus, adds them and returns boolean
            add_bonus(salary, bonus):
                Calculates supervisor's new salary after bonus
        Display
            __str__
    """
    DEFAULT_NAME = Employee.DEFAULT_NAME
    DEFAULT_EMP_NUM = Employee.DEFAULT_EMP_NUM
    DEFAULT_SHIFT = Employee.DEFAULT_SHIFT
    DEFAULT_ANNUAL_SALARY: int = 50000

    MAX_ANNUAL_SALARY: int = 200000
    MIN_ANNUAL_SALARY: int = 50000
    DEFAULT_MAX_WORKER_SPOTS: int = 10
    DEFAULT_MIN_MAX_WORKER_SPOTS: int = 0

    MIN_WORKERS_NEEDED_FOR_BONUS: int = 5
    SUPERVISOR_BONUS: int = 10000

    def __init__(self, name = DEFAULT_NAME, emp_num = DEFAULT_EMP_NUM,
                 annual_salary = DEFAULT_ANNUAL_SALARY, shift = DEFAULT_SHIFT,
                 max_worker_spots = DEFAULT_MAX_WORKER_SPOTS):
        # Pulling name and emp_num handling from Employee parent class
        super().__init__(name, emp_num, shift)
        # Values set in set functions. If set functions fail, fallback to the
        # default values
        if not self.set_annual_salary(annual_salary):
            self.annual_salary = self.DEFAULT_ANNUAL_SALARY
        if not self.set_max_worker_spots(max_worker_spots):
            self.max_worker_spots = self.DEFAULT_MAX_WORKER_SPOTS

        self.array_of_prod_workers = []
        self.current_spots_taken = 0

    # mutators ------------------------
    def set_annual_salary(self, annual_salary):
        """Set annual salary if valid int and within the valid range, then
        returns boolean"""
        if type(annual_salary) != int and not self.valid_salary(
                annual_salary):
            return False
        # else
        self.annual_salary = int(annual_salary)
        return True

    def set_max_worker_spots(self, max_worker_spots):
        """Set the limit of workers a supervisor can accept on their shift"""
        if not type(max_worker_spots) == int:
            return False
        # else
        self.max_worker_spots = max_worker_spots
        return True

    def add_prod_worker(self, prod_worker_obj):
        """Validates and adds production workers to the array of workers if
        they are in the supervisor's shift and the shift is not full. Returns
        boolean"""
        if self.shift_valid(prod_worker_obj):
            if self.current_spots_taken == self.max_worker_spots:
                return False
            else:
                self.current_spots_taken += 1
                # check if the worker is already on the list
                if prod_worker_obj in self.array_of_prod_workers:
                    return False
                # if not, then add the worker
                self.array_of_prod_workers.append(prod_worker_obj)
                return True
        else:
            return False

    # accessors ------------------------
    def get_annual_salary(self):
        """Grab annual salary and return it"""
        return self.annual_salary

    def get_max_worker_spots(self):
        """Grab max worker spots and return it"""
        return self.max_worker_spots

    def get_array_of_prod_workers(self):
        """Grab current worker spots and return it"""
        return self.array_of_prod_workers

    # class/instance helpers ------------------------
    @classmethod
    def valid_salary(cls, salary):
        """Checks if salary is valid and returns boolean"""
        if cls.MIN_ANNUAL_SALARY <= salary <= cls.MAX_ANNUAL_SALARY:
            return True
        # else
        return False

    def shift_valid(self, prod_worker_obj):
        """Checks if shift is valid and returns boolean"""
        if prod_worker_obj.get_shift() == self.shift:
            return True
        # else
        return False

    def bonus(self, current_array_spots_taken):
        """Validates if a supervisor has enough workers in their shift to
        receive a bonus, adds them and returns boolean"""
        if current_array_spots_taken >= self.MIN_WORKERS_NEEDED_FOR_BONUS:
            self.annual_salary += self.add_bonus(self.annual_salary,
                                                 self.SUPERVISOR_BONUS)
            return True
        # else
        return False

    @staticmethod
    def add_bonus(salary, bonus):
        """Calculates supervisor's new salary after bonus"""
        return salary + bonus

    # output ------------------------
    def __str__(self):
        output_str = "SUPERVISOR:"
        output_str += super().__str__()
        output_str += f"""\nSalary: ${self.annual_salary}
Shift: {self.shift.name}
{self.current_spots_taken} worker(s) in their shift:
"""
        # printing any errors
        for prod_worker in self.array_of_prod_workers:
            output_str += f"\n{prod_worker.get_name()}"
        return output_str

# GUI ------------------------------------------------------
# Main Window Class
class Main(QMainWindow):
    """
    A class to represent the main window GUI logic/behavior
     ...
        Attributes
        ----------
        Instance (Non-UI Components Only)
            emp_type: str
                the type of employee being added/modified
            supervisors_array: list
                list of all supervisors
            workers_array: list
                list of all workers
            no_input_error: bool
                blocked submission: critical error indicates whether a missing
                input needs attention (user has entered no required fields)
            invalid_input_error: bool
                non-blocked warning: indicates warning of invalid data types
                were entered by the user which will be replaced by defaults (
                does not block submission)
            array_limit_error: bool
                 blocked submission: Indicates whether user has reached maximum
                 array capacity
            range_error: bool
                non-blocked warning: Indicates whether user has entered data
                that is out of  range
            no_supervisor error: bool
                blocked submission: Indicated no supervisors in the system.
            shift_mismatch_error: bool:
                blocked submission: Indicates whether user has attempted to
                add a worker to a supervisor that has a non-matching shift
                (e.g., Jack's shift = NIGHT, Mary's Shift = DAY)
            worker_cap_error: bool:
                blocked submission: Indicates whether user has attempted to
                add more workers than the supervisor's maximum worker spots.
            invalid_input_error: list
                an array of items the user has incorrectly added (range
                error or invalid inputs error).
        Class
            MAX_SUPERVISORS_LIMIT: int
                the maximum amount of supervisors in the system.
            MAX_WORKERS_LIMIT: int
                the maximum amount of workers a supervisor can accept on their
                shift

        Methods
        ---------
        Mutators
            set_shift_to_enum:
                Sets Shift dropdown text to shift enum equivalent and returns True
                if it exists, otherwise returns False.
        Accessors
            get_emp_type:
                Grabs the employee type and returns it.
        Event Handlers
            save():
                Saves data to the JSON database in a dictionary, list and
                string structure and returns boolean
            load()
                loads data from the JSON database, converts complex structures
                back to original form (classes, enums, etc.) and returns boolean
            remove(label):
                removes the object from UI and lists. Returns True if successful
                and False if not.
            open_worker_window()
                validates that supervisors are in the system, then initializes a
                ProductionWorkerWindow instance with passback and popup logic.
                Returns Boolean.
            open_supervisor_window():
                Validates that supervisors are in the system, then initializes a
                ProductionWorkerWindow instance with passback and popup logic.
                Returns Boolean.
            send_data_back_to_main(emp_type, item = None)
                Appends added item to worker/supervisor arrays and returns
                Boolean.
        Mutators
            set_supervisor_dropdown_options:
                Adds the last item of the supervisor's array to the drop-down
                menu.
            set_workers_dropdown_options:
                Adds the last item of the supervisor's array to the drop-down
                menu.
        Accessors
            get_dropdown_text(emp_type):
                Grabs text from the drop-down selected.
            get_supervisor_obj_by_name(input_name):
                Grabs supervisor from the supervisor list and returns
                the object if found, return None if not found.
            get_worker_obj_by_name(input_name):
                Grabs the worker from the worker list and returns the object if
                found, return None if not found.
        Instance Helpers and Class Methods
            load_assigned_employees(self, supervisors_array, workers_array):
                loads all objects in shift assignment positions (supervisor's
                list of workers and worker's assigned supervisor and returns
                true
            reset_dropdown_options():
                resets the drop-down menu options to the default values
            generate_dictionaries():
                generates a JSON serializable dictionary from the employee
                arrays and returns it.
            valid_nums
                validates that input is an integer and returns it.
            max_supervisor_limit
                 validates whether the supervisor array is full
            validate_supervisor_available():
                Validates whether there are any supervisors added to the system
        Output/Display
            show_popup(emp_type, no_input_error, array_limit_error,
                   invalid_input_error, range_error, no_supervisor_error,
                   shift_mismatch_error = None,
                   worker_cap_error = None,
                   invalid_inputs_array = None):
                Alerts user of success/failure to add items.
            display(button_text, emp_type):
                Displays selected supervisors and workers in the main window
                label.
    """
    MAX_SUPERVISORS_LIMIT = 3
    MAX_WORKERS_LIMIT = 5

    def __init__ (self):
        super(Main, self).__init__()

        # loading window UI files ---------
        uic.loadUi("mainwindow__ui.ui", self)

        # defining widgets ---------
        # > main window widgets
        # >> main window supervisor labels
        self.supervisors_dropdown = self.findChild(QComboBox,
                                                   "supervisors_comboBox")
        self.display_supervisor_button = self.findChild(QPushButton,
                                                        "display_supervisor_button")

        # >> main window worker labels
        self.workers_dropdown = self.findChild(QComboBox, "prodws_comboBox")
        self.display_worker_button = self.findChild(QPushButton,
                                                        "display_prodw_button")

        # >> main window output area labels
        """Debugging statement: may not need the scroll area"""
        self.display_box = self.findChild(QLabel, "display_box")

        # >> main window menubar labels
        self.file_load_menu_item = self.findChild(QAction, "actionLoad")
        self.file_save_menu_item = self.findChild(QAction, "actionSave")
        self.input_supervisor_menu_item = self.findChild(QAction,
                                                         "input_supervisor_menu_item")
        self.input_worker_menu_item = self.findChild(QAction,
                                                    "input_prodw_menu_item")
        self.remove_worker_menu_item = self.findChild(QAction,
                                                     "remove_prodw_menu_item")
        self.remove_supervisor_menu_item = self.findChild(QAction,
                                                          "remove_supervisor_menu_item")

        # file status indicator/label
        self.file_status_text_label = self.findChild(QLabel,
                                                     "file_status_text_label")
        self.file_status_indicator = self.findChild(QLabel,
                                                    "file_status_indicator")

        # naming window
        self.setWindowTitle("Employee Management App")

        # __init__ Logic Begins  ---------
        print("---------- Main Window Initialized ----------")
        self.emp_type = None
        self.supervisors_array = []
        self.set_supervisor_dropdown_options()
        self.workers_array = []
        self.set_workers_dropdown_options()

        # errors for worker and supervisor ui classes
        self.no_input_error = False
        self.invalid_input_error = False
        self.array_limit_error = False
        self.range_error = False
        self.no_supervisor_error = False
        self.shift_mismatch_error = False
        self.worker_cap_error = False
        self.invalid_inputs_array = []

        # connecting display buttons to display function
        self.display_supervisor_button.clicked.connect(
            lambda: self.display(self.display_supervisor_button.text(),
                                 "Supervisor")
        )
        self.display_worker_button.clicked.connect(
            lambda: self.display(self.display_worker_button.text(),
                                 "Production Worker")
        )

        # menu signals connecting File > Save and File > Load actions
        self.file_load_menu_item.triggered.connect(self.load)
        self.file_save_menu_item.triggered.connect(self.save)

        # menu signals connecting inputs to corresponding open window functions
        self.input_worker_menu_item.triggered.connect(self.open_worker_window)
        self.input_supervisor_menu_item.triggered.connect(
            self.open_supervisor_window)

        # connecting remove functions to remove menu items
        self.remove_worker_menu_item.triggered.connect(
            lambda: self.remove(self.remove_worker_menu_item.text()))
        self.remove_supervisor_menu_item.triggered.connect(
            lambda: self.remove(self.remove_supervisor_menu_item.text()))

        # showing app ---------
        self.show()

    # event handlers --------------------------------------------------------
    def save(self):
        """Saves data to the JSON database and returns boolean"""
        try:
            print("Attempting to save data to file...")
            # generate employee dictionaries (results in tuple)
            data = self.generate_dictionaries()
            # if data exists and the dictionaries are not empty save the file
            if data and (data["supervisors"] != {} or data["workers"] != {}):
                with open("data.json", "w") as file:
                    json.dump(data, file)
            else: # else raise a value error
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
        else: # if no errors, set the status indicator to "Data saved!"
            self.file_status_indicator.setText("Data saved!")
            self.file_status_indicator.adjustSize()
            # adding console message for tracking
            print("Successfully saved data to JSON file!")
            return True

    def load(self):
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
            with (open("data.json", "r") as file):
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
                                    temp = Employee()
                                    temp.set_shift_name_to_enum(shift)
                                elif subkey_detail_key == "salary":
                                    salary = sub_detail_value
                                elif subkey_detail_key == "max_workers":
                                    max_workers = sub_detail_value
                                elif subkey_detail_key == "array_of_prod_workers":
                                    array_of_prod_workers = sub_detail_value

                            self.supervisors_array.append(
                                ShiftSupervisor(name, emp_num, salary,
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
                                    temp = Employee() # temp object
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
                                ProductionWorker(name, emp_num,
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

    def remove(self, label):
        """removes the object from UI and lists. Returns True if successful
        and False if not."""
        name = self.get_dropdown_text(label)
        if label == "Supervisor":
            # search for the supervisor object by name
            supervisor_object = self.get_supervisor_obj_by_name(name)

            # filter through the array to find the object
            if supervisor_object in self.supervisors_array:
                # finding combobox index of supervisors name
                index = self.supervisors_dropdown.findText(name)

                # deleting supervisor from dropdown
                self.supervisors_dropdown.removeItem(index)

                # clearing display
                self.display_box.clear()

                # remove file status error's for consistency
                self.file_status_indicator.setText("Status: N/A")
                self.file_status_indicator.adjustSize()

                # grabbing workers assigned to supervisor
                assigned_workers = supervisor_object.get_array_of_prod_workers()

                # looping through to update their assigned supervisors to "No
                # one"
                for worker in assigned_workers:
                    worker_index = self.workers_array.index(worker)
                    # setting assigned supervisor to default fallback
                    self.workers_array[worker_index].assigned_supervisor_name = \
                            self.workers_array[worker_index].REMOVED_SUPERVISOR_FALLBACK
                    print(f"Assigned supervisor after reset:"
                          f" {worker.assigned_supervisor_name}")

                print(f"Supervisor list length before removal:"
                      f" {len(self.supervisors_array)}")
                # removing supervisor from the array
                self.supervisors_array = list(filter(
                    lambda supervisor: supervisor != supervisor_object,
                    self.supervisors_array))
                print(f"Supervisor list length after removal:"
                      f" {len(self.supervisors_array)}")
                return True
            else:
                print(f"Supervisor item not found/removed. List Length:"
                      f" {len(self.supervisors_array)}")
                return False
        # else: if the label signals removal of a Worker
        name = self.get_dropdown_text(label)
        worker_object = self.get_worker_obj_by_name(name)
        if worker_object in self.workers_array:
            # finding combobox index of supervisors name
            index = self.workers_dropdown.findText(name)

            # deleting supervisor from dropdown
            self.workers_dropdown.removeItem(index)

            # clearing display
            self.display_box.clear()

            print(f"Worker list length before removal:"
                  f" {len(self.workers_array)}")
            # removing supervisor from the array
            self.workers_array = list(filter(
                lambda worker: worker != worker_object,
                self.workers_array))
            print(f"Worker list length after removal:"
                  f" {len(self.workers_array)}")
            return True
        else:
            print(f"Worker item not found/removed. List Length:"
                  f" {len(self.workers_array)}")
            return False

    def open_worker_window(self):
        """Validates that supervisors are in the system then initializes a
        ProductionWorkerWindow instance with passback and popup logic.
        Returns Boolean."""
        self.emp_type = "Production Worker"
        try:
            if not self.validate_supervisors_available():
                raise NoSupervisorsError
        except NoSupervisorsError:
            self.no_supervisor_error = True
            self.show_popup(self.emp_type, self.no_input_error,
                            self.array_limit_error, self.invalid_input_error,
                            self.range_error, self.no_supervisor_error)
            self.no_supervisor_error = False # clearing out error after popup
        except Exception as err:
            print(f"Exception: {err}")
        else:
            self.worker_window = ProductionWorkerWindow(self, passback_to_main \
            = lambda: (self.send_data_back_to_main(self.emp_type)))

    def open_supervisor_window(self):
        """Validates that supervisors have not reached max capacity,
        then opens a supervisor input form with passback functionality.
        Returns Boolean."""
        self.emp_type = "Supervisor"
        try:
            if not self.max_supervisor_limit(self.supervisors_array):
                raise IndexError
        except IndexError:
            self.array_limit_error = True
            self.show_popup(self.emp_type, self.no_input_error,
                            self.array_limit_error, self.invalid_input_error,
                            self.range_error, self.no_supervisor_error)
            self.array_limit_error = False # clearing out error after popup
        except Exception as err:
            print(f"Exception: {err}")
        else:
            self.supervisor_window = SupervisorWindow(
                self, passback_to_main = lambda: (
                    self.send_data_back_to_main(self.emp_type)
                ))

    def send_data_back_to_main(self, emp_type, item = None):
        """Appends added item to worker/supervisor arrays and returns
        Boolean."""
        if emp_type == "Supervisor":
            self.supervisors_array.append(item)
            print(f"Length of supervisors_array after adding new item in Main: "
                  f"{len(self.supervisors_array)}")
            self.set_supervisor_dropdown_options()
            self.file_status_indicator.setText("Status: N/A")
            self.file_status_indicator.adjustSize()
            return True
        if emp_type == "Production Worker":
            self.workers_array.append(item)
            print(f"Length of workers_array after adding new item in Main: "
                  f"{len(self.workers_array)}")
            self.set_workers_dropdown_options()
            self.file_status_indicator.setText("Status: N/A")
            self.file_status_indicator.adjustSize()
            return True
        return False

    # mutators  --------------------------------------------------------------

    def set_supervisor_dropdown_options(self):
        """Adds the last item from the supervisors array to the drop-down
        menu."""
        if len(self.supervisors_array) > 0:
            self.supervisors_dropdown.addItem(
                self.supervisors_array[-1].get_name())
            return True
        # else
        return False

    def set_workers_dropdown_options(self):
        """Adds the last item from the worker's array to the drop-down menu."""
        if len(self.workers_array) > 0:
            self.workers_dropdown.addItem(self.workers_array[-1].get_name())
            return True
        # else
        return False

    # accessors  --------------------------------------------------------------
    def get_dropdown_text(self, emp_type):
        """Grabs text from the drop-down selected."""
        if emp_type.title() == "Production Worker":
            name = self.workers_dropdown.currentText()
            return name
        # else
        name = self.supervisors_dropdown.currentText()
        return name

    def get_supervisor_obj_by_name(self, input_name):
        """Grabs supervisor from the supervisor list and returns the object if
                found, return None if not found."""
        print(f"length of supervisor array: {len(self.supervisors_array)}")
        # input_name = input_name.split()[0] # commenting this out b/c I don't remember why this is needed and it interferes with names that have spaces.
        for supervisor in self.supervisors_array:
            if supervisor.get_name() == input_name:
                print(f"\nSupervisor {input_name} found!")
                return supervisor
        print(f"Search for {input_name} did not find a match (default was selected)")
        return None

    def get_worker_obj_by_name(self, input_name):
        """Grabs worker from the worker list and returns the object if
                found, return None if not found."""
        for worker in self.workers_array:
            if worker.get_name() == input_name:
                print(f"\nWorker {input_name} found!")
                return worker
        print("No such worker found (default dropdown item was selected)")
        return None

    # instance helpers and class methods  -------------------------------------
    def load_assigned_employees(self, supervisors_array, workers_array):
        """Loads all objects in shift assignment positions (supervisor's
        list of workers and worker's assigned supervisor and returns
        true."""
        # loop through all supervisors
        for supervisor in supervisors_array:
            # check the supervisor's list of workers
            for k in range(len(supervisor.array_of_prod_workers)):
                # if the supervisor's list of workers are still strings
                if type(supervisor.array_of_prod_workers[k]) == str:
                    # grab the workers name
                    worker_name_from_supervisor_list = (\
                        supervisor.array_of_prod_workers)[k]

                    # loop through the workers array
                    for worker in workers_array:
                        # check if the worker's name matches the name from
                        # the supervisor's list
                        if worker.get_name() == worker_name_from_supervisor_list:
                            # add the worker object to the supervisor's list
                            supervisor.array_of_prod_workers[k] = worker
                            # add the supervisor to the worker's assigned
                            # supervisor attribute
                            worker.set_assigned_supervisor_obj(supervisor)
                            worker.set_assigned_supervisors_name(supervisor)
        return True

    def reset_dropdown_options(self):
        """Resets the drop-down menu options to the default values."""
        self.supervisors_dropdown.clear() # clear supervisor dropdown
        self.workers_dropdown.clear() # clear worker dropdown
        # set default text for each
        self.supervisors_dropdown.addItem("SELECT SUPERVISOR")
        self.workers_dropdown.addItem("SELECT WORKER")
        return True

    def generate_dictionaries(self):
        """Generates a JSON serializable dictionary from the employee
        arrays and returns it."""
        employees_dict = {"supervisors": {}, "workers": {}}

        print("Generating dictionaries...")
        print("Processing supervisor dictionary...")
        for supervisor in self.supervisors_array:
            name = supervisor.get_name()
            emp_num = supervisor.get_emp_num()
            shift = str(supervisor.get_shift().name)
            salary = supervisor.get_annual_salary()
            max_workers = supervisor.get_max_worker_spots()
            array_of_prod_workers = []
            # looping through the array to grab names of workers
            for worker in supervisor.get_array_of_prod_workers():
                # only grabbing names because JSON does not support class obj's
                array_of_prod_workers.append(worker.get_name())

            data = {"emp_num": emp_num, "shift": shift,
                    "salary": salary, "max_workers": max_workers,
                    "array_of_prod_workers": array_of_prod_workers}

            employees_dict["supervisors"][name] = data
        print("Completed generation of supervisor dictionary.")

        try:
            print(f"""Current employees dict: 
                        supervisors --> {employees_dict["supervisors"]}
                        workers --> {employees_dict["workers"]}""")
        except KeyError:
            print("No employees found when trying to add supervisors!")
        except Exception as err:
            print(f"Exception: {err}")
        print("Processing worker dictionary...")

        for worker in self.workers_array:
            name = worker.get_name()
            emp_num = worker.get_emp_num()
            shift = str(worker.get_shift().name)
            pay_rate = worker.get_pay_rate()
            hours_worked = worker.get_hours_worked()
            assigned_supervisor_name = str(worker.get_assigned_supervisor_obj().name)
            data = {"emp_num": emp_num, "shift": shift,
                    "pay_rate": pay_rate, "hours_worked": hours_worked,
                    "assigned_supervisor_name": assigned_supervisor_name}

            employees_dict["workers"][name] = data
        print("Completed generation of worker's dictionary.")

        try:
            print(f"""Current employees dict: 
                        supervisors --> {employees_dict["supervisors"]}
                        workers --> {employees_dict["workers"]}""")
        except KeyError:
            print("No employees found when trying to add workers!")
        except Exception as err:
            print(f"Exception: {err}")
        print("Successfully generated dictionaries for JSON serialization")
        return employees_dict

    @staticmethod
    def valid_nums(instance_var, float_type = False):
        """Validates that input is an integer and returns it."""
        if float_type:
            try:
                print(f"float type verification: '{instance_var}")
                instance_var = float(instance_var)
            except ValueError:
                print("float false")
                return False
            else:
                print("float evaluated true")
                return instance_var
        # else if not a float type
        try:
            print(f"int type verification: '{instance_var}'")
            instance_var = int(instance_var)
        except ValueError:
            print("int false")
            return False
        else:
            print("int true")
            return instance_var

    @classmethod
    def max_supervisor_limit(cls, supervisors_array):
        """Validates whether the supervisor array is full"""
        if len(supervisors_array) < cls.MAX_SUPERVISORS_LIMIT:
            return True
        # else
        return False

    def validate_supervisors_available(self):
        """Validates whether there are any supervisors added to the system"""
        if len(self.supervisors_array) == 0:
            return False
        # else
        return True
    # output  -----------------------------------------------------------------
    @staticmethod
    def show_popup(emp_type, no_input_error, array_limit_error,
                   invalid_input_error, range_error, no_supervisor_error,
                   shift_mismatch_error = None,
                   worker_cap_error = None,
                   invalid_inputs_array = None):
        """Alerts user of success/failure to add items."""
        # initiating a popup object (MessageBox)
        msg = QMessageBox()
        # sending error type values to the console for tracking
        print(f"""emp_type: {emp_type} | no_input_error: {no_input_error} | 
              array_limit_error: {array_limit_error} | 
              no_supervisor_error: {no_supervisor_error}  | 
              invalid_input_error: {invalid_input_error} | 
              range_error: {range_error} | 
              shift_mismatch_error: {shift_mismatch_error} | 
              worker_cap_error: {worker_cap_error} | 
              invalid_inputs_array: {invalid_inputs_array}""")

        # if the user attempts to create Production Worker input window,
        # but there are no supervisors created in the supervisor's array
        if no_supervisor_error:
            msg.setWindowTitle("Error")
            msg.setText(f"""Unable to add any {emp_type}s because there are no 
Supervisors! Please add a Supervisor before proceeding!""")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return False

        # if the user attempts to add a worker to a supervisor with a different
        # shift (e.g., worker shift = Day, supervisor shift = Night)
        if shift_mismatch_error:
            msg.setWindowTitle("Error")
            msg.setText(f"""{emp_type} details were not added, because
the assigned supervisor is in a different shift! Assigned supervisors and 
workers MUST be on the same shift!""")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return False

        # if the user does not input any required fields
        if no_input_error:
            msg.setWindowTitle("Error")
            msg.setText(f"""{emp_type} details were not added, because 
there are required fields missing!""")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return False

        # if the user attempts to add more employees than a supervisor's max
        # worker limit
        elif worker_cap_error:
            msg.setWindowTitle("Error")
            msg.setText(f"""Maximum worker spots reached! You are unable to add 
                    any more {emp_type}s to the this supervisor's workers, because 
                    they've run out of open worker spots for this shift!""")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return False

        # if the user attempts to add invalid data types
        elif invalid_input_error or range_error:
            msg.setWindowTitle("Warning")
            labels = ('\n'.join(invalid_inputs_array)).replace('*', '')
            msg.setText(f"""The {emp_type} was added, but the following 
{emp_type} details were invalid or out of range and replaced with default 
values: \n\n{labels}""")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()
            return True

        # if the user attempts to add more employees than the defined array
        # limit
        elif array_limit_error:
            msg.setWindowTitle("Error")
            msg.setText(f"""You are unable to add any more {emp_type}s to the
{emp_type} list, because you've reached the maximum limit for adding 
{emp_type}s!""")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return False

        # if the user has added valid required entries and no other errors exist
        else:
            msg.setWindowTitle(f"{emp_type} Added")
            msg.setText(
                f"""Successfully added all of the {emp_type} details to the 
{emp_type} list!""")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            return True

    def display(self, button_text, emp_type):
        """Displays selected supervisors and workers in the main window
        label."""
        selected_name = self.get_dropdown_text(emp_type)
        print(f"selected name {selected_name}")
        if "Worker" in button_text:
            worker = self.get_worker_obj_by_name(selected_name)
            self.display_box.setText(str(worker))
            return True
        # else
        print(f"the length of the supervisor array is: "
              f"{len(self.supervisors_array)}")
        if "Supervisor" in button_text:
            supervisor = self.get_supervisor_obj_by_name(selected_name)
            self.display_box.setText(str(supervisor))
            return True
        return False

# Production Worker Window Class
class ProductionWorkerWindow(Main):
    """
     class to represent the input Production Worker GUI logic/behavior
     ...
        Attributes
        ----------
        Instance
            name: str
                production worker name
            num: int
                production worker employee number
            hours_worked: int
                production worker hours worked
            payrate: float
                production worker's pay rate
            temp_obj: ProductionWorker, cls
                A temporary object used to access ProductionWorker methods,
                such as shift
            shift: enum
                production worker's assigned shift
            assigned_supervisor: None, class
                production worker's assigned supervisor if one exists
            main: class
                the passed instance of the parent class to main
            __supervisors_array: list
                private supervisor's array taken from the main window
            __workers_array: list
                private worker's array taken from the main window
            supervisor_obj: class
                specific supervisor assigned to the production worker
            emp_type: str
                the type of employee (`supervisor or worker)
        Class
            DEFAULT_SUPERVISOR: str
                the default assigned supervisor dropdown text
        Methods
        ---------
        Mutators
            add_supervisors_to_dropdown():
                Grabs supervisors from the array and adds them to assigned
                supervisors combobox.
        Event Handlers
            clicked():
                Checks if the production worker was added on submit, sends it to
                the main window and closes the production worker window.
            handle_worker_submit():
                Sets worker attributes, checks if array has space, if so,
                adds worker to the list, otherwise an error is displayed and
                returns Boolean
        Instance Helpers and Class Methods
            clear_worker_input_fields():
                Resets production worker input fields in GUI to empty/index 0 and
                returns True
            validate_matching_shift(worker_shift, supervisor):
                Validates that workers shift matches assigned supervisor and
                returns True otherwise, returns false
            validate_max_worker_limit_supervisor(self, supervisor_object):
                Validates whether supervisor has spots open for new worker in their
                worker array and returns a boolean
    """
    DEFAULT_SUPERVISOR: str = "SUPERVISOR"

    def __init__(self, parent_class, passback_to_main =
    None):
        super(ProductionWorkerWindow, self).__init__()
        # Loading Window UI Files ---------
        uic.loadUi("prodw_input__window.ui", self)

        # Defining Widgets ---------
        # > worker input window widgets
        self.worker_name_label = self.findChild(QLabel, "prodw_name_label")
        self.worker_name_input = self.findChild(QLineEdit, "prodw_name_input")
        self.worker_emp_num_input = self.findChild(QLineEdit,
                                                  "prodw_emp_num_input")
        self.worker_emp_num_label = self.findChild(QLabel,
                                                  "prodw_emp_num_label")
        self.worker_shift_dropdown = self.findChild(QComboBox,
                                                   "prodw_shift_dropdown")
        self.worker_shift_label = self.findChild(QLabel, "prodw_shift_label")
        self.worker_payrate_input = self.findChild(QLineEdit,
                                                  "prodw_payrate_input")
        self.worker_payrate_label = self.findChild(QLabel, "prodw_payrate_label")
        self.worker_hours_worked_input = self.findChild(QLineEdit,
                                                       "prodw_hours_worked_input")
        self.worker_hours_worked_label = self.findChild(QLabel,
                                                       "prodw_hours_worked_label")
        self.worker_assign_supervisor_dropdown = self.findChild(QComboBox,
                                                               "prodw_assign_supervisor_combobox")
        self.enter_worker = self.findChild(QPushButton, "enter_prodw")

        # naming window
        self.setWindowTitle("Add Production Worker")

        # Worker Window Logic Here ---------
        print("---------- Production Worker Window Initialized ----------")
        # initializing worker instance variables
        self.name = ProductionWorker.DEFAULT_NAME
        self.num = ProductionWorker.DEFAULT_EMP_NUM
        self.hours_worked = ProductionWorker.DEFAULT_HOURS_WORKED
        self.payrate = ProductionWorker.DEFAULT_PAY_RATE
        # will be used to grab and validate shift during submit
        print("Creating a temp ProductionWorker object..")
        self.temp_obj = ProductionWorker()
        print("Temp ProductionWorker object created!")
        self.shift = self.temp_obj.DEFAULT_SHIFT
        self.assigned_supervisor = None
        # reinitializing main class in ProductionWorkerWindow for functionality
        self.main = parent_class
        # initializing private array variables (keeping array local for memory)
        self.__supervisors_array = self.main.supervisors_array
        self.__workers_array = []
        # add assigned supervisor option names if they exist
        self.add_supervisors_to_dropdown()
        self.supervisor_obj = None

        # if any errors, with initial submit before creating objects, gen emp
        # details will be the type referenced in the popup
        self.emp_type = "Production Worker"

        # Note: errors set to false by default from Main class

        # enter worker button connected to clicked validation function
        self.enter_worker.clicked.connect(self.clicked)

        # Showing App ---------
        self.show()

    # mutators ---------------------------------------
    def add_supervisors_to_dropdown(self):
        """Grabs supervisors from the array and adds them to assigned
        supervisors combobox"""
        for supervisor in self.__supervisors_array:
            name = supervisor.get_name()
            shift = supervisor.get_shift().name
            self.worker_assign_supervisor_dropdown.addItem(f"{name} ({shift})")
        return True

    # event handlers --------------------------------------------------------
    def clicked(self):
        """Checks if a production worker was added on submit, sends it to
        the main window and closes the production worker window."""
        if self.handle_worker_submit():
            self.main.send_data_back_to_main(
                self.emp_type,
                item = self.__workers_array[0]
            )
            print("length of workers array after sending back from "
                  "Production Worker Window class: ", len(self.__workers_array))
            self.close()
        return None

    def handle_worker_submit(self):
        """Sets worker attributes, checks if the array has space, if so,
        adds worker to the list, otherwise an error is displayed.
        Returns Boolean"""
        # assigning worker-specific attribute input values
        self.name = self.worker_name_input.text()
        # grabbing assigned supervisor text and removing the text ' (SHIFT)' from it
        self.assigned_supervisor = self.worker_assign_supervisor_dropdown.currentText().split(" (")[0]
        self.shift = self.worker_shift_dropdown.currentText()
        self.payrate = self.worker_payrate_input.text()
        self.hours_worked = self.worker_hours_worked_input.text()
        self.num = self.worker_emp_num_input.text()

        # transforming shift input, validating and setting it to enum
        if not self.temp_obj.set_shift_name_to_enum(str(
                self.shift)):
            self.temp_obj.shift = self.temp_obj.DEFAULT_SHIFT
            self.invalid_inputs_array.append(
                self.worker_shift_label.text())
            self.shift_mismatch_error = True
        # else:
        #     self.temp_obj.shift = self.temp_obj.set_shift(self.temp_obj.shift)
        print("set_shift_name_to_enum() was successful")

        # initialize truthy value (avoids warnings in IDE)
        successfully_added = False
        try:
            # validating that user input exists for the assigned supervisor
            # dropdown and that text is not default
            if self.assigned_supervisor != self.DEFAULT_SUPERVISOR:
                # if populated, grab the text and return the object
                self.supervisor_obj = self.main.get_supervisor_obj_by_name(
                    self.assigned_supervisor)
                # validating whether the shifts match
                if not self.validate_matching_shift(self.temp_obj,
                                                    self.supervisor_obj):
                    # raise ShiftMismatchError if validation fails
                    raise ShiftMismatchError
            else:
                self.supervisor_obj = None

            # if the assigned supervisor dropdown is set to default or all of
            # the following (pay rate, hours worked, employee number) are
            # blank, raise a ValueError
            if (self.assigned_supervisor == self.DEFAULT_SUPERVISOR
                    or (not (self.payrate or self.hours_worked or self.num))):
                raise ValueError
        except ShiftMismatchError:
            print(f"Shift Mismatch Error was raised.")
            self.shift_mismatch_error = True
        except ValueError:
            print("Value error was raised")
            self.no_input_error = True
        except Exception as err:
            print(f"Exception was raised: {err}")
        else:
            # validate that input is not invalid, if so, defaults will be used
            if not self.name:
                self.name = ProductionWorker.DEFAULT_NAME
                self.invalid_inputs_array.append(
                    self.worker_name_label.text())
                self.invalid_input_error = True

            # validating whether the employee number is an integer
            if not self.valid_nums(self.num):
                self.num = ProductionWorker.DEFAULT_EMP_NUM
                self.invalid_inputs_array.append(
                    self.worker_emp_num_label.text())
                self.invalid_input_error = True
            else:
                self.num = int(self.worker_emp_num_input.text())
                if not ProductionWorker.valid_emp_num(self.num):
                    self.num = ProductionWorker.DEFAULT_EMP_NUM
                    self.invalid_inputs_array.append(
                        self.worker_emp_num_label.text())
                    self.range_error = True

            # validating whether the pay rate is a float or integer (can be
            # either)
            if not self.valid_nums(self.payrate, float_type = True):
                self.payrate = ProductionWorker.DEFAULT_PAY_RATE
                self.invalid_inputs_array.append(
                    self.worker_payrate_label.text())
                self.invalid_input_error = True
            else:
                self.payrate = float(self.worker_payrate_input.text())
                if not ProductionWorker.validate_pay_rate(self.payrate):
                    self.payrate = ProductionWorker.DEFAULT_PAY_RATE
                    self.invalid_inputs_array.append(
                        self.worker_payrate_label.text())
                    self.range_error = True

            # validating whether hours worked is an integer
            if not self.valid_nums(self.hours_worked):
                self.hours_worked = ProductionWorker.DEFAULT_HOURS_WORKED
                self.invalid_inputs_array.append(
                    self.worker_hours_worked_label.text())
                self.invalid_input_error = True
            else:
                self.hours_worked = int(self.worker_hours_worked_input.text())
                if not ProductionWorker.validate_hours_worked(self.hours_worked):
                    self.hours_worked = ProductionWorker.DEFAULT_HOURS_WORKED
                    self.invalid_inputs_array.append(
                        self.worker_hours_worked_label.text())
                    self.range_error = True

            # Sending data to the console log for tracking purposes
            print(f"""Final values collected for Production Worker: 
                        name = {self.name}
                        employee number = {self.num}
                        shift = {self.temp_obj.shift}
                        pay rate = {self.payrate}
                        hours worker = {self.hours_worked}
                        assigned supervisor object = \
{type(self.supervisor_obj)}""")

            # checking whether a supervisor has worker spots open in their
            # worker array before adding a new instance
            if self.validate_max_worker_limit_supervisor(self.supervisor_obj):
                # add production worker
                print("About to create new worker object...")
                worker = ProductionWorker(self.name, self.num,
                                               self.temp_obj.shift,
                                               self.payrate,
                                               self.hours_worked,
                                               self.supervisor_obj)
                print("Worker object created successfully")
                self.__workers_array.append(worker)
                print(f"Production Worker added to array from inside the "
                      f"ProductionWorkerWindow class!")
                successfully_added = True
        finally:
            # always show the popup to describe success/failure/warnings
            if self.show_popup(self.emp_type, self.no_input_error,
                              self.array_limit_error, self.invalid_input_error,
                               self.range_error, self.no_supervisor_error,
                               shift_mismatch_error = self.shift_mismatch_error,
                               worker_cap_error = self.worker_cap_error,
                               invalid_inputs_array = self.invalid_inputs_array):
                # clear/reset all fields
                self.clear_worker_input_fields()
                print(f"Status: successfully_added = {successfully_added}")
                return successfully_added

            # clear/reset all fields
            self.clear_worker_input_fields()
        print(f"Status: successfully_added = {successfully_added}")
        return successfully_added

    # instance helpers and class methods  -------------------------------------
    def clear_worker_input_fields(self):
        """Resets production worker input fields in GUI to empty/index 0 and
        returns True"""
        # clearing form fields and resetting dropdowns to index 0
        self.worker_emp_num_input.clear()
        self.worker_name_input.clear()
        self.worker_shift_dropdown.setCurrentIndex(0)
        self.worker_assign_supervisor_dropdown.setCurrentIndex(0)
        self.worker_payrate_input.clear()
        self.worker_hours_worked_input.clear()

        # resetting popup error flags
        self.no_input_error = False
        self.array_limit_error = False
        self.invalid_input_error = False
        self.range_error = False
        self.shift_mismatch_error = False
        self.worker_cap_error = False
        self.invalid_inputs_array = []
        return True

    @staticmethod
    def validate_matching_shift(worker, supervisor):
        """Validates that workers shift matches assigned supervisor and
        returns True otherwise, returns false"""

        print(f"""comparing worker's shift: {worker.get_shift()} 
to supervisor's shift: {supervisor.get_shift()}""")

        # Worker's enum name is extracted and compared to the supervisors enum
        # name
        if worker.get_shift() != supervisor.get_shift():
            print(f"""mismatch shift found in validate_matching_shift_function
                returning value: 
{not (worker.get_shift() != supervisor.get_shift())}""")
            return False
        # else
        print(f""" matching shift found in validate matching shift function
    returning value: 
{not (worker.get_shift() != supervisor.get_shift())}""")
        return True

    def validate_max_worker_limit_supervisor(self, supervisor_object):
        """Validates whether a supervisor has spots open for the new worker in
        their worker array and returns a boolean"""
        try:
            print("Initiating validate max worker limit function "
                  "(checking if worker can be assigned to supervisor)")
            if (supervisor_object.current_spots_taken ==
                    supervisor_object.max_worker_spots):
                raise IndexError
        except IndexError:
            print("IndexError raised")
            # popup error flag: worker_cap_error set to true
            self.worker_cap_error = True
            return False
        except Exception as err:
            print(f"Exception was raised: {err}")
            return False
        else:
            return True

# Supervisor Window Class
class SupervisorWindow(Main):
    """
      class to represent the input Supervisor GUI logic/behavior
      ...
         Attributes
         ----------
         Instance
            emp_type: str
                the type of employee (`supervisor or worker`)
            name: str
                the supervisor name
            num: int
                the supervisor's employee number
            temp_supervisor_obj: Supervisor, cls
                a temporary object used to access Supervisor methods, such as
                the shift
            shift: enum
                the supervisor's shift
            salary: int
                the supervisor's salary
            max_workers: int
                the maximum number of workers the supervisor can have on
                their shift
            main: class
                the parent class from the Main class
            __supervisors_array: list
                a private array of the supervisor's list
        Class
            SUPERVISOR_ARRAY_LIMIT: int
                the maximum amount of supervisors in the system.

         Methods
         ---------
         Event Handlers
            clicked():
                checks if supervisor was added on submit, sends it to the main.
                Returns nothing.
            handle_supervisor_submit():
                grabs supervisor attributes, validates them and adds them to an
                instance and supervisor array. Returns boolean.
         Instance Helpers and Class Methods
            validate_supervisor_array_limit(supervisors_array):
                validates whether the supervisor array has reached its limit and
                returns True if so, otherwise returns False
            clear_supervisor_input_fields():
                resets the supervisor input form in the GUI to empty
                values/first index for dropdowns and returns True
     """

    SUPERVISOR_ARRAY_LIMIT: int = Main.MAX_SUPERVISORS_LIMIT

    def __init__(self, parent_class, passback_to_main =
    None):
        super(SupervisorWindow, self).__init__()

        # Loading Window UI Files ---------
        uic.loadUi("supervisor_input__window.ui", self)

        # Defining Widgets ---------
        # > supervisor input window widgets
        self.supervisor_name_label = self.findChild(QLabel,
                                                 "supervisor_name_label")
        self.supervisor_name_input = self.findChild(QLineEdit,
                                                    "supervisor_name_input")
        self.supervisor_emp_num_input = self.findChild(QLineEdit,
                                                       "supervisor_emp_num_input")
        self.supervisor_emp_num_label = self.findChild(QLabel,
                                                       "supervisor_emp_num_label")
        self.supervisor_shift_dropdown = self.findChild(QComboBox,
                                                        "supervisor_shift_dropdown")
        self.supervisor_shift_label = self.findChild(QLabel,
                                                     "supervisor_shift_label")
        self.supervisor_salary_input = self.findChild(QLineEdit,
                                                      "supervisor_salary_input")
        self.supervisor_salary_label = self.findChild(QLabel,
                                                      "supervisor_salary_label")
        self.supervisor_max_workers_input = self.findChild(QLineEdit,
                                                    "supervisor_max_workers_input")
        self.supervisor_max_workers_label = self.findChild(QLabel,
                                                    "supervisor_max_workers_label")
        self.enter_supervisor = self.findChild(QPushButton, "enter_supervisor")

        # naming window
        self.setWindowTitle("Add Supervisor")

        # Supervisor Window Logic Here ----------------------------
        print("---------- Supervisor Window Initialized ----------")
        self.emp_type = "Supervisor"
        self.name = ShiftSupervisor.DEFAULT_NAME
        self.num = ShiftSupervisor.DEFAULT_EMP_NUM
        # will be used to grab and validate shift during submit
        print("Creating a temp ShiftSupervisor object..")
        self.temp_supervisor_obj = ShiftSupervisor()
        print("Temp ShiftSupervisor object created!")
        self.shift = self.temp_supervisor_obj.DEFAULT_SHIFT
        self.salary = ShiftSupervisor.DEFAULT_ANNUAL_SALARY
        self.max_workers = ShiftSupervisor.DEFAULT_MAX_WORKER_SPOTS
        self.main = parent_class
        self.__supervisors_array = []

        # form submission button connected to clicked validation function
        self.enter_supervisor.clicked.connect(self.clicked)

        # showing Window
        self.show()

    # event handlers --------------------------------------------------------
    def clicked(self):
        """Checks if supervisor was added on submit, sends it to the main.
        Returns nothing."""
        # if submission was successful
        if self.handle_supervisor_submit():
            # call the send_data_back_to_main function and pass in the item
            # created from the submission
            self.main.send_data_back_to_main(
                self.emp_type,
                item = self.__supervisors_array[0]
            )
            # Show length to console for ease of debugging later/tracking
            print(f"Length of __supervisors_array after sending back from "
                  f"inside the SupervisorWindow class:"
                  f" {len(self.__supervisors_array)}")
            self.close()
        return

    def handle_supervisor_submit(self):
        """Grabs supervisor attributes, validates them and adds them to an
        instance and supervisor array. Returns boolean."""
        # grab input text for comparisons
        self.name = self.supervisor_name_input.text()
        self.num = self.supervisor_emp_num_input.text()
        self.shift = self.supervisor_shift_dropdown.currentText()
        self.salary = self.supervisor_salary_input.text()
        self.max_workers = self.supervisor_max_workers_input.text()

        # initialize truthy value (avoids warnings in IDE)
        successfully_added = False
        try:
            if not (self.num or self.salary or self.max_workers):
                raise ValueError
        except ValueError:
            # if none of the required fields (employee number, salary and max
            # workers are filled), raise a value error.
            print("No input error raised (Value Error)")
            self.no_input_error = True
        except Exception as err:
            print(f"Exception was raised: {err}")
        else:
            # validate that input is not invalid, if so, defaults will be used
            # validating supervisor name is present. Invalid input error flag
            # will be raised in the popup if any invalid values
            if not self.name:
                self.name = ShiftSupervisor.DEFAULT_NAME
                self.invalid_inputs_array.append(
                    self.supervisor_name_label.text())
                self.invalid_input_error = True

            # validating supervisor employee number is an integer
            if not self.valid_nums(self.num):
                self.num = ShiftSupervisor.DEFAULT_EMP_NUM
                self.invalid_inputs_array.append(
                    self.supervisor_emp_num_label.text())
                self.invalid_input_error = True
            else:
                self.num = int(self.num)
                if not ShiftSupervisor.valid_emp_num(self.num):
                    self.num = ShiftSupervisor.DEFAULT_EMP_NUM
                    self.invalid_inputs_array.append(
                        self.supervisor_emp_num_label.text())
                    self.range_error = True

            # transforming shift input, validating and setting it to enum
            if not self.temp_supervisor_obj.set_shift_name_to_enum(str(
                    self.shift)):
                self.temp_supervisor_obj.shift = ShiftSupervisor.DEFAULT_SHIFT
                self.invalid_inputs_array.append(
                    self.supervisor_shift_label.text())
                self.invalid_input_error = True

            # validating supervisor salary is an integer
            if not self.valid_nums(self.salary):
                self.salary = ShiftSupervisor.DEFAULT_ANNUAL_SALARY
                self.invalid_inputs_array.append(
                    self.supervisor_salary_label.text())
                self.invalid_input_error = True
            else:
                self.salary = int(self.supervisor_salary_input.text())
                if not ShiftSupervisor.valid_salary(self.salary):
                    self.salary = ShiftSupervisor.DEFAULT_ANNUAL_SALARY
                    self.invalid_inputs_array.append(
                        self.supervisor_salary_label.text())
                    self.range_error = True

            # validating supervisor max worker is an integer
            if not self.valid_nums(self.max_workers):
                self.max_workers = ShiftSupervisor.DEFAULT_MAX_WORKER_SPOTS
                self.invalid_inputs_array.append(
                    self.supervisor_max_workers_label.text())
                self.invalid_input_error = True
            else:
                self.max_workers = int(self.supervisor_max_workers_input.text())

            print(f"""Final values collected for supervisor: 
            name = {self.name}
            employee number = {self.num}
            salary = {self.salary}
            shift = {self.temp_supervisor_obj.shift}
            max_workers = {self.max_workers}""")

            # add supervisor
            if self.validate_supervisor_array_limit(self.__supervisors_array):
                shift_supervisor = ShiftSupervisor(self.name, self.num,
                                                self.salary,
                                                self.temp_supervisor_obj.shift,
                                                self.max_workers)
                self.__supervisors_array.append(shift_supervisor)
                print(f"Supervisor added to supervisor array from the "
                      f"SupervisorWindow class")
                successfully_added = True
        finally:
            # always show the popup to describe success/failure/warnings
            if self.show_popup(self.emp_type, self.no_input_error,
                               self.array_limit_error, self.invalid_input_error,
                               self.range_error,
                               self.no_supervisor_error,
                               invalid_inputs_array =
                               self.invalid_inputs_array):
                # clear/reset all fields
                self.clear_supervisor_input_fields()
                return successfully_added
            # clear/reset all fields
            self.clear_supervisor_input_fields()
        return successfully_added

    # instance helpers and class methods  -------------------------------------
    @classmethod
    def validate_supervisor_array_limit(cls, supervisors_array):
        """Validates whether the supervisor array has reached its limit and
        returns True if so, otherwise returns False"""
        if len(supervisors_array) < cls.SUPERVISOR_ARRAY_LIMIT:
            return True
        # else
        return False

    def clear_supervisor_input_fields(self):
        """Resets the supervisor input form in the GUI to empty values/first
        index for dropdowns and returns True"""
        self.supervisor_emp_num_input.clear()
        self.supervisor_name_input.clear()
        self.supervisor_shift_dropdown.setCurrentIndex(0)
        self.supervisor_salary_input.clear()
        self.supervisor_max_workers_input.clear()

        # instance var reset
        self.array_limit_error = False
        self.no_input_error = False
        self.invalid_input_error = False
        self.range_error = False
        self.invalid_inputs_array = []
        return True

# Exception Classes
class NoSupervisorsError(Exception):
    """Exception raised when the user attempts to add a Production Worker
    when there are no Supervisors in the system"""
    pass

class ShiftMismatchError(Exception):
    """Exception raised when the user attempts to add Production Worker to
    Supervisor in a different shift"""
    pass

class NoInputError(Exception):
    """Exception raised when the user attempts to save an empty database"""
    pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = Main()
    app.exec()



