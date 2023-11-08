def pixel_to_geo(centroid_pixel, corner_coords, image_shape):
    rows, cols = image_shape
    ul_lat, ul_lon = corner_coords[0]  # Upper Left Corner
    lr_lat, lr_lon = corner_coords[2]  # Lower Right Corner
    
    lon_per_pixel = (lr_lon - ul_lon) / cols
    lat_per_pixel = (ul_lat - lr_lat) / rows  # Latitude decreases from top to bottom
    
    centroid_geo_lon = ul_lon + centroid_pixel[0] * lon_per_pixel
    centroid_geo_lat = ul_lat - centroid_pixel[1] * lat_per_pixel  # Subtract since latitude decreases
    
    return "{:.10f}".format(centroid_geo_lat), "{:.10f}".format(centroid_geo_lon)


