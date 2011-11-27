from units_core import Unit, Quantity, safe_dict_merge

multipliers = (
       ( 'giga','G',  Unit(powerTen=9)  ),
       ( 'mega','M',  Unit(powerTen=6)  ),
       ( 'kilo','k',  Unit(powerTen=3)  ),
       ( 'centi','c', Unit(powerTen=-2) ) ,
       ( 'milli','m', Unit(powerTen=-3) ) ,
       ( 'micro','u', Unit(powerTen=-6) ) ,
       ( 'nano','n',  Unit(powerTen=-9) ) ,
       ( 'pico','p',  Unit(powerTen=-12)) ,
        )

units = (
       ( 'meter','m',       Unit(meter=1) ),
       ( 'gram','g',        Unit(kilogram=1,powerTen=-3) ),
       ( 'second','s',      Unit(second=1) ),
       ( 'amp','A',         Unit(ampere=1) ),
       ( 'kelvin','K',      Unit(kelvin=1) ),
       ( 'mole','mol',      Unit(mole=1) ),
       ( 'candela','cd',    Unit(candela=1) ),

       ( 'volt','V',    Unit(meter=2, kilogram=1,second=-3,ampere=-1) ),
       ( 'siemen','S',  Unit(meter=-2, kilogram=-1,second=3,ampere=2) ),
       ( 'farad','F',   Unit(meter=-2, kilogram=-1,second=4,ampere=2) ),
       ( 'ohm','Ohm',   Unit(meter=2, kilogram=1,second=-3,ampere=-2) ),
       ( 'coulomb','C', Unit(second=1,ampere=1) ),
       
       ( 'hertz','Hz',  Unit(second=-1) ),
       ( 'watt','W',    Unit(kilogram=1, meter=2, second=-3) ),
       ( 'joule','J',   Unit(kilogram=1, meter=2, second=-2) ),
       ( 'newton','N',  Unit(kilogram=1, meter=1, second=-2) ),
       ( 'liter','l',   Unit(powerTen=-3, meter=3) ),
       
)


unit_long_LUT = dict([(u[0],u[2]) for u in units] ) 
unit_short_LUT = dict([(u[1],u[2]) for u in units] ) 
unit_LUT = safe_dict_merge(unit_long_LUT, unit_short_LUT)

multiplier_long_LUT = dict([(u[0],u[2]) for u in multipliers] ) 
multiplier_short_LUT = dict([(u[1],u[2]) for u in multipliers] ) 
multiplier_LUT = safe_dict_merge(multiplier_long_LUT, multiplier_short_LUT)


special_unit_abbrs = ( 
        ( 'm', Unit(meter=1)  ),
        ( 'cm', Unit(meter=1, powerTen=-2)  ),
        ( 'mm', Unit(meter=1, powerTen=-3)  ),
        ( 'um', Unit(meter=1, powerTen=-6)  ),
        ( 'nm', Unit(meter=1, powerTen=-9)  ),
        ( 'pm', Unit(meter=1, powerTen=-12)  ),
            )



constants = {
    'pi':       Quantity(3.141592653, Unit() ),
    'e_euler':   Quantity(2.718281828,   Unit() ),
    'e_charge': Quantity(1.602176565, unit_long_LUT['coulomb']   ),

    'Na':       Quantity(6.02214129e23, Unit(mole=-1) ),                                                               # [Avagadro's Constant]
    'k':        Quantity(1.380648e-23,  unit_long_LUT['joule']/unit_long_LUT["kelvin"] ),                              # [Boltzmanns Constant]
    'F':        Quantity(96485.3365,    unit_long_LUT['coulomb']/unit_long_LUT["mole"] ),                              # [Faraday's  Constant]
    'R':        Quantity(8.3144621,     unit_long_LUT['joule']/(unit_long_LUT["mole"]*unit_long_LUT['kelvin'] ) ),     # [Gas Constant]

    'int': Quantity(1, Unit()),
    'ext': Quantity(1, Unit()),
        }


std_funcs = (
    'log2',
    'exp',
    'sin',
    'cos'
    )
