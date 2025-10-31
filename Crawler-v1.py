import csv
import socket,ssl
from cryptography import x509
from pymongo import MongoClient
from datetime import datetime, timedelta

URL="mongodb://localhost:27017"
DB_NAME="Trunco_data"

client=MongoClient(URL)
db=client[DB_NAME]
collection=db["certificates"]


def load_domains_from_csv(file_path):
    """Read the CSV file containing domain names and return a list of domains."""
    file=open(file_path,newline='')
    csvreader=csv.reader(file,delimiter=",")
    domain_list=[]
    for row in csvreader:
        domain_list.append(row[0])

    # print(domain_list[0])
    return domain_list



def connect_to_domain(domain):
    """Establish an SSL connection to the given domain on port 443 and fetch its certificate in PEM format."""
    #print(domain)
    ssl_context=ssl.create_default_context()
    sock=socket.create_connection((domain,443))
    ssl_sock=ssl_context.wrap_socket(sock,server_hostname=domain)
    cert_bin=ssl_sock.getpeercert(binary_form=True)
    
    pem_data=ssl.DER_cert_to_PEM_cert(cert_bin)
    filename = f"{domain}.pem"
    with open(filename, "w") as f:
        f.write(pem_data)
    
    # Close sockets
    ssl_sock.close()
    sock.close()
    #print(cert_bin)
    return pem_data


def parse_certificate(pem_data):
    """Parse the PEM-encoded certificate and extract structured data (issuer, subject, validity, version, etc.)."""
    if isinstance(pem_data,str):
        pem_data = pem_data.encode("utf-8")

    data= x509.load_pem_x509_certificate(pem_data)
    #print(data.signature_algorithm_oid._name)
    return data


def save_certificate_to_mongodb(parsed_data):
    """Insert the parsed certificate data into MongoDB with proper document structure."""
    print(client.server_info())


def main():
    file_path="domains.csv"
    domain_list=load_domains_from_csv(file_path)
    for domain in domain_list:
        pem_data=connect_to_domain(domain)
        data = parse_certificate(pem_data)


# main()







# data=parse_certificate(pem_data)
data=123
save_certificate_to_mongodb(data)