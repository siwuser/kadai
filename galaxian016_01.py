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
		# ### 変更点１：弾速を設定 ###
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
		
		# ### 変更点２：設定した弾速で移動させる ###
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
		# マウスのX座標をゲーム内座標に変換し、自機のx座標に設定
		new_x = (pyxel.mouse_x - BEGIN_X) / 2
		self.x = max(MIN_X, min(new_x, MAX_X - 4))

		# マウスの左クリックでビーム発射
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
		# ("type", "x", "y", "dir"),
		( 1, 59, 5,  3), # 0
		( 1, 19, 5, -3), # 1
		( 4, 54, 4,  3), # 2
		( 4, 24, 4, -3), # 3
		( 1, 59, 6,  3), # 4
		( 1, 19, 6, -3), # 5
		( 2, 54, 5,  3), # 6
		( 2, 24, 5, -3), # 7
		( 1, 59, 7,  3), # 8
		( 1, 19, 7, -3), # 9
		( 2, 54, 6,  3), #10
		( 2, 24, 6, -3), #11
		( 2, 54, 7,  3), #12
		( 2, 24, 7, -3), #13
		( 3, 49, 4,  3), #14
		( 3, 29, 4, -3), #15
		( 1, 49, 5,  3), #16
		( 1, 29, 5, -3), #17
		( 1, 49, 6,  3), #18
		( 1, 29, 6, -3), #19
		( 1, 49, 7,  3), #20
		( 1, 29, 7, -3), #21
		( 4, 44, 4,  3), #22
		( 4, 34, 4, -3), #23
		( 3, 39, 4,  3), #24
		( 2, 44, 5,  3), #25
		( 1, 39, 5, -3), #26
		( 2, 34, 5, -3), #27
		( 2, 34, 6, -3), #28
		( 1, 39, 6,  3), #29
		( 2, 44, 6,  3), #30
		( 2, 44, 7,  3), #31
		( 1, 39, 7, -3), #32
		( 2, 34, 7, -3), #33
		( 5, 29, 3, -3), #34
		( 6, 34, 3, -3), #35
		( 5, 39, 3, -3), #36
		( 6, 44, 3,  3), #37
		( 5, 49, 3,  3), #38
		( 7, 34, 2, -3), #39
		( 7, 44, 2,  3), #40
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
				"alive": True,
				"type":	adata[0],
				"x":	adata[1],
				"y":	adata[2],
				"dir":	adata[3],
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
	
		if pyxel.frame_count % 8 != 0:
			return
			
		if pyxel.frame_count % 32 != 0:
			mf = 0
		else:
			mf = 1
	
		min_x = SIZE_X
		max_x = 0
		for i in range(self.num_of_alians):
			self.alians[i]["x"] += self.move_dir * mf
			min_x = min(min_x, self.alians[i]["x"])
			max_x = max(max_x, self.alians[i]["x"])
			if self.alians[i]["type"] <= 2:
				self.alians[i]["type"] = 3 - self.alians[i]["type"]
			elif self.alians[i]["type"] <= 4:
				self.alians[i]["type"] = 7 - self.alians[i]["type"]
			elif self.alians[i]["type"] <= 6:
				self.alians[i]["type"] = 11 - self.alians[i]["type"]
				
		if min_x < 11:
			self.move_dir = 1
		if max_x > SIZE_X - 16:
			self.move_dir = -1
		
	def kogeki(self):
	
		if self.underWaiting():
			return
	
		# 攻撃するエイリアンを決める
		if pyxel.frame_count % 32 != 0:
			return
			
		for i in range(self.num_of_alians):
			if self.alians[i]["alive"]:
				break
		else:
			return
			
		self.attack(i, "alone")
		
	def attack(self, i, kind):
		self.attacks.append({
			"type":	int((self.alians[i]["type"]+1)/2) + 7,
			"x":	self.alians[i]["x"],
			"y":	self.alians[i]["y"],
			"dir":	self.alians[i]["dir"],
			"org":	i,
			"kind": kind,
		})
		self.alians[i]["alive"] = False
		
	def formation(self):
	
		if self.underWaiting():
			return False
	
		if pyxel.frame_count % 128 != 0:
			return False
	
		together = 0
		if random.randint(1, 2) == 1:
			if not self.alians[39]["alive"]:
				return False
			self.attack(39, "formation")
			if self.alians[34]["alive"]:
				self.attack(34, "formation")
				together += 1
			if self.alians[35]["alive"]:
				self.attack(35, "formation")
				together += 1
			if together < 2 and self.alians[36]["alive"]:
				self.alians[36]["dir"] = -3
				self.attack(36, "formation")
		else:
			if not self.alians[40]["alive"]:
				return False
			self.attack(40, "formation")
			if self.alians[38]["alive"]:
				self.attack(38, "formation")
				together += 1
			if self.alians[37]["alive"]:
				self.attack(37, "formation")
				together += 1
			if together < 2 and self.alians[36]["alive"]:
				self.alians[36]["dir"] = 3
				self.attack(36, "formation")
				
		return True
	
	def point(self, type):
		return [30, 30, 40, 40, 50, 50, 60, 60, 80, 100, 150][type-1]

	# ### 変更点４：当たり判定のロジックを修正 ###
	def hitByBeam(self, beam):
		beam_x, beam_y_current = beam.pos()

		# 弾が1フレームで移動した軌跡（Y座標）をすべてチェックする
		for y_check in range(beam_y_current + beam.speed - 1, beam_y_current - 1, -1):
			# 編隊のエイリアンとの当たり判定
			for i in range(self.num_of_alians):
				if self.alians[i]["alive"]:
					if (self.alians[i]["x"] <= beam_x <= self.alians[i]["x"] + 4) and \
					   self.alians[i]["y"] == y_check:
						self.alians[i]["alive"] = False
						self.count -= 1
						beam.y = y_check  # 爆発表示のため、弾の位置を衝突座標に更新
						return self.point(self.alians[i]["type"])

			# 攻撃中のエイリアンとの当たり判定（リストから削除するため逆順でループ）
			for i in range(len(self.attacks) - 1, -1, -1):
				if (self.attacks[i]["x"] <= beam_x <= self.attacks[i]["x"] + 4) and \
				   self.attacks[i]["y"] == y_check:
					point = self.point(self.attacks[i]["type"])
					beam.y = y_check  # 爆発表示のため、弾の位置を衝突座標に更新
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
		if pyxel.frame_count % 3 != 0:
			return
	
		if len(self.attacks) == 0:
			return
			
		for i in  range(len(self.attacks)-1, -1, -1):
			type = self.attacks[i]["type"]
			x = self.attacks[i]["x"]
			y = self.attacks[i]["y"]
			dir = self.attacks[i]["dir"]
			kind = self.attacks[i]["kind"]
			if self.underWaiting():
				kind = "alone"
				self.attacks[i]["kind"] = kind
			if kind == "random":
				dir = random.randint(-3, 3)
				self.attacks[i]["dir"] = dir
			else:
				if type == 8:
					if y == 7:
						self.attacks[i]["dir"] = random.randint(1, 2) * 4 - 6
						dir = 0
				if type == 9:
					if y == 6:
						self.attacks[i]["dir"] = random.randint(1, 2) * 10 - 15
						dir = 0
				if type == 10:
					if y == 4:
						dir = 0
					if y == 5:
						if kind == "formation":
							for j in range(i, -1, -1):
								if self.attacks[j]["type"] == 11:
									break
							self.attacks[i]["dir"] = self.attacks[j]["dir"]
							dir = self.attacks[i]["dir"]
						else:
							self.attacks[i]["dir"] = random.randint(1, 2) * 4 - 6
							dir = 0
				if type == 11:
					if y == 3:
						self.attacks[i]["dir"] = random.randint(1, 2) * 4 - 6
						dir = 0
			x += dir
			y += 1
			if x < MIN_X or x > MAX_X - 4 or y > SIZE_Y:
				if kind == "random":
					self.attacks[i]["x"] = random.randint(20, 60)
					self.attacks[i]["y"] = 2
					self.missile.set(x+2, y+1)
					continue
				if self.left() < 6 and not self.underWaiting():
					if type == 11:
						self.count -= 1
						self.attacks.pop(i)
						continue
					self.attacks[i]["y"] = 2
					self.attacks[i]["kind"] = "random"
					continue
				org = self.attacks[i]["org"]
				self.alians[org]["alive"] = True
				self.attacks.pop(i)
			else:
				self.attacks[i]["x"] = x
				self.attacks[i]["y"] = y
				self.missile.set(x+2, y+1)
					
			
			
	def draw(self):
		for i in range(self.num_of_alians):
			if self.alians[i]["alive"]:
				pyxel.blt(
					self.alians[i]["x"] * 2 + BEGIN_X, self.alians[i]["y"] * 5,
					0,
					(self.alians[i]["type"] - 1) * 10, 0,
					10, 4
				)
		for attack in self.attacks:
			pyxel.blt(
				attack["x"] * 2 + BEGIN_X, attack["y"] * 5,
				0,
				(attack["type"]-1) * 10, 0,
				10, 4
			)
	
