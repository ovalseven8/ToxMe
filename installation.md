# Installation
**Please be aware that ToxMe is still an experimental software. You run it on
your own risk!**

ToxMe only works with Python 3. It is recommended to use at least Python 3.4.

### Installation process for Ubuntu Server 16.04:

 1. Install [Python Tornado Framework](http://www.tornadoweb.org/en/stable/)
 2. Install [PyNaCl](https://pypi.python.org/pypi/PyNaCl/)
 3. Go to the place where ToxMe should be installed.
 4. Download ToxMe:
    ```bash
    git clone https://github.com/ovalseven8/ToxMe
    ```
 5. `cd ToxMe/src`
 6. You can just run `python3 main.py` and ToxMe is running and creates
    automatically the server's secret key and the database.

Important notes:
 - At the moment ToxMe does not support multiple processes. One process should,
   however, definitely be enough for decentralized ToxMe servers right now.
 - ToxMe is supposed to run behind a proxy. It is recommend to use for
   example [Hiawatha](https://hiawatha-webserver.org) as a reverse proxy.
   The good thing about Hiawatha is that it offers great security-related
   options to protect against different forms of attacks.
 - ToxMe runs at `127.0.0.1:8888`.
 - ToxMe services should only be accessible via HTTPS.
 - ToxMe logs to `ToxMe/src/server.log`.
 - Only requests to `/api`and `/pk` are handled by ToxMe.
 - In case you run your own ToxMe service, please invest time in a good
   configuration and don't forget to update all your server software
   (including ToxMe, Tornado, PyNaCl) on a regular basis. Also don't forget to
   backup the ToxMe database regularly!
 - ToxMe automatically creates the server's secret key when you start the
   software the first time. Keep it secret!
