import  psutil, configparser, schedule, time, datetime, json, logging
#LOGGER
logger = logging.getLogger()
handler = logging.FileHandler('applog.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
#CONFIG
config=configparser.ConfigParser()
config.read('config5.ini')
output=config.get('common', 'output')
interval=config.get('common', 'interval')
snapshot=1 
#TRACER
def tracer(dec_f):
	def wrapper(file):
		dec_f(file)
	return wrapper 
#DICT
class base1(object):                                            		
 def createdict(self, p):
    val = list(p)
    key = p._fields
    result_dict = dict(zip(key, val))
    return result_dict

#TXT FILE
class base2(base1):
 @tracer
 def iffiletxt(self, file="sys_stat.txt"):
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
class base3(base1):
 @tracer
 def iffilej(self,file="sys_stat.json"):
    global snapshot
    logging.debug('DEBUG JSON')
    logging.info('INFO JOSN')
    logging.warning('WARNING JSON')
    print("Writing text snapshot {}".format(snapshot))
    time=datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H:%M:%S')
    statusfile=open(file, "a+")
    statusfile.write("\nSnapshot{0}:{1}\n".format(snapshot,time))
    statusfile.write("\nCPU\n")
    json.dump(psutil.cpu_percent(), statusfile)
    statusfile.write("\nMEMORY\n")
    json.dump(super().createdict(psutil.virtual_memory()), statusfile, indent=4)
    statusfile.write("\nHDD\n")
    json.dump(super().createdict(psutil.disk_io_counters()), statusfile, indent=4)
    statusfile.write("\nNETWORK\n")
    json.dump(psutil.net_io_counters(), statusfile, indent=4)
    statusfile.write("\n")
    statusfile.close()
txt_f=base2()
json_f=base3()
#OUT
def out():
 if output == "txt":
    txt_f.iffiletxt()
 elif output == "json":
    json_f.iffilej()
  

try:
    out()
except Exception as e:
    logger.exception("Failed out(), {}".format(e))
try:
    schedule.every(int(interval)).seconds.do(out)
except Exception as e:
    logging.exception("Schedule failed, {}".format(e))
while True:
  schedule.run_pending()
  time.sleep(10)
