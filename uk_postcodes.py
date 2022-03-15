'''
This file has methods to validate and format Post codes of UK.
More information about the post codes can be found at https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Formatting
Once user enters post code, the script will first check if it falls under a normal post code or a special cases.
if the post code is in normal format (Please refer to wiki site), then additional checks are performed to validate its authenticity.
if the post code is in special format (Please refer to wiki site), then it will be checked in special_cases.py file if it is mentioned there.
appropriate message will be displayed on the screen.
'''

import re
import special_cases as sc
from dataclasses import dataclass



# in case of normal postcode this function will format any post code to '{area}{district} {sector}{unit}'
# in case of special postcode this function will simply convert post code to uppercase.
def format_postcodes(p, type_of_postcode):
    if type_of_postcode == 'normal':
        Postcode.formatted_postcode = f"{Postcode.area}{Postcode.district} {Postcode.sector}{Postcode.unit}"
    else:
        Postcode.formatted_postcode = p.upper()


# Purpose of this function is to find particular element el in list l.
# used binary search algorithm.
def find_element_in_List(el, l):
    l.sort()
    start = 0
    end = len(l) - 1
    to_return = False
    while start <= end and not to_return:
        mid = (start + end) // 2
        if l[mid] == el:
            to_return = True
        else:
            if el < l[mid]:
                end = mid - 1
            else:
                start = mid + 1
    return to_return


# Purpose of this function is to display messages.
# In case of error more information will be provided.
def display_message(message_type, *error):

    if message_type == "error":
        print(f"Invalid Post Code {error[0]}.\nPlease check your response!")
    elif message_type == "success":
        print(f"Entered Post Code '{Postcode.formatted_postcode}', can be a valid one.")
    elif message_type == "confirmSuccess":
        print(f"Entered Post Code '{Postcode.formatted_postcode}', is a valid one.")


@dataclass
class Postcode:
    area: str
    district: str
    sector: str
    unit: str
    postcode: str
    outward: str
    inward: str
    formatted_postcode: str

# User defined exceptions
class Error(Exception):
    """Base Class for other exceptions"""
    pass


class InvalidPostcode(Error):
    """Raised When Entered Postcode is invalid"""
    pass


class InvalidOutward(Error):
    """Raised when Outward is not in proper format"""
    pass


class InvalidInward(Error):
    """Raised When Inward is not in proper format"""
    pass


