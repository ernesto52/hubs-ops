import json
import sys
import array
import urllib.request
import socket
import os
import shutil

service_name = sys.argv[1]
service_group = sys.argv[2]
service_org = sys.argv[3]

hostname = socket.gethostname()
hostname_parts = hostname.split(".")
hostname_parts[0] = hostname_parts[0] + "-local"
hostname = ".".join(hostname_parts)
response = urllib.request.urlopen("http://" + hostname + ":9631/census")
file_data = json.loads(response.read())['census_groups'][service_name + '.' + service_group + '@' + service_org]['service_files']

outpath = "/hab/svc/" + service_name + "/files"
os.makedirs(outpath, exist_ok=True)

for filename, info in file_data.items():
    output_body = bytearray(info["body"]).decode("utf-8")
    output_file_path = outpath + "/" + filename
    output_file = open(output_file_path, "w")
    output_file.write(output_body)
    output_file.close()
    shutil.chown(output_file_path, user="hab", group="hab")
