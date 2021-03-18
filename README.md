# Application Access Example with Redirect

## How to run

To run this example locally, you'll need a running docker instance and a copy of docker-compose.

Update `aapteleport.yaml` with a token, ca_pin, and auth_server URL of your teleport cluster. You can use a static token or use a token created via `tctl tokens add --type app`.

Run `docker-compose up --build` and you should see the test application appear in your teleport web UI.

## Explanation

This is an example python application that does a couple simple redirects (when accessed directly, not through teleport).

```
curl -Is http://localhost:8000/temp | grep Location
Location: http://localhost/foo/bar

curl -Is http://localhost:8000/temp2 | grep Location
Location: http://localhost:8000/foo/bar
```

The `aapteleport.yaml` file has the following redirect configuration:

```
  - name: aaptest
    uri: "http://web:8000"
    insecure_skip_verify: true
    rewrite:
      redirect:
        - "localhost"
```

When accessing this location through chrome, the network panel in the web developer tools functionality shows that when accessing either /temp or /temp2, the Location header is updated:

```
HTTP/1.1 302 Found
Content-Length: 0
Content-Type: text/html; charset=UTF-8
Date: Thu, 18 Mar 2021 14:58:15 GMT
Location: https://aaptest.teleport.example.com:3080/foo/bar
Server: WSGIServer/0.1 Python/2.7.18
X-DNS-Prefetch-Control: off
```

## Log info from my test cluster

non-debug logs from auth/proxy node (single node cluster)

```
Mar 18 15:08:18 ip-172-31-17-247.us-east-2.compute.internal teleport[22559]: INFO [AUDIT]     app.session.chunk cluster_name:ip-172-31-16-7-us-east-2-compute-internal code:T2008I ei:0 event:app.session.chunk namespace:default server_id:132c1be5-1263-4803-bbf1-ea664692bdef session_chunk_id:46adffe8-ae4c-4b5c-ae14-10f0966fdc9e sid:a64b3784-7ec7-49aa-a66f-f81dd2fefc29 time:2021-03-18T15:08:18.681Z uid:6919e6d6-8cc1-4635-8e3f-2856c36c41b1 user:jeff events/emitter.go:318
Mar 18 15:08:18 ip-172-31-17-247.us-east-2.compute.internal teleport[22559]: INFO [APP:WEB]   Round trip: GET /, code: 200, duration: 243.238151ms tls:version: 304, tls:resume:false, tls:csuite:1301, tls:server:aaptest.telepart.example.com forward/fwd.go:196
Mar 18 15:08:19 ip-172-31-17-247.us-east-2.compute.internal teleport[22559]: INFO [APP:WEB]   Round trip: GET /favicon.ico, code: 404, duration: 98.193314ms tls:version: 304, tls:resume:false, tls:csuite:1301, tls:server:aaptest.telepart.example.com forward/fwd.go:196
Mar 18 15:08:31 ip-172-31-17-247.us-east-2.compute.internal teleport[22559]: INFO [APP:WEB]   Round trip: GET /temp, code: 302, duration: 91.662631ms tls:version: 304, tls:resume:false, tls:csuite:1301, tls:server:aaptest.telepart.example.com forward/fwd.go:196
Mar 18 15:08:31 ip-172-31-17-247.us-east-2.compute.internal teleport[22559]: INFO [APP:WEB]   Round trip: GET /foo/bar, code: 200, duration: 91.128331ms tls:version: 304, tls:resume:false, tls:csuite:1301, tls:server:aaptest.telepart.example.com forward/fwd.go:196
```

debug logs from application_service via `docker-compose up -d && docker-compose logs -f app`:

