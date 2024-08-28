# CFAutoDNS | Cloudflare Autmatic DNS Record Updater
<img alt="GitHub last commit (branch)" src="https://img.shields.io/github/last-commit/Eli-Zac/CFAutoDNS/main"> <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/Eli-Zac/CFAutoDNS"> <img alt="GitHub" src="https://img.shields.io/github/license/Eli-Zac/CFAutoDNS?color=white">

> #### Recomended For Use With A Dynamic IP Address.
> This tool will scan for ip (external ip) changes on your windows device and automatically update your set record on Cloudflare DNS. You dont have to worry about getting the record id, this app gets it automatically.

## Donate :) Nah dont idc
[![Donate Via Paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://store.spectracraft.com.au/category/454558)


## Installation
> This program is compatible with Windows.

To download the latest version of CFAutoDNS visit the releases page or click the link below.

https://github.com/Eli-Zac/CFAutoDNS/releases/latest
___
To download an older version of CFAutoDNS visit the link below.

https://github.com/Eli-Zac/CFAutoDNS/releases


## Usage
> After downloading the exe file from the releases tab, open the file and the program should run automatically. 

### To automatically run on computer start without logging in:
1. Press ```⊞ Win``` + ```R``` to open run.
2. Type in ```taskschd.msc``` and press enter.
3. Click on ```Task Scheduler Library``` in the left menu.
4. Under actions, click on ```Create Basic Task...```.
5. In the name box type ```CFAutoDNS``` then click next.
6. For trigger, select ```When the computer starts``` then click next.
7. For action, select ```Start a program``` then click next.
8. Click on browse and choose the CFAutoDNS exe file.
9. Save.


## Tested Environments:
Windows 11 (23H2 22631.4037)<br />

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://github.com/Eli-Zac/CFAutoDNS/blob/main/LICENSE)
