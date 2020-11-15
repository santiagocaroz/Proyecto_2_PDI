# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 20:43:28 2020

@author: Santiago Caro
"""

#%% Carga imagen 4D
#fileName = "C:/Users/CarlosJoseMunoz/Desktop/semestres/2020-2/PDI/Proyecto_2/luimarcarcar/4D.hdr"
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

#%% Extracción de frames y filtrado

escena = slicer.mrmlScene;
volumen4D = escena.GetNodeByID('vtkMRMLMultiVolumeNode1')
imagenvtk4D = volumen4D.GetImageData()
numero_imagenes = volumen4D.GetNumberOfFrames()


extract1 = vtk.vtkImageExtractComponents()
extract1.SetInputData(imagenvtk4D)

ras2ijk = vtk.vtkMatrix4x4()
ijk2ras = vtk.vtkMatrix4x4()
volumen4D.GetRASToIJKMatrix(ras2ijk)
volumen4D.GetIJKToRASMatrix(ijk2ras)

for i in range(numero_imagenes):
    volumenFijo = slicer.vtkMRMLScalarVolumeNode();    
    imagen_fija = extract1.SetComponents(i)
    extract1.Update()
    volumenFijo.SetAndObserveImageData(extract1.GetOutput())
    extract1.Update()
    volumenFijo.SetName("frame"+str(i))
    volumenFijo.SetRASToIJKMatrix(ras2ijk)
    volumenFijo.SetIJKToRASMatrix(ijk2ras)
    escena.AddNode(volumenFijo)
    
for i in range(numero_imagenes):
    cliModule = slicer.modules.gradientanisotropicdiffusion
    n = cliModule.cliModuleLogic().CreateNode()
    parameters = {}
    parameters['conductance'] = 1.0 
    parameters['numberOfIterations'] = 5
    parameters['timeStep'] = 0.05
    volumen_entrada = slicer.mrmlScene.GetNodeByID("vtkMRMLScalarVolumeNode"+str(i+1))
    #volumen_entrada = volumenFijo
    volumen_salida = slicer.vtkMRMLScalarVolumeNode()
    slicer.mrmlScene.AddNode(volumen_salida)
    parameters['inputVolume'] = volumen_entrada.GetID()
    parameters['outputVolume'] = volumen_salida.GetID()
    cliModule = slicer.modules.gradientanisotropicdiffusion
    cliNode = slicer.cli.run(cliModule,None,parameters,wait_for_completion=True)

#%% Registro

volumenFijo = slicer.vtkMRMLScalarVolumeNode();
#le asigno las transformaciones
volumenFijo.SetRASToIJKMatrix(ras2ijk)
volumenFijo.SetIJKToRASMatrix(ijk2ras)

#le asigno el volumen 3D fijo
imagen_fija = extract1.SetComponents(0)
extract1.Update()

volumenFijo.SetName('fijo')
volumenFijo.SetAndObserveImageData(extract1.GetOutput())
extract1.Update()

#anado el nuevo volumen a la escena\
escena.AddNode(volumenFijo)

for i in range(numero_imagenes-1):
    imagen_movil = slicer.mrmlScene.GetNodeByID("vtkMRMLScalarVolumeNode"+str(i+62))#Seleccionamos un volumen lejano
    
    volumenMovil = slicer.vtkMRMLScalarVolumeNode();
    volumenMovil.SetRASToIJKMatrix(ras2ijk)
    volumenMovil.SetIJKToRASMatrix(ijk2ras)
    volumenMovil.SetAndObserveImageData(imagen_movil.GetImageData())
    volumenMovil.SetName('movil'+str(i+1))
    escena.AddNode(volumenMovil)
    transformadaSalida = slicer.vtkMRMLLinearTransformNode()
    transformadaSalida.SetName('Transformada de registro')
    slicer.mrmlScene.AddNode(transformadaSalida)   
    parameters = {}
    parameters['fixedVolume'] = volumenFijo.GetID()
    parameters['movingVolume'] = volumenMovil.GetID()
    parameters['transformType'] = 'Rigid'
    parameters['outputTransform'] = transformadaSalida.GetID()    
    cliNode = slicer.cli.run(slicer.modules.brainsfit,None,parameters, wait_for_completion=True)

#%%
#parametros para la operacion de segmentado para un solo volumen 
parameters = {}
parameters['smoothingIterations'] = 5.0 
parameters['timestep'] = 0.0625

parameters['iterations'] = 5
parameters['multiplier'] = 2.5
parameters['neighborhood'] = 1
parameters['labelvalue'] = 2

fiducials = slicer.mrmlScene.GetNodeByID('vtkMRMLMarkupsFiducialNode2')#Se especifíca el fiducial que se va a usar
parameters['seed'] = fiducials.GetID()

volumen_entrada = slicer.mrmlScene.GetNodeByID('vtkMRMLScalarVolumeNode182')#se especficia el volumen que se va a usar 
parameters['inputVolume'] = volumen_entrada.GetID()

volumen_salida = slicer.vtkMRMLLabelMapVolumeNode()
slicer.mrmlScene.AddNode(volumen_salida)
parameters['outputVolume'] = volumen_salida.GetID()

cliModule = slicer.modules.simpleregiongrowingsegmentation
cliNode = slicer.cli.run(cliModule,None,parameters,wait_for_completion=True)
