# -*- coding: utf-8 -*-

import bs
import random
from bsBomb import Blast, Bomb, BombFactory, ExplodeHitMessage
from bsSpaz import _BombDiedMessage
from bsScoreBoard import ScoreBoard
from bsDeathMatch import DeathMatchGame
from bsPowerup import _TouchedMessage
import bsSpaz
import bsUtils


def bsGetAPIVersion():
	# see bombsquadgame.com/apichanges
	return 4

def bsGetGames():
	return [IceDeathMatchGame]


class Blast(bs.Actor):

	def __init__(self, position=(0,1,0), velocity=(0,0,0), blastRadius=2.0,
				blastType="normal", sourcePlayer=None, hitType='explosion',
				hitSubType='normal'):
		"""
		Instantiate with given values.
		"""
		bs.Actor.__init__(self)
		
		factory = Bomb.getFactory()

		self.blastType = blastType
		self.sourcePlayer = sourcePlayer

		self.hitType = hitType
		self.hitSubType = hitSubType

		# blast radius
		self.radius = blastRadius

		# set our position a bit lower so we throw more things upward
		self.node = bs.newNode('region', delegate=self, attrs={
			'position':(position[0], position[1]-0.1, position[2]),
			'scale':(self.radius,self.radius,self.radius),
			'type':'sphere',
			'materials':(factory.blastMaterial,
						 bs.getSharedObject('attackMaterial'))})

		bs.gameTimer(50, self.node.delete)

		# throw in an explosion and flash
		# explosion = bs.newNode("explosion", attrs={
		# 	'position':position,
		# 	'velocity':(velocity[0],max(-1.0,velocity[1]),velocity[2]),
		# 	'radius':self.radius,
		# 	'big':(self.blastType == 'tnt')})
		# if self.blastType == "ice":
		# 	explosion.color = (0, 0.05, 0.4)

		# bs.gameTimer(1000,explosion.delete)

		if self.blastType != 'ice':
			bs.emitBGDynamics(position=position, velocity=velocity,
							  count=int(1.0+random.random()*4),
							  emitType='tendrils',tendrilType='thinSmoke')
		bs.emitBGDynamics(
			position=position, velocity=velocity,
			count=int(4.0+random.random()*4), emitType='tendrils',
			tendrilType='ice' if self.blastType == 'ice' else 'smoke')
		bs.emitBGDynamics(
			position=position, emitType='distortion',
			spread=1.0 if self.blastType == 'tnt' else 2.0)
		
		# and emit some shrapnel..
		if self.blastType == 'ice':
			def _doEmit():
				bs.emitBGDynamics(position=position, velocity=velocity,
								  count=30, spread=2.0, scale=0.4,
								  chunkType='ice', emitType='stickers')
			bs.gameTimer(50, _doEmit) # looks better if we delay a bit

		elif self.blastType == 'sticky':
			def _doEmit():
				bs.emitBGDynamics(position=position, velocity=velocity,
								  count=int(4.0+random.random()*8),
								  spread=0.7,chunkType='slime')
				bs.emitBGDynamics(position=position, velocity=velocity,
								  count=int(4.0+random.random()*8), scale=0.5,
								  spread=0.7,chunkType='slime')
				bs.emitBGDynamics(position=position, velocity=velocity,
								  count=15, scale=0.6, chunkType='slime',
								  emitType='stickers')
				bs.emitBGDynamics(position=position, velocity=velocity,
								  count=20, scale=0.7, chunkType='spark',
								  emitType='stickers')
				bs.emitBGDynamics(position=position, velocity=velocity,
								  count=int(6.0+random.random()*12),
								  scale=0.8, spread=1.5,chunkType='spark')
			bs.gameTimer(50,_doEmit) # looks better if we delay a bit

		elif self.blastType == 'impact': # regular bomb shrapnel
			def _doEmit():
				bs.emitBGDynamics(position=position, velocity=velocity,
								  count=int(4.0+random.random()*8), scale=0.8,
								  chunkType='metal')
				bs.emitBGDynamics(position=position, velocity=velocity,
								  count=int(4.0+random.random()*8), scale=0.4,
								  chunkType='metal')
				bs.emitBGDynamics(position=position, velocity=velocity,
								  count=20, scale=0.7, chunkType='spark',
								  emitType='stickers')
				bs.emitBGDynamics(position=position, velocity=velocity,
								  count=int(8.0+random.random()*15), scale=0.8,
								  spread=1.5, chunkType='spark')
			bs.gameTimer(50,_doEmit) # looks better if we delay a bit

		else: # regular or land mine bomb shrapnel
			def _doEmit():
				if self.blastType != 'tnt':
					bs.emitBGDynamics(position=position, velocity=velocity,
									  count=int(4.0+random.random()*8),
									  chunkType='rock')
					bs.emitBGDynamics(position=position, velocity=velocity,
									  count=int(4.0+random.random()*8),
									  scale=0.5,chunkType='rock')
				bs.emitBGDynamics(position=position, velocity=velocity,
								  count=30,
								  scale=1.0 if self.blastType=='tnt' else 0.7,
								  chunkType='spark', emitType='stickers')
				bs.emitBGDynamics(position=position, velocity=velocity,
								  count=int(18.0+random.random()*20),
								  scale=1.0 if self.blastType == 'tnt' else 0.8,
								  spread=1.5, chunkType='spark')

				# tnt throws splintery chunks
				if self.blastType == 'tnt':
					def _emitSplinters():
						bs.emitBGDynamics(position=position, velocity=velocity,
										  count=int(20.0+random.random()*25),
										  scale=0.8, spread=1.0,
										  chunkType='splinter')
					bs.gameTimer(10,_emitSplinters)
				
				# every now and then do a sparky one
				if self.blastType == 'tnt' or random.random() < 0.1:
					def _emitExtraSparks():
						bs.emitBGDynamics(position=position, velocity=velocity,
										  count=int(10.0+random.random()*20),
										  scale=0.8, spread=1.5,
										  chunkType='spark')
					bs.gameTimer(20,_emitExtraSparks)
						
			bs.gameTimer(50,_doEmit) # looks better if we delay a bit

		light = bs.newNode('light', attrs={
			'position':position,
			'volumeIntensityScale': 10.0,
			'color': (0.6, 0.6, 1.0)})

		s = random.uniform(0.6,0.9)
		scorchRadius = lightRadius = self.radius
		if self.blastType == 'tnt':
			lightRadius *= 1.4
			scorchRadius *= 1.15
			s *= 3.0

		iScale = 1.6
		bsUtils.animate(light,"intensity", {
			0:2.0*iScale, int(s*20):0.1*iScale,
			int(s*25):0.2*iScale, int(s*50):17.0*iScale, int(s*60):5.0*iScale,
			int(s*80):4.0*iScale, int(s*200):0.6*iScale,
			int(s*2000):0.00*iScale, int(s*3000):0.0})
		bsUtils.animate(light,"radius", {
			0:lightRadius*0.2, int(s*50):lightRadius*0.55,
			int(s*100):lightRadius*0.3, int(s*300):lightRadius*0.15,
			int(s*1000):lightRadius*0.05})
		bs.gameTimer(int(s*3000),light.delete)

		# make a scorch that fades over time
		scorch = bs.newNode('scorch', attrs={
			'position':position,
			'size':scorchRadius*0.5,
			'big':(self.blastType == 'tnt')})
		scorch.color = (1,1,1.5)

		bsUtils.animate(scorch,"presence",{3000:1, 13000:0})
		bs.gameTimer(13000,scorch.delete)

		bs.playSound(factory.hissSound, 0.8, position=light.position)
			
		p = light.position
		# bs.playSound(factory.getRandomExplodeSound(),position=p)
		# bs.playSound(factory.debrisFallSound,position=p)

		bs.shakeCamera(intensity=5.0 if self.blastType == 'tnt' else 1.0)

		# tnt is more epic..
		if self.blastType == 'tnt':
			bs.playSound(factory.getRandomExplodeSound(),position=p)
			def _extraBoom():
				bs.playSound(factory.getRandomExplodeSound(),position=p)
			bs.gameTimer(250,_extraBoom)
			def _extraDebrisSound():
				bs.playSound(factory.debrisFallSound,position=p)
				bs.playSound(factory.woodDebrisFallSound,position=p)
			bs.gameTimer(400,_extraDebrisSound)

	def handleMessage(self, msg):
		self._handleMessageSanityCheck()
		
		if isinstance(msg, bs.DieMessage):
			self.node.delete()

		elif isinstance(msg, ExplodeHitMessage):
			node = bs.getCollisionInfo("opposingNode")
			if node is not None and node.exists():
				t = self.node.position

				# new
				mag = 1000.0
				if self.blastType == 'ice': mag *= 1.0
				elif self.blastType == 'landMine': mag *= 2.5
				elif self.blastType == 'tnt': mag *= 2.0

				node.handleMessage(bs.HitMessage(
					pos=t,
					velocity=(0,0,0),
					magnitude=mag,
					hitType=self.hitType,
					hitSubType=self.hitSubType,
					radius=self.radius,
					sourcePlayer=self.sourcePlayer))
				bs.playSound(Bomb.getFactory().freezeSound, 1, position=t)
				node.handleMessage(bs.FreezeMessage())

		else:
			bs.Actor.handleMessage(self, msg)


