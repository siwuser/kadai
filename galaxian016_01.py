import pyxel
import random

SIZE_X, SIZE_Y = (80, 40)
OUTER_SIZE = (255,  SIZE_Y*5)
INNER_SIZE = (SIZE_X*2, SIZE_Y*5)
BEGIN_X = int((OUTER_SIZE[0] - INNER_SIZE[0]) / 2)
MAX_X = SIZE_X - 1
MIN_X = 0

class Explosion:

	def __init__(self):
		self.underExplosion = []
		
	def start(self, pos):
		self.underExplosion.append([10, *pos])
		
	def start2(self, pos):
		self.underExplosion.append([10, *pos])
		self.underExplosion.append([10, pos[0], pos[1]-1])
		
	def move(self):
		for i in range(len(self.underExplosion)-1, -1, -1):
			t, x, y = self.underExplosion[i]
			if t == 1:
				self.underExplosion.pop(i)
			else:
				self.underExplosion[i][0] -= 1
				
	def draw(self):
		for exp in self.underExplosion:
			pyxel.blt(
				exp[1] * 2 + BEGIN_X, exp[2] * 5,
				0,
				(exp[0]-int(exp[0]/2)*2+11) * 10, 0,
				10, 4
			)

class Beam:

	def __init__(self):
		self.x = 0
		self.y = 0
		self.speed = 3
		self.init()
		
	def init(self):
		self.shot = False
		
	def set(self, x, y):
		self.x = x
		self.y = y
		self.shot = True
		
	def pos(self):
		return (self.x, self.y)
		
	def move(self):
		if not self.underShot():
			return
		
		self.y -= self.speed
		if self.y <= 0:
			self.shot = False
			
	def underShot(self):
		return self.shot
		
	def draw(self):
		if not self.underShot():
			return

		pyxel.rectb(
			self.x * 2 + BEGIN_X, self.y * 5,
			2, 4, 9
		)		

class Ship:

	def __init__(self, beam):
		self.beam = beam
		self.y = SIZE_Y - 3
		self.init()
		
	def init(self):
		self.count = 4
		self.x = int((MAX_X+MIN_X)/2)
		
	def pos(self):
		return (self.x, self.y)
		
	def dec(self):
		if self.count > 0:
			self.count -= 1
			
	def left(self):
		return self.count
		
	def move(self):
		new_x = (pyxel.mouse_x - BEGIN_X) / 2
		self.x = max(MIN_X, min(new_x, MAX_X - 4))

		if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and not self.beam.underShot():
			self.beam.set(self.x+2, self.y-1)
			
	def draw(self):
		pyxel.blt(
			self.x * 2 + BEGIN_X, self.y * 5,
			0,
			13 * 10, 0,
			10, 4
		)
		if not self.beam.underShot():
			pyxel.rectb(
				(self.x+2)*2 + BEGIN_X, (self.y-1)*5,
				2, 4, 9
			)

class Missile:
	def __init__(self):
		self.init()
		
	def init(self):
		self.missiles = []
		
	def set(self, x, y):
		if y < 4 or y > int(SIZE_Y * .7):
			return
		if random.randint(1, 10) != 1:
			return
		if len(self.missiles) == 10:
			return
		self.missiles.append([x, y])
		
	def hitShip(self, pos):
		ship_x, ship_y = pos
		for i in range(len(self.missiles)-1, -1, -1):
			if ship_x <= self.missiles[i][0] <= ship_x + 4 and \
			   self.missiles[i][1] == ship_y:
				self.missiles.pop(i)
				return True
		return False
		
	def move(self):
		if pyxel.frame_count % 2 != 0:
			return
		for i in range(len(self.missiles)-1, -1, -1):
			if self.missiles[i][1] + 1 > SIZE_Y:
				self.missiles.pop(i)
			else:
				self.missiles[i][1] += 1
				
	def draw(self):
		for missile in self.missiles:
			pyxel.rectb(
				missile[0]*2 + BEGIN_X, missile[1]*5, 
				2, 4, 10
			)

