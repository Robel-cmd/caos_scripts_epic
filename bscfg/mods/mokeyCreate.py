
import bs
from bsMap import Map, registerMap
import bsUtils
import random


##Create Empty Map
class newZizagMap(Map):
    import monkeyFaceLevelDefs as defs
    name = 'ZizagMap Test'
    playTypes = ['test', 'melee']

    @classmethod
    def getPreviewTextureName(cls):
        return 'rampageBGColor'

    @classmethod
    def onPreload(cls):
        data = {}
        data['model'] = bs.getModel('monkeyFaceLevel')
        data['modelBottom'] = bs.getModel('monkeyFaceLevelBottom')
        data['modelBG'] = bs.getModel('doomShroomBG')
        data['bgVRFillModel'] = bs.getModel('natureBackgroundVRFill')
        data['collideModel'] = bs.getCollideModel('monkeyFaceLevelCollide')
        data['tex'] = bs.getTexture('monkeyFaceLevelColor')
        data['modelBGTex'] = bs.getTexture('menuBG')
        data['collideBG'] = bs.getCollideModel('natureBackgroundCollide')
        data['railingCollideModel'] = bs.getCollideModel('monkeyFaceLevelBumper')
        #data['bgMaterial'] = bs.Material()
        #data['bgMaterial'].addActions(actions=('modifyPartCollision',
                                               #'friction', 10.0))
        return data

    def __init__(self):
        Map.__init__(self)
        self.locs=[]
        self.regions=[]
        self.explo=[]
        self.collision = bs.Material()
        self.collision.addActions(
            actions=(('modifyPartCollision', 'collide', True)))


        self.node = bs.newNode('terrain', delegate=self, attrs={
            'collideModel':self.preloadData['collideModel'],
            'model':self.preloadData['model'],
            'colorTexture':self.preloadData['tex'],
            'materials':[bs.getSharedObject('footingMaterial')]})
        self.foo = bs.newNode('terrain', attrs={
            'model':self.preloadData['modelBG'],
            'lighting':False,
            'colorTexture':self.preloadData['modelBGTex']})
        # self.bottom = bs.newNode('terrain', attrs={
        #     'model':self.preloadData['modelBottom'],
        #     'lighting':False,
        #     'colorTexture':self.preloadData['tex']})
        # bs.newNode('terrain', attrs={
        #     'model':self.preloadData['bgVRFillModel'],
        #     'lighting':False,
        #     'vrOnly':True,
        #     'background':True,
        #     #'colorTexture':self.preloadData['modelBGTex']})
        # self.bgCollide = bs.newNode('terrain', attrs={
        #     'collideModel':self.preloadData['collideBG'],
        #     'materials':[bs.getSharedObject('footingMaterial'),
        #                  self.preloadData['bgMaterial'],
        #                  bs.getSharedObject('deathMaterial')]})
        # self.railing = bs.newNode('terrain', attrs={
        #     'collideModel':self.preloadData['railingCollideModel'],
        #     'materials':[bs.getSharedObject('railingMaterial')],
        #     'bumper':True})

        posDict = [{'pos': (-1.5, 3.25, -2.155), 'size': (16, 0.1, 11)},
      
                        #verticales izquierda

        ]
        for a, map in enumerate(posDict):
            self.locs.append(bs.newNode('locator',
                attrs={'shape': 'box',
                       'position': posDict[a]['pos'],
                       'color': (0, 1, 0),
                       'opacity': 5.0,
                       'drawBeauty': True,
                       'size': posDict[a]['size'],
                       'additive': False}))

            self.regions.append(bs.newNode('region',
                attrs={'scale': tuple(posDict[a]['size']),
                       'type': 'box',
                       'materials': [self.collision, bs.getSharedObject('footingMaterial')]}))
            self.locs[-1].connectAttr('position', self.regions[-1], 'position')



        bsGlobals = bs.getSharedObject('globals')
        bsGlobals.tint = (1, 1, 1)
        bsGlobals.ambientColor = (random.uniform(0.3, 3), random.uniform(0.3, 3), random.uniform(0.3, 3))
        bsGlobals.vignetteOuter = (2, 1, 1)
        bsGlobals.vignetteInner = (5.97, 8.95, 6.93)
        bsGlobals.vrCameraOffset = (-1.5, 0, 0)

registerMap(newZizagMap)