class Bomb(Bomb):

	def explode(self):
		if self._exploded: return
		self._exploded = True
		activity = self.getActivity()
		if activity is not None and self.node.exists():
			blast = Blast(
				position=self.node.position,
				velocity=self.node.velocity,
				blastRadius=self.blastRadius,
				blastType=self.bombType,
				sourcePlayer=self.sourcePlayer,
				hitType=self.hitType,
				hitSubType=self.hitSubType).autoRetain()
			for c in self._explodeCallbacks: c(self,blast)
			
		# we blew up so we need to go away
		bs.gameTimer(1, bs.WeakCall(self.handleMessage, bs.DieMessage()))


class Power(bs.Actor):

	def __init__(
		self,
		position = (0.0, 1.0, 0.0),
		velocity = (0.0, 0.0, 0.0),
		max_position = 1.0,
		modelScale = 1.0,
	):
		bs.Actor.__init__(self)
		self._time = 0
		self._max_position = max_position
		self._circle_gameTimer = None
		self.model_index = 0
		self._touched = False
		self._position = position
		self._modelScale = modelScale
		no_collision = bs.Material()
		no_collision.addActions(
			actions=(
				('modifyPartCollision', 'collide', False),
				('modifyPartCollision', 'physical', False),
			)
		)
		no_collision.addActions(
			conditions=('theyHaveMaterial', bs.getSharedObject('playerMaterial')),
			actions=(
				('modifyPartCollision', 'collide', True),
				('modifyPartCollision', 'physical', False),
				('message', 'ourNode', 'atConnect', _TouchedMessage())
			)
		)
		self.node = bs.newNode(
			'prop',
			delegate=self,
			attrs={
				'position': position,
				'velocity': velocity,
				'model': bs.getModel('flash'),
				'colorTexture': bs.getTexture('tipTopBGColor'),
				'body': 'sphere',
				'bodyScale': 1.0,
				'modelScale': modelScale,
				'shadowSize': 0.0,
				'gravityScale': 0,
				'reflection': 'powerup',
				'reflectionScale': [5.0],
				'materials': [no_collision],
			},
		)
		self.circle = bs.newNode(
			'locator',
			owner=self.node,
			attrs={
				'shape': 'circleOutline',
				'position': position,
				'color': (0, 0.9, 1),
				'opacity': 0.0,
				'drawBeauty': False,
				'additive': True,
			},
		)
		self.circle2 = bs.newNode(
			'locator',
			owner=self.node,
			attrs={
				'shape': 'circleOutline',
				'position': position,
				'color': (0, 0.9, 1),
				'opacity': 0.0,
				'drawBeauty': False,
				'additive': True,
			},
		)
		self.light = bs.newNode(
			'light',
			owner=self.node,
			attrs={
				'volumeIntensityScale': 10.0,
				'color': (0.6, 0.6, 1.0),
				'intensity': 0.0,
				'radius': 0.0,
			},
		)
		self._update()

	def _update(self):
		self.update_time()
		self._circle_gameTimer = bs.Timer(
			1000, self.update_time, repeat=True)
		self.circle_animation()
		bs.gameTimer(800, self.do_sound, repeat=True)
		bsUtils.animateArray(self.node, 'position', 3, {
			0.0: (
				self._position[0],
				self._position[1] + self._max_position,
				self._position[2],
			),
			7000: (
				self._position[0],
				self._position[1] + 0.6,
				self._position[2],
			),
		})
		bs.gameTimer(7000, self.model_position)
		self.change_model()
		bs.gameTimer(800, self.change_model, repeat=True)
		# bs.gameTimer(0.1 * 1000, self.efx, repeat=True)

	def update_time(self):
		self._time += 1
		if self._time > 7:
			self._circle_gameTimer = None

	def circle_animation(self):
		self.animate_circle()
		bs.gameTimer(1300, self.animate_circle2)
		bs.gameTimer(2600, self.animate_circle, repeat=True)
		bs.gameTimer(1300, lambda: bs.gameTimer(
			2600, self.animate_circle2, repeat=True))

	def animate_circle(self):
		if not self.node.exists():
			return
		bsUtils.animateArray(self.circle, 'size', 1, {
			0.0: [0.0],
			2600: [1.5],
		})
		bsUtils.animate(self.circle, 'opacity', {
			0.0: 0.0,
			200: (0.5 * self._time) / 7,
			1800: (0.5 * self._time) / 7,
			2600: 0.0,
		})

	def animate_circle2(self):
		if not self.node.exists():
			return
		bsUtils.animateArray(self.circle2, 'size', 1, {
			0.0: [0.0],
			2600: [1.5],
		})
		bsUtils.animate(self.circle2, 'opacity', {
			0.0: 0.0,
			200: (0.5 * self._time) / 7,
			1800: (0.5 * self._time) / 7,
			2600: 0.0,
		})

	def do_sound(self):
		if not self.node.exists():
			return
		sound = bs.getSound('sparkle02')
		bs.playSound(sound, 0.2, position=self.node.position)
		
	# def efx(self):
	# 	if not self.node.exists():
	# 		return
	# 	bs.emitfx(
	# 		position=self.node.position,
	# 		emit_type='fairydust',
	# 	)
		
	def model_position(self):
		if not self.node.exists():
			return
		bsUtils.animateArray(self.node, 'position', 3, {
			0.0: (
				self._position[0],
				self._position[1] + 0.6,
				self._position[2],
			),
			150: (
				self._position[0],
				self._position[1] + 0.55,
				self._position[2],
			),
			400: (
				self._position[0],
				self._position[1] + 0.5,
				self._position[2],
			),
			650: (
				self._position[0],
				self._position[1] + 0.55,
				self._position[2],
			),
			800: (
				self._position[0],
				self._position[1] + 0.6,
				self._position[2],
			),
			950: (
				self._position[0],
				self._position[1] + 0.65,
				self._position[2],
			),
			1200: (
				self._position[0],
				self._position[1] + 0.7,
				self._position[2],
			),
			1450: (
				self._position[0],
				self._position[1] + 0.65,
				self._position[2],
			),
			1600: (
				self._position[0],
				self._position[1] + 0.6,
				self._position[2],
			),
		}, loop=True)
		
	def change_model(self):
		if not self.node.exists():
			return
		if self.model_index == 0:
			self.node.model = bs.getModel('flash')
			scale = 0.9 * self._modelScale
		elif self.model_index == 1:
			self.node.model = bs.getModel('box')
			scale = 1.0 * self._modelScale
		elif self.model_index == 2:
			self.node.model = bs.getModel('frostyPelvis')
			scale = 2.0 * self._modelScale
		bsUtils.animate(self.node, 'modelScale', {
			0.0: 0,
			100: scale,
			700: scale,
			800: 0.0,
		})
		self.model_index += 1
		if self.model_index > 2:
			self.model_index = 0
	
	def do_flash(self):
		bsUtils.animate(self.light, 'intensity', {
			0.0: 0.0,
			100: 0.5,
			200: 0.0,
		})
		bsUtils.animate(self.light, 'radius', {
			0.0: 0.0,
			100: 0.2,
			200: 0.0,
		})

	def handleMessage(self, msg):
		if isinstance(msg, bs.OutOfBoundsMessage):
			if not self.node.exists():
				return
			self.node.delete()
		elif isinstance(msg, bs.DieMessage):
			if self.node:
				if msg.immediate:
					self.node.delete()
				else:
					bsUtils.animate(self.node, 'modelScale', {0: 1, 100: 0})
					bs.gameTimer(100, self.node.delete)
		elif isinstance(msg, _TouchedMessage):
			if self._touched:
				return
			self._touched = True
			node = bs.getCollisionInfo("opposingNode")
			node.handleMessage(
				bs.PowerupMessage('super_ice')
			)
			sound = bs.getSound('sparkle03')
			bs.playSound(sound, 0.5, position=self.node.position)
			bs.getActivity()._update_power()
			self.handleMessage(bs.DieMessage())
		else:
			bs.Actor.handleMessage(self, msg)


