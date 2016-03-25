import  psutil, configparser, schedule, time, datetime, json
#CONFIG
config=configparser.ConfigParser()
config.read('config.ini')
output=config.get('common', 'output')
interval=config.get('common', 'interval')
snapshot=1    
#DICT                                            		
def createdict(p):
    val = list(p)
    key = p._fields
    result_dict = dict(zip(key, val))
    return result_dict
#TXT FILE
def iffiletxt(file="system_status.txt"):
    global snapshot 
    print("Writing text snapshot {}".format(snapshot))					
    time=datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H:%M:%S')
    status_file_t=open(file, "a+")
    status_file_t.write("Snapshot{0}:{1}\n".format(snapshot,time))
    status_file_t.write("\nCPU {0}\n".format(psutil.cpu_percent(percpu=True)))
    status_file_t.write("\nMEMORY total {0} bytes \navailable {1} \nused {2} \n".format(psutil.virtual_memory()[0], psutil.virtual_memory()[1], psutil.virtual_memory()[4]))
    status_file_t.write("\nHDD read cout {0} \nread {2} \nwrite {3} \nhdd usage {4}\n".format(psutil.disk_io_counters(perdisk=False)[0],psutil.disk_io_counters(perdisk=False)[1],psutil.disk_io_counters(perdisk=False)[2],psutil.disk_io_counters(perdisk=False)[3],psutil.disk_usage('/')))
    status_file_t.write("\nNETWORK: {}\n".format(psutil.net_io_counters(pernic=True)))
    status_file_t.write("\nUSERS {}\n".format(psutil.users()))
    status_file_t.write("\n")
    status_file_t.close()
    snapshot += 1
#JSON FILE
def iffilej(file="system_status.json"):
    global snapshot
    print("Writing text snapshot {}".format(snapshot))
    time=datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H:%M:%S')
    statusfile=open(file, "a+")
    statusfile.write("\nSnapshot{0}:{1}\n".format(snapshot,time))
    statusfile.write("\nCPU\n")
    json.dump(psutil.cpu_percent(), statusfile)
    statusfile.write("\nMEMORY\n")
    json.dump(createdict(psutil.virtual_memory()), statusfile, indent=4)
    statusfile.write("\nHDD\n")
    json.dump(createdict(psutil.disk_io_counters()), statusfile, indent=4)
    statusfile.write("\nNETWORK\n")
    json.dump(psutil.net_io_counters(), statusfile, indent=4)
    statusfile.write("\n")
    statusfile.close()
#OUT
if output == "txt":
    schedule.every(int(interval)).minutes.do(iffiletxt)
    iffiletxt()
    quit()
elif output == "json":
    schedule.every(int(interval)).minutes.do(iffilej)
    iffilej()
    quit()
while True:
   schedule.run_pending()
   time.sleep(10)
