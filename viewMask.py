import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr
import maya.api.OpenMayaUI as omui

import maya.cmds as cmds


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


class ViewMaskLocator(omui.MPxLocatorNode):
    """
    """

    NAME = "viewMask"
    TYPE_ID = om.MTypeId(0x0011A885)
    DRAW_DB_CLASSIFICATION = "drawdb/geometry/viewMask"
    DRAW_REGISTRANT_ID = "ViewMaskNodePlugin"

    TEXT_ATTRS = ["topLeftText", "tlt", "topCenterText", "tct", "topRightText", "trt",
                  "bottomLeftText", "blt", "bottomCenterText", "bct", "bottomRightText", "brt"]

    def __init__(self):
        """
        """
        super(ViewMaskLocator, self).__init__()

    @classmethod
    def creator(cls):
        """
        """
        return ViewMaskLocator()

    @classmethod
    def initialize(cls):
        """
        """

        tAttr = om.MFnTypedAttribute()
        stringData = om.MFnStringData()
        obj = stringData.create("")
        cameraName = tAttr.create("camera", "cam", om.MFnData.kString, obj)
        tAttr.writable = True
        tAttr.storable = True
        tAttr.keyable = False
        ViewMaskLocator.addAttribute(cameraName)

        attr = om.MFnNumericAttribute()
        counterPosition = attr.create("counterPosition", "cp", om.MFnNumericData.kShort, 6)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        attr.setMin(0)
        attr.setMax(6)
        ViewMaskLocator.addAttribute(counterPosition)

        attr = om.MFnNumericAttribute()
        counterPadding = attr.create("counterPadding", "cpd", om.MFnNumericData.kShort, 0)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        attr.setMin(1)
        attr.setMax(6)
        ViewMaskLocator.addAttribute(counterPadding)

        for i in range(0, len(cls.TEXT_ATTRS), 2):
            tAttr = om.MFnTypedAttribute()
            stringData = om.MFnStringData()
            #obj = stringData.create("Position {0}".format(str(i / 2 + 1).zfill(2)))
            obj = stringData.create()
            position = tAttr.create(cls.TEXT_ATTRS[i], cls.TEXT_ATTRS[i + 1], om.MFnData.kString, obj)
            tAttr.writable = True
            tAttr.storable = True
            tAttr.keyable = True
            ViewMaskLocator.addAttribute(position)

        attr = om.MFnNumericAttribute()
        counterPosition = attr.create("textPadding", "tp", om.MFnNumericData.kShort, 10)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        attr.setMin(0)
        attr.setMax(50)
        ViewMaskLocator.addAttribute(counterPosition)

        tAttr = om.MFnTypedAttribute()
        stringData = om.MFnStringData()
        obj = stringData.create("Times New Roman")
        fontName = tAttr.create("fontName", "fn", om.MFnData.kString, obj)
        tAttr.writable = True
        tAttr.storable = True
        tAttr.keyable = True
        ViewMaskLocator.addAttribute(fontName)

        attr = om.MFnNumericAttribute()
        fontColor = attr.createColor("fontColor", "fc")
        attr.default = (1.0, 1.0, 1.0)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        ViewMaskLocator.addAttribute(fontColor)

        attr = om.MFnNumericAttribute()
        fontAlpha = attr.create("fontAlpha", "fa", om.MFnNumericData.kFloat, 1.0)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        attr.setMin(0.0)
        attr.setMax(1.0)
        ViewMaskLocator.addAttribute(fontAlpha)

        attr = om.MFnNumericAttribute()
        fontScale = attr.create("fontScale", "fs", om.MFnNumericData.kFloat, 0.7)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        attr.setMin(0.1)
        attr.setMax(2.0)
        ViewMaskLocator.addAttribute(fontScale)

        attr = om.MFnNumericAttribute()
        topBorder = attr.create("topBorder", "tbd", om.MFnNumericData.kBoolean, False)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        ViewMaskLocator.addAttribute(topBorder)

        attr = om.MFnNumericAttribute()
        bottomBorder = attr.create("bottomBorder", "bbd", om.MFnNumericData.kBoolean, False)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        ViewMaskLocator.addAttribute(bottomBorder)

        attr = om.MFnNumericAttribute()
        borderColor = attr.createColor("borderColor", "bc")
        attr.default = (0.0, 0.0, 0.0)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        ViewMaskLocator.addAttribute(borderColor)

        attr = om.MFnNumericAttribute()
        borderAlpha = attr.create("borderAlpha", "ba", om.MFnNumericData.kFloat, 1.0)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        attr.setMin(0.0)
        attr.setMax(1.0)
        ViewMaskLocator.addAttribute(borderAlpha)

        attr = om.MFnNumericAttribute()
        borderScale = attr.create("borderScale", "bs", om.MFnNumericData.kFloat, 1.0)
        attr.writable = True
        attr.storable = True
        attr.keyable = True
        attr.setMin(0.5)
        attr.setMax(2.0)
        ViewMaskLocator.addAttribute(borderScale)