```
Attaching to aaptest_app_1
app_1  | INFO [PROC]      Generating new host UUID: 132c1be5-1263-4803-bbf1-ea664692bdef. service/service.go:583
app_1  | DEBU [SQLITE]    Connected to: file:/var/lib/teleport/proc/sqlite.db?_busy_timeout=10000&_sync=OFF, poll stream period: 1s lite/lite.go:173
app_1  | DEBU [SQLITE]    Synchronous: 0, busy timeout: 10000 lite/lite.go:218
app_1  | DEBU [KEYGEN]    SSH cert authority started with no keys pre-compute. native/native.go:107
app_1  | DEBU [PROC]      Adding service to supervisor. service:register.app service/supervisor.go:181
app_1  | DEBU [PROC]      Adding service to supervisor. service:apps.start service/supervisor.go:181
app_1  | DEBU [PROC]      Adding service to supervisor. service:apps.stop service/supervisor.go:181
app_1  | DEBU [PROC]      Adding service to supervisor. service:common.rotate service/supervisor.go:181
app_1  | DEBU [PROC:1]    Service has started. service:apps.start service/supervisor.go:242
app_1  | DEBU [PROC:1]    Service has started. service:apps.stop service/supervisor.go:242
app_1  | DEBU [PROC:1]    No signal pipe to import, must be first Teleport process. service/service.go:761
app_1  | DEBU [PROC:1]    Service has started. service:common.rotate service/supervisor.go:242
app_1  | DEBU [PROC:1]    Service has started. service:register.app service/supervisor.go:242
app_1  | INFO [PROC:1]    Joining the cluster with a secure token. service/connect.go:349
app_1  | DEBU [PROC:1]    Generating new key pair for App first-time-connect. service/connect.go:256
app_1  | DEBU [AUTH]      Registering node to the cluster. auth-servers:[{telepart.example.com:3080 tcp }] auth/register.go:121
app_1  | DEBU [AUTH]      The first specified auth server appears to be a proxy. auth/register.go:127
app_1  | INFO [AUTH]      Attempting registration via proxy server. auth/register.go:133
app_1  | DEBU [CLIENT]    HTTPS client init(proxyAddr=telepart.example.com:3080, insecure=false) client/weblogin.go:307
app_1  | INFO [AUTH]      Successfully registered via proxy server. auth/register.go:140
app_1  | DEBU [PROC:1]    Deleted generated key pair App first-time-connect. service/connect.go:242
app_1  | INFO [PROC]      App has obtained credentials to connect to cluster. service/connect.go:377
app_1  | DEBU [PROC]      Attempting to connect to Auth Server directly. service/connect.go:793
app_1  | DEBU [PROC]      Attempting to connect to Auth Server through tunnel. service/connect.go:801
app_1  | DEBU [CLIENT]    HTTPS client init(proxyAddr=telepart.example.com:3080, insecure=false) client/weblogin.go:307
app_1  | DEBU [PROC]      Discovered address for reverse tunnel server: telepart.example.com:3080. service/connect.go:881
app_1  | DEBU [HTTP:PROX] No valid environment variables found. proxy/proxy.go:222
app_1  | DEBU [HTTP:PROX] No proxy set in environment, returning direct dialer. proxy/proxy.go:137
app_1  | DEBU [PROC]      Connected to Auth Server through tunnel. service/connect.go:807
app_1  | INFO [PROC:1]    The process has successfully wrote credentials and state of App to disk. service/connect.go:417
app_1  | DEBU [PROC:1]    Connected client: Identity(App, cert(132c1be5-1263-4803-bbf1-ea664692bdef.ip-172-31-16-7-us-east-2-compute-internal issued by ip-172-31-16-7-us-east-2-compute-internal:241862610978300771705338367615132370622),trust root(ip-172-31-16-7-us-east-2-compute-internal:241862610978300771705338367615132370622)) service/connect.go:81
app_1  | DEBU [PROC:1]    Connected server: Identity(App, cert(132c1be5-1263-4803-bbf1-ea664692bdef.ip-172-31-16-7-us-east-2-compute-internal issued by ip-172-31-16-7-us-east-2-compute-internal:241862610978300771705338367615132370622),trust root(ip-172-31-16-7-us-east-2-compute-internal:241862610978300771705338367615132370622)) service/connect.go:82
app_1  | DEBU [PROC]      Adding service to supervisor. service:auth.client.app service/supervisor.go:181
app_1  | DEBU [PROC:1]    Broadcasting event. event:AppsIdentity service/supervisor.go:332
app_1  | DEBU [PROC:1]    Service is completed and removed. service:register.app service/supervisor.go:219
app_1  | DEBU [APP:SERVI] Received event "AppsIdentity". service/service.go:2718
app_1  | DEBU [PROC:1]    Creating sqlite backend for [app:service:1]. service/service.go:1443
app_1  | DEBU [SQLITE]    Connected to: file:/var/lib/teleport/cache/app:service:1/sqlite.db?_busy_timeout=10000&_sync=OFF, poll stream period: 100ms lite/lite.go:173
app_1  | DEBU [PROC:1]    Service has started. service:auth.client.app service/supervisor.go:242
app_1  | DEBU [SQLITE]    Synchronous: 0, busy timeout: 10000 lite/lite.go:218
app_1  | DEBU [AUTH]      GRPC(CLIENT): keep alive 1m0s count: 3. auth/clt.go:320
app_1  | DEBU [HTTP:PROX] No valid environment variables found. proxy/proxy.go:222
app_1  | DEBU [HTTP:PROX] No proxy set in environment, returning direct dialer. proxy/proxy.go:137
app_1  | INFO [APP:SERVI] Cache "apps" first init succeeded. cache/cache.go:574
app_1  | INFO [AUDIT:1]   Creating directory /var/lib/teleport/log. service/service.go:1867
app_1  | INFO [AUDIT:1]   Creating directory /var/lib/teleport/log/upload. service/service.go:1867
app_1  | INFO [AUDIT:1]   Creating directory /var/lib/teleport/log/upload/sessions. service/service.go:1867
app_1  | INFO [AUDIT:1]   Creating directory /var/lib/teleport/log/upload/sessions/default. service/service.go:1867
app_1  | INFO [AUDIT:1]   Creating directory /var/lib/teleport/log. service/service.go:1867
app_1  | INFO [AUDIT:1]   Creating directory /var/lib/teleport/log/upload. service/service.go:1867
app_1  | INFO [AUDIT:1]   Creating directory /var/lib/teleport/log/upload/streaming. service/service.go:1867
app_1  | INFO [AUDIT:1]   Creating directory /var/lib/teleport/log/upload/streaming/default. service/service.go:1867
app_1  | DEBU [PROC]      Adding service to supervisor. service:uploader.service service/supervisor.go:181
app_1  | DEBU [PROC]      Adding service to supervisor. service:uploader.shutdown service/supervisor.go:181
app_1  | DEBU [PROC]      Adding service to supervisor. service:fileuploader.service service/supervisor.go:181
app_1  | DEBU [PROC]      Adding service to supervisor. service:fileuploader.shutdown service/supervisor.go:181
app_1  | DEBU [PROC]      Adding service to supervisor. service:debug.app.service service/supervisor.go:181
app_1  | DEBU [PROC:1]    Service has started. service:uploader.service service/supervisor.go:242
app_1  | DEBU [PROC]      Adding service to supervisor. service:debug.app.shutdown service/supervisor.go:181
app_1  | DEBU [PROC:1]    Service has started. service:debug.app.shutdown service/supervisor.go:242
app_1  | DEBU [PROC:1]    Service has started. service:uploader.shutdown service/supervisor.go:242
app_1  | DEBU [PROC:1]    Service has started. service:fileuploader.service service/supervisor.go:242
app_1  | DEBU [PROC:1]    Service has started. service:debug.app.service service/supervisor.go:242
app_1  | DEBU [PROC:1]    Service has started. service:fileuploader.shutdown service/supervisor.go:242
app_1  | DEBU [PROC:1]    Broadcasting event. event:DebugAppReady service/supervisor.go:332
app_1  | DEBU [PROC:1]    Service is completed and removed. service:debug.app.service service/supervisor.go:219
app_1  | DEBU [APP:SERVI] Starting App heartbeat with announce period: 1m0s, keep-alive period 5m44.911258128s, poll period: 5s srv/heartbeat.go:139
app_1  | DEBU [PROXY:AGE] Starting agent pool 132c1be5-1263-4803-bbf1-ea664692bdef.ip-172-31-16-7-us-east-2-compute-internal.ip-172-31-16-7-us-east-2-compute-internal... cluster:ip-172-31-16-7-us-east-2-compute-internal reversetunnel/agentpool.go:166
app_1  | DEBU [PROC:1]    Broadcasting event. event:AppsReady service/supervisor.go:332
app_1  | DEBU [PROXY:AGE] Seeking: {Addr:telepart.example.com:3080 AddrNetwork:tcp Path:}. cluster:ip-172-31-16-7-us-east-2-compute-internal reversetunnel/agentpool.go:196
app_1  | DEBU [PROXY:AGE] Adding agent(leaseID=1,state=connecting) -> ip-172-31-16-7-us-east-2-compute-internal:telepart.example.com:3080. cluster:ip-172-31-16-7-us-east-2-compute-internal reversetunnel/agentpool.go:284
app_1  | DEBU [PROC:1]    Broadcasting mapped event. in:AppsReady out:EventMapping(in=[AppsReady], out=TeleportReady) service/supervisor.go:351
app_1  | DEBU [HTTP:PROX] No valid environment variables found. proxy/proxy.go:222
app_1  | DEBU [HTTP:PROX] No proxy set in environment, returning direct dialer. proxy/proxy.go:137
app_1  | INFO [APP:SERVI] All applications successfully started. service/service.go:2874
app_1  | INFO [PROC:1]    The new service has started successfully. Starting syncing rotation status with period 10m0s. service/connect.go:433
app_1  | INFO [APP:SERVI] Connected to 3.17.189.92:3080 leaseID:1 target:telepart.example.com:3080 reversetunnel/agent.go:341
app_1  | DEBU [APP:SERVI] Agent connected to proxy: [cfed963c-b394-4d9b-8a50-19c2cd22ca72.ip-172-31-16-7-us-east-2-compute-internal cfed963c-b394-4d9b-8a50-19c2cd22ca72 localhost 127.0.0.1 ::1 ip-172-31-17-247-us-east-2-compute-internal telepart.example.com remote.kube.proxy.teleport.cluster.local]. leaseID:1 target:telepart.example.com:3080 reversetunnel/agent.go:343
app_1  | DEBU [APP:SERVI] Changing state connecting -> connected. leaseID:1 target:telepart.example.com:3080 reversetunnel/agent.go:185
app_1  | DEBU [APP:SERVI] Discovery request channel opened: teleport-discovery. leaseID:1 target:telepart.example.com:3080 reversetunnel/agent.go:454
app_1  | DEBU [APP:SERVI] handleDiscovery requests channel. leaseID:1 target:telepart.example.com:3080 reversetunnel/agent.go:472
```
output paused until my first access of the application in the web browser at /

