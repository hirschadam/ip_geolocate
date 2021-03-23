import csv
import requests


def get_addresses(filename):
    """
    Given a CSV file, this function returns a list of lists
    where each element (list) in the outer list contains the
    row info from the csv file.
    """
    all_addresses = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            all_addresses.append(row)
    return all_addresses

def get_geolocation(all_the_ip_address):
    """
    Given a list of lists from `get_addresses()`, this function
    returns an updated lists of lists containing the geolocation.
    """
    print("Getting geo information...")
    updated_addresses = []
    counter = 1
    # update header
    header_row = all_the_ip_address.pop(0)
    header_row.extend(['Country', 'City', 'State', 'Username'])
    # get geolocation
    for line in all_the_ip_address:
        print("Grabbing geo info for row #"+str(counter))
        r = requests.get('https://reallyfreegeoip.org/json/{0}'.format(line[0]))
        line.extend([str(r.json()['country_name']), str(r.json()['city']), str(r.json()['region_code']), str(line[1])])
        updated_addresses.append(line)
        counter += 1
    updated_addresses.insert(0, header_row)
    return updated_addresses
	
def create_csv(updated_address_list):
    """
    Given the updated lists of lists from `get_geolocation()`, this function
    creates a new CSV.
    """
    with open('output.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(updated_address_list)
    print("All done!")


if __name__ == '__main__':
    csv_file = 'input.csv'
    all_the_ip_address = get_addresses(csv_file)
    updated_address_list = get_geolocation(all_the_ip_address)
    create_csv(updated_address_list)