class ViewMaskData(om.MUserData):
    """
    """

    def __init__(self):
        """
        """
        super(ViewMaskData, self).__init__(False)


class ViewMaskDrawOverride(omr.MPxDrawOverride):
    """
    """

    NAME = "ViewMaskDrawOverride"

    def __init__(self, obj):
        """
        """
        super(ViewMaskDrawOverride, self).__init__(obj, ViewMaskDrawOverride.draw)

    def supportedDrawAPIs(self):
        """
        """
        return (omr.MRenderer.kAllDevices)

    def isBounded(self, objPath, cameraPath):
        """
        """
        return False

    def boundingBox(self, objPath, cameraPath):
        """
        """
        return om.MBoundingBox()

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        """
        """
        data = oldData
        if not isinstance(data, ViewMaskData):
            data = ViewMaskData()

        fnDagNode = om.MFnDagNode(objPath)

        data.cameraName = fnDagNode.findPlug("camera", False).asString()

        data.textFields = []
        for i in range(0, len(ViewMaskLocator.TEXT_ATTRS), 2):
            data.textFields.append(fnDagNode.findPlug(ViewMaskLocator.TEXT_ATTRS[i], False).asString())

        counterPadding = fnDagNode.findPlug("counterPadding", False).asInt()
        if counterPadding < 1:
            counterPadding = 1
        elif counterPadding > 6:
            counterPadding = 6

        camera = om.MFnCamera(cameraPath)
        data.textFields[4] = "{0}/{1:.1f}".format(cameraPath.partialPathName(), camera.focalLength)

        currentTime = int(cmds.currentTime(q=True))
        counterPosition = fnDagNode.findPlug("counterPosition", False).asInt()
        if counterPosition > 0 and counterPosition <= len(ViewMaskLocator.TEXT_ATTRS) / 2:
            data.textFields[counterPosition - 1] = "{0}{1}".format(str(currentTime).zfill(counterPadding), data.textFields[counterPosition - 1])

        data.textPadding = fnDagNode.findPlug("textPadding", False).asInt()

        data.fontName = fnDagNode.findPlug("fontName", False).asString()

        r = fnDagNode.findPlug("fontColorR", False).asFloat()
        g = fnDagNode.findPlug("fontColorG", False).asFloat()
        b = fnDagNode.findPlug("fontColorB", False).asFloat()
        a = fnDagNode.findPlug("fontAlpha", False).asFloat()
        data.fontColor = om.MColor((r, g, b, a))

        data.fontScale = fnDagNode.findPlug("fontScale", False).asFloat()

        r = fnDagNode.findPlug("borderColorR", False).asFloat()
        g = fnDagNode.findPlug("borderColorG", False).asFloat()
        b = fnDagNode.findPlug("borderColorB", False).asFloat()
        a = fnDagNode.findPlug("borderAlpha", False).asFloat()
        data.borderColor = om.MColor((r, g, b, a))

        data.borderScale = fnDagNode.findPlug("borderScale", False).asFloat()

        data.topBorder = fnDagNode.findPlug("topBorder", False).asBool()
        data.bottomBorder = fnDagNode.findPlug("bottomBorder", False).asBool()

        return data

    def hasUIDrawables(self):
        """
        """
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        """
        """
        if not isinstance(data, ViewMaskData):
            return

        cameraPath = frameContext.getCurrentCameraPath()
        camera = om.MFnCamera(cameraPath)

        if data.cameraName and self.cameraExists(data.cameraName) and not self.isCameraMatch(cameraPath, data.cameraName):
            return

        cameraAspectRatio = camera.aspectRatio()
        deviceAspectRatio = cmds.getAttr("defaultResolution.deviceAspectRatio")

        vpX, vpY, vpWidth, vpHeight = frameContext.getViewportDimensions()
        vpHalfWidth = 0.5 * vpWidth
        vpHalfHeight = 0.5 * vpHeight
        vpAspectRatio = vpWidth / float(vpHeight)

        scale = 1.0

        if camera.filmFit == om.MFnCamera.kHorizontalFilmFit:
            #maskWidth = vpWidth / camera.overscan
            maskWidth = vpWidth
            maskHeight = maskWidth / deviceAspectRatio
        elif camera.filmFit == om.MFnCamera.kVerticalFilmFit:
            #maskHeight = vpHeight / camera.overscan
            maskHeight = vpHeight
            maskWidth = maskHeight * deviceAspectRatio
        elif camera.filmFit == om.MFnCamera.kFillFilmFit:
            if vpAspectRatio < cameraAspectRatio:
                if cameraAspectRatio < deviceAspectRatio:
                    scale = cameraAspectRatio / vpAspectRatio
                else:
                    scale = deviceAspectRatio / vpAspectRatio
            elif cameraAspectRatio > deviceAspectRatio:
                scale = deviceAspectRatio / cameraAspectRatio

            #maskWidth = vpWidth / camera.overscan * scale
            maskWidth = vpWidth * scale
            maskHeight = maskWidth / deviceAspectRatio

        elif camera.filmFit == om.MFnCamera.kOverscanFilmFit:
            if vpAspectRatio < cameraAspectRatio:
                if cameraAspectRatio < deviceAspectRatio:
                    scale = cameraAspectRatio / vpAspectRatio
                else:
                    scale = deviceAspectRatio / vpAspectRatio
            elif cameraAspectRatio > deviceAspectRatio:
                scale = deviceAspectRatio / cameraAspectRatio

            #maskHeight = vpHeight / camera.overscan / scale
            maskHeight = vpHeight / scale
            maskWidth = maskHeight * deviceAspectRatio
        else:
            om.MGlobal.displayError("[ViewMask] Unknown Film Fit value")
            return

        maskHalfWidth = 0.5 * maskWidth
        maskX = vpHalfWidth - maskHalfWidth

        maskHalfHeight = 0.5 * maskHeight
        maskBottomY = vpHalfHeight - maskHalfHeight
        maskTopY = vpHalfHeight + maskHalfHeight

        borderHeight = int(0.05 * maskHeight * data.borderScale)
        bgSize = (int(maskWidth), borderHeight)

        drawManager.beginDrawable()
        drawManager.setFontName(data.fontName)
        drawManager.setFontSize(int((borderHeight - borderHeight * 0.15) * data.fontScale))
        drawManager.setColor(data.fontColor)

        if data.topBorder:
            self.drawBorder(drawManager, om.MPoint(maskX, maskTopY - borderHeight), bgSize, data.borderColor)
        if data.bottomBorder:
            self.drawBorder(drawManager, om.MPoint(maskX, maskBottomY), bgSize, data.borderColor)

        self.drawText(drawManager, om.MPoint(maskX + data.textPadding, maskTopY - borderHeight), data.textFields[0], omr.MUIDrawManager.kLeft, bgSize)
        self.drawText(drawManager, om.MPoint(vpHalfWidth, maskTopY - borderHeight), data.textFields[1], omr.MUIDrawManager.kCenter, bgSize)
        self.drawText(drawManager, om.MPoint(maskX + maskWidth - data.textPadding, maskTopY - borderHeight), data.textFields[2], omr.MUIDrawManager.kRight, bgSize)
        self.drawText(drawManager, om.MPoint(maskX + data.textPadding, maskBottomY), data.textFields[3], omr.MUIDrawManager.kLeft, bgSize)
        self.drawText(drawManager, om.MPoint(vpHalfWidth, maskBottomY), data.textFields[4], omr.MUIDrawManager.kCenter, bgSize)
        self.drawText(drawManager, om.MPoint(maskX + maskWidth - data.textPadding, maskBottomY), data.textFields[5], omr.MUIDrawManager.kRight, bgSize)

        drawManager.endDrawable()

    def drawBorder(self, drawManager, position, bgSize, color):
        """
        """
        drawManager.text2d(position, " ", alignment=omr.MUIDrawManager.kLeft, backgroundSize=bgSize, backgroundColor=color)

    def drawText(self, drawManager, position, text, alignment, bgSize):
        """
        """
        if(len(text) > 0):
            drawManager.text2d(position, text, alignment=alignment, backgroundSize=bgSize, backgroundColor=om.MColor((0.0, 0.0, 0.0, 0.0)))

    def cameraExists(self, name):
        """
        """
        return name in cmds.listCameras()

    def isCameraMatch(self, cameraPath, name):
        """
        """
        path_name = cameraPath.fullPathName()
        split_path_name = path_name.split('|')
        if len(split_path_name) >= 1:
            if split_path_name[-1] == name:
                return True
        if len(split_path_name) >= 2:
            if split_path_name[-2] == name:
                return True

        return False

    @staticmethod
    def creator(obj):
        """
        """
        return ViewMaskDrawOverride(obj)

    @staticmethod
    def draw(context, data):
        """
        """
        return


