
from formatterSOL import Formatter
import pandas as pd

#you should create a .xlsx file with the formatterSOL 

data = Formatter(pd.read_excel("./SOL.xlsx"))

data.resultShort().to_excel("SOL_format.xlsx")
data.resultShort().drop_duplicates(subset=['UC_BRAND', 'UC_MODEL', 
                            'UC_FUEL', 'UC_VERSION', 'BRAND', 
                            'COUNTRY','UC_REGISTRATION_DATE', 
                            'CURRENT_MILEAGE'] ,keep='first').to_excel("SOL_format_dedoublon.xlsx")