```
app_1  | DEBU [APP:SERVI] Transport request: teleport-transport. leaseID:1 target:telepart.example.com:3080 reversetunnel/agent.go:428
app_1  | DEBU [APP:SERVI] Received out-of-band proxy transport request for @local-node [132c1be5-1263-4803-bbf1-ea664692bdef.ip-172-31-16-7-us-east-2-compute-internal]. leaseID:1 target:telepart.example.com:3080 reversetunnel/transport.go:229
app_1  | DEBU [APP:SERVI] Handing off connection to a local SSH service leaseID:1 target:telepart.example.com:3080 reversetunnel/transport.go:301
app_1  | DEBU [AUTH]      ClientCertPool -> cert(ip-172-31-16-7-us-east-2-compute-internal issued by ip-172-31-16-7-us-east-2-compute-i
## Log info from my test cluster
nternal:241862610978300771705338367615132370622) auth/middleware.go:569
app_1  | DEBU [AUTH]      ClientCertPool -> cert(ip-172-31-16-7-us-east-2-compute-internal issued by ip-172-31-16-7-us-east-2-compute-internal:39735523962307312490014810652290170243) auth/middleware.go:569
app_1  | DEBU             Skipping login 0cf8fc2d-fde3-460f-a4eb-07ac5227358d, not a valid Unix login. services/role.go:360
app_1  | DEBU [APP:SERVI] Using async streamer for session 46adffe8-ae4c-4b5c-ae14-10f0966fdc9e. app/session.go:170
app_1  | INFO             Round trip: GET /, code: 200, duration: 2.1029ms tls:version: 304, tls:resume:false, tls:csuite:1301, tls:server:69702d3137322d33312d31362d372d75732d656173742d322d636f6d707574652d696e7465726e616c.teleport.cluster.local forward/fwd.go:196
app_1  | DEBU             Skipping login 0cf8fc2d-fde3-460f-a4eb-07ac5227358d, not a valid Unix login. services/role.go:360
app_1  | INFO             Round trip: GET /favicon.ico, code: 404, duration: 6.5132ms tls:version: 304, tls:resume:false, tls:csuite:1301, tls:server:69702d3137322d33312d31362d372d75732d656173742d322d636f6d707574652d696e7465726e616c.teleport.cluster.local forward/fwd.go:196
```

