import sys
import json
import time
class product:
    """
    A class used to represent an Product
    
    """ 
    def __init__(self,file_path):
        """
        Parameters
        ----------
        filePath : str
            The path of the input file
        """
        self.filePath = file_path
        self.product_cnt = []
    
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
            json.dump(data, f,indent = 4)
            
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

    def get_dimentions(self,data):
        """
        Return dictionary of dimentions from list of elements
        
        Parameters
        ----------
        data : list
            A list of dictionaries,with elements defination
            
        Returns
        -------
        Dictionary
            A dictionary of dimentions
        
        """
        metrics = dict()
        for key,val in enumerate(data):
            metrics[key] = val['id']
        return metrics
    
    def flatten_json(self,report_data,dimensions,metrics):
        """
        Return a list of dictionaries, with dimentions values and  metric definitions as the key, and metric counts as value
        
        Parameters
        ----------
        data : list
            A list of dictionaries,with key metrics defination
        dimensions: dictionary
            A dictionary of dimentions
        metrics: dictionary
            A dictionary of key metrics
            
        Returns
        -------
        list
            A list of dictionaries, with dimentions values and metric definitions as the key, and metric counts as value
        
        """
        def flatten(breakdown,dim=0,res={}):
            if dim==len(dimensions)-1:    
                for i in breakdown:
                    res[dimensions[dim]] = i['name']
                    for key,val in enumerate(i['counts']):
                        res[metrics[key]] = val
                    self.product_cnt.append(res.copy())
            else:
                for i in breakdown:
                    res[dimensions[dim]] = i['name']
                    flatten(i['breakdown'],dim+1,res)
        flatten(report_data)
        
    def main(self):
        product_df = self.read_file(self.filePath)
        dimensions = self.get_dimentions(product_df['report']['elements'])
        metrics = self.get_metrics(product_df['report']['metrics'])
        self.flatten_json(product_df['report']['data'],dimensions,metrics)
        write_path = 'output_' + self.filePath 
        self.write_file(write_path,self.product_cnt)

if __name__ == "__main__":
    start_time = time.time()
    try:
        filePath = sys.argv[1]
    except:
        print("Please parse file name as argument.")
        sys.exit(1)
    try:
        prd = product(filePath)
        prd.main()
    except Exception as e:
        print(e)
    print("--- %s seconds ---" % (time.time() - start_time))
    
        
        


