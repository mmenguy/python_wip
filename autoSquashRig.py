import maya.cmds as cmds
import zTools.rig.zbw_rig as rig

def create_squash_rig(*args):
    """
    creates a rig around the selected objects. Two squashes are created (upDown/lfRt)
    :param args:
    :return:
    """
    sel = cmds.ls(sl=True, type="transform")

    if not sel:
        cmds.warning("You need to select some transforms!")
        return()

    mainCtrlRaw = rig.boundingBoxCtrl(sel, False)
    mainCtrl = cmds.rename(mainCtrlRaw, "{0}_CTRL".format(sel[0]))
    grp = rig.groupFreeze(mainCtrl)
    rig.scaleNurbsCtrl(mainCtrl, 1.2, .2, 1.2)
    secCtrl = cmds.duplicate(mainCtrl, name="{0}2_CTRL".format(sel[0]))[0]
    rig.scaleNurbsCtrl(secCtrl, .9, .9, .9)
    thrdCtrl = cmds.duplicate(mainCtrl, name="{0}3_CTRL".format(sel[0]))[0]
    rig.scaleNurbsCtrl(thrdCtrl, .8, .8, .8)
    cmds.parent(thrdCtrl, secCtrl)
    cmds.parent(secCtrl, mainCtrl)
    cmds.parent(sel, thrdCtrl)

    try:
        rig.assignColor(mainCtrl, "red")
    except:
        pass
    try:
        rig.assignColor(secCtrl, "pink")
    except:
        pass
    try:
        rig.assignColor(thrdCtrl, "lightRed")
    except:
        pass

    cmds.addAttr(mainCtrl, ln="__xtraAttrs__", nn="__xtraAttrs__", at="enum", en="------", k=True)
    cmds.setAttr("{0}.__xtraAttrs__".format(mainCtrl), l=True)

    cmds.addAttr(mainCtrl, ln="secondaryCtrlVis", at="long", min=0, max=1, dv=0, k=True)
    secShp = cmds.listRelatives(secCtrl, s=True)[0]
    cmds.connectAttr("{0}.secondaryCtrlVis".format(mainCtrl), "{0}.visibility".format(secShp))
    thrdShp = cmds.listRelatives(thrdCtrl, s=True)[0]
    cmds.connectAttr("{0}.secondaryCtrlVis".format(mainCtrl), "{0}.visibility".format(thrdShp))

    # create squash
    cmds.select(sel, r=True)
    sq1Def, sq1Handle = cmds.nonLinear(type="squash", name="{0}_squash1".format(sel[0]))
    cmds.parent(sq1Handle, thrdCtrl)
    cmds.addAttr(mainCtrl, ln="squash1Factor", at="float", min=-5, max=5, dv=0, k=True)
    cmds.addAttr(mainCtrl, ln="squash1Vis", at="long", min=0, max=1, dv=0, k=True)
    cmds.connectAttr("{0}.squash1Factor".format(mainCtrl), "{0}.factor".format(sq1Def))
    cmds.connectAttr("{0}.squash1Vis".format(mainCtrl), "{0}.v".format(sq1Handle))

    cmds.select(sel, r=True)
    sq2Def, sq2Handle = cmds.nonLinear(type="squash", name="{0}_squash1".format(sel[0]))
    cmds.parent(sq2Handle, thrdCtrl)
    cmds.addAttr(mainCtrl, ln="squash2Factor", at="float", min=-5, max=5, dv=0, k=True)
    cmds.addAttr(mainCtrl, ln="squash2Vis", at="long", min=0, max=1, dv=0, k=True)
    cmds.setAttr("{0}.rz".format(sq2Handle), 90)
    cmds.connectAttr("{0}.squash2Factor".format(mainCtrl), "{0}.factor".format(sq2Def))
    cmds.connectAttr("{0}.squash2Vis".format(mainCtrl), "{0}.v".format(sq2Handle))

    cmds.setAttr("{0}.lowBound".format(sq1Def), -1.3)
    cmds.setAttr("{0}.lowBound".format(sq2Def), -1.3)
    cmds.setAttr("{0}.highBound".format(sq1Def), 1.3)
    cmds.setAttr("{0}.highBound".format(sq2Def), 1.3)            