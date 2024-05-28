import os, json, requests, csv

ak= os.environ.get("ACCESS_KEY")
secret = os.environ.get("SECRET")

def token():
    url="https://api4.prismacloud.io/login"
    payload={
        "username":ak,
        "password":secret
    }
    headers={
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8'
    }

    response=requests.request("POST",url,headers=headers,data=json.dumps(payload))
    response=json.loads(response.content)

    return response['token']

def download_csv_report_from_rql(query):
    url="https://api4.prismacloud.io/search/api/v1/config/download"
    payload={
        "query":query
    }
    headers={
        'Accept': 'text/csv; charset=UTF-8',
        'x-redlock-auth': token()
    }

    response=requests.request("POST",url,headers=headers,json=payload)
    print(response)
    response=response.content
    print(response)
    return response

def handler():
    rql="""config from cloud.resource where resource.status = Active AND cloud.type = 'aws'"""
    data=download_csv_report_from_rql(rql)
    with open("my_data.csv", "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for line in data.splitlines():
            writer.writerow([line])
    

handler()
