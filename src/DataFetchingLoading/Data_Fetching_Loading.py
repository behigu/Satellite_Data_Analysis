import pdal
import json
import laspy
import geopandas as gpd
import numpy as np
from shapely.geometry import box, Point, Polygon


class FetchAndLoad():

    def __init__(self, polygon: Polygon, epsg: int = 4326, state='IA_FullState'):
        self.polygon = polygon

        self.state = state
        self.epsg = epsg
        self.bounds = None
        self.crs_polygon = None

        self.pipe_path = './pipeline.json'
        self.las_path = self.state+'.las'
        self.tif_path = self.state+'.tif'
        self.api_path = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/" + \
            self.state+"/ept.json"

        self.pipeline = None

        self.las_file = None
        self.points = None
        self.elevation = None
        self.geo_df = None

    def read_json(self):
        '''
        Read json file and return the string format
        '''

        try:
            file_path = self.pipe_path
            print("File Path : ", file_path)
            with open(file_path, 'r') as json_file:
                data = json.loads(json_file.read())
            return data

        except:
            print('File Not found')
            return None

    def get_bounds_and_ploygon(self):
        '''
        set boundaries and polygons after converting user CRS - coordinate system
        to the coordinate system we use ( 3857 ).
        '''
        polygon_df = gpd.GeoDataFrame([self.polygon], columns=['geometry'])

        polygon_df.set_crs(epsg=self.epsg, inplace=True)
        polygon_df['geometry'] = polygon_df['geometry'].to_crs(
            epsg=3857)
        minx, miny, maxx, maxy = polygon_df['geometry'][0].bounds

        polygon_input = 'POLYGON(('

        xcord, ycord = polygon_df['geometry'][0].exterior.coords.xy
        for x, y in zip(list(xcord), list(ycord)):
            polygon_input += f'{x} {y}, '
        polygon_input = polygon_input[:-2]
        polygon_input += '))'

        self.bounds = f"({[minx, maxx]},{[miny,maxy]})"
        self.crs_polygon = polygon_input

    def prepare_pipe(self):
        '''
        Populate The pipe line with boundary, and return pipeline
        '''
        self.get_bounds_and_ploygon()
        data = self.read_json()
        data['pipeline'][0]['bounds'] = self.bounds
        data['pipeline'][0]['filename'] = self.api_path

        data['pipeline'][1]['polygon'] = self.crs_polygon

        data['pipeline'][4]['out_srs'] = f'EPSG:{self.epsg}'

        data['pipeline'][7]['filename'] = self.las_path
        data['pipeline'][8]['filename'] = self.tif_path

        print("data LInk : ", data['pipeline'][0]['filename'])
        self.pipeline = data

    def run_pipe(self):
        '''
        Generate .las and .tif file from the pipeline
        '''
        print("Run pipe ...")
        result = self.prepare_pipe()
        pdal_pipe = pdal.Pipeline(json.dumps(self.pipeline))
        pdal_result = pdal_pipe.execute()
        print("Fetching Completed!")

    def read_laz(self):
        '''
        Read Generated Las file
        Return laspy read las file
        '''
        try:
            print("Reading Las File from :", self.las_path)
            las = laspy.read(self.las_path)
            self.las_file = las
            return las

        except FileNotFoundError:
            print("Log: File Not found")
            print("Please use the function run_pipe before this funciton")

    def generate_points_elevation(self):
        '''
        Return Points (x, y) and elevation (z)
        '''
        print("Generating Points from las File ...")
        points = [Point(x, y)
                  for x, y in zip(self.las_file.x, self.las_file.y)]
        elevation = np.array(self.las_file.z)

        self.points, self.elevation = points, elevation
        print("Finished Generating Points!")

        return points, elevation

    def create_geopandasdf(self):
        '''
        Return Geopandas data frame from elevation and geometic points
        '''
        self.read_laz()
        self.generate_points_elevation()

        print("Making Geopandas Data Frame...")
        geopanda_df = gpd.GeoDataFrame(
            {"elevation": self.elevation, "geometry": self.points})
        geopanda_df.set_geometry('geometry')
        geopanda_df.set_crs(epsg=4326, inplace=True)

        self.geo_df = geopanda_df
        print("Finished Making Geopandas Data Frame!")
        return geopanda_df

    def get_geopandas_df(self):
        return self.geo_df
