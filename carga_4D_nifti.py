# def read4DNIfTI(self, mvNode, fileName):
#     """Try to read a 4D nifti file as a multivolume"""
#     print('trying to read %s' % fileName)

#     # use the vtk reader which seems to handle most nifti variants well
#     reader = vtk.vtkNIFTIImageReader()
#     reader.SetFileName(fileName)
#     reader.SetTimeAsVector(True)
#     reader.Update()
#     header = reader.GetNIFTIHeader()
#     qFormMatrix = reader.GetQFormMatrix()
#     if not qFormMatrix:
#       print('Warning: %s does not have a QFormMatrix - using Identity')
#       qFormMatrix = vtk.vtkMatrix4x4()
#     spacing = reader.GetOutputDataObject(0).GetSpacing()
#     timeSpacing = reader.GetTimeSpacing()
#     nFrames = reader.GetTimeDimension()
#     if header.GetIntentCode() != header.IntentTimeSeries:
#       intentName = header.GetIntentName()
#       if not intentName:
#         intentName = 'Nothing'
#       print('Warning: %s does not have TimeSeries intent, instead it has \"%s\"' % (fileName,intentName))
#       print('Trying to read as TimeSeries anyway')
#     units = header.GetXYZTUnits()

#     # try to account for some of the unit options
#     # (Note: no test data available but we hope these are right)
#     if units & header.UnitsMSec == header.UnitsMSec:
#       timeSpacing /= 1000.
#     if units & header.UnitsUSec == header.UnitsUSec:
#       timeSpacing /= 1000. / 1000.
#     spaceScaling = 1.
#     if units & header.UnitsMeter == header.UnitsMeter:
#       spaceScaling *= 1000.
#     if units & header.UnitsMicron == header.UnitsMicron:
#       spaceScaling /= 1000.
#     spacing = [e * spaceScaling for e in spacing]

#     # create frame labels using the timing info from the file
#     # but use the advanced info so user can specify offset and scale
#     volumeLabels = vtk.vtkDoubleArray()
#     volumeLabels.SetNumberOfTuples(nFrames)
#     frameLabelsAttr = ''
#     for i in range(nFrames):
#       frameId = self.__veInitial.value + timeSpacing * self.__veStep.value * i
#       volumeLabels.SetComponent(i, 0, frameId)
#       frameLabelsAttr += str(frameId)+','
#     frameLabelsAttr = frameLabelsAttr[:-1]

#     # create the display node
#     mvDisplayNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMultiVolumeDisplayNode')
#     mvDisplayNode.SetScene(slicer.mrmlScene)
#     slicer.mrmlScene.AddNode(mvDisplayNode)
#     mvDisplayNode.SetReferenceCount(mvDisplayNode.GetReferenceCount()-1)
#     mvDisplayNode.SetDefaultColorMap()

#     # spacing and origin are in the ijkToRAS, so clear them from image data
#     imageChangeInformation = vtk.vtkImageChangeInformation()
#     imageChangeInformation.SetInputConnection(reader.GetOutputPort())
#     imageChangeInformation.SetOutputSpacing( 1, 1, 1 )
#     imageChangeInformation.SetOutputOrigin( 0, 0, 0 )
#     imageChangeInformation.Update()

#     # QForm includes directions and origin, but not spacing so add that
#     # here by multiplying by a diagonal matrix with the spacing
#     scaleMatrix = vtk.vtkMatrix4x4()
#     for diag in range(3):
#       scaleMatrix.SetElement(diag, diag, spacing[diag])
#     ijkToRAS = vtk.vtkMatrix4x4()
#     ijkToRAS.DeepCopy(qFormMatrix)
#     vtk.vtkMatrix4x4.Multiply4x4(ijkToRAS, scaleMatrix, ijkToRAS)
#     mvNode.SetIJKToRASMatrix(ijkToRAS)
#     mvNode.SetAndObserveDisplayNodeID(mvDisplayNode.GetID())
#     mvNode.SetAndObserveImageData(imageChangeInformation.GetOutputDataObject(0))
#     mvNode.SetNumberOfFrames(nFrames)

#     # set the labels and other attributes, then display the volume
#     mvNode.SetLabelArray(volumeLabels)
#     mvNode.SetLabelName(self.__veLabel.text)

#     mvNode.SetAttribute('MultiVolume.FrameLabels',frameLabelsAttr)
#     mvNode.SetAttribute('MultiVolume.NumberOfFrames',str(nFrames))
#     mvNode.SetAttribute('MultiVolume.FrameIdentifyingDICOMTagName','')
#     mvNode.SetAttribute('MultiVolume.FrameIdentifyingDICOMTagUnits','')

#     mvNode.SetName(str(nFrames)+' frames NIfTI MultiVolume')
#     slicer.mrmlScene.AddNode(mvNode)
#     # Helper.SetBgFgVolumes(mvNode.GetID(),None)
    
#%%
fileName = "C:/Users/Santiago Caro/Documents/Santiago Consultas/Bioingenieria/Procesamiento Digital de Imagenes/Slicer/luimarcarcar/4D.hdr"

"""Try to read a 4D nifti file as a multivolume"""
print('trying to read %s' % fileName)

# use the vtk reader which seems to handle most nifti variants well
reader = vtk.vtkNIFTIImageReader()
reader.SetFileName(fileName)
reader.SetTimeAsVector(True)
reader.Update()
header = reader.GetNIFTIHeader()
qFormMatrix = reader.GetQFormMatrix()
if not qFormMatrix:
  print('Warning: %s does not have a QFormMatrix - using Identity')
  qFormMatrix = vtk.vtkMatrix4x4()