class PlayerSpaz(bsSpaz.PlayerSpaz):

	def __init__(self, **kwargs):
		bsSpaz.PlayerSpaz.__init__(self, **kwargs)
		self._ice_power = False
		self._ice_power_gameTimer = None
		# self._ice_power_efx_gameTimer = None
		self._ice_power_flash_gameTimer = None
		self._ice_power_wear_gameTimer = None
		self._old_impact_scale = None
		self._old_color = None
		self._old_highlight = None
		self._old_colorTexture = None
		self._old_color_mask_texture = None
		self._hockey_material = bs.Material()
		self._hockey_material.addActions(
			actions=('modifyPartCollision', 'friction', 500),
		)
		self._ice_light = bs.newNode(
			'light',
			owner=self.node,
			attrs={
				'volumeIntensityScale': 10.0,
				'color': (0.6, 0.6, 1.0),
				'intensity': 0.0,
				'radius': 0.0,
			},
		)
		self.node.connectAttr('position', self._ice_light, 'position')

	def dropBomb(self):
		if (self.landMineCount <= 0 and self.bombCount <= 0) or self.frozen:
			return
		p = self.node.positionForward
		v = self.node.velocity

		if self.landMineCount > 0:
			droppingBomb = False
			self.setLandMineCount(self.landMineCount-1)
			bombType = 'landMine'
		else:
			droppingBomb = True
			bombType = self.bombType

		bomb = Bomb(position=(p[0], p[1] - 0.0, p[2]),
					   velocity=(v[0], v[1], v[2]),
					   bombType=bombType,
					   blastRadius=self.blastRadius,
					   sourcePlayer=self.sourcePlayer,
					   owner=self.node).autoRetain()

		if droppingBomb:
			self.bombCount -= 1
			bomb.node.addDeathAction(bs.WeakCall(self.handleMessage,
												 _BombDiedMessage()))
		self._pickUp(bomb.node)

		for c in self._droppedBombCallbacks: c(self, bomb)
		
		return bomb
	
	# def _ice_power_efx(self):
	# 	if not self.node.exists():
	# 		return
	# 	bs.emitfx(
	# 		position=self.node.position,
	# 		emit_type='fairydust',
	# 	)

	def _equip_ice_power(self):
		if not self.node.exists():
			return
		self.handleMessage(bs.ThawMessage())
		self.handleMessage(bs.PowerupMessage('health'))
		self._old_impact_scale = self._impactScale
		self._old_color = self.node.color
		self._old_highlight = self.node.highlight
		self._old_colorTexture = self.node.colorTexture
		self._old_color_mask_texture = self.node.colorMaskTexture
		self._ice_power_wear_custom()
		self._impactScale = 0.2
		self.node.hockey = True
		self._ice_power = True
		self.node.rollerMaterials += (self._hockey_material, )
		# self._ice_power_efx_gameTimer = bs.Timer(
		# 	0.1 * 1000, self._ice_power_efx, repeat=True)
		bsUtils.animate(self._ice_light, 'intensity', {
			0.0: 0.0,
			100: 0.5,
			200: 0.4,
		})
		bsUtils.animate(self._ice_light, 'radius', {
			0.0: 0.0,
			100: 0.2,
			200: 0.15,
		})
		bs.playSound(bs.getSound('powerup01'), 3, position=self.node.position)

	def _ice_power_wear_default(self):
		if not self.node.exists():
			return
		self.node.color = self._old_color
		self.node.highlight = self._old_highlight
		self.node.colorTexture = self._old_colorTexture
		self.node.colorMaskTexture = self._old_color_mask_texture

	def _ice_power_wear_custom(self):
		if not self.node.exists():
			return
		self.node.color = self.node.highlight = (0.5, 1.5, 1.5)
		self.node.colorTexture = bs.getTexture('flagColor')
		self.node.colorMaskTexture = bs.getTexture('aliColorMask')
		
	def _ice_power_wear_off_flash(self):
		if not self.node.exists():
			return
		self._ice_power_flash_gameTimer = None
		self.custom = True
		def flash():
			if self.custom:
				self._ice_power_wear_default()
				self.custom = False
			else:
				self._ice_power_wear_custom()
				self.custom = True
		self._ice_power_wear_gameTimer = bs.Timer(
			50, flash, repeat=True)

	def _ice_power_wear_off(self):
		if not self.node.exists():
			return
		bs.playSound(bs.getSound('powerdown01'), position=self.node.position)
		self._impactScale = self._old_impact_scale
		self._ice_power = False
		self._ice_power_gameTimer = None
		# self._ice_power_efx_gameTimer = None
		self._ice_power_wear_gameTimer = None
		self._ice_power_wear_default()
		self.node.hockey = False
		rollerMaterials = list(self.node.rollerMaterials)
		rollerMaterials.remove(self._hockey_material)
		self.node.rollerMaterials = tuple(rollerMaterials)
		bsUtils.animate(self._ice_light, 'intensity', {
			0.0: 0.4,
			100: 0.5,
			200: 0.0,
		})
		bsUtils.animate(self._ice_light, 'radius', {
			0.0: 0.15,
			100: 0.2,
			200: 0.0,
		})

	def handleMessage(self, msg):
		if isinstance(msg, bs.FreezeMessage):
			if not self.node.exists(): return
			if self.node.invincible == True:
				bs.playSound(self.getFactory().blockSound, 1.0,
							 position=self.node.position)
				return
			if self.shield is not None: return
			if not self.frozen:
				self.frozen = True
				self.node.frozen = 1
				bs.gameTimer(int(bs.getActivity()._freezing_time * 1000),
				 	bs.WeakCall(self.handleMessage, bs.ThawMessage()))
				# instantly shatter if we're already dead
				# (otherwise its hard to tell we're dead)
				if self.hitPoints <= 0:
					self.shatter()
		elif isinstance(msg, bs.PowerupMessage):
			if self._dead or not self.node.exists():
				return True
			if msg.powerupType == 'super_ice':
				if not self._ice_power:
					self._equip_ice_power()
				self._ice_power_wear_gameTimer = None
				self._ice_power_wear_custom()
				self._ice_power_flash_gameTimer = bs.Timer(
					int((bs.getActivity()._ice_power_time - 1.5) * 1000), self._ice_power_wear_off_flash)
				self._ice_power_gameTimer = bs.Timer(
					int(bs.getActivity()._ice_power_time * 1000), self._ice_power_wear_off)
			else:
				bsSpaz.PlayerSpaz.handleMessage(self, msg)
		else:
			return bsSpaz.PlayerSpaz.handleMessage(self, msg)
		return None


