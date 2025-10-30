import numpy as np
import copy
from abc import ABC, abstractmethod

class BarcodeABC(ABC):
    """Defines the I/O and basic methods of any barcode class
    ...
    Attributes
    ----------
    bc: BarcodeImage
        The image data of the barcode
    text: str
        The text data of the barcode
    ----------
    Subclass: InfoBox(BarcodeABC)

    ----------
    Abstract Methods
        scan(bc):
            Accepts an image represented as BarcodeImage, stores it and
            returns a boolean.

            Basic InfoBox option will be an exact clone of this method. No text
            translation is allowed within this method.
        read_text(text):
            Read the text to be encoded into an image and return a boolean. No
            image translation is allowed here.
        generate_image_from_text():
            Decodes internal text stored in the implementing class and produces a
            companion BarcodeImage (or in the format of the implementing class).
            Results in a complimentary image and text representation of the
            barcode and returns a boolean.
        translate_image_to_text():
            Translate the image from the implementing class into a string.
        display_text_to_console():
            Display the text to the console.
        display_image_to_console()
            Display the image to the console.

    """
    def __init__(self, bc, text):
        self.bc = bc
        self.text = text

    @abstractmethod
    def scan(self, bc):
        """Accepts an image represented as BarcodeImage, stores it and
        returns a boolean

        Basic InfoBox option will be an exact clone of this method. No text
        translation is allowed within this method."""
        self.bc = bc
        return True

    @abstractmethod
    def read_text(self, text):
        """Read the text to be encoded into an image and return a boolean. No
        image translation is allowed here."""
        self.text = text
        return True

    @abstractmethod
    def generate_image_from_text(self):
        """Decodes internal text stored in the implementing class and produces a
        companion BarcodeImage (or in the format of the implementing class).
        Results in a complimentary image and text representation of the
        barcode and returns a boolean."""
        pass

    @abstractmethod
    def translate_image_to_text(self):
        """Translate the image from the implementing class into a string."""
        pass

    @abstractmethod
    def display_text_to_console(self):
        """Display the text to the console."""
        pass

    def display_image_to_console(self):
        """Display the image to the console."""
        pass

class BarcodeImage:
    """Manages optical data of a barcode. Contain some methods for storing,
    modifying and retrieving the data in a 2D image. The interpretation of
    the data is not part of this class.
    ...
    Attributes
    ----------
    General
        data: str, BarcodeImage
            Used to store the data to be encoded into an image or text input.
        image_data: 2D List
            A 2D list of integers representing binary image data.
        active_row: int
            The current row of the image being processed.
        active_col: int
            The current column of the image being processed.
    Misc Variables
        MAX_WIDTH: int
            The maximum width of the image.
        MAX_HEIGHT: int
            The maximum height of the image.
        BLACK_CHAR_BINARY: int
            The binary value of a black pixel.
        WHITE_CHAR_BINARY: int
            The binary value of a white pixel.

    Methods
    ----------
    Mutators
        set_pixel(row, col, value):
            Sets the value of the pixel at the specified row and column to the
            specified value.
    Accessors
        get_pixel(row, col):
            Returns the value of the pixel at the specified row and column.
    Instance Helpers
        check_size(data):
            Checks the size of the data to be encoded and returns a boolean.
    """
    MAX_WIDTH = 65
    MAX_HEIGHT = 30
    BLACK_CHAR_BINARY: int = 1
    WHITE_CHAR_BINARY: int = 0

    def __init__(self, str_data = None):
        self.data = str_data
        # check if the data is a sub-instance of the class
        if isinstance(self.data, BarcodeImage):
            # if so, extract the data attribute so we can grab the list
            self.data = str_data.data

        # initialize 2D List
        self.image_data = [[0 for row in range(BarcodeImage.MAX_WIDTH)]
        for col in range(BarcodeImage.MAX_HEIGHT)]
        # setting max column width
        self.image_data_col = BarcodeImage.MAX_WIDTH
        # tracking active row for the loop starting from the bottom
        self.active_row = BarcodeImage.MAX_HEIGHT - 1
        # tracking active column for the loop starting from the left
        self.active_col = 0
        # check if the size of the data is within valid image_data bounds
        if self.check_size(self.data):
            # traverse each line in the image going from bottom to top row
            for line_index in range(len(self.data) - 1, -1, -1):
                # traverse each character in the line going from left to right
                for char_index in range(len(self.data[line_index])):
                    # if the character is a black marking
                    if self.data[line_index][char_index] == "*":
                        # set the pixel to 1 in the binary image_data array
                        self.set_pixel(self.active_row,
                                       self.active_col,
                                       self.BLACK_CHAR_BINARY)
                    # advance to the next column
                    self.active_col += 1
                # after exhausting characters in the string: advance to the
                # next row/item (descending) in the list and reset col
                self.active_row -= 1
                self.active_col = 0

    # mutators -----------------------------------------------------------
    def set_pixel(self, row, col, value):
        """Sets the value of the pixel at the specified row and column to the
        specified value."""
        # if the pixel is not equal to an empty space
        if self.get_pixel(row, col) != " ":
            # set the pixel to the designated value
            self.image_data[row][col] = value
            return True
        # else
        return False
    # accessors -----------------------------------------------------------
    def get_pixel(self, row, col):
        """Returns the value of the pixel at the specified row and column."""
        if row <= self.MAX_HEIGHT and col <= self.MAX_WIDTH:
            return self.image_data[row][col]
        # else
        return False

    # instance helper ------------------------------------------------------
    def check_size(self, data):
        """Checks the size of the data to be encoded and returns a boolean."""
        # if the data is less than the max height
        if len(data) < self.MAX_HEIGHT:
            # loop through the data (array) to check if the columns are less
            # than the max width
            for i in range(len(data)):
                if len(data[i]) > self.MAX_WIDTH:
                    # return false if columns bigger than width
                    return False
            # return True if columns and height are within range
            return True
        # else
        return False

