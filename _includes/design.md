- Logstash chooses Elasticsearch Data Index sizes, which can be
tailored to your log data for best analysis performance.
- While the template allows for as few as one Elasticsearch node, we
recommend a minimum of three for redundancy and data access speed.
- You can segment your logging agents to point to any Logstash server
which allows for horizontal growth of Logstash endpoints. When one
Logstash server is overwhelmed, you can point your agents to
another Logstash server.
- For long term storage, you can stream logs to an additional
endpoint more appropriate for archival such as Hadoop and maintain a short 
term expiry time on your Elasticsearch log data.
