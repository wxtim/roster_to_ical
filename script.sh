for input in $(ls ~/depot/rosters/*.csv)
    do
    /usr/local/sci/bin/python2.7 ~/roster_to_ical/calendar.py  $input ${input%.*}.txt
    
    done

