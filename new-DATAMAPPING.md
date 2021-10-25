# Mapping GRIB data variables into SmartMet-Server variables 

GRIB parameter and level identifiers need to be mapped into FMI parameter and level identifiers that the SmartMet-Server system recognizes. This will enable querying for the data from Timeseries, WMS or other plugins with FMI parameter names. There are several default mappings already defined, but adding your own mappings is possible as well. Some explanation for the contents of the mapping files is given as comments at the beginning of the files. Notice that the mapping is a bit different for GRIB1 and GRIB2 parameters. (For more detailed description, please see the [Grid files documentation](https://github.com/fmidev/smartmet-library-grid-files/blob/master/doc/grid-files.pdf).)

1. First check if config/libraries/grid-files/**fmi_parameters.csv** has already a suitable parameter. Important FMI parameter identifier fields here are fmi-name and fmi-id, since there sould be different names and ids for different variables and different units. In case there is no suitable default parameter definition, define a new one in **ext/fmi_parameters.csv**. The first number (fmi-id) should be a number that is not present in fmi_parameters.csv or ext/fmi_parameters.csv. For the rest, follow the example of existing definitions. You should define at least fields 1)-4), rest of the fields can be left undefined.
2. Next, check if config/libraries/grid-files/**fmi_geometries.csv** contains suitable geometry identifiers. If not, define your own geometries **ext/fmi_geometries.csv**, for instance. 
3. FMI level type identifiers can be found in config/libraries/grid-files/**fmi_levels.csv**. If you want to define your own FMI level identifiers, just add them to **ext/fmi-levels.csv**, for instance.
4. Next, check that config/libraries/grid-files/**grib_parameters.csv** contains the GRIB parameter identifiers and definitions that you need. If not, it is possible to add own GRIB parameter identifiers in ext/**grib_parameters.csv**, for example. 
5. GRIB1/GRIB2 fields need to be mapped into GRIB parameters, which is done in config/libraries/grid-files/**grib1_parameters.csv** and .../**grib2_parameters.csv**. Check if these files have already a suitable mappings. If not, you can define your own additional mappings in **ext/grib1_parameters.csv** or **ext/grib2_parameters.csv** files, for instance.  
6. Next, we need to map GRIB identifiers to FMI identifiers. Check if config/libraries/grid-files/**fmi_parameterId_grib.csv** has already suitable mappings. Here, the first field is the fmi-name and the second field is the grib-id. You can find both of these in the previous files. If you want to define your own "GRIB to FMI" mappings, you can add them to **ext/fmi_parameterId_grib.csv**, for example.  
7. Additionally, GRIB1/GRIB2 fields need to be mapped into FMI level identifiers, which is done in config/libraries/grid-files/**fmi_levelId_grib1.csv** and .../**fmi_levelId_grib2.csv**. If you want to add your own definitions, you can add them to **ext/fmi_levelId_grib1.csv** or **ext/fmi_levelId_grib2.csv**, for instance. 

Many of the csv files can be automatically updated from a FMI database. The ext/ versions are used to bypass this database update, so it will not overwrite local configurations. It is therefore recommended to add your own settings mainly into files in the ext/ directory. If you created your own mapping files (in ext/ or other), remember to add their name (and path, if defined in ext/ or other) to the main configuration file config/libraries/grid-files/**grid-files.conf**. 

Next, you might need to fun the following filesys2smartmet command:

`sudo docker exec smartmet-server /bin/fmi/filesys2smartmet /home/smartmet/config/libraries/tools-grid/filesys-to-smartmet.cfg 0` 

(The above should work if adding and mapping new GRIB files to the system. In case you are changing the mappings for GRIB files that already had been mapped before or creating new mappings for GRIB files added earlier to the system, you need to first temporarily move all the GRIB files in question to some other location, run the filesys2smartmet command, move GRIB files back to the original location, and run filesys2smartmet again.)   

Since mapping should be automatic, new mappings should pop up in config/engines/grid-engine/**mapping_fmi_auto.csv**. If not, the mapping can be forced in config/engines/grid-engine/**mapping_fmi.csv**, which contains default mappings. 

In the end it should be possible to query data in timeseries requests or WMS layer definitions with newbase names or strings with FMI-ID:::: names. Those names are in the fmi_parameters.csv


![](https://github.com/fmidev/chile-smartmet/blob/master/parameter-mapping-flow.png)
Note: All the file names mentioned in the flowchart above are ”default names” which can be changed in the ’grid-files.conf’ if necessary. Additionally, all the definitions in question can be distributed to several files. The idea is that a set of ”standard files” are included in the installation and the user can easily add own definitions without them disappearing with the next installation.
