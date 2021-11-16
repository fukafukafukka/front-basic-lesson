function FuelTank(positionX, positionY, name) {
  console.log("燃料タンク" + name + "を作成");
  this.name = name;
  this.positionX = positionX;
  this.positionY = positionY;
  let tank;
  let gun;
  let tankBody;
}
FuelTank.prototype = {
  refueling: function(fuel) {
    this.tank = fuel;
    console.log(this.tank + 'l 給油しました');
  },
  setOnGun: function(gun) {
    this.gun = gun;
    console.log('Gun' + this.gun.name + 'を接続しました');
    if (gun.fuelTank == null) {
      gun.setOnFuelTank(this);
    }
  },
  setOnTankBody: function(tankBody) {
    this.tankBody = tankBody;
    console.log('TankBody' + this.tankBody.name + 'を接続しました');
    if (tankBody.fuelTank == null) {
      tankBody.setOnFuelTank(this);
    }
  },
  consumeFuel: function(fuel){
  	this.tank -= fuel;
  },
  getAmountOfFuel: function(){
  	return this.tank;
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
