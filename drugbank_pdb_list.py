import requests
from collections import namedtuple
import csv

class SearchAPI:
    def __init__(self, search_url):
        self.search_url = search_url
        self.search_options = '&wt=json&rows=100000'


    def url_response(self, url):
        """
        Getting JSON response from URL
        :param url: String
        :return: JSON
        """
        r = requests.get(url=url)
        # Status code 200 means 'OK'
        if r.status_code == 200:
            json_result = r.json()
            return json_result
        else:
            print(r.status_code, r.reason)
            return None

    def run_search(self):

        full_query = self.search_url
        response = self.url_response(full_query)
        return response

def main():
    Data_tuple = namedtuple('mapping', ['dgb', 'het', 'pdb_id']) # main data structure

    # quesry Unichem rest pai
    Unichem_query = SearchAPI(search_url='https://www.ebi.ac.uk/unichem/rest/mapping/3/2')
    drugbank_pdb_mapping = Unichem_query.run_search()
    db_hetcode_dict = {}
    for d in drugbank_pdb_mapping:
        d_values_list = (list(d.values()))
        db_hetcode_dict[d_values_list[0]] = d_values_list[1]
    print(db_hetcode_dict)

    #this is a test dictionary to check the output format
    test_dict = {'IEM': 'DB07960', 'DFT': 'DB07652', 'FTS': 'DB07798', 'BHI': 'DB04170', 'TDA': 'DB02448', 'LC1': 'DB08083'}
    results_list = []

    #to get the full result replace test_dict in next line with db_hetcode_dict once you are happy with the result
    for hetcode, drugbank_id in test_dict.items():

        #query pdbe rest api
        pdbe_qeury = SearchAPI(search_url='https://www.ebi.ac.uk/pdbe/api/pdb/compound/in_pdb/{}'.format(hetcode))
        pdb_list_dict = pdbe_qeury.run_search()

        #create the data structure
        for het_id, pdb_id in pdb_list_dict.items():
            data_tuple = Data_tuple(dgb =drugbank_id, het = het_id, pdb_id = pdb_id)
            results_list.append(data_tuple)

    with open('output.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(('drugbank_id', 'het_id', 'pdb_id_list'))
        w.writerows(results_list)




if __name__ == "__main__":
    main()