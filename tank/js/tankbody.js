function TankBody(positionX, positionY, name) {
  console.log("戦車" + name + "を作成");
  this.name = name;
  this.positionX = positionX;
  this.positionY = positionY;
  let gun;
  let engine;
  let caterpillar;
  let fuelTank;
}
TankBody.prototype = {
  setOnGun: function(gun) {
    this.gun = gun;
    console.log('Gun' + this.gun.name + 'を接続しました');
    if (gun.tankBody == null) {
      gun.setOnTankBody(this);
    }
  },
  setOnEngine: function(engine) {
    this.engine = engine;
    console.log('エンジン' + this.engine.name + 'を接続しました');
    if (engine.tankBody == null) {
      engine.setOnTankBody(this);
    }
  },
  setOnCaterpillar: function(caterpillar) {
    this.caterpillar = caterpillar;
    console.log('キャタピラ' + this.caterpillar.name + 'を接続しました');
    if (caterpillar.tankBody == null) {
      caterpillar.setOnTankBody(this);
    }
  },
  setOnFuelTank: function(fuelTank) {
    this.fuelTank = fuelTank;
    console.log("燃料タンク" + this.fuelTank.name + "を接続しました");
    if(fuelTank.tankBody == null) {
      fuelTank.setOnTankBody(this);
    }
  },
  turnRight: function() {
  	this.caterpillar.turnRight();
  },
  turnLeft: function() {
    this.caterpillar.turnLeft();
  },
  turnBack: function() {
    this.caterpillar.turnBack();
  },
  getPositionX: function() {
    if (this.caterpillar == null) {
      return this.positionX;
    }else {
      return this.caterpillar.getPositionX();
    }
  },
  getPositionY: function() {
    if(this.caterpillar == null) {
      return this.positionY;
    }else {
      return this.caterpillar.getPositionY();
    }
  }
};
