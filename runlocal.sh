HTTPS_PROXY=http://proxy.hcg.gr:8080
https_proxy=http://proxy.hcg.gr:8080
HTTP_PROXY=http://proxy.hcg.gr:8080
http_proxy=http://proxy.hcg.gr:8080
https_proxy=http://proxy.hcg.gr:8080 gunicorn suppl.wsgi -b 0.0.0.0:8004 -w 3 --reload
