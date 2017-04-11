if [ "$#" = 2 ]; then
	    python3 undo_log.py $1 $2
	else
		python3 undo_recovery.py $1
fi
