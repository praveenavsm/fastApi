import pymongo


client = pymongo.MongoClient("mongodb+srv://praveenavsm:suDPIDRtkgSeNb3S@cluster0.ldajt.mongodb.net/patientdb"
                             "?retryWrites=true&w=majority&tls=true" , tlsAllowInvalidCertificates=True)

mydb = client['patientdb']

mycol = mydb['patients']

mydoc = mycol.find({"patientid": 1})


for x in mydoc:
  print(f"patient id:{x['patientid']}")
