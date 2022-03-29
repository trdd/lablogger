#!/usr/bin/bash
INTERVALL=30
LOGDIR=$HOME/lablogger

CONFDIR=${XDG_CONFIG_DIR:-$HOME/.config}/lablogger
UNITSDIR=$CONFDIR/units

UNITS=$(find $UNITSDIR -type f -executable -name '??_*'|sort)
NUMU_OLD=0
OF=''

while true
do
	UNITS=$(find $UNITSDIR -type f -executable -name '??_*'|sort)
	NUMU=$(echo $UNITS|wc -w)
	if [[ $NUMU -ne $NUMU_OLD || $(echo $OF|cut -d_ -f1) -ne $(date +%Y%m%d) ]]; then
		OF=$LOGDIR/$(date +%Y%m%d_%H%M%S).txt 
		echo -n "# " >> $OF
		for U in $UNITS
		do
			echo -n "$(echo $U | cut -d_ -f2) " >> $OF
		done 
		echo -ne "\n" >> $OF
		NUMU_OLD=$NUMU
	fi
	for U in $UNITS
	do
		echo -n "$($U) " >> $OF
	done
	echo -ne "\n" >> $OF
	sleep $INTERVALL 
done