class Star:

	def __init__(self):
		self.num_of_stars = 80
		self.stars = []
		for i in range(self.num_of_stars):
			self.stars.append([
				random.randint(BEGIN_X, BEGIN_X + INNER_SIZE[0] - 1),
				random.randint(1*5, SIZE_Y * 5),
				random.randint(2, 15)
			])
			
	def move(self):
		for i in range(self.num_of_stars):
			self.stars[i][1] += 1
			if self.stars[i][1] > INNER_SIZE[1]:
				self.stars[i][0] = random.randint(BEGIN_X, BEGIN_X + INNER_SIZE[0] - 1)
				self.stars[i][1] = 1 * 5
	
	def draw(self):
		for i in range(self.num_of_stars):
			# pyxel.pix(self.stars[i][0], self.stars[i][1], self.stars[i][2]) # Ver1,4でpsetに変更
			pyxel.pset(self.stars[i][0], self.stars[i][1], self.stars[i][2])
	
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
		if pyxel.frame_count % 3 != 0:
			return
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
		# 宇宙船の爆発音の設定
		pyxel.sound(1).set("f0f1", "n", "7", "s", 15)
		
		# エイリアンの爆発音の設定
		pyxel.sound(2).set("c0a4c0", "n", "4", "s", 6)
		
		# エイリアンの編隊攻撃中の音の設定
		st = ""
		for i in "432":
			for s in "bagfedc":
				st += s + i
		pyxel.sound(3).set(st, "sp", "4", "s", 16)
		
	def shipBomb(self):
		pyxel.play(1, 1)
		
	def alianBomb(self):
		pyxel.play(2, 2)
	
	def alianFormation(self):
		pyxel.play(3, 3)
	
