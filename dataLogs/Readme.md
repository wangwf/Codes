
A data science project to analyze network capture file(s). This is a on-going project, following the below steps.

<ul>
<li>Data Cleaning: check missing values, data format consistence check,
reshape data. </li>
<li>Data Exploratory Analysis: feature distributions, mutual information, importance.</li>
<li>Data Modeling: Build a model forcasting the reqest response size.
</ul>


Included Files:
<ul>
<li>extract.ipynb:  data-cleaning and rewrite data into CSV, json and MongoDB </li>
<li>exploratory.ipynb: exploratory analysis (to be continue) </li>
<li>graphlab.ipynb : data model using Graphlab (just start...) </li>
<li>mongodb.ipynb : mongodb related query and reshape data. </li>
</ul>

Currently selected features:



* response
 * headers
   * X-Frame-Options, SAMEORIGIN,
   * X-Xss-Protection,13:1; mode=block,
   * X-Content-Type-Options,7:nosniff
   * X-Ua-Compatible,8:chrome=1,:
   * X-Xhr-Current-Location,1:/,]44:12:
   * Content-Type,24:text/html; charset=utf-8,]45:4:
   * Etag,34:"ea927ca92e0c7a85b168d210be0a5df4",]56:13:
   * Cache-Control,35:max-age=0, private, must-revalidate,]56:12:
   * X-Request-Id,36:1c96e7f2-2bd3-4070-b2b9-73ad728c111f,]23:9:
   * X-Runtime,8:0.017533,]50:6:
   * Server,37:WEBrick/1.3.1 (Ruby/2.1.2/2014-05-08),]40:4:
   * Date,29:Tue, 14 Oct 2014 00:36:07 GMT,]25:14:
   * Content-Length,4:3726,]28:10:
   * Connection,10:Keep-Alive,]44:10:
   * Set-Cookie,26:request_method=GET; path=/
 * content
* request
 * httpversion,8:1:1#1:1#]11:
 * client_conn,69:7:
 * address,24:12:50.59.22.130,5:41764#]12:
 * requestcount,1:1#5:
 * error,0:~}4:
 * port,2:80#6:
 * scheme,4:http,4:
 * path,1:/,4:
 * host,13:54.165.254.99,7:
 * headers,399:25:4:
  * Host,14:54.198.102.255,]28:10:
  * Connection,10:keep-alive,]87:6:
  * Accept,74:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,]139:10:
  * User-Agent,120:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36,
    * Accept-Encoding,17:gzip,deflate,sdch,]55:15:
    * Accept-Language,32:en-US,en;q=0.8,ms;q=0.6,id;q=0.4,]]7:
 * content,0:,6:
 * method,3:GET,19:
 * ssl_setup_timestamp,0:~15:
 * timestamp_start,17:1413247021.052226^2:
 * ip,13:54.165.254.99,19:
 * tcp_setup_timestamp,17:1413247021.292858^13:
 * timestamp_end,17:1413247021.055149^



The log files follows the pattern n1:length-n1-string:1#]}:n2:length-n2-string:1#]}... nn:length-nn-string:1#]}


Important features:
path

decisition tree/random forest/Gradient Boosted tree
multi-dimensional gaussian : path,

Clustering: nearest neighbor, kmeans

Naive bayes

