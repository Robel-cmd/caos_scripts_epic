# MADED BY FROSHLEE14
from bsMap import *
import bsPowerup
import bsUtils
import bs

class MegaMineDefs:
    boxes = {}
    points = {}
    boxes['areaOfInterestBounds'] = (0, 1, 0) + (0, 0, 0) + (0, 0, 0)
    boxes['levelBounds'] = (0, 0, 0) + (0, 0, 0) + (20, 20, 20)
    points['ffaSpawn1'] = (3,2,-2)
    points['ffaSpawn2'] = (-3,2,-2)
    points['ffaSpawn3'] = (3,2,2)
    points['ffaSpawn4'] = (-3,2,2)
    points['powerupSpawn1'] = (-2.8,3,0)
    points['powerupSpawn2'] = (2.8,3,0)
    points['powerupSpawn3'] = (0,3,-2.8)
    points['powerupSpawn4'] = (0,3,2.8)

class MegaMineMap(Map):
    from NewMaps import MegaMineDefs as defs
    name = 'Mega-mine'
    playTypes = ['melee']

    @classmethod
    def getPreviewTextureName(cls):
        return 'landMine'

    @classmethod
    def onPreload(cls):
        data = {}
        data['model'] = bs.getModel('landMine')
        data['tex'] = bs.getTexture('landMine')
        data['bgModel'] = bs.getModel('thePadBG')
        data['bgTex'] = bs.getTexture('menuBG')
        return data

    def __init__(self):

        Map.__init__(self)
        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={'position':(0,1,0),
                                      'velocity':(0,0,0),
                                      'model':self.preloadData['model'],
                     'size':[25,13,4],
                                      'modelScale':14.6,
                                      'bodyScale':14.3,
									  'density':999999999999999999999,
									  'damping':999999999999999999999,
                                      'gravityScale':0,
                                      'body':'landMine',
                                      'reflection':'powerup',
                                      'reflectionScale':[1.0],									  
                                      'colorTexture':self.preloadData['tex'],
                                      'materials':[bs.getSharedObject('footingMaterial')]})									  
        self.bg = bs.newNode('terrain',
                              attrs={'model':self.preloadData['bgModel'],
                                     'lighting':False,
                                     'background':True,
                                     'colorTexture':self.preloadData['bgTex']})
        bsGlobals = bs.getSharedObject('globals')
        bsGlobals.tint = (1.0,1.0,0.9)
        bsGlobals.ambientColor = (1.1,1.1,1.0)
        bsGlobals.vignetteOuter = (0.7,0.65,0.75)
        bsGlobals.vignetteInner = (0.95,0.95,0.93)
registerMap(MegaMineMap)

class PowerupsDefs:
    boxes = {}
    points = {}
    boxes['areaOfInterestBounds'] = (0, -2, -2) + (0, 0, 0) + (0, 15, 0)
    boxes['levelBounds'] = (0, 1, 0) + (0, -3, 0) + (50, 30, 50)
    points['ffaSpawn1'] = (3,2,-1.5)
    points['ffaSpawn2'] = (-3,2,-1.5)
    points['ffaSpawn3'] = (3,2,1.5)
    points['ffaSpawn4'] = (-3,2,1.5)
    points['powerupSpawn1'] = (-2,3,0)
    points['powerupSpawn2'] = (2,3,0)

