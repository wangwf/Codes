
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

<ul>
<li>
  features1=["error","response","headers","content"] </li>
<li>
   features2=["X-Frame-Options","X-Xss-Protection","X-Content-Type-Options","X-Ua-Compatible",
               "X-Xhr-Current-Location","Content-Type","Etag","Cache-Control",
               "X-Request-Id","X-Runtime","Server","Date",
               "Content-Length","Connection" 
            ]
</li>
<li>
  features3 =["Set-Cookie"]  # =request_method=GET; path=/' or ]
</li>
</ul>




