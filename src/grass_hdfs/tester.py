# import pyhs2
#
# with pyhs2.connect(host='172.17.0.2',
#                    port=10000,
#                    authMechanism="PLAIN",
#                    user='root',
#                    password='test',
#                    database='default') as conn:
#     with conn.cursor() as cur:
#         #Show databases
#     	print cur.getDatabases()
#
#         #Execute query
#         cur.execute("show tables")
#
#         #Return column info from query
#         print cur.getSchema()
#
#         #Fetch table results
#         for i in cur.fetch():
#             print i

from hdfs import InsecureClient
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery


credentials = GoogleCredentials.get_application_default()
dataproc = discovery.build('dataproc', 'v1', credentials=credentials)




def list_clusters_with_details(project, region):
    result = dataproc.projects().regions().clusters().list(
        projectId=project,
        region = region).execute()
    cluster_list = result['clusters']
    for cluster in cluster_list:
        print "%s - %s" % (cluster['clusterName'], cluster['status']['state'])
    return result

def main():
    project='spatial-hadoop'
    region='global'
    list_clusters_with_details(project,region)

    print(credentials)








main()