output paused again until I accessed /temp

```
app_1  | DEBU             Skipping login 0cf8fc2d-fde3-460f-a4eb-07ac5227358d, not a valid Unix login. services/role.go:360
app_1  | INFO             Round trip: GET /temp, code: 302, duration: 2.9524ms tls:version: 304, tls:resume:false, tls:csuite:1301, tls:server:69702d3137322d33312d31362d372d75732d656173742d322d636f6d707574652d696e7465726e616c.teleport.cluster.local forward/fwd.go:196
app_1  | DEBU             Skipping login 0cf8fc2d-fde3-460f-a4eb-07ac5227358d, not a valid Unix login. services/role.go:360
app_1  | INFO             Round trip: GET /foo/bar, code: 200, duration: 2.4029ms tls:version: 304, tls:resume:false, tls:csuite:1301, tls:server:69702d3137322d33312d31362d372d75732d656173742d322d636f6d707574652d696e7465726e616c.teleport.cluster.local forward/fwd.go:196
app_1  | DEBU [APP:SERVI] Ping -> 3.17.189.92:3080. leaseID:1 target:telepart.example.com:3080 reversetunnel/agent.go:409
```

Here are details from chrome's network panel in the developer tools. (right click on the request and hover over Copy menu and then choose Copy request headers and Copy response headers, respectively:

