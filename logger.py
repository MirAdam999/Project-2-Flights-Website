import json
import os
from datetime import datetime

# 10.01.24
# Mir Shukhman
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
            
            # Creating the log file as part of the instance creation, if not alredy exists
            if not os.path.exists(cls._log_file):
                with open(cls._log_file, 'w') as file:
                    file.write('[]')
            
        return cls._instance
    
    def __init__(self) -> None:
        pass
    
    
    @property
    def log_path(self):
        """
        11.01.24
        Mir Shukhman
        Func getter returns path to the log file
        """
        return self._log_file
    
    
    def log(self, class_name, func_name, func_input, func_output):
        """
        11.01.24
        Mir Shukhman
        Func setter to add log entry
        Input func name, func's input, func's output. Datetime + id set automaticly
        """
        log_entry = {
            'id': self._log_entry_counter,
            'datetime': str(datetime.now()),
            'class-name': str(class_name),
            'func_name': str(func_name),
            'func_input': str(func_input),
            'func_output': str(func_output)
        }
        
        try:
            with open(self._log_file, 'a') as file:
                file.write(',\n')
                json.dump(log_entry, file, indent=2)
                self._log_entry_counter += 1
        
        except Exception as e:
            return str(e)
        

    def read_log(self):
        """
        11.01.24
        Mir Shukhman
        Func to read the log file
        Returns the file in read mode
        """
        try:
            with open(self._log_file, 'r') as file:
                return json.load(file)
            
        except FileNotFoundError:
            return None 

