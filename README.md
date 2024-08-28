# CFAutoDNS | Cloudflare Autmatic DNS Record Updater
<img alt="GitHub last commit (branch)" src="https://img.shields.io/github/last-commit/Eli-Zac/CFAutoDNS/main"> <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/Eli-Zac/CFAutoDNS"> <img alt="GitHub" src="https://img.shields.io/github/license/Eli-Zac/CFAutoDNS?color=white">

> #### Recomended For Use With A Dynamic IP Address.
> This tool will scan for ip (external ip) changes on your windows device and automatically update your set record on Cloudflare DNS. You dont have to worry about getting the record id, this app gets it automatically.

## Donate
[![Donate Via Paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.me/Jasonkkf)


## Installation
> This program is compatible with Windows.

To download the latest version of CFAutoDNS visit the releases page or click the link below.

https://github.com/Eli-Zac/CFAutoDNS/releases/latest
___
To download an older version of CFAutoDNS visit the link below.

https://github.com/Eli-Zac/CFAutoDNS/releases


## Usage
This script is used with crontab. Specify the frequency of execution through crontab.

```bash
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday 7 is also Sunday on some systems)
# │ │ │ │ │ ┌───────────── command to issue                               
# │ │ │ │ │ │
# │ │ │ │ │ │
# * * * * * /bin/bash {Location of the script}
```

## Tested Environments:
macOS Mojave version 10.14.6 (x86_64) <br />
AlmaLinux 9.3 (Linux kernel: 5.14.0 | x86_64) <br />
Debian Bullseye 11 (Linux kernel: 6.1.28 | aarch64) <br />

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Reference
This script was made with reference from [Keld Norman](https://www.youtube.com/watch?v=vSIBkH7sxos) video.

## License
[MIT](https://github.com/K0p1-Git/cloudflare-ddns-updater/blob/main/LICENSE)
