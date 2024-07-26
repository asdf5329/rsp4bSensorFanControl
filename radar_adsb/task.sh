ps -eaf | grep send_message.py | grep -v grep
# if not found - equals to 1, start it
if [ $? -eq 1 ]
then
python3 -O /sdr/radar_adsb/get_message/send_message.py &
echo `date "+%G-%m-%d %H:%M:%S"`" send_message            restart" >> /var/log/sdr.txt
echo "------------------------------------------------------------------------"
else
echo `date "+%G-%m-%d %H:%M:%S"`" send_message            running" >> /var/log/sdr.txt
echo "------------------------------------------------------------------------"
fi

