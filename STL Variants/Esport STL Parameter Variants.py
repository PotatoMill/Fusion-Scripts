#Author-Christian
#Description-Building on the Export STL variants. Can export lots of STF files with different parameters

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        
        # Get the root component of the active design
        rootComp = design.rootComponent

        # Specify the folder to write out the results.
        folder = 'C:/Users/chris/Downloads/STLExport/'

        # Get the parameters named "Length" and "Width" to change.
        AxleDiameterParam = design.allParameters.itemByName('AxleDiameter')
        ToothHeightParam = design.allParameters.itemByName('ToothHeight')
        ToothWidthParam = design.allParameters.itemByName('ToothWidth')

        for i in range(0,3): #1,2,3 ikke 4
            for j in range(0,3):
                for k in range(0,3):
                    AxleDiameter = 4.7 + i * 0.1
                    ToothHeight = 0.1 + j * 0.1
                    ToothWidth = 0.4 + k * 0.1

                    AxleDiameterParam.expression = str(AxleDiameter)
                    ToothHeightParam.expression = str(ToothHeight)
                    ToothWidthParam.expression = str(ToothWidth)
                    
                    # Let the view have a chance to paint just so you can watch the progress.
                    #adsk.doEvents()
                    design.computeAll()
                    
                    # Construct the output filename.
                    filename = folder + str(AxleDiameter) + 'x' + str(ToothHeight) + 'x' + str(ToothWidth) + '.stl'
                    
                    # Save the file as STL.
                    exportMgr = adsk.fusion.ExportManager.cast(design.exportManager)
                    stlOptions = exportMgr.createSTLExportOptions(rootComp)
                    stlOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
                    stlOptions.filename = filename
                    exportMgr.execute(stlOptions)
                
        ui.messageBox('Finished.')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))