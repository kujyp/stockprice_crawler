#!/bin/bash

/bin/curl localhost:8000/api/crawlers/corps/
/bin/curl localhost:8000/api/crawlers/stockprices/?from_date=$(date +'%Y-%m-%d')
