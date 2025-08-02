Control systemd service with very basic website.

Made simple on purpose to minimize attack vector (because it is required
to run as root).

To run:

```shell
SERVICE_NAME=my_service.service TITLE="cool service manager" ./main.py
```

or use this simple systemd service

```toml
[Unit]
Description=<service> web manager
After=network.target

[Service]
Environment="HOST=localhost" "TITLE=<service> management" "SERVICE_NAME=my_service.service" "SUBPATH=/my/path"
ExecStart=/path/to/systemd-web/main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
