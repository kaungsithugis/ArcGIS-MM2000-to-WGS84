import arcpy

def one_click_project():
    # Get parameters from the tool menu
    in_raster = arcpy.GetParameterAsText(0)      # Raster Layer
    out_raster = arcpy.GetParameterAsText(1)     # Raster Dataset
    
    out_cs = arcpy.GetParameter(2)               

    try:
        arcpy.AddMessage("Extracting spatial reference and setting up the mathematical bridge...")
        
        # Get the input custom spatial reference
        desc = arcpy.Describe(in_raster)
        custom_sr = desc.spatialReference
        
        # Define the base WGS 1984 geographic coordinate system for the math
        wgs84_gcs = arcpy.SpatialReference(4326)


        transform_name = "Auto_MM2000_to_WGS84"
        method_str = "GEOCENTRIC_TRANSLATION 246.632 784.833 276.923"

        # build the transformation bridge in the background
        arcpy.management.CreateCustomGeoTransformation(
            geot_name=transform_name,
            in_coor_system=custom_sr,
            out_coor_system=wgs84_gcs,
            custom_geot=method_str
        )

        arcpy.AddMessage("Projecting raster to WGS 84...")

        # Run the actual Project Raster tool using the automated bridge
        arcpy.management.ProjectRaster(
            in_raster=in_raster,
            out_raster=out_raster,
            out_coor_system=out_cs,
            geographic_transform=transform_name
        )

        arcpy.AddMessage("Success! Your WGS 84 .tif has been created and is ready for Google Maps.")

    except arcpy.ExecuteError:
        arcpy.AddError(arcpy.GetMessages(2))
    except Exception as e:
        arcpy.AddError(str(e))

if __name__ == '__main__':
    one_click_project()