class ValidatePostcode(Postcode):
    def __init__(self, pc):
        self.message = ""
        self.postcode_without_space = ""
        self.pc = pc.strip()
        self.special_cases = ""
        self.mode = "Test"

    # Purpose of this function is to divide the entered post code and assign values to area, district, sector, unit
    def fetch_details(self, p):
        Postcode.postcode = p.upper()
        self.postcode_without_space = Postcode.postcode.replace(" ", "")

        # In post code, Last 3 characters will in inward and everything else will be outward.
        Postcode.outward = self.postcode_without_space[:len(self.postcode_without_space) - 3]
        Postcode.inward = self.postcode_without_space[len(self.postcode_without_space) - 3:]

        # disctrict will always start with number. Anything before that will be area.
        district_start_pos = 0
        for pos, char in enumerate(Postcode.outward):
            if char.isdigit():
                district_start_pos = pos
                break

        Postcode.area = Postcode.outward[0:district_start_pos]
        Postcode.district = Postcode.outward[district_start_pos:]
        Postcode.sector = Postcode.inward[0]
        Postcode.unit = Postcode.inward[1:]

    def func_validate_postcode(self):
        if self.pc == "":
            raise ValueError

        # it will fetch details from entered postcode
        self.fetch_details(self.pc)

        # Normal Postcodes
        if re.fullmatch(r"^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$", self.postcode):
            format_postcodes(Postcode.postcode, "normal")

            try:
                # Areas with only single-digit districts: BR, FY, HA, HD, HG, HR, HS, HX, JE, LD, SM, SR, WC, WN, ZE (although WC is always subdivided by a further letter, e.g. WC1A)
                if find_element_in_List(self.area,
                                     ['BR', 'FY', 'HA', 'HD', 'HG', 'HR', 'HS', 'HX', 'JE', 'LD', 'SM', 'SR', 'WN',
                                      'ZE']) and len(self.district) > 1:
                    display_message("error", f"'{self.formatted_postcode}': {self.area} should have only 1 digit for District")
                    raise InvalidOutward

                # Areas with only double-digit districts: AB, LL, SO
                elif find_element_in_List(self.area, ['AB', 'LL', 'SO']) and (not len(self.district) == 2 or re.search(r'[A-Z]+', self.district)):
                    display_message("error", f"'{self.formatted_postcode}': 'AB', 'LL', 'SO' areas should have only double-digit district")
                    raise InvalidOutward

                # Areas with a district '0' (zero): BL, BS, CM, CR, FY, HA, PR, SL, SS
                elif not find_element_in_List(self.area, ['BL', 'BS', 'CM', 'CR', 'FY', 'HA', 'PR', 'SL', 'SS']) and self.district == "0":
                    display_message("error", f"'{self.formatted_postcode}': Only 'BL', 'BS', 'CM', 'CR', 'FY', 'HA', 'PR', 'SL', 'SS' areas can have district 0")
                    raise InvalidOutward

                # BS is the only area to have both a district 0 and a district 10
                elif find_element_in_List(self.area, ['BL', 'CM', 'CR', 'FY', 'HA', 'PR', 'SL', 'SS']) and self.district == "10":
                    display_message("error", f"'{self.formatted_postcode}': BS is the only area that can have both a district 0 and a district 10")
                    raise InvalidOutward

                # The only letters to appear in the third position are A, B, C, D, E, F, G, H, J, K, P, S, T, U and W when the structure starts with A9A.
                elif re.match(r'^[A-Z0-9]{2}[A-Z]',self.postcode) and not find_element_in_List(self.postcode[2], list("ABCDEFGHJKPSTUW")):
                    display_message("error", f"'{self.formatted_postcode}': The only letters to appear in the third position are A, B, C, D, E, F, G, H, J, K, P, S, T, U and W when the structure starts with A9A")
                    raise InvalidOutward

                # The only letters to appear in the fourth position are A, B, E, H, M, N, P, R, V, W, X and Y when the structure starts with AA9A.
                elif re.match(r'^[A-Z]{2}[0-9]{1}[A-Z]{1}',self.postcode) and not find_element_in_List(self.postcode[3], list("ABEHMNPRVWXY")):
                    display_message("error", f"'{self.formatted_postcode}': The only letters to appear in the fourth position are A, B, E, H, M, N, P, R, V, W, X and Y when the structure starts with AA9A")
                    raise InvalidOutward

                # The letters Q, V and X are not used in the first position.
                elif re.match(r'^Q|V|X',self.area):
                    display_message("error", f"'{self.formatted_postcode}': Postcode cannot start with Q, V, or X")
                    raise InvalidOutward

                # The letters I, J and Z are not used in the second position.
                elif re.match(r'^.[IJZ]{1}',self.area):
                    display_message("error", f"'{self.formatted_postcode}': Second character of postcode cannot be I, J, or Z")
                    raise InvalidOutward

                # The final two letters do not use C, I, K, M, O or V, so as not to resemble digits or each other when hand-written.
                elif set(self.postcode[-2:]).intersection(set(list("CIKMOV"))):
                    display_message("error", f"'{self.formatted_postcode}': Final two letters can not use C, I, K, M, O or V, so as not to resemble digits or each other when hand-written")
                    raise InvalidInward

                # Postcode sectors are one of ten digits: 0 to 9, with 0 only used once 9 has been used in a post town, save for Croydon and Newport
                elif self.sector == "0" and not re.match(r'[0-9][A-Z]',self.district):
                    display_message("error", f"'{self.formatted_postcode}': Post code can have sector 0 only if 0-9 has been used in a post town")
                    raise InvalidInward

                # Central London single-digit districts have been further divided by inserting a letter after the digit and before the space.
                elif self.district[-1].isalpha():

                    # only these districts can have a character at the end.
                    if not find_element_in_List(self.outward[:-1], ['EC1','EC2','EC3','EC4','SW1','W1','WC1','WC2','E1','N1','NW1','SE1']):
                        display_message("error", f"'{self.formatted_postcode}': Only 'EC1-EC4','SW1','W1','WC1','WC2','E1','N1','NW1','SE1' areas can have a letter after digit for district")
                        raise InvalidOutward

                    # district E1 can have only W as last character.
                    elif self.outward[:-1] == "E1" and not self.outward[-1] == "W":
                        display_message("error", f"'{self.formatted_postcode}': Only possible outward for E1 is E1W")
                        raise InvalidOutward

                    # district N1 can have only C or P as last character.
                    elif self.outward[:-1] == "N1" and not self.outward[-1] in 'CP':
                        display_message("error", f"'{self.formatted_postcode}': Only possible outward for N1 are N1C or N1P")
                        raise InvalidOutward

                    # district NW1 can have only W as last character.
                    elif self.outward[:-1] == "NW1" and not self.outward[-1] == 'W':
                        display_message("error", f"'{self.formatted_postcode}': Only possible outward for NW1 is NW1W")
                        raise InvalidOutward

                    # district SE1 can have only P as last character.
                    elif self.outward[:-1] == "SE1" and not self.outward[-1] == 'P':
                        display_message("error", f"'{self.formatted_postcode}': Only possible outward for SE1 is SE1P")
                        raise InvalidOutward
            finally:
                pass

        # Special Postcodes
        elif re.fullmatch(
                r"^(([A-Z]{1,2}[0-9][A-Z0-9]?|ASCN|STHL|TDCU|BBND|[BFS]IQQ|PCRN|TKCA) ?[0-9][A-Z]{2}|BFPO ?[0-9]{1,4}|(KY[0-9]|MSR|VG|AI)[ -]?[0-9]{4}|[A-Z]{2} ?[0-9]{2}|GE ?CX|GIR ?0A{2}|SAN ?TA1)$",
                Postcode.postcode):

            format_postcodes(self.postcode, "special")

            # importing all special cases post codes from special_cases.py and storing it in special_cases.
            self.special_cases = sc.special_postcodes()

            # if entered post code is not a part of special cases then exception will be raised.
            if not find_element_in_List(self.postcode, self.special_cases):
                display_message("error", f"'{self.formatted_postcode}':\nIf the provided post code falls under special category, then make sure to include space as well, if applicable.")
                raise InvalidPostcode
        else:
            display_message('error', f"'{self.postcode}': Please Enter Valid Post code")
            raise InvalidPostcode

        if self.mode == "Test":
            return True

if __name__ == '__main__':
    entered_postcode = input("Please enter Post code to validate: ")
    pc1 = ValidatePostcode(entered_postcode.strip())

    try:
        pc1.func_validate_postcode()
    except ValueError:
        print("Please enter correct Postcode !")
    except InvalidInward:
        print("There might be an issue with Inward part of the post code!")
    except InvalidOutward:
        print("There might be an issue with Outward part of the post code!")
    except InvalidPostcode:
        # print("Invalid Postcode!")
        pass
    else:
        print(f"Entered Postcode '{Postcode.formatted_postcode}' is/can be a valid one!")