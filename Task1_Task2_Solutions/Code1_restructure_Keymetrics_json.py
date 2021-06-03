import json
import datetime
import time
import sys

class Key_metrics:
    """
    A class used to represent an Key_metrics
    
    """ 
    
    def __init__(self, filePath):
        """
        Parameters
        ----------
        filePath : str
            The path of the input file
        """
        self.filePath = filePath
    
    def default(self,o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
      
    def read_file(self,file_path):
        """
        Read file as json object from given path
        
        Parameters
        ----------
        file_path : str
            The path of the input file
        
        Returns
        -------
        Object
            a json Object
        """
        file = open(file_path)
        return json.load(file)
    
    def write_file(self,file_path, data):
        """
        Write data as json object to given path file
        
        Parameters
        ----------
        file_path : str
            The path of the output file
        data : list
            A list of dictionaries, with metric definitions as the key, and metric counts as value 
        
        """
        with open(file_path, 'w') as f:
            json.dump(data, f, default=self.default, indent = 4)
    
    def get_metrics(self,data):
        """
        Return dictionary of metrics from list of key metrics
        
        Parameters
        ----------
        data : list
            A list of dictionaries,with key metrics defination
            
        Returns
        -------
        Dictionary
            a dictionary of metrics
        
        """
        metrics = dict()
        for key,val in enumerate(data):
            metrics[key] = val['id']
        return metrics
    
    def get_count_data(self, data, metrics):
        """
        Return a list of dictionaries, with metric definitions as the key, and metric counts as value
        
        Parameters
        ----------
        data : list
            A list of dictionaries,with key metrics defination
        metrics: dictionary
            A dictionary of key metrics
            
        Returns
        -------
        list
            A list of dictionaries, with metric definitions as the key, and metric counts as value
        
        """
        count_data = list()
        for i in data:
            count_dic = dict()
            date = str(i['day']) + '-' + str(i['month']) + '-' + str(i['year'])
            date_time_obj = datetime.datetime.strptime(date, '%d-%m-%Y')
            count_dic['date'] = date_time_obj
            for key,val in enumerate(i['counts']):
                count_dic[metrics[key]] = val
            count_data.append(count_dic)
        return count_data
    
    def main(self):
        key_metrics_df = self.read_file(self.filePath)
        metrics = self.get_metrics(key_metrics_df['report']['metrics'])
        count_data = self.get_count_data(key_metrics_df['report']['data'], metrics)
        writeFile = 'output_'+self.filePath
        self.write_file(writeFile,count_data)
    
if __name__ == "__main__":
    start_time = time.time()
    try:
        filePath = sys.argv[1]
    except:
        print("Please parse file name as argument.")
        sys.exit(1)
    try:
        prd = Key_metrics(filePath)
        prd.main()
    except Exception as e:
        print(e)
    print("--- %s seconds ---" % (time.time() - start_time))
        