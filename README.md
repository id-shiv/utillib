# utillib

Python libraries as general utilities.

`runner.py` contains sample invokations of utility libraries.

`utillib`

|____ `browser`

      |____ protocol

      |____ domain_name

      |____ start

      |____ stop

      |____ get_hyper_links  

|____ `data`

      |____ string

            |____ substring

|____ `environment`

      |____ get

|____ `general`

      |____ print_dictionary

## Modules

---

### **browser/protocol**

Returns communication protocol specified in the url.  
e.g. : returns "https" if specified url is <https://youtube.com>.

---

### **browser/domain_name**

Returns domain name specified in the url.

e.g. : returns "youtube.com" if specified url is <https://youtube.com>.

---

### **browser/start**

1. Starts a browser session with specified url
2. Launches the specified url page
3. Waits in the state for seconds specified in `wait_seconds_after_launch`
4. Returns the driver object of browser sesssion

---

### **browser/stop**

Stops the specified browser session

---

### **browser/get_hyper_links**

Returns a list of hyper links in specified url as dictionary

Items in dictionary represent each hyper link with

Key : Link text

Value : Hyper Link

---

### **data/string/sub_string**

Retrieve substring of a string between specified start and end

---

### **environment/get**

Returns environment parameters as a dictionary

1. Virtual environment path
2. Python version

---

### **general/print_dictionary**

Print dictionary as table

`width` : specify width of the table. By default 80 is set.  
`cell_outer_border` : specify cell outer border character. By default "--" is set.  
`cell_inner_border` : specify cell inner border character. By default "|" is set.

---