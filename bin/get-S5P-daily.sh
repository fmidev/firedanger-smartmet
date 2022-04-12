#!/bin/env bash
#https://zipper.creodias.eu/download/b7d83a6f-1e34-53cc-9b86-d5e5475846c4
eval "$(conda shell.bash hook)"
conda activate xr
if [ $# -ne 0 ]
then
    d=$1
else
    d=$(date -d '1 day ago' +%Y%m%d)
fi
sdate="${d:0:4}-${d:4:2}-${d:6:2}"
cd ~/data/sen5p
#token='eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ5RUhvWks0aWR2WHFmeExZWFhabjFmTi1YSU1UTXJvdTJ2NmVIQXI5ZWE0In0.eyJleHAiOjE2NDk1NTkxNzgsImlhdCI6MTY0OTUyMzE4MCwiYXV0aF90aW1lIjoxNjQ5NTIzMTc4LCJqdGkiOiIxMGNjNmIwYy0xM2I2LTQyNDItYmE2Mi01Y2NjZjE2MWYwMzkiLCJpc3MiOiJodHRwczovL2lkZW50aXR5LmNsb3VkZmVycm8uY29tL2F1dGgvcmVhbG1zL2RpYXMiLCJhdWQiOlsiQ0xPVURGRVJST19QQVJUTkVSUyIsIkNMT1VERkVSUk9fUFVCTElDIiwiY3Jlb2RpYXMtd2ViYXBwIiwiYWNjb3VudCJdLCJzdWIiOiIyNTE3YWYwOC03OTI4LTQzMjYtOWZhYS0wMThjMzk4YmFiMmEiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJjcmVvZGlhcy13ZWJhcHAiLCJub25jZSI6IjZhOTM4MTZlLTk4MDItNGRjZi04N2YzLTljZTcxOTYyY2Q4ZCIsInNlc3Npb25fc3RhdGUiOiI1Nzk3ZDAzNC1kYWZjLTQyMDEtOWJmYi05NzZhMDc1MjZlNWQiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vZmluZGVyMi5pbnRyYS5jbG91ZGZlcnJvLmNvbS8qIiwiaHR0cHM6Ly9ob3Jpem9uLmNmMi5jbG91ZGZlcnJvLmNvbSIsImh0dHBzOi8vZmluZGVyLmNyZW9kaWFzLmV1IiwiaHR0cHM6Ly9wb3J0YWwuY3Jlb2RpYXMuZXUiLCJodHRwczovL2NmMi5jbG91ZGZlcnJvLmNvbSIsImh0dHBzOi8vZGlzY292ZXJ5LmNyZW9kaWFzLmV1IiwiKiIsImh0dHBzOi8vMTg1LjE3OC44NS4yMjIiLCJodHRwczovL3d3dy5jcmVvZGlhcy5ldSIsImh0dHBzOi8vZGFzaGJvYXJkLmNyZW9kaWFzLmV1IiwiaHR0cHM6Ly9zZXJ2aWNlcy5zZW50aW5lbC1odWIuY29tIiwiaHR0cHM6Ly93aG1jcy5jbG91ZGZlcnJvLmNvbSIsImh0dHBzOi8vMTg1LjE3OC44NC4xOCIsImh0dHBzOi8vYXV0aC5jbG91ZC5jb2RlLWRlLm9yZy8qIiwiaHR0cHM6Ly9wb3J0YWwuY3Jlb2RpYXMuZXUvKiIsImh0dHBzOi8vZmluZGVyZGV2LmludHJhLmNsb3VkZmVycm8uY29tIiwiaHR0cHM6Ly9jcmVvZGlhcy5ldSIsImh0dHBzOi8vY3Jlb2FwcHMuc2VudGluZWwtaHViLmNvbS8qIiwiaHR0cDovL2ZpbmRlcjIuaW50cmEuY2xvdWRmZXJyby5jb20iLCJodHRwczovL2Jyb3dzZXIuY3Jlb2RpYXMuZXUiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBhdWQtZml4IHByb2ZpbGUgYXVkLWZpeC1wYXJ0bmVycyBhZGRyZXNzIGVtYWlsIiwic2lkIjoiNTc5N2QwMzQtZGFmYy00MjAxLTliZmItOTc2YTA3NTI2ZTVkIiwiYWRkcmVzcyI6e30sImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6Ik1pa2tvIFN0cmFobGVuZG9yZmYiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJtaWtrby5zdHJhaGxlbmRvcmZmQGZtaS5maSIsImdpdmVuX25hbWUiOiJNaWtrbyIsImZhbWlseV9uYW1lIjoiU3RyYWhsZW5kb3JmZiIsImVtYWlsIjoibWlra28uc3RyYWhsZW5kb3JmZkBmbWkuZmkifQ.Y97-ouHLXUk4SRv_t42EsVkkEDFIP4UFg20dQp4LjjycH4v-uWbXdeyM71KjPLIM60gu6iR8lj6J2lt28nTzojZNiOKuTTRLuIBnRC0ZZprPl7WYw9Fqtaa9N18yASOUo7GW7SG70IkLBu1jjP8FuEmWODRecbca93ZS_tMI537nszqGZN6LJ_yW9X0lnmMH55lQG_FltaXASb8jg3Ai3oNYve0Uir1MOIc-4DM979YVkUEiDYQlwbEqfNXwvq0ENQCZVxeipqGzjgxI6ghymDewjGjmk5y0QNb8HYFF7B17DAY5r7PFTtbX4lS07_dgekw_EAzA19TaOfWm5mdrXA'
export token=$(curl -s -d 'client_id=CLOUDFERRO_PUBLIC' \
                             -d "username=mikko.strahlendorff@fmi.fi" \
                             -d "password=Hehec3po" \
                             -d 'grant_type=password' \
                             'https://auth.creodias.eu/auth/realms/DIAS/protocol/openid-connect/token' | \
                             python -m json.tool | grep "access_token" | awk -F\" '{print $4}')
query="https://finder.creodias.eu/resto/api/collections/Sentinel5P/search.json?maxRecords=2000&startDate=${sdate}T00:00:00Z&completionDate=${sdate}T23:59:59Z&timeliness=Near+real+time&processingLevel=LEVEL2&geometry=POLYGON((-80+-10,-80+-60,-50+-60,-50+-10,-80+-10))&sortParam=startDate&sortOrder=descending&status=all&dataset=ESA-DATASET"
echo $query
linkstxt=$(curl -s "$query" | jq -r '.features[].properties.services.download.url')
IFS=' ' readarray links <<< "$linkstxt"
get-unzip-rm() {
    wget -qcO "${1:36:36}.zip" "${1:0:72}?token=$token" && unzip -qu "${1:36:36}.zip" \
     && rm "${1:36:36}.zip"
}
export -f get-unzip-rm
#for i in "${!links[@]}"
#do
#    wget -qcO "${links[i]:36:36}.zip" "${links[i]:0:72}?token=$token" && unzip -qu "${links[i]:36:36}.zip" \
#     && rm "${links[i]:36:36}.zip"
#done && \
parallel get-unzip-rm ::: "${links[@]}" #&& \
parallel fix-s5p-nc.sh ::: S5P_NRTI_L2__*_$d*/S*[0-9].nc && \
  parallel merge-day-s5.sh $d :::: s5p-vars.lst #&&\
sudo docker exec smartmet-server /bin/fmi/filesys2smartmet /home/smartmet/config/libraries/tools-grid/filesys-to-smartmet.cfg 0