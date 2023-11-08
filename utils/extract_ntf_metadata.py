from osgeo import gdal

def dms_to_dd(dms_str, direction):
    """Convert DMS string to DD format."""
    degrees, minutes, seconds = int(dms_str[:2]), int(dms_str[2:4]), float(dms_str[4:6])
    dd = degrees + (minutes / 60) + (seconds / 3600)
    if direction in ['S', 'W']:
        dd = -dd
    return dd

def parse_igeolo(igeolo):
    """Parse IGEOL to extract corner coordinates in DD."""
    corners = [igeolo[i:i+15] for i in range(0, len(igeolo), 15)]
    corners_dd = []
    for corner in corners:
        lat_dd = dms_to_dd(corner[0:7], corner[7])  # Extract and convert latitude
        lon_dd = dms_to_dd(corner[8:14], corner[14]) # Extract and convert longitude
        corners_dd.append((lat_dd, lon_dd))
    return corners_dd


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
            # Add any other desired properties here
        }
        
        # Applying the mapping
        extracted_metadata = {}
        for prop, renamed in desired_props.items():
            if prop in metadata:
                value = metadata[prop]
                
                # Convert NITF_IGEOLO to DD format for corners
                if prop == 'NITF_IGEOLO':
                    corners_dd = parse_igeolo(value)
                    value = corners_dd
                
                extracted_metadata[renamed] = value
        
        return extracted_metadata
    
    except Exception as e:
        # Handle exceptions as needed
        raise e