* accessing / request and response headers

    ```
    GET / HTTP/1.1
    Host: aaptest.telepart.example.com:3080
    Connection: keep-alive
    sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"
    sec-ch-ua-mobile: ?0
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
    Sec-Fetch-Site: same-origin
    Sec-Fetch-Mode: navigate
    Sec-Fetch-Dest: document
    Accept-Encoding: gzip, deflate, br
    Accept-Language: en-US,en;q=0.9
    Cookie: grv_app_session=2161436becf922686c356b949c2ef7cf9023316e63eca5270e87e60b8a239709
    ```
   
    ```
    HTTP/1.1 200 OK
    Content-Length: 13
    Content-Type: text/html; charset=UTF-8
    Date: Thu, 18 Mar 2021 15:08:18 GMT
    Server: WSGIServer/0.1 Python/2.7.18
    X-DNS-Prefetch-Control: off
    ```

* accessing /temp request / response headers

   ```
   GET /temp HTTP/1.1
   Host: aaptest.telepart.example.com:3080
   Connection: keep-alive
   sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"
   sec-ch-ua-mobile: ?0
   Upgrade-Insecure-Requests: 1
   User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36
   Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
   Sec-Fetch-Site: none
   Sec-Fetch-Mode: navigate
   Sec-Fetch-User: ?1
   Sec-Fetch-Dest: document
   Accept-Encoding: gzip, deflate, br
   Accept-Language: en-US,en;q=0.9
   Cookie: grv_app_session=2161436becf922686c356b949c2ef7cf9023316e63eca5270e87e60b8a239709
   ```
   
   ```
   HTTP/1.1 302 Found
   Content-Length: 0
   Content-Type: text/html; charset=UTF-8
   Date: Thu, 18 Mar 2021 15:08:31 GMT
   Location: https://aaptest.telepart.example.com:3080/foo/bar
   Server: WSGIServer/0.1 Python/2.7.18
   X-DNS-Prefetch-Control: off
   ```
