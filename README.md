# utillib

Python libraries as general utilities.

`runner.py` contains sample invokations of utility libraries.

`utillib`

|____ `browser`

      |____ protocol

      |____ domain_name

      |____ launch

      |____ quit

      |____ get_hyper_links  

      |____ screen_shot

|____ `data`

      |____ string

            |____ substring

|____ `environment`

      |____ get

|____ `general`

      |____ print_dictionary

      |____ logger

      |____ generate_random_string

      |____ get_timestamp_as_string

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

### **browser/launch**

1. Starts a browser session with specified url
2. Launches the specified url page
3. Waits in the state for seconds specified in `wait_seconds_after_launch`
4. Returns the driver object of browser sesssion

---

### **browser/quit**

Stops the specified browser session

---

### **browser/get_hyper_links**

Returns a list of hyper links in specified url as dictionary

Items in dictionary represent each hyper link with

Key : Link text

Value : Hyper Link

---

### **browser/screen_shot**

Saves screen shot of current browser state with specified output file name

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

### **general/logger**

Returns logging handler to specified log file with specified log level.  
log message example entry :  
`[ERROR, 2019-05-12 18:27:04,867, runner.py, runner, main, line#12] test error.`

---

### **general/generate_random_string**

Generate a random string of fixed length.

---

### **general/get_timestamp_as_string**

Gets the current time and returns it as string.

---