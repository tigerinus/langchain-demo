---
title: AppStore does not load
description: 
published: true
date: 2023-02-14T22:47:53.904Z
tags: troubleshooting
editor: markdown
dateCreated: 2023-02-14T22:24:26.345Z
---

# Legacy AppStore (v0.4.3 and earlier)

Legacy AppStore makes API call to https://api.casaos.io to retrieve app catalog before anything is cached.

1. Run through following commands to check if AppStore API returns app catalog

    ```shell
    curl https://api.casaos.io/casaos-api/token
    ```
    
   If successful, a JSON payload like sample below will be returned
    
    ```json
    {
       "code" : 200,
       "data" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IiIsInBhc3N3b3JkIjoiIiwiZXhwIjoxNjc2NDI0MDIzLCJpc3MiOiJnaW4tYmxvZyJ9._nj5ZFUsicx5q5swKh1cwUdooslnK582By3o3K-P_u4",
       "mssage" : "ok"
    }
    ```

   Copy the token in `data` above and replace the `<token>` below with it
    
    ```shell
    curl https://api.casaos.io/casaos-api/v2/app/newlist  -H "Authorization: <token>"
    ```

	 If AppStore API is running, a JSON payload of app catalog will be returned.

# Git-based AppStore (v0.4.4 and later)

> TODO
