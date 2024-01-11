import json
from datetime import datetime

#Defining the class Logger to create a running log of every func run from "Repository" class
class Logger(object):
    _instance = None
    _log_file = 'log.json'
    _log_entry_counter = 1
    
    def __new__(cls):
        """
        11.01.24
        Mir Shukhman
        Func to define class Logger as "singelton" to avoide duplications of "log"
        And initial creation of log.json as part of cretion of the class instance
        Returns class instance
        """
        if cls._instance is None:
            cls._instance= super(Logger,cls).__new__(cls)
            
            # Creating the log file as part of the instance creation
            with open(cls._log_file, 'w') as file:
                file.write('[]')
            
        return cls._instance
    
    def __init__(self) -> None:
        pass
    
    @property
    def log(self):
        """
        11.01.24
        Mir Shukhman
        Func getter returns the log file
        """
        return self._log_file
    
    @log.setter
    def log(self, func_name, func_input, func_output):
        """
        11.01.24
        Mir Shukhman
        Func setter to add log entry
        Input func name, func's input, func's output. Datetime + id set automaticly
        """
        log_entry = {
            'id': self._log_entry_counter,
            'datetime': str(datetime.now()),
            'func_name': func_name,
            'func_input': func_input,
            'func_output': func_output
        }
        
        try:
            with open(self.log, 'a') as file:
                file.write(',\n')
                json.dump(log_entry, file, indent=2)
                self._log_entry_counter += 1
        
        except Exception as e:
            raise e
        

    def read_log(self):
        """
        11.01.24
        Mir Shukhman
        Func to read the log file
        Returns the file in read mode
        """
        try:
            with open(self.log, 'r') as file:
                return json.load(file)
            
        except FileNotFoundError:
            return None 