class Alian:

	alian_data = [
		( 1, 59, 5,  3), ( 1, 19, 5, -3), ( 4, 54, 4,  3), ( 4, 24, 4, -3),
		( 1, 59, 6,  3), ( 1, 19, 6, -3), ( 2, 54, 5,  3), ( 2, 24, 5, -3),
		( 1, 59, 7,  3), ( 1, 19, 7, -3), ( 2, 54, 6,  3), ( 2, 24, 6, -3),
		( 2, 54, 7,  3), ( 2, 24, 7, -3), ( 3, 49, 4,  3), ( 3, 29, 4, -3),
		( 1, 49, 5,  3), ( 1, 29, 5, -3), ( 1, 49, 6,  3), ( 1, 29, 6, -3),
		( 1, 49, 7,  3), ( 1, 29, 7, -3), ( 4, 44, 4,  3), ( 4, 34, 4, -3),
		( 3, 39, 4,  3), ( 2, 44, 5,  3), ( 1, 39, 5, -3), ( 2, 34, 5, -3),
		( 2, 34, 6, -3), ( 1, 39, 6,  3), ( 2, 44, 6,  3), ( 2, 44, 7,  3),
		( 1, 39, 7, -3), ( 2, 34, 7, -3), ( 5, 29, 3, -3), ( 6, 34, 3, -3),
		( 5, 39, 3, -3), ( 6, 44, 3,  3), ( 5, 49, 3,  3), ( 7, 34, 2, -3),
		( 7, 44, 2,  3),
	]
	
	def __init__(self, missile):
		self.num_of_alians = len(Alian.alian_data)
		self.missile = missile
		self.clock = 0
		self.init()
		
	def init(self):
		self.alians = []
		self.count = self.num_of_alians
		for adata in Alian.alian_data:
			self.alians.append({
				"alive": True, "type":	adata[0], "x":	adata[1],
				"y":	adata[2], "dir":	adata[3],
			})
		self.attacks = []
		self.move_dir = 1
		
	def left(self):
		return self.count
		
	def stopAttack(self):
		self.clock = 100
		
	def underWaiting(self):
		return self.clock > 0
			
	def move(self):
		if self.clock > 0:
			self.clock -= 1
	
		if pyxel.frame_count % 8 != 0: return
			
		mf = 1 if pyxel.frame_count % 32 == 0 else 0
	
		min_x, max_x = SIZE_X, 0
		for i in range(self.num_of_alians):
			self.alians[i]["x"] += self.move_dir * mf
			min_x = min(min_x, self.alians[i]["x"])
			max_x = max(max_x, self.alians[i]["x"])
			if self.alians[i]["type"] <= 2:   self.alians[i]["type"] = 3 - self.alians[i]["type"]
			elif self.alians[i]["type"] <= 4: self.alians[i]["type"] = 7 - self.alians[i]["type"]
			elif self.alians[i]["type"] <= 6: self.alians[i]["type"] = 11 - self.alians[i]["type"]
				
		if min_x < 11: self.move_dir = 1
		if max_x > SIZE_X - 16: self.move_dir = -1
		
	def kogeki(self):
		if self.underWaiting(): return
		if pyxel.frame_count % 32 != 0: return
			
		for i in range(self.num_of_alians):
			if self.alians[i]["alive"]: break
		else: return
		self.attack(i, "alone")
		
	def attack(self, i, kind):
		self.attacks.append({
			"type":	int((self.alians[i]["type"]+1)/2) + 7, "x": self.alians[i]["x"],
			"y": self.alians[i]["y"], "dir": self.alians[i]["dir"],
			"org": i, "kind": kind,
		})
		self.alians[i]["alive"] = False
		
	def formation(self):
		if self.underWaiting(): return False
		if pyxel.frame_count % 128 != 0: return False
	
		together = 0
		if random.randint(1, 2) == 1:
			if not self.alians[39]["alive"]: return False
			self.attack(39, "formation")
			if self.alians[34]["alive"]:
				self.attack(34, "formation"); together += 1
			if self.alians[35]["alive"]:
				self.attack(35, "formation"); together += 1
			if together < 2 and self.alians[36]["alive"]:
				self.alians[36]["dir"] = -3
				self.attack(36, "formation")
		else:
			if not self.alians[40]["alive"]: return False
			self.attack(40, "formation")
			if self.alians[38]["alive"]:
				self.attack(38, "formation"); together += 1
			if self.alians[37]["alive"]:
				self.attack(37, "formation"); together += 1
			if together < 2 and self.alians[36]["alive"]:
				self.alians[36]["dir"] = 3
				self.attack(36, "formation")
		return True
	
	def point(self, type):
		return [30, 30, 40, 40, 50, 50, 60, 60, 80, 100, 150][type-1]

	def hitByBeam(self, beam):
		beam_x, beam_y_current = beam.pos()

		for y_check in range(beam_y_current + beam.speed - 1, beam_y_current - 1, -1):
			for i in range(self.num_of_alians):
				if self.alians[i]["alive"]:
					if (self.alians[i]["x"] <= beam_x <= self.alians[i]["x"] + 4) and \
					   self.alians[i]["y"] == y_check:
						self.alians[i]["alive"] = False
						self.count -= 1
						beam.y = y_check
						return self.point(self.alians[i]["type"])

			for i in range(len(self.attacks) - 1, -1, -1):
				if (self.attacks[i]["x"] <= beam_x <= self.attacks[i]["x"] + 4) and \
				   self.attacks[i]["y"] == y_check:
					point = self.point(self.attacks[i]["type"])
					beam.y = y_check
					self.attacks.pop(i)
					self.count -= 1
					return point
		return 0
		
	def hitShip(self, pos):
		ship_x, ship_y = pos
		for i in range(len(self.attacks)-1, -1, -1):
			if abs(self.attacks[i]["x"]-ship_x) <= 4 and \
			   self.attacks[i]["y"] == ship_y:
				self.attacks.pop(i)
				self.count -= 1
				return True
		return False
		
	def down(self):
		if pyxel.frame_count % 3 != 0 or len(self.attacks) == 0: return
	
		for i in  range(len(self.attacks)-1, -1, -1):
			a = self.attacks[i]
			if self.underWaiting():
				a["kind"] = "alone"
			if a["kind"] == "random":
				a["dir"] = random.randint(-3, 3)
			else:
				if a["type"] == 8 and a["y"] == 7:
					a["dir"] = 0; a["dir"] = random.randint(1, 2) * 4 - 6
				if a["type"] == 9 and a["y"] == 6:
					a["dir"] = 0; a["dir"] = random.randint(1, 2) * 10 - 15
				if a["type"] == 10:
					if a["y"] == 4: a["dir"] = 0
					if a["y"] == 5:
						if a["kind"] == "formation":
							for j in range(i, -1, -1):
								if self.attacks[j]["type"] == 11: break
							a["dir"] = self.attacks[j]["dir"]
						else:
							a["dir"] = 0; a["dir"] = random.randint(1, 2) * 4 - 6
				if a["type"] == 11 and a["y"] == 3:
					a["dir"] = 0; a["dir"] = random.randint(1, 2) * 4 - 6
			a["x"] += a["dir"]; a["y"] += 1

			if not (MIN_X <= a["x"] <= MAX_X - 4 and a["y"] <= SIZE_Y):
				if a["kind"] == "random":
					a["x"] = random.randint(20, 60); a["y"] = 2
					self.missile.set(a["x"]+2, a["y"]+1)
					continue
				if self.left() < 6 and not self.underWaiting():
					if a["type"] == 11:
						self.count -= 1; self.attacks.pop(i)
						continue
					a["y"] = 2; a["kind"] = "random"
					continue
				self.alians[a["org"]]["alive"] = True
				self.attacks.pop(i)
			else:
				self.missile.set(a["x"]+2, a["y"]+1)
					
	def draw(self):
		for alian in self.alians:
			if alian["alive"]:
				pyxel.blt(
					alian["x"] * 2 + BEGIN_X, alian["y"] * 5, 0,
					(alian["type"] - 1) * 10, 0, 10, 4
				)
		for attack in self.attacks:
			pyxel.blt(
				attack["x"] * 2 + BEGIN_X, attack["y"] * 5, 0,
				(attack["type"]-1) * 10, 0, 10, 4
			)
	
