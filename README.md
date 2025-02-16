# SmartMet-server for IBA Arctic wildfire preparedness project

SmartMet Server is a data and product server which provides acces to both observation and forecast data. It is used for data services and product generation. Smartmet Server can read input from various sources and it provides several ouput interfaces and formats. For more detailed description, see the [SmartMet Server wiki pages](https://github.com/fmidev/smartmet-server/wiki).

SmartMet Server purpose is a service to make data available directly to web apps without needing any data downloading and processing steps on a server. You can directly write javascript web apps to use Copernicus data for the Chile Hackathon. To get a feel for the data offered https://smart.nsdc.fmi.fi/grid-gui is a general data browser. For the Impacto Chile Hackathon you can get this data into your own app. This service has datasets from several producers (currently working: CAMS, ECB2SF, ECBSF, ECSF, ERA5). CAMS atmospheric composition model output is available every day for 5 day forcasts with hourly data. ECSF, ECB2SF and ECBSF seasonal forecasts are available once per month for 215 daily forecasts 7 months ahead. ERA5 is every day the reanalysis from 5 days ago. To utilize datasets shown on this service, the SmartMet Server TimeSeries plugin can be used.

For example web app code using a smartmet-server check out the https://github.com/fmidev/harvesterseasons-site repository and check out the service https://harvesterseasons.com.

# Using the Timeseries API for data in table format

The TimeSeries plugin can be used to fetch time series information for observation and forecast data, with specific time or time interval chosen by the user. The datasets can be downloaded with a HTTP request which contains the parameters needed to obtain the information, processing the results and formatting the output. For example, the following request fetches the 'particulate matter d<2.5 um' for the city of Santiago:

<!---*Mäppäyksen jälkeen vaihda param-nimi:*-->

`https://smart.nsdc.fmi.fi/timeseries?producer=CAMS&lonlat=-70.67,-33.45&format=debug&param=name,time,GRIB-210073:CAMS:6002:1:0:1:0&starttime=20210812T000000&precision=full`

The service location that starts the HTTP request query is **smart.nsdc.fmi.fi**, and the parameters following it are given as name-value pairs separated by the ampersand (&) character. (Hint: copy the FMI key from the https://smart.nsdc.fmi.fi/grid-gui service for the parameter definition 'param'.)

An example response for this query is shown below: 

![timeseries output](https://github.com/annikanni/kuvatestaus/blob/main/Screenshot%202021-08-19%20at%2017-33-35%20Debug%20mode%20output.png)

For more information and examples of the usage of the TimeSeries plugin, see SmartMet Server [Timeseries-plugin Wiki pages](https://github.com/fmidev/smartmet-plugin-timeseries/wiki). 

# Using the WMS/Dali plugin for images

Dali is the engine to make images from smartmet-server internal data. It can be used directly or with appropriate layer definitions can provide an OGC compliant WebMapService interface. Open Geospatial Consortiums (OGC) Web Map Service (WMS) offers a convenient way for generating map images from a map server over the Web using the HTTP protocol. Several image products can be generated using the SmartMet Server WMS plugin. 

An example WMS request to the server (CAMS Total aerosol optical depth at 550nm):

`https://smart.nsdc.fmi.fi/wms?&SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.0&LAYERS=gui:isobands:CAMS_AOD550&STYLES=&FORMAT=image/png&TRANSPARENT=true&HEIGHT=800&WIDTH=400&20220302T000000&CRS=EPSG:4326&BBOX=-60,-80,-10,-50`

An example response for this query is shown below: 

![WMS layer](https://smart.nsdc.fmi.fi/wms?&SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.0&LAYERS=gui:isobands:CAMS_AOD550&STYLES=&FORMAT=image/png&TRANSPARENT=true&HEIGHT=800&WIDTH=400&20220302T000000&CRS=EPSG:4326&BBOX=-60,-80,-10,-50)

Available WMS 'LAYERS' can be checked with the GetCapabilities request as follows: 

`https://smart.nsdc.fmi.fi/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities`

An example Dali request to the server (ECBSF dew point temperature in Kelvins): 

`https://smart.nsdc.fmi.fi/dali?customer=gui&product=temperature_1&source=grid&size=1&l1.parameter=TD-K&producer=ECBSF&origintime=20220401T000000&geometryId=6003&levelId=1&level=0&forecastType=1&forecastNumber=0&type=png&time=20220402T000000`

A response for the previous example query is shown below. The dali product urls can be copied from the grid-gui page by changing a parameters Presentation menu to Dali and copying the image urls. The time setting can be used to make an animation that loads consequitive time steps.

![WMS layer](https://smart.nsdc.fmi.fi/dali?customer=gui&product=temperature_1&source=grid&size=1&l1.parameter=TD-K&producer=ECBSF&origintime=20220401T000000&geometryId=6003&levelId=1&level=0&forecastType=1&forecastNumber=0&type=png&time=20220402T000000)

For more information about the WMS plugin, see for example [SmartMet plugin WMS (Dali & WMS) Wiki pages](https://github.com/fmidev/smartmet-plugin-wms/wiki/SmartMet-plugin-WMS-(Dali-&-WMS)) or [the Web Map Server specification](https://www.ogc.org/standards/wms). (The Dali plugin enables more advanced requests than the WMS plugin.) 

<!---
# Using the Download/WFS API

Mainly for showing ERA5 Land grib datasets and seasonal and weather forecast data.
This entails a GRID  smartmet-server and related plugins to run. ... let's see how it works:

First prepare a data directory at the same level as this cloned directory (../data) and `ln -s smartmet-server/config ../config`
Then you can let docker-compose build and run everything else.

# Start all services (even with --detatch the build process will wait until finished)
docker-compose up --detatch

This will quickly add all components, but below are steps for all of the three Docker containers needed.

# Transfer files from C3S CDS with shell scripts
You will need grib_set and cdo, so install something like libeccodes-tools and cdo packages on Ubuntu and equivalents on other OSs.
under bin you have the get-seasonal.sh for now. Similar scripts for ERA5 and ERA5L will be added soon.

This should used to put data in a ~/data/grib directory, where the smartmet-server will look for new grib files read in.

# Docker setup 
## Build and run ssl-proxy

For https addresses of the server, there is an ssl-proxy handling this

`docker-compose up --detatch --build ssl-proxy`

## Build and run postgres-database

Setup database for geonames-engine because of who knows why

`docker-compose up --detatch --build fminames-db`

## Build and run Redis

Setup database for storing grib-file details

`docker-compose up --detatch --build redis_db`

## Build and run smartmet-server

`docker-compose up --build smartmet-server`

## Fire up all three services at once

This will:

* Start the Postgresql-database and create a db-directory to store all the data there.
* Start Redis for storing information about available grib data
* Start SmartMet Server after the Postgersql is ready

`docker-compose up --detatch`

# Data ingestion and configuring on SmartMet-Server

## Read data to Redis to be used by SmartMet-server
Then docker and its four instances (smartmet-server, fminames-db, redis and ssl-proxy), put grib files with data in the ../data directory.
Filenames will have to match the pattern (dataproducer)_(YYYYMMDDTHHMM)_(description as you like).grib
Dataproducer needs to be something defined in the ../config/engines/grid-engine/producers.csv. For mapping data into the server refer to [MAPPING.md](MAPPING.md)

Run a `filesys-to-smartmet`-script in the smartmet-server container... once Redis is ready. The location of filesys-to-smartmet.cfg depends on where
the settings-files are located at. With `docker-compose.yaml` the settings are currently stored in `/home/smartmet/config`.

`docker exec --user smartmet smartmet-server /bin/fmi/filesys2smartmet /home/smartmet/config/libraries/tools-grid/filesys-to-smartmet.cfg 0`

This should tell you how the grib data was ingested. you can check also by going to https://[yourserver]/grid-gui

## HOPS forecasts and analysis into grid smartmet-server

### HOPS initial state and forcing data retrieval

HOPS needs initial state of soil parameters in the domain it is running for and forcing data for the forecasts. In harvester-seasons the initial state is kept
up from C3S ERA5(L) reanalysis data and the forcing is coming from C3S seasonal forecast data. Shell scripts for getting these datasets are:
`get-seasonal.sh`
`get-ERA5-daily.sh`

The scripts run without arguments to fetch the most recent available data set or can be run with year month arguments like '2020 3' for seasonal
and '2020 4 11' for daily ERA5(L) to retrieve older data. Within the shell scripts there are calls to cds-api python scripts and commands to move data to
proper directories.

To take in account of bias adjustments monthly biases are calculated with the following cmds (variables which bias was calculated have added):
* `seq 0 24 | parallel -j 16 --tmpdir tmp/ --compress cdo ymonmean -sub -selvar,2d,2t,e,tp,stl1,sd,rsn,ro, era5l/era5l_2000-2019_stats-monthly-nordic.grib -remapbil,era5l-nordic-grid -daymean -selvar,2d,2t,stl1,sd,rsn,var205 ens/ec-sf-2000_2019-stats-monthly-fcmean-{}.grib era5l-ecsf_2000-2019_monthly-fcmean-{}.grib`
* `seq 0 24 | parallel -j 16 --compress --tmpdir tmp/ cdo --eccodes div -ymonmean -selvar,tp,e era5_2000-2019_stats-monthly-euro.grib -mulc,2592000 -ymonmean -remapbil,era5-eu-grid -selvar,tprate,erate ens/ec-sf-2000_2019-stats-monthly-euro-{}.grib era5_ecsf_2000-2019_e+tp-monthly-eu-{}.grib`
* `cdo ensmean era5l-ecsf_2000-2019_monthly-fcmean-*.grib era5l-ecsf_2000-2019_monthly-bias.grib`
Using parallel makes this faster as the 16 core system can faster calculate results for 25 ensemble members than one cdo thread doing the ensemble first and then carry on.
And a mean of many biases seems to be a better idea than the bias of an ensemble mean.

The seasonal forecast can now be interpolated on the ERA5L grid and the adjustments can be added:
* `cdo ymonadd era5l-ecsf_2000-2019_monthly-fcmean-em.grib -remapbil,era5l-nordic-grid grib/ECSF_20200402T0000_all-24h-nordic.grib`
Again doing this 51 times in parallel is faster, so that's how it is done for real, but the above explain better the operation. In fact adding some timeshifting/interpolation
is needed to complete the job successfully. This was used for real, last step is needed, because cdo fails to add the ensemble attributes:
* `seq 0 50 | parallel -j 16 --compress --tmpdir tmp/ cdo ymonadd -selmonth,2020-04-02,2020-11-02 -inttime,2020-04-02,00:00:00,1days -shifttime,1year era5l-ecsf_2000-2019_monthly-bias-fixed.grib -remapbil,era5l-nordic-grid -selvar,var168,var167,var182,var205,var33,var141,var139,var228 ens/ec-sf_20200402_all-24h-nordic-{}.grib ens/ec-bsf_20200402_all-24h-nordic-{}.grib`
* `cat ens/ec-bsf_20200402_all-24h-nordic-*.grib > grib/ECBSF_20200402_all-24h-nordic.grib`
* `for f in ec-bsf_20200402_all-24h-nordic-*.grib ; do i=$(echo $f | sed s:.*nordic-::|sed s:\.grib::); grib_set -s centre=98,setLocalDefinition=1,localDefinitionNumber=15,totalNumber=51,number=$i $f ${f:0:-5}-fixed.grib; done`

As only soil temperature level 1 is available in seasonal forecasts, the deeper temperatures on level 2, 3 and 4 are prodcued by using the
ERA5L monthly statistics from 2000-2019 to give each gridpoint the relation between stl1 and the deeper temperatures. The forecasted stl1 with bias adjustement is used to produce level 2,3,4 temperatures. This data set will be used to demonstrate the added value from using HOPS.
* `seq 0 50 |parallel -j 16 --compress --tmpdir tmp/ cdo --eccodes add -seldate,2020-04-02,2020-11-02 -inttime,2020-04-02,00:00:00,1days -shifttime,1year -selvar,stl1,stl2,stl3 era5l-stls-diff-climate.grib -add -seldate,2020-04-02,2020-11-02 -inttime,2020-04-02,00:00:00,1days -shifttime,1year -selvar,stl1 era5l-ecsf_2000-2019_bias-monthly.grib -remapbil,era5l-nordic-grid -selvar,stl1 ens/ec-sf_20200402_all-24h-nordic-{}.grib ens/ec-bsf_20200402_stl-24h-nordic-{}.grib`

To be available as addressable variables the grib variables need to be mapped into SmartMet-server FMI-IDs or newbase names.
A general guide explaining this is under [DATAMAPPING](DATAMAPPING.md).

# Using timeseries, WMS or WFS plugins of the SmartMet-server

The aim is to have timeseries and WMS layers for the http://harvesterseasons.com/ service and WFS downloads available for data sets that will be exported to
other service outlets of HOPS output.

Example:

`/timeseries?param=place,utctime,WindSpeedMS:ERA5:26:0:0:0&latlon=60.192059,24.945831&format=debug&source=grid&producer=ERA5&starttime=data&timesteps=5`
`/timeseries?producer=ERA5&param=WindSpeedMS&latlon=60.192059,24.94583&format=debug&source=grid&&starttime=2017-08-01T00:00:00Z`
`/wfs?request=getFeature&storedquery_id=windgustcoverage&starttime=2017-08-01T00:00:00Z&endtime=2017-08-01T00:00:00Z&source=grid&bbox=21,60,24,64&crs=EPSG:4326&limits=15,999,20,999,25,999,30–999`
`/wfs?request=getFeature&storedquery_id=pressurecoverage&starttime=2017-08-01T00:00:00Z&endtime=2017-08-01T00:00:00Z&source=grid&bbox=21,60,24,64&crs=EPSG:4326&limits=0,1000`

A big thanks to this citation for using parallel a lot:
  O. Tange (2011): GNU Parallel - The Command-Line Power Tool,
  ;login: The USENIX Magazine, February 2011:42-47.
-->