class PowerupMap(Map):
    from NewMaps import PowerupsDefs as defs 
    name = 'Powerups'
    playTypes = ['melee']

    @classmethod
    def getPreviewTextureName(cls):
        return 'powerupShield'

    @classmethod
    def onPreload(cls):
        data = {}
        data['bgModel'] = bs.getModel('thePadBG')
        data['bgTex'] = bs.getTexture('menuBG')
        return data

    def __init__(self):
        Map.__init__(self)
        Box(position=(-3,-2,0),texture='powerupShield')	
        Box(position=(3,-2,0),texture='powerupSpeed')	
        Box(position=(-3,-7,0),texture='powerupHealth')	
        Box(position=(3,-7,0),texture='powerupCurse')
        if not bs.getEnvironment()['platform'] == 'android': self._bombUp = bs.Timer(100,bs.WeakCall(self.upB),repeat = True)
        else: self._bombUp = bs.Timer(900,bs.WeakCall(self.upB),repeat = True)
        self.bg = bs.newNode('terrain',
                              attrs={'model':self.preloadData['bgModel'],
                                     'lighting':False,
                                     'background':True,
                                     'colorTexture':self.preloadData['bgTex']})
        bsGlobals = bs.getSharedObject('globals')
        bsGlobals.tint = (1.0,1.0,1.0)
        bsGlobals.ambientColor = (1.1,1.1,1.0)
        bsGlobals.vignetteOuter = (0.7,0.65,0.75)
        bsGlobals.vignetteInner = (0.95,0.95,0.93)
		
    def upB(self):
        pos = (-15+random.random()*30,-10,-15+random.random()*30)
        b = bs.Powerup(position=pos,powerupType=bs.Powerup.getFactory().getRandomPowerupType()).autoRetain()
        b.node.gravityScale = -0.1
registerMap(PowerupMap)

class Box(bs.Actor):
    def __init__(self,position=(0,0,0),texture=None):
        bs.Actor.__init__(self)
        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={'position':position,
                                      'velocity':(0,0,0),
                                      'model':bs.getModel('powerup'),
                                      'modelScale':8.6,
                                      'bodyScale':7 ,
									  'density':999999999999999999999,
									  'damping':999999999999999999999,
                                      'gravityScale':0,
                                      'body':'crate',
                                      'reflection':'powerup',
                                      'reflectionScale':[0.3],									  
                                      'colorTexture':bs.getTexture(texture),
                                      'materials':[bs.getSharedObject('footingMaterial')]})

class DarknessDefs:
    boxes = {}
    points = {}
    boxes['areaOfInterestBounds'] = (0, 1, 0) + (0, 0, 0) + (17, 0, 0)
    boxes['levelBounds'] = (0, 0, 0) + (0, 0, 0) + (10.5, 20, 10.5)
    points['flagDefault'] = (0,1,0)
    points['flag1'] = (-4,1,0)
    points['spawn1'] = (-4,1,0)
    points['flag2'] = (4,1,0)
    points['spawn2'] = (4,1,0)
    points['ffaSpawn1'] = (0,1,2)
    points['ffaSpawn2'] = (0,1,-2)
    points['ffaSpawn3'] = (2,1,0)
    points['ffaSpawn4'] = (-2,1,0)
    points['powerupSpawn1'] = (-3.5,2,-3.5)
    points['powerupSpawn2'] = (-3.4,2,3.5)
    points['powerupSpawn3'] = (3.5,2,-3.5)
    points['powerupSpawn4'] = (3.5,2,3.5)

class Dark(Map):
    from NewMaps import DarknessDefs as defs
    name = 'Dark world'
    playTypes = ['melee','kingOfTheHill','keepAway','teamFlag']

    @classmethod
    def getPreviewTextureName(cls):
        return 'bg'

    @classmethod
    def onPreload(cls):
        data = {}
        data['model'] = bs.getModel('footballStadium')
        data['collideModel'] = bs.getCollideModel('footballStadiumCollide')
        data['tex'] = bs.getTexture('bg')
        return data
    
    def __init__(self):
        Map.__init__(self)		
        self.node = bs.newNode("terrain", delegate=self,
                    attrs={'model':self.preloadData['model'],'collideModel':self.preloadData['collideModel'],
                    'colorTexture':self.preloadData['tex'], 'materials':[bs.getSharedObject('footingMaterial')]})
        self.zone = bs.newNode('locator',attrs={'shape':'circleOutline','position':(0,0,0),
                    'color':(1,1,1),'opacity':1,'drawBeauty':True,'additive':False,'size':[11]})
        bsGlobals = bs.getSharedObject('globals')
        bsGlobals.tint = (0.8,0.8,1)
        bsGlobals.ambientColor = (1.15,1.25,1.6)
        bsGlobals.vignetteOuter = (0.66,0.67,0.73)
        bsGlobals.vignetteInner = (0.93,0.93,0.95)
