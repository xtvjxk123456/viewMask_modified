# coding:utf-8
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
            # obj = stringData.create("Position {0}".format(str(i / 2 + 1).zfill(2)))
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

    def draw(self, view, path, style, status):
        # collect data
        cameraPath = view.getCamera()
        camera = om.MFnCamera(cameraPath)
        fnDagNode = om.MFnDagNode(path.extendToShape())
        cameraName = fnDagNode.findPlug("camera", False).asString()
        textFields = []
        for i in range(0, len(ViewMaskLocator.TEXT_ATTRS), 2):
            textFields.append(fnDagNode.findPlug(ViewMaskLocator.TEXT_ATTRS[i], False).asString())
        counterPadding = fnDagNode.findPlug("counterPadding", False).asInt()
        if counterPadding < 1:
            counterPadding = 1
        elif counterPadding > 6:
            counterPadding = 6

        # textFields[4] = "{0}/{1:.1f}".format(cameraPath.partialPathName(), camera.focalLength)

        # currentTime = int(cmds.currentTime(q=True))
        # counterPosition = fnDagNode.findPlug("counterPosition", False).asInt()
        # if counterPosition > 0 and counterPosition <= len(ViewMaskLocator.TEXT_ATTRS) / 2:
        #     textFields[counterPosition - 1] = "{0}".format(str(currentTime).zfill(counterPadding), )

        textPadding = fnDagNode.findPlug("textPadding", False).asInt()

        fontName = fnDagNode.findPlug("fontName", False).asString()
        r = fnDagNode.findPlug("fontColorR", False).asFloat()
        g = fnDagNode.findPlug("fontColorG", False).asFloat()
        b = fnDagNode.findPlug("fontColorB", False).asFloat()
        a = fnDagNode.findPlug("fontAlpha", False).asFloat()
        fontColor = om.MColor((r, g, b, a))

        fontScale = fnDagNode.findPlug("fontScale", False).asFloat()
        r = fnDagNode.findPlug("borderColorR", False).asFloat()
        g = fnDagNode.findPlug("borderColorG", False).asFloat()
        b = fnDagNode.findPlug("borderColorB", False).asFloat()
        a = fnDagNode.findPlug("borderAlpha", False).asFloat()
        borderColor = om.MColor((r, g, b, a))

        borderScale = fnDagNode.findPlug("borderScale", False).asFloat()

        topBorder = fnDagNode.findPlug("topBorder", False).asBool()
        bottomBorder = fnDagNode.findPlug("bottomBorder", False).asBool()

        # draw-----------------------------------------------------------
        if cameraName and cameraName in cmds.listCameras() and not self.isCameraMatch(cameraPath, cameraName):
            return

        cameraAspectRatio = camera.aspectRatio()
        deviceAspectRatio = cmds.getAttr("defaultResolution.deviceAspectRatio")

        vpWidth = view.portWidth()
        vpHeight = view.portHeight()
        vpHalfWidth = 0.5 * vpWidth
        vpHalfHeight = 0.5 * vpHeight
        vpAspectRatio = vpWidth / float(vpHeight)

        scale = 1.0

        if camera.filmFit == om.MFnCamera.kHorizontalFilmFit:
            # maskWidth = vpWidth / camera.overscan
            maskWidth = vpWidth/camera.overscan
            maskHeight = maskWidth / deviceAspectRatio
        elif camera.filmFit == om.MFnCamera.kVerticalFilmFit:
            # maskHeight = vpHeight / camera.overscan
            maskHeight = vpHeight/camera.overscan
            maskWidth = maskHeight * deviceAspectRatio
        elif camera.filmFit == om.MFnCamera.kFillFilmFit:
            if vpAspectRatio < cameraAspectRatio:
                if cameraAspectRatio < deviceAspectRatio:
                    scale = cameraAspectRatio / vpAspectRatio
                else:
                    scale = deviceAspectRatio / vpAspectRatio
            elif cameraAspectRatio > deviceAspectRatio:
                scale = deviceAspectRatio / cameraAspectRatio

            # maskWidth = vpWidth / camera.overscan * scale
            maskWidth = vpWidth/camera.overscan * scale
            maskHeight = maskWidth / deviceAspectRatio

        elif camera.filmFit == om.MFnCamera.kOverscanFilmFit:
            if vpAspectRatio < cameraAspectRatio:
                if cameraAspectRatio < deviceAspectRatio:
                    scale = cameraAspectRatio / vpAspectRatio
                else:
                    scale = deviceAspectRatio / vpAspectRatio
            elif cameraAspectRatio > deviceAspectRatio:
                scale = deviceAspectRatio / cameraAspectRatio

            # maskHeight = vpHeight / camera.overscan / scale
            maskHeight = vpHeight / camera.overscan/scale
            maskWidth = maskHeight * deviceAspectRatio
        else:
            om.MGlobal.displayError("[ViewMask] Unknown Film Fit value")
            return

        maskHalfWidth = 0.5 * maskWidth
        maskX = vpHalfWidth - maskHalfWidth

        maskHalfHeight = 0.5 * maskHeight
        maskBottomY = vpHalfHeight - maskHalfHeight
        maskTopY = vpHalfHeight + maskHalfHeight

        borderHeight = int(0.05 * maskHeight * borderScale)
        bgSize = (int(maskWidth), borderHeight)

        # Getting the OpenGL renderer
        import maya.OpenMayaRender as v1omr
        import maya.OpenMayaUI as v1omui
        glRenderer = v1omr.MHardwareRenderer.theRenderer()
        glFT = glRenderer.glFunctionTable()

        # Pushed current state
        glFT.glPushAttrib(v1omr.MGL_CURRENT_BIT)
        # Enabled Blend mode (to enable transparency)
        glFT.glEnable(v1omr.MGL_BLEND)
        # Defined Blend function
        glFT.glBlendFunc(v1omr.MGL_SRC_ALPHA, v1omr.MGL_ONE_MINUS_SRC_ALPHA)
        # create x-ray view and will be seen always
        glFT.glDisable(v1omr.MGL_DEPTH_TEST)

        # Starting the OpenGL drawing
        view.beginGL()
        # 设置字体，字体大小，字体颜色
        # viewport 1无法自定义字体和字体大小
        view.setDrawColor(fontColor)
        if topBorder:
            pass
        if bottomBorder:
            pass
        self.drawText(view, om.MPoint(maskX + textPadding, maskTopY - borderHeight), textFields[0],
                      v1omui.M3dView.kLeft)
        self.drawText(view, om.MPoint(vpHalfWidth, maskTopY - borderHeight), textFields[1],
                      v1omui.M3dView.kCenter)
        self.drawText(view, om.MPoint(maskX + maskWidth - textPadding, maskTopY - borderHeight),
                      textFields[2], v1omui.M3dView.kRight)
        self.drawText(view, om.MPoint(maskX + textPadding, maskBottomY), textFields[3],
                      v1omui.M3dView.kLeft)
        self.drawText(view, om.MPoint(vpHalfWidth, maskBottomY), textFields[4], v1omui.M3dView.kCenter
                      )
        self.drawText(view, om.MPoint(maskX + maskWidth - textPadding, maskBottomY), textFields[5],
                      v1omui.M3dView.kRight)

        glFT.glDisable(v1omr.MGL_BLEND)
        glFT.glEnable(v1omr.MGL_DEPTH_TEST)
        # Restore the state
        glFT.glPopAttrib()
        # Ending the OpenGL drawing
        view.endGL()

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

    def drawText(self, view, position2d, text, alignment, ):
        """
        """
        if len(text) > 0:
            # 转换位置
            textPositionNearPlane = om.MPoint()
            textPositionFarPlane = om.MPoint()
            view.viewToWorld(int(position2d.x), int(position2d.y), textPositionNearPlane, textPositionFarPlane)
            view.drawText(text, textPositionNearPlane, alignment)


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

        data.camera_name = fnDagNode.findPlug("camera", False).asString()

        data.text_fields = []
        for i in range(0, len(ViewMaskLocator.TEXT_ATTRS), 2):
            data.text_fields.append(fnDagNode.findPlug(ViewMaskLocator.TEXT_ATTRS[i], False).asString())

        counter_padding = fnDagNode.findPlug("counterPadding", False).asInt()
        if counter_padding < 1:
            counter_padding = 1
        elif counter_padding > 6:
            counter_padding = 6

        # current_time = int(cmds.currentTime(q=True))
        # counter_position = fnDagNode.findPlug("counterPosition", False).asInt()
        # if counter_position > 0 and counter_position <= len(ViewMaskLocator.TEXT_ATTRS) / 2:
        #     data.text_fields[counter_position - 1] = "{0}".format(str(current_time).zfill(counter_padding))

        data.text_padding = fnDagNode.findPlug("textPadding", False).asInt()

        data.font_name = fnDagNode.findPlug("fontName", False).asString()

        r = fnDagNode.findPlug("fontColorR", False).asFloat()
        g = fnDagNode.findPlug("fontColorG", False).asFloat()
        b = fnDagNode.findPlug("fontColorB", False).asFloat()
        a = fnDagNode.findPlug("fontAlpha", False).asFloat()
        data.font_color = om.MColor((r, g, b, a))

        data.font_scale = fnDagNode.findPlug("fontScale", False).asFloat()

        r = fnDagNode.findPlug("borderColorR", False).asFloat()
        g = fnDagNode.findPlug("borderColorG", False).asFloat()
        b = fnDagNode.findPlug("borderColorB", False).asFloat()
        a = fnDagNode.findPlug("borderAlpha", False).asFloat()
        data.border_color = om.MColor((r, g, b, a))

        data.border_scale = fnDagNode.findPlug("borderScale", False).asFloat()

        data.top_border = fnDagNode.findPlug("topBorder", False).asBool()
        data.bottom_border = fnDagNode.findPlug("bottomBorder", False).asBool()

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

        camera_path = frameContext.getCurrentCameraPath()
        camera = om.MFnCamera(camera_path)

        if data.camera_name and self.cameraExists(data.camera_name) and not self.isCameraMatch(camera_path, data.camera_name):
            return

        camera_aspect_ratio = camera.aspectRatio()
        device_aspect_ratio = cmds.getAttr("defaultResolution.deviceAspectRatio")

        vp_x, vp_y, vp_width, vp_height = frameContext.getViewportDimensions()
        vp_half_width = 0.5 * vp_width
        vp_half_height = 0.5 * vp_height
        vp_aspect_ratio = vp_width / float(vp_height)

        scale = 1.0

        if camera.filmFit == om.MFnCamera.kHorizontalFilmFit:
            mask_width = vp_width / camera.overscan
            mask_height = mask_width / device_aspect_ratio
        elif camera.filmFit == om.MFnCamera.kVerticalFilmFit:
            mask_height = vp_height / camera.overscan
            mask_width = mask_height * device_aspect_ratio
        elif camera.filmFit == om.MFnCamera.kFillFilmFit:
            if vp_aspect_ratio < camera_aspect_ratio:
                if camera_aspect_ratio < device_aspect_ratio:
                    scale = camera_aspect_ratio / vp_aspect_ratio
                else:
                    scale = device_aspect_ratio / vp_aspect_ratio
            elif camera_aspect_ratio > device_aspect_ratio:
                scale = device_aspect_ratio / camera_aspect_ratio

            mask_width = vp_width / camera.overscan * scale
            mask_height = mask_width / device_aspect_ratio

        elif camera.filmFit == om.MFnCamera.kOverscanFilmFit:
            if vp_aspect_ratio < camera_aspect_ratio:
                if camera_aspect_ratio < device_aspect_ratio:
                    scale = camera_aspect_ratio / vp_aspect_ratio
                else:
                    scale = device_aspect_ratio / vp_aspect_ratio
            elif camera_aspect_ratio > device_aspect_ratio:
                scale = device_aspect_ratio / camera_aspect_ratio

            mask_height = vp_height / camera.overscan / scale
            mask_width = mask_height * device_aspect_ratio
        else:
            om.MGlobal.displayError("[ZShotMask] Unknown Film Fit value")
            return

        mask_half_width = 0.5 * mask_width
        mask_x = vp_half_width - mask_half_width

        mask_half_height = 0.5 * mask_height
        mask_bottom_y = vp_half_height - mask_half_height
        mask_top_y = vp_half_height + mask_half_height

        border_height = int(0.05 * mask_height * data.border_scale)
        background_size = (int(mask_width), border_height)

        drawManager.beginDrawable()
        drawManager.setFontName(data.font_name)
        drawManager.setFontSize(int((border_height - border_height * 0.15) * data.font_scale))
        drawManager.setColor(data.font_color)

        if data.top_border:
            self.drawBorder(drawManager, om.MPoint(mask_x, mask_top_y - border_height), background_size, data.border_color)
        if data.bottom_border:
            self.drawBorder(drawManager, om.MPoint(mask_x, mask_bottom_y), background_size, data.border_color)

        self.drawText(drawManager, om.MPoint(mask_x + data.text_padding, mask_top_y - border_height), data.text_fields[0], omr.MUIDrawManager.kLeft, background_size)
        self.drawText(drawManager, om.MPoint(vp_half_width, mask_top_y - border_height), data.text_fields[1], omr.MUIDrawManager.kCenter, background_size)
        self.drawText(drawManager, om.MPoint(mask_x + mask_width - data.text_padding, mask_top_y - border_height), data.text_fields[2], omr.MUIDrawManager.kRight, background_size)
        self.drawText(drawManager, om.MPoint(mask_x + data.text_padding, mask_bottom_y), data.text_fields[3], omr.MUIDrawManager.kLeft, background_size)
        self.drawText(drawManager, om.MPoint(vp_half_width, mask_bottom_y), data.text_fields[4], omr.MUIDrawManager.kCenter, background_size)
        self.drawText(drawManager, om.MPoint(mask_x + mask_width - data.text_padding, mask_bottom_y), data.text_fields[5], omr.MUIDrawManager.kRight, background_size)

        drawManager.endDrawable()

    def drawBorder(self, drawManager, position, bgSize, color):
        """
        """
        drawManager.text2d(position, " ", alignment=omr.MUIDrawManager.kLeft, backgroundSize=bgSize,
                           backgroundColor=color)

    def drawText(self, drawManager, position, text, alignment, bgSize):
        """
        """
        if (len(text) > 0):
            drawManager.text2d(position, text, alignment=alignment, backgroundSize=bgSize,
                               backgroundColor=om.MColor((0.0, 0.0, 0.0, 0.0)))

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
        omr.MDrawRegistry.deregisterDrawOverrideCreator(ViewMaskLocator.DRAW_DB_CLASSIFICATION,
                                                        ViewMaskLocator.DRAW_REGISTRANT_ID)
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
