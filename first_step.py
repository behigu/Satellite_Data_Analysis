import json, ast
from os import stat
import pdal

def read_json(file_name):
  '''
  Read json file and return the string format
  '''

  try:
    with open(file_name, 'r') as json_file:
      data = json.loads(json_file.read())
    return data

  except:
    return None

def prepare_pipe(bound, us_state='IA_FullState'):
  data = read_json('./iowa.json')
  data['pipeline'][0]['bounds'] = bound
  data['pipeline'][0]['filename'] = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"+us_state+"/ept.json"
  print("data")
  return data

def run_pipe(bound, us_state):
  print("Run pipe")
  result = prepare_pipe(bound, us_state)
  pipeline = pdal.Pipeline(json.dumps(result))
  pipe_result  = pipeline.execute()
  print(pipe_result)

bound = str(([-10425171.940, -10423171.940], [5164494.710, 5166494.710]))
state = 'IA_FullState'
# data = read_json('./iowa.json')
# bounds = data['pipeline'][0]['bounds']
# result = prepare_pipe(bound)
# print(result)


run_pipe(bound, state)
