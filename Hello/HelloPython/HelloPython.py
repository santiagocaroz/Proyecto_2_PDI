import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# HelloPython
#

class HelloPython(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "HelloPython" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["John Doe (AnyWare Corp.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
It performs a simple thresholding on the input volume and optionally captures a screenshot.
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# HelloPythonWidget
#

class HelloPythonWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
#%%
    # Instantiate and connect widgets ...
    #obtener volumentes. ----------------------------------------------
    
    
    parametersCollapsibleButtonZero = ctk.ctkCollapsibleButton()
    parametersCollapsibleButtonZero.text = "Obtener volumenes del 4D"
    self.layout.addWidget(parametersCollapsibleButtonZero)
    
    
    parametersFormLayoutZero = qt.QFormLayout(parametersCollapsibleButtonZero)
    
    #carga 4D
    self.chargeButton = qt.QPushButton("Cargar")
    self.chargeButton.toolTip = "Run the algorithm."
    self.chargeButton.enabled = True
    parametersFormLayoutZero.addRow(self.chargeButton)
    
    
    #input volume selector Zero
    self.inputSelectorZero = slicer.qMRMLNodeComboBox()
    self.inputSelectorZero.nodeTypes = ["vtkMRMLMultiVolumeNode"]
    self.inputSelectorZero.selectNodeUponCreation = True
    self.inputSelectorZero.addEnabled = False
    self.inputSelectorZero.removeEnabled = False
    self.inputSelectorZero.noneEnabled = False
    self.inputSelectorZero.showHidden = False
    self.inputSelectorZero.showChildNodeTypes = False
    self.inputSelectorZero.setMRMLScene( slicer.mrmlScene )
    self.inputSelectorZero.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayoutZero.addRow("Input Volume: ", self.inputSelectorZero)
    
    #Get volumes
    self.applyButtonZero = qt.QPushButton("Apply")
    self.applyButtonZero.toolTip = "Run the algorithm."
    self.applyButtonZero.enabled = False
    parametersFormLayoutZero.addRow(self.applyButtonZero)
    
    #obtener volumentes. ----------------------------------------------
#%%    
    
    #
    # Parameters Area
    #
    #filtrado -----------------------------------------------------------
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Filtrado"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # input volume selector
    #
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    #self.inputSelector.nodeTypes = ["vtkMRMLMultiVolumeNode"]
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

    #
    # output volume selector
    #
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.outputSelector.selectNodeUponCreation = True
    self.outputSelector.addEnabled = True
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = True
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

    #
    # Conductance value
    #
    self.conductanceWidget = ctk.ctkSliderWidget()
    self.conductanceWidget.singleStep = 0.01
    self.conductanceWidget.minimum = 0.00
    self.conductanceWidget.maximum = 10.00
    self.conductanceWidget.value = 0.5
    self.conductanceWidget.setToolTip("Set threshold value for computing the output image. Voxels that have intensities lower than this value will set to zero.")
    parametersFormLayout.addRow("Conductance", self.conductanceWidget)
    
    #
    # Iterations value
    #
    self.iterationsWidget = ctk.ctkSliderWidget()
    self.iterationsWidget.singleStep = 1
    self.iterationsWidget.minimum = 1
    self.iterationsWidget.maximum = 30
    self.iterationsWidget.value = 5
    self.iterationsWidget.setToolTip("Set threshold value for computing the output image. Voxels that have intensities lower than this value will set to zero.")
    parametersFormLayout.addRow("Iterations", self.iterationsWidget)

    #
    #
    # Time Step value
    #
    self.timeStepWidget = ctk.ctkSliderWidget()
    self.timeStepWidget.singleStep = 0.001
    self.timeStepWidget.minimum = 0.00
    self.timeStepWidget.maximum = 0.20
    self.timeStepWidget.value = 0.01
    self.timeStepWidget.setToolTip("Set threshold value for computing the output image. Voxels that have intensities lower than this value will set to zero.")
    parametersFormLayout.addRow("Time Step", self.timeStepWidget)

    #
    # check box to trigger taking screen shots for later use in tutorials
    #
    # self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
    # self.enableScreenshotsFlagCheckBox.checked = 0
    # self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
    # parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)
    
    self.inputSelectorUno = slicer.qMRMLNodeComboBox()
    self.inputSelectorUno.nodeTypes = ["vtkMRMLMultiVolumeNode"]
    self.inputSelectorUno.selectNodeUponCreation = True
    self.inputSelectorUno.addEnabled = False
    self.inputSelectorUno.removeEnabled = False
    self.inputSelectorUno.noneEnabled = False
    self.inputSelectorUno.showHidden = False
    self.inputSelectorUno.showChildNodeTypes = False
    self.inputSelectorUno.setMRMLScene( slicer.mrmlScene )
    self.inputSelectorUno.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume: ", self.inputSelectorUno)
    
    self.filtrarButton = qt.QPushButton("Filter all")
    self.filtrarButton.toolTip = "Run the algorithm."
    self.filtrarButton.enabled = False
    parametersFormLayout.addRow(self.filtrarButton)
    
    
    
    #filtrado -----------------------------------------------------------
#%%
    #Registro------------------------------------------------------------
    parametersCollapsibleButtonUno = ctk.ctkCollapsibleButton()
    parametersCollapsibleButtonUno.text = "Registro"
    self.layout.addWidget(parametersCollapsibleButtonUno)

    # Layout within the dummy collapsible button
    parametersFormLayoutUno = qt.QFormLayout(parametersCollapsibleButtonUno)
    
    self.inputSelectorDos = slicer.qMRMLNodeComboBox()
    self.inputSelectorDos.nodeTypes = ["vtkMRMLMultiVolumeNode"]
    self.inputSelectorDos.selectNodeUponCreation = True
    self.inputSelectorDos.addEnabled = False
    self.inputSelectorDos.removeEnabled = False
    self.inputSelectorDos.noneEnabled = False
    self.inputSelectorDos.showHidden = False
    self.inputSelectorDos.showChildNodeTypes = False
    self.inputSelectorDos.setMRMLScene( slicer.mrmlScene )
    self.inputSelectorDos.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayoutUno.addRow("Input Volume: ", self.inputSelectorDos)
    
    self.registroButton = qt.QPushButton("apply")
    self.registroButton.toolTip = "Run the algorithm."
    self.registroButton.enabled = False
    parametersFormLayoutUno.addRow(self.registroButton)
    
    #Registro-------------------------------
    
#%%
    #Segmentacion--------------------------------------
    parametersCollapsibleButtonDos = ctk.ctkCollapsibleButton()
    parametersCollapsibleButtonDos.text = "Segmentation"
    self.layout.addWidget(parametersCollapsibleButtonDos)

    # Layout within the dummy collapsible button
    parametersFormLayoutDos = qt.QFormLayout(parametersCollapsibleButtonDos)
    
    self.inputSelectorTres = slicer.qMRMLNodeComboBox()
    self.inputSelectorTres.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputSelectorTres.selectNodeUponCreation = True
    self.inputSelectorTres.addEnabled = False
    self.inputSelectorTres.removeEnabled = False
    self.inputSelectorTres.noneEnabled = False
    self.inputSelectorTres.showHidden = False
    self.inputSelectorTres.showChildNodeTypes = False
    self.inputSelectorTres.setMRMLScene( slicer.mrmlScene )
    self.inputSelectorTres.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayoutDos.addRow("Input Volume: ", self.inputSelectorTres)
    
    self.inputSelectorCuatro = slicer.qMRMLNodeComboBox()
    self.inputSelectorCuatro.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
    self.inputSelectorCuatro.selectNodeUponCreation = True
    self.inputSelectorCuatro.addEnabled = False
    self.inputSelectorCuatro.removeEnabled = False
    self.inputSelectorCuatro.noneEnabled = False
    self.inputSelectorCuatro.showHidden = False
    self.inputSelectorCuatro.showChildNodeTypes = False
    self.inputSelectorCuatro.setMRMLScene( slicer.mrmlScene )
    self.inputSelectorCuatro.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayoutDos.addRow("Fiducial: ", self.inputSelectorCuatro)
    
    self.segmenButton = qt.QPushButton("Apply")
    self.segmenButton.toolTip = "Run the algorithm."
    self.segmenButton.enabled = False
    parametersFormLayoutDos.addRow(self.segmenButton)
    
#%%
    #Grafico de curvas
    parametersCollapsibleButtonTres = ctk.ctkCollapsibleButton()
    parametersCollapsibleButtonTres.text = "Graph"
    self.layout.addWidget(parametersCollapsibleButtonTres)

    # Layout within the dummy collapsible button
    parametersFormLayoutTres = qt.QFormLayout(parametersCollapsibleButtonTres)
    
    self.inputSelectorS = slicer.qMRMLNodeComboBox()
    self.inputSelectorS.nodeTypes = ["vtkMRMLMultiVolumeNode"]
    self.inputSelectorS.selectNodeUponCreation = True
    self.inputSelectorS.addEnabled = False
    self.inputSelectorS.removeEnabled = False
    self.inputSelectorS.noneEnabled = False
    self.inputSelectorS.showHidden = False
    self.inputSelectorS.showChildNodeTypes = False
    self.inputSelectorS.setMRMLScene( slicer.mrmlScene )
    self.inputSelectorS.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayoutTres.addRow("Input Volume: ", self.inputSelectorS)
    
    self.inputSelectort = slicer.qMRMLNodeComboBox()
    self.inputSelectort.nodeTypes = ["vtkMRMLLabelMapVolumeNode"]
    self.inputSelectort.selectNodeUponCreation = True
    self.inputSelectort.addEnabled = False
    self.inputSelectort.removeEnabled = False
    self.inputSelectort.noneEnabled = False
    self.inputSelectort.showHidden = False
    self.inputSelectort.showChildNodeTypes = False
    self.inputSelectort.setMRMLScene( slicer.mrmlScene )
    self.inputSelectort.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayoutTres.addRow("Label Map Volume: ", self.inputSelectort)
    
    
    self.grafButton = qt.QPushButton("Graph")
    self.grafButton.toolTip = "Run the algorithm."
    self.grafButton.enabled = False
    parametersFormLayoutTres.addRow(self.grafButton)  
    
    
#%%
    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputSelectorZero.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputSelectorUno.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputSelectorDos.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputSelectorTres.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputSelectorCuatro.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputSelectorS.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputSelectort.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    
    self.chargeButton.connect('clicked(bool)', self.onChargeButton)
    self.applyButtonZero.connect('clicked(bool)', self.onApplyButtonZero)
    self.filtrarButton.connect('clicked(bool)', self.onFiltrarButton)
    self.registroButton.connect('clicked(bool)', self.onRegistroButton)
    self.segmenButton.connect('clicked(bool)', self.onSegmenButton)
    self.grafButton.connect('clicked(bool)', self.onGrafButton)
    

    # Add vertical spacer
    self.layout.addStretch(5)

    # Refresh Apply button state
    self.onSelect()
    
    
  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()
    self.applyButtonZero.enabled = self.inputSelectorZero.currentNode()
    self.filtrarButton.enabled = self.inputSelectorUno.currentNode()
    self.registroButton.enabled = self.inputSelectorDos.currentNode()
    self.segmenButton.enabled= self.inputSelectorTres.currentNode() and self.inputSelectorCuatro.currentNode()
    self.grafButton.enabled=self.inputSelectorS.currentNode() and self.inputSelectort.currentNode()
    

  def onApplyButton(self):
    logic = HelloPythonLogic()
    #enableScreenshotsFlag = self.enableScreenshotsFlagCheckBox.checked
    conductance= self.conductanceWidget.value
    iterations= self.iterationsWidget.value
    timeStep=self.timeStepWidget.value
    logic.filtrado(self.inputSelector.currentNode(), self.outputSelector.currentNode(), conductance, iterations, timeStep)
   
  def onApplyButtonZero(self):
      logic = HelloPythonLogic()
      logic.volumenes()
  
  def onChargeButton(self):
      logic = HelloPythonLogic()
      logic.charge()
      
  def onFiltrarButton(self):
      logic=HelloPythonLogic()
      conductance= self.conductanceWidget.value
      iterations= self.iterationsWidget.value
      timeStep=self.timeStepWidget.value
      logic.filTodo(self.inputSelectorUno.currentNode(), conductance,iterations, timeStep)
     
  def onRegistroButton(self):
      logic=HelloPythonLogic()
      logic.registro(self.inputSelectorDos.currentNode())

  def onSegmenButton(self):
      logic=HelloPythonLogic
      logic.segmentar(self.inputSelectorTres.currentNode(), self.inputSelectorCuatro.currentNode())

  def onGrafButton(self):
      logic=HelloPythonLogic
      logic.graficar(self.inputSelectorS.currentNode(), self.inputSelectorT.currentNode())
#
# HelloPythonLogic
#

class HelloPythonLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def hasImageData(self,volumeNode):
    """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      logging.debug('hasImageData failed: no volume node')
      return False
    if volumeNode.GetImageData() is None:
      logging.debug('hasImageData failed: no image data in volume node')
      return False
    return True

  def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
    """Validates if the output is not the same as input
    """
    if not inputVolumeNode:
      logging.debug('isValidInputOutputData failed: no input volume node defined')
      return False
    if not outputVolumeNode:
      logging.debug('isValidInputOutputData failed: no output volume node defined')
      return False
    if inputVolumeNode.GetID()==outputVolumeNode.GetID():
      logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
      return False
    return True

  def run(self, inputVolume, outputVolume, imageThreshold, enableScreenshots=0):
    """
    Run the actual algorithm
    """
      
    if not self.isValidInputOutputData(inputVolume, outputVolume):
      slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
      return False
      
    logging.info('Processing started')
      
    # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
    cliParams = {'InputVolume': inputVolume.GetID(), 'OutputVolume': outputVolume.GetID(), 'ThresholdValue' : imageThreshold, 'ThresholdType' : 'Above'}
    cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True)
      
    # Capture screenshot
    if enableScreenshots:
      self.takeScreenshot('HelloPythonTest-Start','MyScreenshot',-1)
      
    logging.info('Processing completed')
      
    return True

  def graficar(self, inputVolume, labelMapVolume):
      import numpy
      labelName=labelMapVolume.GetImageData()
      label = array(labelName)#se especifica la region segmentada
      points  = numpy.where( label == 2 )
      escena = slicer.mrmlScene;
      volumen4D=escena.GetNodeByID(inputVolume.GetID())
      imagenvtk4D = volumen4D.GetImageData()
      numero_imagenes = volumen4D.GetNumberOfFrames()
      eje_x=numpy.array(range(numero_imagenes))
      data=numpy.zeros(())
      
      for i in range(numero_imagenes): #obtiene todos los volumenes 
          volumenFijo = slicer.vtkMRMLScalarVolumeNode();    
          imagen_fija = extract1.SetComponents(i)
          extract1.Update()
          volumenFijo.SetAndObserveImageData(extract1.GetOutput())
          extract1.Update()
          volumenFijo.SetName("frame"+str(i))
          volumenFijo.SetRASToIJKMatrix(ras2ijk)
          volumenFijo.SetIJKToRASMatrix(ijk2ras)
          escena.AddNode(volumenFijo)
      
      prom=numpy.array([])
      for i in range(numero_imagenes):
          volume=array("frame"+str(i))
          values = volume[points]
          prom=numpy.append(prom,values.mean())
          
      chartNode = slicer.util.plot((eje_x,prom), xColumnIndex=0, columnNames=['X', 'X^2'])
      chartNode.SetXAxisTitle('X')
      chartNode.SetYAxisTitle('Y')
      chartNode.LegendVisibilityOff()
      chartNode.SetTitle('Volume vs Intensity')
      
      
  
  def charge(self):
    fileName=qt.QFileDialog.getOpenFileName()    
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
    print("Successfully loaded")

  def volumenes(self):
      
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
      print("Finished")
      
  def segmentar(self, inputVolume, fiducialNode):
      parameters = {}
      parameters['smoothingIterations'] = 5.0 
      parameters['timestep'] = 0.0625
      
      

      parameters['iterations'] = 5
      parameters['multiplier'] = 2.5
      parameters['neighborhood'] = 1
      parameters['labelvalue'] = 2
      
      parameters['seed'] = fiducialNode.GetID()
      parameters['inputVolume'] = inputVolume.GetID()
      
      volumen_salida = slicer.vtkMRMLLabelMapVolumeNode()
      slicer.mrmlScene.AddNode(volumen_salida)
      parameters['outputVolume'] = volumen_salida.GetID()

      cliModule = slicer.modules.simpleregiongrowingsegmentation
      cliNode = slicer.cli.run(cliModule,None,parameters,wait_for_completion=True)
      
      
  def filtrado(self, inputVolume, outputVolume, conductance, iterations, timeStep):     
      
      if not self.isValidInputOutputData(inputVolume, outputVolume):
          slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
          return False
      
      logging.info('Processing started')
      
      cliModule = slicer.modules.gradientanisotropicdiffusion
      n = cliModule.cliModuleLogic().CreateNode()
      parameters = {}
      parameters['conductance'] = conductance
      parameters['numberOfIterations'] = iterations
      parameters['timeStep'] = timeStep
      parameters['inputVolume'] = inputVolume.GetID()
      parameters['outputVolume'] = outputVolume.GetID()
      cliModule = slicer.modules.gradientanisotropicdiffusion
      cliNode = slicer.cli.run(cliModule,None,parameters,wait_for_completion=True)
      print("Finished")
      
  def filTodo(self, inputVolume, conductance, iterations, timeStep):
      escena = slicer.mrmlScene;
      volumen4D=escena.GetNodeByID(inputVolume.GetID())
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
          parameters['conductance'] = conductance 
          parameters['numberOfIterations'] = iterations
          parameters['timeStep'] = timeStep
          volumen_entrada = slicer.mrmlScene.GetNodeByID("vtkMRMLScalarVolumeNode"+str(i+1))
          volumen_salida = slicer.vtkMRMLScalarVolumeNode()
          slicer.mrmlScene.AddNode(volumen_salida)
          parameters['inputVolume'] = volumen_entrada.GetID()
          parameters['outputVolume'] = volumen_salida.GetID()
          cliModule = slicer.modules.gradientanisotropicdiffusion
          cliNode = slicer.cli.run(cliModule,None,parameters,wait_for_completion=True)
      print("Finished")
      
  def registro(self, inputVolume):
      escena = slicer.mrmlScene;
      volumen4D=escena.GetNodeByID(inputVolume.GetID())
      imagenvtk4D = volumen4D.GetImageData()
      numero_imagenes = volumen4D.GetNumberOfFrames()
      #print('imagenes: ' + str(numero_imagenes))
        
      #dimensiones
      
      #print(imagenvtk4D.GetBounds())
      
      extract1 = vtk.vtkImageExtractComponents()
      extract1.SetInputData(imagenvtk4D)
      
      #matrices de transformacion
      ras2ijk = vtk.vtkMatrix4x4()
      ijk2ras = vtk.vtkMatrix4x4()
      
      #le solicitamos al volumen original que nos devuelva sus matrices\
      volumen4D.GetRASToIJKMatrix(ras2ijk)
      volumen4D.GetIJKToRASMatrix(ijk2ras)
      
      #creo un volumen nuevo que ser\'e1 el volumen fijo a registrar\
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
          imagen_movil = extract1.SetComponents(i+1) #Seleccionamos un volumen lejano
          extract1.Update()
          volumenMovil = slicer.vtkMRMLScalarVolumeNode();
          volumenMovil.SetRASToIJKMatrix(ras2ijk)
          volumenMovil.SetIJKToRASMatrix(ijk2ras)
          volumenMovil.SetAndObserveImageData(extract1.GetOutput())
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


     

class HelloPythonTest(ScriptedLoadableModuleTest):
    
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """
    
    def setUp(self):
        """ Do whatever is needed to reset the state - typically a scene clear will be enough.
        """
        slicer.mrmlScene.Clear(0)
    
    def runTest(self):
        """Run as few or as many tests as needed here.
        """
        self.setUp()
        self.test_HelloPython1()
    
    def test_HelloPython1(self):
        """ Ideally you should have several levels of tests.  At the lowest level
        tests should exercise the functionality of the logic with different inputs
        (both valid and invalid).  At higher levels your tests should emulate the
        way the user would interact with your code and confirm that it still works
        the way you intended.
        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on,
        your test should break so they know that the feature is needed.
        """
      
        self.delayDisplay("Starting the test")
        #
        # first, get some data
        #
        import SampleData
        SampleData.downloadFromURL(
          nodeNames='FA',
          fileNames='FA.nrrd',
          uris='http://slicer.kitware.com/midas3/download?items=5767')
        self.delayDisplay('Finished with download and loading')
      
        volumeNode = slicer.util.getNode(pattern="FA")
        logic = HelloPythonLogic()
        self.assertIsNotNone( logic.hasImageData(volumeNode) )
        self.delayDisplay('Test passed!')
