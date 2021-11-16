const necessaryFuelToTurnGun = 4;

function GunOnTheTank(tankBody, direction, Direction, turn) {
  console.log('Gunを戦車上に作成');
  this.setOnTankBody(tankBody);
  //一時的に位置情報を代入。caterpillarが移動する度に調べないといけない。
  this.positionX = tankBody.positionX;
  this.positionY = tankBody.positionY;
  this.direction = direction;
  this.Direction = Direction;
  this.turn = turn;
}

function Gun(positionX, positionY, name, direction, Direction, turn) {
  console.log("Gun" + name + "を作成");
  this.positionX = positionX;
  this.positionY = positionY;
  this.name = name;
  this.direction = direction;
  this.Direction = Direction;
  this.turn = turn;
  this.shellCover = [];
}

Gun.prototype = {
  setOnTankBody: function(tankBody) {
    this.tankBody = tankBody;
    console.log('戦車体' + this.tankBody.name + 'を接続しました')
    if (tankBody.gun == null) {
      tankBody.setOnGun(this);
    }
  },
  addShells: function(shell) {
    this.shellCover.push(shell);
  },
  fire: function() {
  	if (this.shellCover.length < 1) {
  		console.log("砲弾切れのため発射できません。")
  		return;
  	}
    let firedShell;
    if (firedShell == null) {
      firedShell = this.shellCover.shift();
    }
    if (firedShell.necessaryFuelToShoot > this.tankBody.fuelTank.getAmountOfFuel()){
  		console.log("燃料不足のため発射できません。")
  		return;
  	}
    this.tankBody.fuelTank.consumeFuel(firedShell.necessaryFuelToShoot );

    console.log(Direction.getByName(this.getDirection()).direction + 'の方角に発射！');
    if (this.tankBody == null) {
      firedShell.landingPointX = this.positionX + firedShell.flyingDistance * Direction.getByName(this.getDirection()).xVector;
      firedShell.landingPointY = this.positionY + firedShell.flyingDistance * Direction.getByName(this.getDirection()).yVector;
    } else {
      firedShell.landingPointX = this.tankBody.getPositionX() + firedShell.flyingDistance * Direction.getByName(this.getDirection()).xVector;
      firedShell.landingPointY = this.tankBody.getPositionY() + firedShell.flyingDistance * Direction.getByName(this.getDirection()).yVector;
    }
    console.log("砲弾" + firedShell.name + "の着弾点は、(x,y)=(" + firedShell.landingPointX + "," + firedShell.landingPointY + ")です。");
  },
  turnRight: function() {
  	if (this.checkFuel() && this.checkEngine()) {
  		this.tankBody.fuelTank.consumeFuel(this.necessaryFuelToTurnGun);
  		this.direction = this.turn.turnRight(this.direction);
  	}
  },
  turnLeft: function() {
  	if (this.checkFuel() && this.checkEngine()) {
  		this.tankBody.fuelTank.consumeFuel(this.necessaryFuelToTurnGun);
  		this.direction = this.turn.turnLeft(this.direction);
  	}
  },
  turnBack: function() {
  	if (this.checkFuel() && this.checkEngine()) {
      this.tankBody.fuelTank.consumeFuel(this.necessaryFuelToTurnGun);
  	  this.direction = this.turn.turnBack(this.direction);
  	}
  },
  checkFuel: function(){
  	if (this.necessaryFuelToTurnGun > this.tankBody.fuelTank.getAmountOfFuel){
  		console.log("燃料不足のため回転できません。")
  		return false;
  	}　else {
  		return true;
  	}
  },
  checkEngine: function() {
    if (this.tankBody.engine.getCondition() == true) {
      return true;
    }else {
      return false;
    }
  },
  getDirection: function() {
  	return this.direction;
  },
  getPositionX: function() {
    if (tankBody == null) {
      return this.positionX;
    } else{
      return this.tankBody.getPositionX();
    }
  },
  getPositionY: function() {
    if(tankBody == null) {
      return this.positionY;
    } else {
      return this.tankBody.getPositionY();
    }
  }
};