spacing = reader.GetOutputDataObject(0).GetSpacing()
timeSpacing = reader.GetTimeSpacing()
nFrames = reader.GetTimeDimension()
print(nFrames)
if header.GetIntentCode() != header.IntentTimeSeries:
  intentName = header.GetIntentName()
  if not intentName:
    intentName = 'Nothing'
  print('Warning: %s does not have TimeSeries intent, instead it has \"%s\"' % (fileName,intentName))
  print('Trying to read as TimeSeries anyway')

units = header.GetXYZTUnits()

# try to account for some of the unit options
# (Note: no test data available but we hope these are right)
if units & header.UnitsMSec == header.UnitsMSec:
  timeSpacing /= 1000.

if units & header.UnitsUSec == header.UnitsUSec:
  timeSpacing /= 1000. / 1000.

spaceScaling = 1.
if units & header.UnitsMeter == header.UnitsMeter:
  spaceScaling *= 1000.

if units & header.UnitsMicron == header.UnitsMicron:
  spaceScaling /= 1000.

spacing = [e * spaceScaling for e in spacing]

# create frame labels using the timing info from the file
# but use the advanced info so user can specify offset and scale
volumeLabels = vtk.vtkDoubleArray()
volumeLabels.SetNumberOfTuples(nFrames)
frameLabelsAttr = ''
for i in range(nFrames):
  frameId = 0 + timeSpacing * 0.1 * i
  volumeLabels.SetComponent(i, 0, frameId)
  frameLabelsAttr += str(frameId)+','

frameLabelsAttr = frameLabelsAttr[:-1]

# create the display node
mvDisplayNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMultiVolumeDisplayNode')
mvDisplayNode.SetScene(slicer.mrmlScene)
slicer.mrmlScene.AddNode(mvDisplayNode)
mvDisplayNode.SetReferenceCount(mvDisplayNode.GetReferenceCount()-1)
mvDisplayNode.SetDefaultColorMap()

# spacing and origin are in the ijkToRAS, so clear them from image data
imageChangeInformation = vtk.vtkImageChangeInformation()
imageChangeInformation.SetInputConnection(reader.GetOutputPort())
imageChangeInformation.SetOutputSpacing( 1, 1, 1 )
imageChangeInformation.SetOutputOrigin( 0, 0, 0 )
imageChangeInformation.Update()

# QForm includes directions and origin, but not spacing so add that
# here by multiplying by a diagonal matrix with the spacing
scaleMatrix = vtk.vtkMatrix4x4()
for diag in range(3):
  scaleMatrix.SetElement(diag, diag, spacing[diag])

ijkToRAS = vtk.vtkMatrix4x4()
ijkToRAS.DeepCopy(qFormMatrix)
vtk.vtkMatrix4x4.Multiply4x4(ijkToRAS, scaleMatrix, ijkToRAS)

mvNode = slicer.vtkMRMLMultiVolumeNode()

mvNode.SetIJKToRASMatrix(ijkToRAS)
mvNode.SetAndObserveDisplayNodeID(mvDisplayNode.GetID())
mvNode.SetAndObserveImageData(imageChangeInformation.GetOutputDataObject(0))
mvNode.SetNumberOfFrames(nFrames)

# set the labels and other attributes, then display the volume
mvNode.SetLabelArray(volumeLabels)
mvNode.SetLabelName("MultiVolumen")

mvNode.SetAttribute('MultiVolume.FrameLabels',frameLabelsAttr)
mvNode.SetAttribute('MultiVolume.NumberOfFrames',str(nFrames))
mvNode.SetAttribute('MultiVolume.FrameIdentifyingDICOMTagName','')
mvNode.SetAttribute('MultiVolume.FrameIdentifyingDICOMTagUnits','')

mvNode.SetName(str(nFrames)+' frames NIfTI MultiVolume')

#the node is inserted in the scene
slicer.mrmlScene.AddNode(mvNode)

#%%

cliModule = slicer.modules.gradientanisotropicdiffusion
n = cliModule.cliModuleLogic().CreateNode()
for groupIndex in range(n.GetNumberOfParameterGroups()):
    for parameterIndex in range(n.GetNumberOfParametersInGroup(groupIndex)):  
        print('Parameter ({0}/{1}): {2} ({3})'.format(groupIndex, parameterIndex, n.GetParameterName(groupIndex, parameterIndex), n.GetParameterLabel(groupIndex, parameterIndex)))

#parametros para la operacion de registro
parameters = {}
parameters['conductance'] = 1.0 
parameters['numberOfIterations'] = 10
parameters['timeStep'] = 0.05
#volumen_entrada = slicer.mrmlScene.GetNodeByID('vtkMRMLScalarVolumeNode1')
volumen_entrada = slicer.mrmlScene.GetNodeByID('vtkMRMLMultiVolumeNode1')
volumen_salida = slicer.vtkMRMLMultiVolumeNode()
slicer.mrmlScene.AddNode(volumen_salida)
parameters['inputVolume'] = volumen_entrada.GetID()
parameters['outputVolume'] = volumen_salida.GetID()
cliModule = slicer.modules.gradientanisotropicdiffusion
cliNode = slicer.cli.run(cliModule,None,parameters,wait_for_completion=True)
#%%