class InfoBox(BarcodeABC):
    """Implementation of the BarcodeABC abstract class, where barcodes are
    generated into text and the text can be generated out of an image.
    ...
    Attributes
    ----------
    General
        actual_width: int
            The computed width of the image.
        actual_height: int
            The computed width of the image.
        image: BarcodeImage, None
            The image data of the barcode.
        text: str, None
            The text data of the barcode.
    Misc Variables
        BLACK_CHAR: str
            An asterisk that represents a black pixel in the image.
        WHITE_CHAR: str
            A space that represents a white pixel in the image.
        BINARY_BASE: int
            The base used to calculate binary values during image<>text
            conversion.

    Methods
    ----------
    Mutators
        read(text):
            Read the text to be encoded into an image and return a boolean. No
            image translation is allowed here.
        scan(image):
            Accepts an image represented as the BarcodeImage object, and stores
            it and returns a boolean.

            No text translation is allowed within this method.
        generate_image_from_text():
            Decodes internal text stored and produces a companion BarcodeImage
            and returns a boolean.
        translate_image_to_text():
            Translate the image into a string and return a boolean.
        generate_image_side_border(col_index, row_index):
            Generates an open or closed side border for the image and
            returns a boolean.
        generate_image_bottom_border(col_index, row_index):
            Generates a closed limitation line border for bottom row and
            returns boolean.
        generate_image_top_border(col_index, row_index):
            Generates a closed limitation line border for top row and returns
            a boolean.
    Accessors
        get_actual_height():
            Grab the actual height of the image.
        get_actual_width():
            Grab the actual width of the image.
    Instance Helpers
        compute_signal_height():
            Analyze the spine of the array to compute the image height.
            Returns a boolean.
        compute_signal_width():
            Analyze the spine of the array to compute the image width. Return
            boolean.
        set_ordinal_array():
            Creates an array of ordinal values from stored text and returns
            the array.
    Display Methods
        display_image_to_console():
            Displays the image to the console.
        display_text_to_console():
            Display the text to the console.
    """
    BLACK_CHAR: str = "*"
    WHITE_CHAR: str = " "
    BINARY_BASE: int = 2

    def __init__(self, image = None, text = None):
        super().__init__(image, text)
        # initialize width and height values as 0
        self.actual_width = 0
        self.actual_height = 0
        # set the image to input/default value
        self.image = image
        # if the image input is an instance of BarcodeImage
        if isinstance(self.image, BarcodeImage):
            # scan the image
            self.scan(image)
            # set text to default
            self.text = None
        # else leave image as default and read the text instead
        self.read_text(text)

    # mutators -----------------------------------------------------------
    def read_text(self, text):
        """Read the text to be encoded into an image and return a boolean. No
        image translation is allowed here"""
        # if text input exists
        if text:
            self.text = text # set the text to the input
            return True
        # else
        return True

    def scan(self, image):
        """Accepts an image represented as the BarcodeImage object, and stores
        it and returns a boolean

        No text translation is allowed within this method"""
        if image: # if an image input exists
            # make a deep copy of it
            self.image.image_data = copy.deepcopy(image.image_data)
            # compute the height
            self.compute_signal_height()
            return True
        # else
        return False

    def generate_image_from_text(self):
        """Decodes internal text stored and produces a companion BarcodeImage
        and returns a boolean."""
        ordinal_arr = self.set_ordinal_array() # adding text to an array
        self.image = BarcodeImage(self.text) # constructing image memory space
        top_row = self.image.MAX_HEIGHT - 11 # setting max height
        bottom_row = self.image.MAX_HEIGHT - 1 # finding bottom row
        self.actual_width = len(self.text) + 2 # +2 to accommodate side borders
        bit_position = 0
        bit = self.BINARY_BASE ** bit_position # starting at bit 1

        # starting from the bottom row going up
        for row_index in range(bottom_row, top_row, -1):
            # starting from the left column going right
            for col_index in range(self.actual_width):
                # if on the bottom row, generate the closed limitation line
                if row_index == bottom_row:
                    self.generate_image_bottom_border(col_index, row_index)
                # if on the top row, generate the closed limitation line
                elif row_index - 1 == top_row:
                    self.generate_image_top_border(col_index, row_index)
                # if on the side columns, generate the appropriate borders
                elif col_index == 0 or col_index == self.actual_width - 1:
                    self.generate_image_side_border(col_index, row_index)
                # if the position is a barcode position
                else:
                    # comparing ordinal value to bit value
                    if ordinal_arr[col_index - 1] & bit:
                        # adding +1 binary value if bit found
                        self.image.image_data[row_index][col_index] = (
                            self.image.BLACK_CHAR_BINARY)
            # only shift the bit right if not constructing the border
            if row_index != bottom_row:
                bit = bit << 1
        self.compute_signal_height() # compute height to set the final image
        return True

    def translate_image_to_text(self):
        """Translate the image into a string and return a boolean."""
        # create memory space for the binary array
        ordinal_arr = copy.deepcopy([0] * (self.get_actual_width() - 2))
        # start at the row right under the top border of the image
        start_row = self.get_actual_height() + 1
        # end at the last row (bottom border will be excluded in range)
        end_row = BarcodeImage.MAX_HEIGHT
        # start at column 1 to remove the left-most border
        start_col = 1
        # end at second to last column to remove the right-most border
        end_col = self.get_actual_width() - 1
        # initiate the bit position
        bit_position = 7
        bit = self.BINARY_BASE ** bit_position # calculate bit
        # traverse each row starting from the top of the image going down
        for row in range(start_row, end_row):
            # traverse each column going from left to right
            for col in range(start_col, end_col):
                # if the image value at index row, col is == 1 or truthy
                if self.image.image_data[row][col]:
                    # add the ordinal value to the array. Subtracting
                    # col - 1 since the loop starts at column 1 to remove the
                    # border (column 0), but the ordinal array starts at index 0
                    ordinal_arr[col - 1] += bit
            # advance bit position
            bit = bit >> 1

        # updating self.text to empty string to add the message
        self.text = ""
        for i in ordinal_arr:
            # converting each number in the array to a character value
            binary_string = chr(i)
            # assigning text attribute to the string value
            self.text += binary_string
        return True

    def generate_image_side_border(self, col_index, row_index):
        """Generates an open or closed side border for the image and
        returns a boolean"""
        # if the item is in the first column, generate the closed limitation
        # line
        if col_index == 0:
            self.image.image_data[row_index][col_index] = (
                self.image.BLACK_CHAR_BINARY)
            return True
        # if the item is in the last column
        elif col_index == self.actual_width - 1:
            # if the row is even
            if row_index % 2 != 0:
                # generate the open borderline piece
                self.image.image_data[row_index][col_index] = (
                    self.image.BLACK_CHAR_BINARY)
                return True
            # else don't do anything, leave the value == 0 / white space
            return False
        # else don't do anything and return
        return False

    def generate_image_bottom_border(self, col_index, row_index):
        """Generates a closed limitation line border for bottom row and
        returns boolean"""
        # add a black character for the closed limitation line border and return
        self.image.image_data[row_index][col_index] = (
            self.image.BLACK_CHAR_BINARY)
        return True

    def generate_image_top_border(self, col_index, row_index):
        """Generates a closed limitation line border for top row and returns
        a boolean"""
        # if the column is even
        if col_index % 2 == 0:
            # add a black character for the border and return
            self.image.image_data[row_index][col_index] = (
                self.image.BLACK_CHAR_BINARY)
            return True
        # else don't fill in the space (leave it as 0/white) and return
        return False

    # accessors ----------------------------------------------------------
    def get_actual_height(self):
        """Grab the actual height of the image"""
        return self.actual_height

    def get_actual_width(self):
        """Grab the actual width of the image"""
        return self.actual_width

    # instance helpers  --------------------------------------------------
    def compute_signal_height(self):
        """Analyze the spine of the array to compute the image height.
        Returns a boolean"""
        # traverse the image_data array starting from each row
        for row in range(BarcodeImage.MAX_HEIGHT):
            # check the first column in each row
            for col in range(1):
                # if the column is a truthy value (1)
                if self.image.get_pixel(row, col):
                    # set the height to the difference between the max height
                    # and the row, the value was found (marks the beginning
                    # of the image data)
                    self.actual_height = row
                    # calculate the width and return True
                    self.compute_signal_width()
                    return True
        # if nothing found return False
        return False

    def compute_signal_width(self):
        """Analyze the spine of the array to compute the image width. Return
        boolean"""
        # grab the top row of the image
        top_row = self.image.image_data[self.actual_height]

        # traverse every other character in the row
        for col in range(0, len(top_row), 2):
            active_column = top_row[col]
            # grab the column next to the active column for comparison
            next_column = top_row[col + 1]
            # if the active column and next column follow the '1, 0' pattern,
            # move onto the next column (this is the border)
            if (active_column == BarcodeImage.BLACK_CHAR_BINARY and
                    next_column == BarcodeImage.WHITE_CHAR_BINARY):
                continue
            else:  # if no more border characters are found
                # set the width's edge to the previous column and return
                self.actual_width = col - 1
                return True
        return False

    def set_ordinal_array(self):
        """Creates an array of ordinal values from stored text and returns
        the array"""
        # adding letters to the ordinal array
        ordinal_arr = []
        for char in self.text:
            ordinal_arr.append(ord(char))
        return ordinal_arr

    # display methods -----------------------------------------------------
    def display_image_to_console(self):
        """Displays the image to the console."""
        # create top and side borders
        top_border = "-" * (self.get_actual_width() + 2) # 2 hugs sides borders
        side_border = "|"
        # add top border to the output
        output = top_border + "\n"
        # grab only the rows with image content
        image_rows = self.image.image_data[self.get_actual_height():]
        # loop through each row
        for row in image_rows:
            # at the start of each row add the left-side border
            output += side_border
            # loop through each column only grabbing the left-most filled
            # image data
            for col in row[:self.get_actual_width()]:
                # if the column is truthy, i.e., 1
                if col:
                    # print an asterisk (black character)
                    output += self.BLACK_CHAR
                # if the column is false, i.e., 0 print a white character
                else:
                    output += self.WHITE_CHAR
            # at the end of each row add the right-side border
            output += side_border + "\n"
        print(output)

    def display_text_to_console(self):
        """Display the text to the console"""
        print(self.text)

