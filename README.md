# GetMCSkins

## Basic usage
>python getSkins.py \<amount\> \<skinType\> \<saveDir\> \<offset\>  
amount - The amount of skins that you want to download (up to max int value).  
skinType - Can be 0 (1.8+ 64x64) or 1 (pre-1.8 64x32).  
saveDir - Name of directory to save.  
offset - From which page (20 skins per page) should the script start downloading.  
## Example
>python getSkins.py 10000 0 data/ 0  
This will download 10000 skins in 64x64 format into folder called data inside current directory and will start from first page.  
