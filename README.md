<h1 align="center">
  <img src="https://github.com/behigu/Satellite_Data_Analysis/blob/main/pictures/user_cartoon.png" width="224px"/><br/>
  Hello world, this is <strong> Behigu </strong>
</h1>


# AgriTech - USGS LIDAR Challenge
This project tries to build a python package for AgriTech. IN AgriTech, the interest is in how water flows through a maize farm field. This knowledge will help us improve our research on new agricultural products being tested on farms.

## Package Functionalities
- **Data Featching and loading** : Fetch spacialy bound LIDAR data from user input and return python dictionary contining all years of geopandas file 

- **Terrain Visualization** : Give option to show data as
  - 3D render plot or
  - Heat map

- **Data Transformation**
  - Topographic wetness index (TWI) - as an additional column returned with geopandas dataframe
  - Standardized grid - A python code that takes elevation points output from the USGS LIDAR tool and interpolates them to a grid.

## Package Installation

   - params : 
        polygon : polygon of area we need to crop
        state : state to do the elevation

   - instruction:
        Make sure to run them sequentially.
        run_pipe() : will generate the neccessary files
        create_geopandasdf() : generate data frame from the files
        get_geopandas_df() : will provide the data frame


![Your Repository's Stats](https://github-readme-stats.vercel.app/api?username=behigu&show_icons=true)
  