class Galaxian:
	def __init__(self):
		# pyxelの初期化
		pyxel.init(*OUTER_SIZE)
		pyxel.caption = "Galaxian"
		# マウスカーソルを表示する
		pyxel.mouse(True)		
		# 各キャラクタの準備
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
		
		
		# pyxelの実行
		# (フレーム更新時、描画時に呼ぶ関数の登録)
		pyxel.run(self.update, self.draw)
		
	def init(self):
		self.alian.init()
		self.missile.init()
		self.beam.init()
		self.scene += 1
		
	def demoPlay(self):
		if self.ship.left() == 0:
			pyxel.text(BEGIN_X+58, 80, "GAME OVER", 8)
		pyxel.text(BEGIN_X+50, 100, "Pyxel GALAXIAN", 7)
		# スタートの案内文言を変更
		pyxel.text(BEGIN_X+45, 116, "START : MOUSE CLICK", 7)
		pyxel.text(BEGIN_X+50, 132, "HIGH SCORE {}".format(
			self.score.hi_value()), 7)
		# スペースキーからマウスクリックでのスタートに変更
		if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
			self.demoMode = False
			self.alian.stopAttack()
			self.score.init()
			self.ship.init()
			self.scene = 0
			self.init()
			
	def update(self):
		"""フレーム更新時の処理"""

		# 各キャラクタの移動
		self.alian.move()
		self.alian.kogeki()
		if self.alian.formation():
			if not self.demoMode:
				self.sound.alianFormation()
		self.alian.down()
		self.missile.move()
		self.star.move()
		self.beam.move()
		self.explosion.move()
		self.point.move()
		
		if self.demoMode:
			return

		self.ship.move()
		
		# 衝突判定
		if self.beam.underShot():
			# ### 変更点３：当たり判定メソッドにbeamオブジェクト自体を渡す ###
			pt = self.alian.hitByBeam(self.beam)
			if pt > 0:
				self.explosion.start(self.beam.pos())
				self.point.start(pt, self.beam.pos())
				self.score.add(pt)
				self.sound.alianBomb()
				self.beam.init()

		if self.missile.hitShip(self.ship.pos()):
			self.explosion.start2(self.ship.pos())
			self.sound.shipBomb()
			self.ship.dec()
			self.alian.stopAttack()
			self.missile.init()
		if self.alian.hitShip(self.ship.pos()):
			self.explosion.start2(self.ship.pos())
			self.ship.dec()
			self.sound.shipBomb()
			self.alian.stopAttack()
			self.missile.init()
			
		# 終了判定
		if self.alian.left() == 0:
			self.alian.stopAttack()
			self.init()
		if self.ship.left() == 0:
			self.demoMode = True
		
	def draw(self):
		"""描画処理"""

		# 画面クリア
		pyxel.cls(0)
		
		pyxel.rect(0, 0, *OUTER_SIZE, 1)
		pyxel.rect(BEGIN_X, 0, *INNER_SIZE, 0)
		
		# 各キャラクタの描画処理
		self.star.draw()
		pyxel.text(BEGIN_X, 0,
			" SCENE:{0:2d}   HI:{1:05d} SCORE:{2:05d} LEFT:{3:1d}".format(
				self.scene,
				self.score.hi_value(),
				self.score.value(),
				self.ship.left()
			), 7)
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