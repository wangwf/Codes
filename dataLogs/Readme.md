
A data science project to analyze network capture file(s). This is a on-going project, following the below steps.

<ul>
<li>Data Cleaning: check missing values, data format consistence check,
reshape data. </li>
<li>Data Exploratory Analysis: feature distributions, mutual information, importance.</li>    
<li>Data Modeling: Build a model forcasting the reqest response size.  
</ul>


Included Files:

extract.ipynb:  data-cleaning and rewrite data into CSV, json and MongoDB

exploratory.ipynb: exploratory analysis (to be continue)

graphlab.ipynb : data model using Graphlab (just start...)

mongodb.ipynb : mongodb related query and reshape data.

Features:

  features1=["error","response","headers","content"]

  features2=["X-Frame-Options","X-Xss-Protection","X-Content-Type-Options","X-Ua-Compatible",
               "X-Xhr-Current-Location","Content-Type","Etag","Cache-Control",
               "X-Request-Id","X-Runtime","Server","Date",
               "Content-Length","Connection" 
            ]

  features3 =["Set-Cookie"]  # =request_method=GET; path=/' or ]





