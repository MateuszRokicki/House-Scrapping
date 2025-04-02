import pandas as pd
basic_info = {'Title': 'Sprzedam mieszkanie w Łambinowicach', 'Price': '245 000 zł', 'PpSM': '4 804 zł/m²', 'Area': '51m²', 'Rooms': '3 pokoje'}
mapped_dict = {'Heating': 'miejskie', 'Floor': '3/4', 'Rent': '500 zł', 'Condition': 'do remontu', 'Market': 'wtórny', 'Form of Ownership': 'pełna własność', 'Availability': '', 'Seller Type': 'prywatny', 'Additional Information': ['balkon', 'piwnica'], 'Elevator': 'nie', 'Type of Development': 'blok', 'Windows': 'drewniane', 'Energy Certificate': 'W trakcie realizacji / Zwolnione', 'Equipment': ['lodówka', 'piekarnik', 'kuchenka', 'telewizor', 'pralka'], 'Security': 'domofon / wideofon', 'Media': ['internet', 'telefon']}
basic_info.update(mapped_dict)
print(basic_info)
apartment_columns = ['URL', 'Title', 'Price', 'PpSM', #Basic info
                    'Street', 'Subdistrict', 'City District', 'City', 'Commune', 'District', 'Voivodeship', #Address
                    'Area', 'Rooms', 'Heating', 'Floor', 'Rent', 'Condition', 'Market', 'Form of Ownership', 'Availability', 'Seller Type', 'Additional Information', #Details
                    'Year', 'Elevator', 'Type of Development', 'Building Material', 'Windows', 'Energy Certificate', 'Safety', #Building and materials
                    'Security', 'Media', 'Equipment', #Equipment
                    'Description']
df = pd.DataFrame(columns=apartment_columns)
df.loc[len(df)] = basic_info
print(df)