class Star:
	def __init__(self):
		self.stars = [
			[
				random.randint(BEGIN_X, BEGIN_X + INNER_SIZE[0] - 1),
				random.randint(1*5, SIZE_Y * 5),
				random.randint(2, 15)
			] for _ in range(80)
		]
			
	def move(self):
		for star in self.stars:
			star[1] += 1
			if star[1] > INNER_SIZE[1]:
				star[0] = random.randint(BEGIN_X, BEGIN_X + INNER_SIZE[0] - 1)
				star[1] = 1 * 5
	
	def draw(self):
		for star in self.stars:
			pyxel.pset(star[0], star[1], star[2])
	
class Score:
	def __init__(self):
		self.init()
		self.hi_score = 0
		
	def init(self):
		self.score = 0
		
	def add(self, n):
		self.score += n
		self.hi_score = max(self.score, self.hi_score)
		
	def value(self):
		return self.score
		
	def hi_value(self):
		return self.hi_score
	
class Point:
	def __init__(self):
		self.points = []
		
	def start(self, pt, pos):
		self.points.append([pt, 10, *pos])
		
	def move(self):
		if pyxel.frame_count % 3 != 0: return
		for i in range(len(self.points)-1, -1, -1):
			self.points[i][1] -= 1
			if self.points[i][1] == 0:
				self.points.pop(i)
	
	def draw(self):
		for point in self.points:
			pyxel.text(point[2]*2+BEGIN_X+5, point[3]*5+5,
				str(point[0]), 15)
	
