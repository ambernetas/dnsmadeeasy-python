from dme import dme


def main():
    # Sandbox Auth info
    dns = dme("338b82e0-ce01-4185-83ae-839f261708f7", "1ae2ea2d-53d6-4468-9c46-b1607733a8da")
        
#    # Example use of 'list_domains' returns a list of all domains
    print("\nList all domains: \n")
    domains = dns.list_domains()
    for d in domains:
        print(d)
    
    # Example of using 'list_records' on a single domain
    print("\nList records for a single domain:")
    records = dns.get_records('test1.com')
    for record in records:
        print("")
        for (key, value) in record.items():
            print(key + " : " + str(value))
    
    # Example of using 'get_domain' on a single domain
    print("\nGet general info about a single domain: \n")
    domain_info = dns.get_domain('test1.com')
    for items in domain_info:
        if type(items[1]) is list:
            for ns in items[1]:
                print(ns)
        else:
            print(items[0] + " : " + str(items[1]))

    
    # Example of deleting a domain:
    
    print("Delete domain: \n")
    result = dns.delete_domain("testdomain2.com")
    print(result['status'])
    
    # Example of adding a domain:
    
    print("\nAdd domain")
    content = dns.add_domain("testdomain5.com")
    print(content['name'] + " added!")
    
    # Example of adding a single record to a domain:
    
    print("\nAdd record to domain: \n")
    data =  json.dumps({
                "name":"dummycname",
                "type":"A",
                "data":"208.94.147.96",
                "gtdLocation":"Default",
                "ttl":1800
            }, separators=(',', ':'))    
    result = dns.add_record('testdomain1.com', data)
    print(result) 
    record = dns.get_record_byid('testdomain1.com','6883496')
    print(record)
    
#    record = dns.delete_record_byid('test1.com', '6883496')
    
    
    data =  json.dumps({
            "name":"",
            "type":"MX",
            "data":"10 mail",
            "gtdLocation":"DEFAULT",
            "ttl":1800
    }, separators=(',', ':'))
    record = dns.update_record_byid('testdomain1.com', '6883496', data)
    print(record)
    
    
if __name__ == "__main__":
    main()