class IceDeathMatchGame(DeathMatchGame):

	@classmethod
	def getName(cls):
		return 'Ice Death Match'
	
	@classmethod
	def getDescription(cls, sessionType):
		return (
			'Mata a un número de enemigos.\n'
			'Todas las bombas son de hielo.\n'
			'Cada cierto tiempo aparece un poder.\n'
			'El poder contiene lo siguiente:\n'
			'+ Inmunidad a la Congelación\n'
			'+ Súper Velocidad\n'
			'+ Curación Total\n'
			'+ Reducción de Daño'
		)

	@classmethod
	def getSettings(cls, sessionType):
		settings = [
			("Kills to Win Per Player",
			 {'minValue': 1, 'default': 5, 'increment': 1}),
			("Tiempo De Congelación",
			 {'minValue': 1, 'default': 5, 'increment': 1}),
			("Tiempo De Poder De Hielo",
			 {'minValue': 1, 'default': 10, 'increment': 1}),
			("Tiempo para Aparecer Poder",
			 {'minValue': 1, 'default': 10, 'increment': 1}),
			("Time Limit",
			 {
				 'choices':
				 [('None', 0),
				  ('1 Minute', 60),
					 ('2 Minutes', 120),
					 ('5 Minutes', 300),
					 ('10 Minutes', 600),
					 ('20 Minutes', 1200)],
				 'default': 0}),
			("Respawn Times",
			 {
				 'choices':
				 [('Shorter', 0.25),
				  ('Short', 0.5),
					 ('Normal', 1.0),
					 ('Long', 2.0),
					 ('Longer', 4.0)],
				 'default': 1.0}),
			("Habilitar Agarrar", {'default': False}),
			("Habilitar Golpear", {'default': False}),
			("Habilitar Potenciadores", {'default': False}),
			("Epic Mode", {'default': False})
		]

		if issubclass(sessionType, bs.FreeForAllSession):
			settings.append(("Allow Negative Scores", {'default': False}))

		return settings

	def __init__(self, settings):
		DeathMatchGame.__init__(self, settings)
		self._freezing_time = settings['Tiempo De Congelación']
		self._ice_power_time = settings['Tiempo De Poder De Hielo']
		self._power = None
		self._power_gameTimer = None
		self._power_position = (0.0, 0.0, 0.0)
		self._max_power_position = 7

	def onTransitionIn(self):
		DeathMatchGame.onTransitionIn(self)
		gnode = bs.getSharedObject('globals')
		gnode.tint = (1.0, 1.1, 1.3)
		gnode.ambientColor = (0.8, 1.2, 1.4)
		if self.getMap().getName() == 'Hockey Stadium':
			pos = (-0.0190422218, 0.10072644352, -0.109683029)
			self._max_power_position = 6
		elif self.getMap().getName() == 'Football Stadium':
			pos = (-0.1001374046, 0.04180340146, 0.1095578275)
		elif self.getMap().getName() == 'Bridgit':
			pos = (-0.5227795102, 3.802429326, -1.562586233)
		elif self.getMap().getName() == 'Big G':
			pos = (-7.563673017, 2.890652319, 0.08844978098)
		elif self.getMap().getName() == 'Roundabout':
			pos = (-1.548755407, 1.528324294, -1.1124807596)
		elif self.getMap().getName() == 'Monkey Face':
			pos = (-1.74430215358, 3.38925557136, -2.15618395805)
		elif self.getMap().getName() == 'Zigzag':
			pos = (-1.50993382930, 3.05306534767, -0.01529514975)
		elif self.getMap().getName() == 'The Pad':
			pos = (0.442086964845, 3.33380131721, -2.85514187812)
		elif self.getMap().getName() == 'Doom Shroom':
			pos = (0.729165613651, 2.30488162040, -4.04898214340)
			self._max_power_position = 6
		elif self.getMap().getName() == 'Lake Frigid':
			pos = (0.681899964809, 2.55772190093, 1.383500933647)
		elif self.getMap().getName() == 'Tip Top':
			pos = (0.057506140321, 8.90296630859, -4.632864952087)
			self._max_power_position = 5
		elif self.getMap().getName() == 'Crag Castle':
			pos = (0.608665583133, 6.24972562789, -0.126513488888)
		elif self.getMap().getName() == 'Tower D':
			pos = (-0.01690735171, 0.06139940044, -0.07659307272)
		elif self.getMap().getName() == 'Happy Thoughts':
			pos = (0.099852778017, 12.7525241851, -5.50424814224)
		elif self.getMap().getName() == 'Step Right Up':
			pos = (0.194533213973, 4.11249904632, -2.97467184066)
		elif self.getMap().getName() == 'Courtyard':
			pos = (0.038726758, 2.89662661, -2.19155263)
		elif self.getMap().getName() == 'Rampage':
			pos = (0.278286784887, 5.13772945404, -4.28152322769)
			self._max_power_position = 6
		else:
			pos = (0, 0, 0)
		self._power_position = pos

	def onBegin(self):
		bs.TeamGameActivity.onBegin(self)
		self.setupStandardTimeLimit(self.settings['Time Limit'])
		self._update_power()
		if self.settings['Habilitar Potenciadores']:
			self.setupStandardPowerupDrops()
		if len(self.teams) > 0:
			self._scoreToWin = self.settings['Kills to Win Per Player'] * max(
				1, max(len(t.players) for t in self.teams))
		else:
			self._scoreToWin = self.settings['Kills to Win Per Player']
		self._updateScoreBoard()
		self._dingSound = bs.getSound('dingSmall')

	def _update_power(self):
		self._power = None
		self._power_gameTimer = bs.Timer(
			int(self.settings['Tiempo para Aparecer Poder'] * 1000), self._spawn_power)

	def _spawn_power(self):
		if self._power is not None or self._power:
			return
		
		self._power = Power(
			position=self._power_position,
			max_position=self._max_power_position,
			modelScale=0.5,
		).autoRetain()

	def spawnPlayerSpaz(
		self,
		player,
		position = (0, 0, 0),
		angle = None,
	):
		if isinstance(self.getSession(), bs.TeamsSession):
			position = self.getMap().getStartPosition(player.getTeam().getID())
		else:
			position = self.getMap().getFFAStartPosition(self.players)

		name = player.getName()
		color = player.color
		highlight = player.highlight

		lightColor = bsUtils.getNormalizedColor(color)
		displayColor = bs.getSafeColor(color, targetIntensity=0.75)
		spaz = PlayerSpaz(color=color,
							 highlight=highlight,
							 character=player.character,
							 player=player)
		player.setActor(spaz)

		spaz.node.name = name
		spaz.node.nameColor = displayColor
		spaz.connectControlsToPlayer(
			enablePickUp=self.settings['Habilitar Agarrar'],
			enablePunch=self.settings['Habilitar Golpear']
		)
		self.scoreSet.playerGotNewSpaz(player, spaz)

		# move to the stand position and add a flash of light
		spaz.handleMessage(
			bs.StandMessage(
				position, angle
				if angle is not None else random.uniform(0, 360)))
		t = bs.getGameTime()
		bs.playSound(self._spawnSound, 1, position=spaz.node.position)
		light = bs.newNode('light', attrs={'color': lightColor})
		spaz.node.connectAttr('position', light, 'position')
		bsUtils.animate(light, 'intensity', {0: 0, 250: 1, 500: 0})
		bs.gameTimer(500, light.delete)

		spaz.bombType = 'ice'

		return spaz