from os import listdir, curdir, path

def ingest_sinc(file_path):
    pass

def ingest_terc(file_path):
    pass

def ingest_ulic(file_path):
    pass

def ingest_wmrodz(file_path):
    pass
from geopy.geocoders import Nominatim
def main(date):
    # path_ = f'./Files/{date}/'
    # script_dir = path.dirname(path.abspath(__file__))
    # print(path.abspath(__file__))
    # print(script_dir)
    # print(curdir)
    # print(path_)
    # folder_path = path.join(curdir, 'test_a')
    # print(folder_path)
    # for f in listdir(folder_path):
    #     print(f)
    geo = Nominatim(user_agent='geoapi')
    loc = geo.geocode('Wrocław')
    print(loc.raw)
    print(loc.raw.get("display_name", ""))
if __name__ == '__main__':
    date = '2024-11-30'
    main(date)