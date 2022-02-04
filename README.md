# OpenRedirect Fuzzer

OpenRedirect Fuzzer allows you to fuzz an HTTP parameter and detect open redirect vulnerabilities by checking the original domain and the domain after redirect. 

## Installation

```bash
$ git clone https://github.com/xanhacks/openredirect-fuzzer
$ cd openredirect-fuzzer
$ python3 -m pip install -r requirements.txt
```

## Usage

Basic example

```bash
$ python3 fuzzer.py -u 'https://example.com/login?redirect=FUZZ' -w payloads/open-redirect-payload-list.lst --cookies 'session=abcd'
```

Practical example :

```bash
$ python3 fuzzer.py -u 'https://preview2.dolibarr.org/accountancy/admin/card.php?backtopage=FUZZ&cancel=a' -w payloads/
open-redirect-payload-list.lst --cookies 'DOLUSERCOOKIE_boxfilter_task=all; DOLSESSID_e2cecaf5782bec0de940a8a55e2029e7=a6h19pkt4cgsp72nlffo2sq249; DOLSESSTIMEOU
T_e2cecaf5782bec0de940a8a55e2029e7=2000' --proxy 'http://127.0.0.1:8080'
Start fuzzing ...
Try payload : /%09/example.com
=> Error - Invalid schema

Try payload : /%2f%2fexample.com
=> 302 | Location : example.com, new URL : https://preview2.dolibarr.org/accountancy/admin/example.com

Try payload : /%2f%2f%2fbing.com%2f%3fwww.omise.co
=> 302 | Location : bing.com/?www.omise.co, new URL : https://preview2.dolibarr.org/accountancy/admin/bing.com/?www.omise.co

Try payload : /%2f%5c%2f%67%6f%6f%67%6c%65%2e%63%6f%6d/
=> 302 | Location : google.com/, new URL : https://preview2.dolibarr.org/accountancy/admin/google.com/

Try payload : /%5cexample.com
=> 302 | Location : example.com, new URL : https://preview2.dolibarr.org/accountancy/admin/example.com

Try payload : /%68%74%74%70%3a%2f%2f%67%6f%6f%67%6c%65%2e%63%6f%6d
=> 302 | Location : /http//google.com, new URL : https://preview2.dolibarr.org/http//google.com

Try payload : /.example.com
=> 302 | Location : /.example.com, new URL : https://preview2.dolibarr.org/.example.com

Try payload : //%09/example.com
=> 302 | Location : /example.com, new URL : https://preview2.dolibarr.org/example.com

Try payload : //%5cexample.com
=> 302 | Location : example.com, new URL : https://preview2.dolibarr.org/accountancy/admin/example.com

Try payload : ///%09/example.com
=> 302 | Location : /example.com, new URL : https://preview2.dolibarr.org/example.com
[...]
```