def initializePlugin(obj):
    """
    """
    pluginFn = om.MFnPlugin(obj, "KKAnim", "1.0", "Any")

    try:
        pluginFn.registerNode(ViewMaskLocator.NAME,
                              ViewMaskLocator.TYPE_ID,
                              ViewMaskLocator.creator,
                              ViewMaskLocator.initialize,
                              om.MPxNode.kLocatorNode,
                              ViewMaskLocator.DRAW_DB_CLASSIFICATION)
    except:
        om.MGlobal.displayError("Failed to register node: {0}".format(ViewMaskLocator.NAME))

    try:
        omr.MDrawRegistry.registerDrawOverrideCreator(ViewMaskLocator.DRAW_DB_CLASSIFICATION,
                                                      ViewMaskLocator.DRAW_REGISTRANT_ID,
                                                      ViewMaskDrawOverride.creator)
    except:
        om.MGlobal.displayError("Failed to register draw override: {0}".format(ViewMaskDrawOverride.NAME))


def uninitializePlugin(obj):
    """
    """
    pluginFn = om.MFnPlugin(obj)

    try:
        omr.MDrawRegistry.deregisterDrawOverrideCreator(ViewMaskLocator.DRAW_DB_CLASSIFICATION, ViewMaskLocator.DRAW_REGISTRANT_ID)
    except:
        om.MGlobal.displayError("Failed to deregister draw override: {0}".format(ViewMaskDrawOverride.NAME))

    try:
        pluginFn.deregisterNode(ViewMaskLocator.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to unregister node: {0}".format(ViewMaskLocator.NAME))


if __name__ == "__main__":

    cmds.file(f=True, new=True)

    plugin_name = "viewMask.py"
    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))

    cmds.evalDeferred('cmds.createNode("viewMask")')
