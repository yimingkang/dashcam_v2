0- Modify a few variables in dashcam, dashcam.sh, main.py and recorder.py, change permission with `sudo chmod 755 dashcam` and `sudo chmod 755 dashcam.sh`  
1- Copy dashcam to /etc/init.d/  
2- Config bootup script with `sudo update-rc.d dashcam defaults` (after changing a few variables of course)  
3- `sudo reboot` and voila!  
