# extract_ntf_metadata.py
from osgeo import gdal

def extract_nitf_metadata(nitf_path):
        try:
            dataset = gdal.Open(nitf_path)
            if not dataset:
                return None
            
            # Extracting the full metadata
            metadata = dataset.GetMetadata()
            
            # Specifying the properties to extract and their renamed key
            desired_props = {
                'NITF_FDT': 'File DateTime',
                'NITF_IDATIM': 'Image DateTime',
                'NITF_STDIDC_ACQUISITION_DATE': 'Acquisition Date',
                'NITF_ICORDS': 'Coord Representation',
                'NITF_IGEOLO': 'Geo Location',
                'NITF_STDIDC_LOCATION': 'Std ID Location',
                'NITF_IID1': 'Image ID',
                'NITF_ISORCE': 'Image Source',
                'NITF_PIAIMC_MEANGSD': 'Mean GSD',
                'NITF_PIAIMC_SENSMODE': 'Sensor Mode',
                'NITF_PIAIMC_SENSNAME': 'Sensor Name',
                'NITF_USE00A_ANGLE_TO_NORTH': 'Angle to North',
                'NITF_USE00A_MEAN_GSD': 'Mean Ground Sample Distance',
                'NITF_USE00A_SUN_AZ': 'Sun Azimuth',
                'NITF_USE00A_SUN_EL': 'Sun Elevation'
            }
            
            # Applying the mapping
            extracted_metadata = {}
            for prop, renamed in desired_props.items():
                if prop in metadata:
                    extracted_metadata[renamed] = metadata[prop]
            
            return extracted_metadata
        
        except Exception as e:
          print("Type of exception:", type(e))
          print("Exception arguments:", e.args)
          print(f"Problematic NITF path: {nitf_path}")
          raise ValueError(f"Error extracting metadata from NITF: {e.args}")

