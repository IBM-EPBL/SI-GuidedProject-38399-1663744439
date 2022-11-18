import ibm_db
conn = ibm_db.connect("DATABASE= bludb;HOSTNAME=54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32733;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootpipCA.crt;UID=fmd31832;PWD=tISolCD4D6S358tX;","","")


print(conn)
print("connection successful")