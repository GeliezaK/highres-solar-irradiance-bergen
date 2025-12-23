# High-Resolution Solar Irradiance Model (Applied to Bergen, Norway)

This repository contains the code to reproduce the **high-resolution cloud-informed solar irradiance modeling** for Bergen, Norway. The workflow was developed for the master thesis: "Modeling long-term surface solar irradiance using high-resolution satellite cloud data: a case study in Bergen, Norway" by Gelieza Kötterheinrich.  

The code can be adapted to any study area worldwide.

---

## Folder Structure

### `src/io/`
Download pipelines:  
- `download_frost_data.py`: download meteorological station data.  
- `export_sentinel2_images.ipynb`: export Sentinel-2 images (requires a [Google Earth Engine](https://earthengine.google.com/) account).

### `src/preprocessing/`
Preprocessing steps include:  
- Extract cloud parameters from CLAAS-3 files (`preprocess_netcdf_data.py`)  
- Quality control of station data (`quality_control_flag_stations_data.py`)  
- Merge and process cloud cover tables (`merge_cloud_cover_tables.py`)  
- Preprocess satellite viewing angles (`preprocess_viewing_angles.py`)

### `src/model/`
Model components:  
- Cloud shadow projection (`cloud_shadow.py`)  
- Look-Up Table generation (`generate_LUT.py`)  
- Shortwave correction factor (`shortwave_correction_factor.py`)  
- Upscaling cloud masks (`upscale_cloud_mask.py`)  
- Instantaneous GHI simulation (`instantaneous_GHI_model.py`)  
- Long-term irradiation simulation (`longterm_GHI_simulation.py`)

### `src/plotting/`
Scripts for visualizing results (figures used in the thesis).

### `test/`
Unit tests for the project. To run tests, add the project root to `PYTHONPATH`:

```bash
export PYTHONPATH=$PWD
python -m unittest discover -s test -p "test_*.py"
```

--- 
## Model Pipeline

### 1. Prepare Conda Environment
Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/) first.  

Then, create the environment:

```bash
conda env create -f environment.yml
conda activate gis-env
```


### 2. Download Sentinel-2 Data

* Follow instructions in [`export_sentinel2_images.ipynb`](src/io/export_sentinel2_images.ipynb) to:

  1. Set up a Google Earth Engine project.
  2. Define your study region.
  3. Export cloud mask, cloud cover, and viewing angle images to Google Drive.

* Prerequisite: a Google account.


### 3. Merge Cloud Cover Tables

If cloud cover tables are exported in batches, merge them into one using:

```bash
python src/preprocessing/merge_cloud_cover_tables.py
```
Note that input and output paths are hardcoded inside the script, you need to provide your own paths here. 

### 4. Preprocess Satellite Viewing Angles

Add satellite viewing angles (columns `MEAN_ZENITH`, `MEAN_AZIMUTH`) to cloud cover tables:

```bash
python src/preprocessing/preprocess_viewing_angles.py
```


### 5. Download CLAAS-3 and CLARA Data

* From [CM SAF Web UI](https://wui.cmsaf.eu/safira/action/viewProduktSearch). To order products you must first create a user account.
* Save files locally.


### 6. Merge Cloud Property and Albedo Data

Extract area-wide median cloud properties and surface albedo:

```bash
python src/preprocessing/preprocess_netcdf_data.py
```


### 7. Download Digital Surface Model (DSM)

* Global 30 m Digital Elevation Model: [Copernicus DEM](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_DEM_GLO30)
* Norwegian DSM: [Hoydedata](https://hoydedata.no/LaserInnsyn2/)


### 8. Compute Direct Shortwave Correction Factor

Using [HORAYZON](https://github.com/ChristianSteger/HORAYZON):

```bash
python src/model/shortwave_correction_factor.py
```


### 9. Compute Cloud Shadow Projection

Using Sentinel-2 images:

```bash
python src/model/cloud_shadow.py
```

* Cloud shadow maps are saved as intermediate `.nc` files.


### 10. Generate Look-Up Table (LUT)

Customize hours of day, days of year, and aerosol optical depth:

```bash
python src/model/generate_LUT.py
```

* Aerosol optical depth: [MODIS MCD19A2.061](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MCD19A2_GRANULES#dois)


### 11. Calculate Instantaneous Solar Irradiance

Requires: LUT, shortwave correction factor, cloud shadow maps, cloud property table:

```bash
python src/model/instantaneous_GHI_model.py
```


### 12. Calculate Clear-Sky Index

Convert instantaneous GHI maps to clear-sky index:

```bash
python src/preprocessing/preprocess_netcdf_data.py
```

* Aggregate per month and sky type.


### 13. Simulate Long-Term Irradiation

Use sky-type and clear-sky index sampling:

```bash
python src/model/longterm_GHI_simulation.py
```

* Outputs mean daily irradiation for synthetic time series.

```