registerMap(Dark)

class SuperTntMap(Map):
    from NewMaps import PowerupsDefs as defs 
    name = 'Super TNT'
    playTypes = ['melee']

    @classmethod
    def getPreviewTextureName(cls):
        return 'tnt'

    @classmethod
    def onPreload(cls):
        data = {}
        data['bgModel'] = bs.getModel('thePadBG')
        data['bgTex'] = bs.getTexture('menuBG')
        return data

    def __init__(self):
        Map.__init__(self)
        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={'position':(0,-3.2,0),
                                      'velocity':(0,0,0),
                                      'model':bs.getModel('powerupSimple'),
                                      'modelScale':18,
                                      'bodyScale':15,
									  'density':999999999999999999999,
									  'damping':999999999999999999999,
                                      'gravityScale':0,
                                      'body':'crate',
                                      'colorTexture':bs.getTexture('tnt'),
                                      'materials':[bs.getSharedObject('footingMaterial')]})
        
        self.bg = bs.newNode('terrain',
                              attrs={'model':self.preloadData['bgModel'],
                                     'lighting':False,
                                     'background':True,
                                     'colorTexture':self.preloadData['bgTex']})
        bsGlobals = bs.getSharedObject('globals')
        bsGlobals.tint = (1.0,1.0,1.0)
        bsGlobals.ambientColor = (1.1,1.1,1.0)
        bsGlobals.vignetteOuter = (0.7,0.65,0.75)
        bsGlobals.vignetteInner = (0.95,0.95,0.93)
registerMap(SuperTntMap)

class GreenScreenMap(Map):
    import doomShroomLevelDefs as defs
    name = 'Green Screen'
    playTypes = ['melee','keepAway','teamFlag']

    @classmethod
    def getPreviewTextureName(cls):
        return 'eggTex2'

    @classmethod
    def onPreload(cls):
        data = {}
        data['model'] = bs.getModel('doomShroomLevel')
        data['collideModel'] = bs.getCollideModel('doomShroomLevelCollide')
        data['tex'] = bs.getTexture('white')
        data['bgModel'] = bs.getModel('doomShroomBG')
        data['stemModel'] = bs.getModel('doomShroomStem')
        data['collideBG'] = bs.getCollideModel('doomShroomStemCollide')
        return data
    
    def __init__(self):
        Map.__init__(self)
        self.node = bs.newNode('terrain',
                               delegate=self,
                               attrs={'collideModel':self.preloadData['collideModel'],
                                      'model':self.preloadData['model'],'color':(0,1,0),
                                      'colorTexture':self.preloadData['tex'],
                                      'materials':[bs.getSharedObject('footingMaterial')]})
        self.foo = bs.newNode('terrain',
                              attrs={'model':self.preloadData['bgModel'],
                                     'lighting':False,
                                     'background':True,'color':(0,1,0),
                                     'colorTexture':self.preloadData['tex']})
        self.stem = bs.newNode('terrain',
                               attrs={'model':self.preloadData['stemModel'],
                                      'lighting':False,'color':(0,1,0),
                                      'colorTexture':self.preloadData['tex']})
        self.bgCollide = bs.newNode('terrain',
                                    attrs={'collideModel':self.preloadData['collideBG'],
                                           'materials':[bs.getSharedObject('footingMaterial'),bs.getSharedObject('deathMaterial')]})
        bsGlobals = bs.getSharedObject('globals')
        bsGlobals.tint = (0.82,1.10,1.15)
        bsGlobals.ambientColor = (0.9,1.3,1.1)
        bsGlobals.shadowOrtho = False
        bsGlobals.vignetteOuter = (0.76,0.76,0.76)
        bsGlobals.vignetteInner = (0.95,0.95,0.99)
registerMap(GreenScreenMap)