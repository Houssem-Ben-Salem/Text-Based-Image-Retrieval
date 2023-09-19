
## Setting Up and Using Elasticsearch, Logstash, and Kibana (ELK Stack) on Ubuntu

### Step 1: Start ELK Services

To begin, ensure that Elasticsearch, Logstash, and Kibana are properly installed on your Ubuntu machine.

**1.1 Start Services**

```bash
sudo systemctl start elasticsearch
sudo systemctl start logstash
sudo systemctl start kibana
```

**1.2 Check Service Status**

To verify that each service is running:

```bash
sudo systemctl status elasticsearch
sudo systemctl status logstash
sudo systemctl status kibana
```

You should see an `active (running)` status for each service.

### Step 2: Use Mapping for Elasticsearch

Before indexing, it's beneficial to define a mapping for Elasticsearch. This tells Elasticsearch how to interpret and store various fields in your data.

**2.1 Apply Mapping**

Navigate to the directory containing the `mapping_flickr_photos.json`:

```bash
curl -X PUT "localhost:9200/your_index_name" -H "Content-Type: application/json" -d @mapping_flickr_photos.json
```

Replace `your_index_name` with a name suitable for your index.

### Step 3: Indexing with Logstash

With Logstash, you can parse and send your data (in this case, image metadata) to Elasticsearch.

**3.1 Modify Configuration File**

Before using the `photos_flicker_conf_37.conf`, make sure to modify the path to the CSV file that contains your image metadata. Open the configuration file and look for the `path` parameter and update its value with the correct path.

**3.2 Start Indexing Process**

```bash
sudo /usr/share/logstash/bin/logstash -f path_to_photos_flicker_conf_37.conf
```

Replace `path_to_photos_flicker_conf_37.conf` with the correct path to the `photos_flicker_conf_37.conf` on your machine.

### Step 4: Verifying Indexation using Kibana

Once you've indexed your data with Logstash, it's always a good practice to verify that the data is indexed correctly using Kibana.

**4.1 Access Kibana**

Open a web browser and navigate to:

```
http://localhost:5601
```

This assumes Kibana is running on the default port `5601`. If you've changed the port during installation, replace `5601` with your specified port.

**4.2 Define the Index Pattern**

1. On the Kibana home page, click on the `Management` tab (usually represented by a gear icon ⚙️).
2. Under `Kibana`, click `Index Patterns`.
3. Click `Create Index Pattern`.
4. In the `Index pattern` box, type the name of your index (e.g., the name you used in place of `your_index_name` earlier).
5. Click `Next step`.
6. Select a field that contains a timestamp if available; otherwise, proceed without it.
7. Click `Create index pattern`.

**4.3 Explore Your Indexed Data**

1. Click on the `Discover` tab on the left side panel.
2. From the available index patterns, choose the one you just created.
3. You should now see a timeline representing your indexed data and below it, the actual documents. You can expand each document to view its fields and values.

Use the search bar at the top to query your indexed data using the Elasticsearch query syntax. For instance, if you've indexed images and added `tags`, you can search for specific tags to verify the data's presence.