def main():
    sImageIn = np.array([
        "* * * * * * * * * * * * * * *",
        "*                           *",
        "**********  *** *** *******  ",
        "* ***************************",
        "**    * *   * *  *   * *     ",
        "* **     ** **          **  *",
        "****** ****  **   *  ** ***  ",
        "****  **     *   *   * **   *",
        "***  *  *   *** * * ******** ",
        "*****************************"])

    sImageIn_2 = np.array([
        "* * * * * * * * * * * * * * *",
        "*                           *",
        "*** ** ******** ** ***** *** ",
        "*  **** ***************** ***",
        "* *  *    *      *  *  *  *  ",
        "*       ** **** *          **",
        "*    * ****  **    * * * *** ",
        "***    ***       * **    * **",
        "*** *   **  *   ** * **   *  ",
        "*****************************"])

    bc1 = BarcodeImage(sImageIn)
    print("-------- first barcode ----------------------"
    "-----------------------")
    ib1 = InfoBox(bc1)

    # First secret message
    ib1.translate_image_to_text()
    ib1.display_text_to_console()
    ib1.display_image_to_console()

    print("-------- second barcode ----------------------"
    "-----------------------")
    #second secret message
    bc2 = BarcodeImage(sImageIn_2)
    ib2 = InfoBox(bc2)
    ib2.translate_image_to_text()
    ib2.display_text_to_console()
    ib2.display_image_to_console()

    print("-------- third barcode (custom text to image) "
          "-----------------------")
    # create your own message
    text = "Who are you? I'm vengeance!"
    ib3 = InfoBox(None, text)
    ib3.generate_image_from_text()
    ib3.display_text_to_console()
    ib3.display_image_to_console()


    print("-------- retranslating custom barcode back from image to text "
          "--------")
    my_image = np.array(["* * * * * * * * * * * * * * *",
                         "*                           *",
                         "**** *** ***  * * *********  ",
                         "* ************ **************",
                         "**    *  * **     *          ",
                         "* **     ** * * *   *   *   *",
                         "** *   *  ***  ** ***** * *  ",
                         "** *  *   * *  *  * **  **  *",
                         "** * * * **** ***  * *** *** ",
                         "*****************************"])

    # retranslated secret message
    re = BarcodeImage(my_image)
    remake = InfoBox(re)
    remake.translate_image_to_text()
    remake.display_text_to_console()
    remake.display_image_to_console()

