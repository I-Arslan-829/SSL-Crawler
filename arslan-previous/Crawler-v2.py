import csv
import socket, ssl
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import subprocess
import json
from cryptography import x509

# ---------------- MongoDB Setup ----------------
URL = "mongodb://localhost:27017"
DB_NAME = "Trunco_data"
client = MongoClient(URL, serverSelectionTimeoutMS=5000)
db = client[DB_NAME]
collection = db["certificates"]

def check_mongo_connection():
    try:
        client.admin.command('ping')
        print("MongoDB connected ")
        return True
    except ServerSelectionTimeoutError:
        print("MongoDB not connected ")
        return False

# ---------------- CSV Loading ----------------
def load_domains_from_csv(file_path):
    domain_list = []
    with open(file_path, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            domain = row.get("Websites URL")
            if domain:
                domain_list.append(domain.strip())
    return domain_list

# ---------------- SSL Certificate Fetch ----------------

def connect_to_domain(domain, timeout=5):
    """
    Fetch SSL certificate in PEM format from domain without saving to file.
    Adds error handling for invalid URLs and non-HTTPS websites.
    
    Returns:
        pem_data (str) if successful, None if any error occurs.
    """
    try:
        # Attempt to connect to the domain
        sock = socket.create_connection((domain, 443), timeout=timeout)
    except (socket.gaierror, socket.timeout, ConnectionRefusedError) as e:
        print(f"[ERROR] Cannot connect to {domain}: {e}")
        return None

    try:
        ssl_context = ssl.create_default_context()
        ssl_sock = ssl_context.wrap_socket(sock, server_hostname=domain)
        cert_bin = ssl_sock.getpeercert(binary_form=True)
        pem_data = ssl.DER_cert_to_PEM_cert(cert_bin)

        # Close connections
        ssl_sock.close()
        sock.close()

        return pem_data

    except ssl.SSLError as e:
        print(f"[ERROR] SSL handshake failed for {domain}: {e}")
        sock.close()
        return None

    except Exception as e:
        print(f"[ERROR] Unexpected error for {domain}: {e}")
        sock.close()
        return None


# ---------------- zcertificate Execution ----------------
def run_zcertificate_on_pem(pem_data):
    """Run zcertificate.exe on in-memory PEM data and return parsed JSON."""
    try:
        process = subprocess.Popen(
            ["zcertificate.exe", "-format", "pem"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(input=pem_data.encode())  # pipe PEM data directly

        if stderr:
            print("zcertificate log:", stderr.decode())

        parsed_json = json.loads(stdout)  # parse JSON output
        return parsed_json

    except Exception as e:
        print("Error running zcertificate:", e)
        return None

# ---------------- MongoDB Insert ----------------
def save_certificate_to_mongodb(parsed_data):
    if parsed_data is None:
        return
    try:
        result = collection.insert_one(parsed_data)
        print("Inserted certificate with _id:", result.inserted_id)
    except Exception as e:
        print("Error inserting into MongoDB:", e)

# ---------------- Main Function ----------------
def main():
    if not check_mongo_connection():
        return

    file_path = "Websites-Domains.csv"
    domain_list = load_domains_from_csv(file_path)

    for domain in domain_list:
        print(f"\nProcessing: {domain}")
        pem_data = connect_to_domain(domain)
        if pem_data != None:
            parsed_json = run_zcertificate_on_pem(pem_data)
            save_certificate_to_mongodb(parsed_json)

# ---------------- Entry Point ----------------
if __name__ == "__main__":
    main()
