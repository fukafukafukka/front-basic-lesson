const necessaryFuelToStartEngine = 10;

function Engine(positionX, positionY, name) {
  console.log("エンジン" + name + "を作成");
  this.name = name;
  this.positionX = positionX;
  this.positionY = positionY;
  let fuelTank;
  let tankBody;
  let working;
}

Engine.prototype = {
  setOnTankBody: function(tankBody) {
    this.tankBody = tankBody;
    console.log('戦車体' + this.tankBody.name + 'を接続しました');
    if (tankBody.engine == null) {
      tankBody.setOnEngine(this);
    }
  },
  getStart: function(){
  	this.tankBody.fuelTank.consumeFuel(necessaryFuelToStartEngine);
  	working = true;
  },
  stop: function(){
  	working = false;
  },
  getCondition: function(){
  	return working;
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
