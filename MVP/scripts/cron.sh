# MVP script to load cron job file
# send output to a log file

timestamp="$(date +"%D %T")"

#echo $timestamp && crontab /home/pi/scripts/MVP_cron.txt >> /home/pi/MVP/logs/sys.log 2>$1
crontab /home/pi/scripts/MVP_cron.txt