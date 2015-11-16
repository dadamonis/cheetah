#!/bin/bash

START=$(date +%s)
LOG=/var/log/shell/killnuo.log
# Set STOP commands
STOPAGENT="launchctl stop com.nuodb.agent"
STOPREST="launchctl stop com.nuodb.restsvc" 
STOPTRAY="launchctl stop com.nuodb.traymonitor" 
echo "Run Date: " $(Date) >> $LOG
echo
echo "Checking Nuo process status..." | tee -a $LOG
echo
echo "### DEBUG DETAILS: /var/log/shell/killnuo.log ### "
echo
function currentStatus {
	AGENT=$(ps -ef | grep nuoagent.jar | awk '{print $2}' | wc -l)
	REST=$(ps -ef | grep nuodbtraymonitor.jar | awk '{print $2}' | wc -l)
	TRAY=$(ps -ef | grep nuodb-rest-api.jar | awk '{print $2}' | wc -l)
	#debug statements
	echo >> $LOG
	echo "AGENT = " $AGENT >> $LOG
	echo "REST  = " $REST >> $LOG
	echo "TRAY  = " $TRAY >> $LOG
	echo >> $LOG

	if [[ $AGENT -lt 2  &&  $REST -lt 2 && $TRAY -lt 2 ]]
	then
		echo "No running NUODB Processes found: ### Exiting ###" | tee -a $LOG
		echo | tee -a $LOG	
	else shutdown
	fi
}
function shutdown {
	echo "Discovered one or more running NUODB processes: Executing shutdown..." | tee -a $LOG
	echo ""
	echo ">> Stopping agent..." | tee -a $LOG
	eval $STOPAGENT
	echo
	echo ">> Stopping REST Service..." | tee -a $LOG
	eval $STOPREST
	echo
	echo ">> Stopping Tray Monitor..." | tee -a $LOG
	eval $STOPTRAY
	sleep 4s
	END=$(date +%s)
	DIFF=$(((END - $START)-4))
	echo
	echo "Shutdown script took $DIFF seconds to complete" | tee -a $LOG
	echo | tee -a $LOG
	echo "Checking shutdown state..."

	currentStatus		
}
currentStatus