class Sound:
	def __init__(self):
		pyxel.sound(1).set("f0f1", "n", "7", "s", 15)
		pyxel.sound(2).set("c0a4c0", "n", "4", "s", 6)
		st = "".join([s + i for i in "432" for s in "bagfedc"])
		pyxel.sound(3).set(st, "sp", "4", "s", 16)
		
	def shipBomb(self): pyxel.play(1, 1)
	def alianBomb(self): pyxel.play(2, 2)
	def alianFormation(self): pyxel.play(3, 3)
	
class Galaxian:
	def __init__(self):
		pyxel.init(*OUTER_SIZE)
		# ### 変更点：ウィンドウタイトルを日本語化 ###
		pyxel.caption = "ギャラクシアン"
		pyxel.mouse(True)		
		pyxel.load("galaxian.pyxres")

		self.missile = Missile()
		self.alian = Alian(self.missile)
		self.star = Star()
		self.beam = Beam()
		self.ship = Ship(self.beam)
		self.explosion = Explosion()
		self.point = Point()
		self.score = Score()
		self.sound = Sound()
		self.demoMode = True
		self.scene = 0
		
		pyxel.run(self.update, self.draw)
		
	def init(self):
		self.alian.init()
		self.missile.init()
		self.beam.init()
		self.scene += 1
		
	def demoPlay(self):
		if self.ship.left() == 0:
			pyxel.text(BEGIN_X+52, 80, "ゲームオーバー", 8)
		
		pyxel.text(BEGIN_X+42, 100, "Pyxel ギャラクシアン", 7)
		pyxel.text(BEGIN_X+52, 116, "クリックでスタート", 7)
		pyxel.text(BEGIN_X+52, 132, "ハイスコア {}".format(self.score.hi_value()), 7)

		if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
			self.demoMode = False
			self.alian.stopAttack()
			self.score.init()
			self.ship.init()
			self.scene = 0
			self.init()
			
	def update(self):
		self.alian.move()
		if self.alian.formation() and not self.demoMode:
			self.sound.alianFormation()
		self.alian.kogeki()
		self.alian.down()
		self.missile.move()
		self.star.move()
		self.beam.move()
		self.explosion.move()
		self.point.move()
		
		if self.demoMode: return

		self.ship.move()
		
		if self.beam.underShot():
			pt = self.alian.hitByBeam(self.beam)
			if pt > 0:
				self.explosion.start(self.beam.pos())
				self.point.start(pt, self.beam.pos())
				self.score.add(pt)
				self.sound.alianBomb()
				self.beam.init()

		if self.missile.hitShip(self.ship.pos()) or self.alian.hitShip(self.ship.pos()):
			self.explosion.start2(self.ship.pos())
			self.sound.shipBomb()
			self.ship.dec()
			self.alian.stopAttack()
			self.missile.init()
			
		if self.alian.left() == 0:
			self.alian.stopAttack()
			self.init()
		if self.ship.left() == 0:
			self.demoMode = True
		
	def draw(self):
		pyxel.cls(0)
		pyxel.rect(0, 0, *OUTER_SIZE, 1)
		pyxel.rect(BEGIN_X, 0, *INNER_SIZE, 0)
		
		self.star.draw()

		status_text = "ステージ:{0:2d} ハイスコア:{1:05d} スコア:{2:05d} 残り:{3:1d}".format(
			self.scene, self.score.hi_value(), self.score.value(), self.ship.left()
		)
		pyxel.text(BEGIN_X+4, 0, status_text, 7)

		if self.demoMode:
			self.demoPlay()

		self.alian.draw()
		self.missile.draw()
		self.ship.draw()
		self.beam.draw()
		self.explosion.draw()
		self.point.draw()

if __name__ == "__main__":
	Galaxian()
