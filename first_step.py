import json, ast
from os import stat
import pdal


def read_json(file_name):
  '''
  Read json file and return the string format
  '''

  try:
    file_path = f"../{file_name}"
    print("File Path : ", file_path)
    with open(file_path, 'r') as json_file:
      data = json.loads(json_file.read())
    return data

  except:
    print('File Not found')
    return None


def prepare_pipe(bound, us_state='IA_FullState'):
    data = read_json('pipeline.json')
    data['pipeline'][0]['bounds'] = bound
    data['pipeline'][0]['filename'] = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"+us_state+"/ept.json"
    
    data['pipeline'][6]['filename'] = '../data/laz/'+us_state+'.laz'
    data['pipeline'][7]['filename'] = '../data/tiff/'+us_state+'.tiff'
    

    print("data LInk : " , data['pipeline'][0]['filename'])
    return data


def run_pipe(bound, us_state):
    print("Run pipe ...")
    result = prepare_pipe(bound, us_state)
    pipeline = pdal.Pipeline(json.dumps(result))
    pipe_result  = pipeline.execute()
    print("Fetching Completed!")

def test_json_reading():
    data = read_json('pipeline.json')
    print(data)
    


def test_prepare_pipe(bound):
    result = prepare_pipe(bound)
    print(result)

## Initial Files
bound = str(([-10425171.940, -10423171.940], [5164494.710, 5166494.710]))
state = 'IA_FullState'


## Test Things are working # test_json_reading() # test_prepare_pipe(bound)
    

run_pipe(bound, state)