if __name__ == "__main__":
    main()

"""
-------- first barcode ---------------------------------------------
Wonderful, you are awesome!
-------------------------------
|* * * * * * * * * * * * * * *|
|*                           *|
|**********  *** *** *******  |
|* ***************************|
|**    * *   * *  *   * *     |
|* **     ** **          **  *|
|****** ****  **   *  ** ***  |
|****  **     *   *   * **   *|
|***  *  *   *** * * ******** |
|*****************************|

-------- second barcode ---------------------------------------------
CS at Foothill is great Fun
-------------------------------
|* * * * * * * * * * * * * * *|
|*                           *|
|*** ** ******** ** ***** *** |
|*  **** ***************** ***|
|* *  *    *      *  *  *  *  |
|*       ** **** *          **|
|*    * ****  **    * * * *** |
|***    ***       * **    * **|
|*** *   **  *   ** * **   *  |
|*****************************|

-------- third barcode (custom text to image) -----------------------
Who are you? I'm vengeance!
-------------------------------
|* * * * * * * * * * * * * * *|
|*                           *|
|**** *** ***  * * *********  |
|* ************ **************|
|**    *  * **     *          |
|* **     ** * * *   *   *   *|
|** *   *  ***  ** ***** * *  |
|** *  *   * *  *  * **  **  *|
|** * * * **** ***  * *** *** |
|*****************************|

-------- retranslating custom barcode back from image to text --------
Who are you? I'm vengeance!
-------------------------------
|* * * * * * * * * * * * * * *|
|*                           *|
|**** *** ***  * * *********  |
|* ************ **************|
|**    *  * **     *          |
|* **     ** * * *   *   *   *|
|** *   *  ***  ** ***** * *  |
|** *  *   * *  *  * **  **  *|
|** * * * **** ***  * *** *** |
|*****************************|

"""