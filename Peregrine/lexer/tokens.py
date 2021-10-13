"""
*  
*  Copyright (c) Peregrine-lang, 2021. All rights reserved.
*
"""

from enum import IntEnum, auto
from dataclasses import dataclass

@dataclass
class Token:  # change class to struct
    keyword: str = ""
    index: int = 0
    line: int = 1
    tk_type: int = 0
    tab: float = 0

class TokenType(IntEnum):
	tk_plus = auto()       # + 
	tk_minus = auto()     # -	
	tk_divide = auto()     # / 
	tk_asterisk = auto()    # * 
	tk_xor = auto()        # ^ 
	tk_modulo = auto()     # % 
	tk_greater = auto()    # > 
	tk_less = auto()       # < 
	tk_ampersand = auto()    # & 
	tk_bit_or = auto()     # | 
	tk_bit_not = auto()    # ~ 
	tk_assign = auto()     # = 
	tk_excl = auto()        # ! 
	tk_colon = auto()      # : 
	tk_dot = auto()        # . 
	tk_l_paren = auto()     # ( 
	tk_r_paren = auto()     # ) 
	tk_hashtag = auto()     # # 
	tk_comma = auto()      # , 

	tk_exponent = auto() #**
	tk_equal = auto()             # == 
	tk_not_equal = auto()         # != 
	tk_floor = auto()             # // 
	tk_gr_or_equ = auto()         # >= 
	tk_less_or_equ = auto()       # <= 
	tk_increment = auto()         # ++ 
	tk_decrement = auto()         # --
	tk_arrow = auto()             # -> 
	tk_shift_right = auto()       # >> 
	tk_shift_left = auto()        # << 
	tk_floor_equal = auto()       # //= 
	tk_plus_equal = auto()        # += 
	tk_minus_equal = auto()        # -= 
	tk_times_equal = auto()       # *= 
	tk_slash_equal = auto()       # /= 
	tk_mod_equal = auto()         # %= 
	tk_shift_right_equal = auto()  # >>= 
	tk_shift_left_equal = auto()   # <<= 
	tk_bit_and_equal = auto()     # &= 
	tk_bit_or_equal = auto()       # |= 
	tk_bit_xor_equal = auto()      # ^= 
	
	tk_identifier = auto()  # foo, bar 

	# keywords tokens
	tk_true = auto()          # true 
	tk_false = auto()         # false 
	tk_none = auto()          # none 
	tk_const = auto()         # const 
	tk_import = auto()        # import 
	tk_cppimport = auto()        # cppimport 
	tk_himport = auto()        # himport
	tk_if = auto()            # if 
	tk_else = auto()          # else 
	tk_elif = auto()          # elif 
	tk_while = auto()         # while 
	tk_for = auto()           # for 
	tk_break = auto()         # break  
	tk_continue = auto()      # continue 
	tk_match = auto()         # match 
	tk_extern = auto()         # extern
	tk_case = auto()          # case 
	tk_default = auto()       # default 
	tk_def = auto()           # def 
	tk_pass = auto()          # pass 
	tk_return = auto()        # return 
	tk_and = auto()           # and 
	tk_or = auto()            # or 
	tk_not = auto()           # not 
	tk_is = auto()            # is 
	tk_in = auto()            # in 
	tk_cppcode = auto()         # Cppcode 
	tk_class = auto()         # class 
	tk_struct = auto()        # struct 

	# language types
	tk_str = auto()  #str
	tk_bool = auto()  #bool
	tk_char = auto()  #char
	tk_float = auto() #float
	tk_float32 = auto() #float32
	tk_void = auto() #void
	tk_int = auto() #int
	tk_int32 = auto() #int32
	tk_int16 = auto() #int16
	tk_int8 = auto() #int8
	tk_uint32 = auto() #uint32
	tk_uint16 = auto() #uint16
	tk_uint8 = auto() #uint8
	tk_uint = auto() #uint
	#value type
	decimal = auto() #5.7
	integer = auto() #89
	cpp= auto() #anything within Cppcode()
	array = auto() #["item"]
	dictionary = auto() #{"item": value}
	string = auto() #"some string"
	tk_ident = auto()         # beginning of identation
	tk_dedent = auto()        # end of identation
	tk_raw = auto() # raw string i.e. r
	tk_format = auto() # formatted string i.e. f


def next(index:int, code:list)-> str:
	if len(code)==index+1:
		return ""
	else:
		return code[index+1]