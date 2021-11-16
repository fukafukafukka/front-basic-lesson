const necessaryFuelToTurnCaterpillar = 4;
const necessaryFuelToRun100m = 4;

function Caterpillar(positionX, positionY, name, direction, Direction, turn) {
  console.log("キャタピラ" + name + "を作成");
  this.name = name;
  this.positionX = positionX;
  this.positionY = positionY;
  this.direction = direction;
  this.Direction = Direction;
  this.turn = turn;
  let tankBody;
}
Caterpillar.prototype = {
  setOnTankBody: function(tankBody) {
    this.tankBody = tankBody;
    console.log('戦車体' + this.tankBody.name + 'を接続しました');
    if (tankBody.caterpillar == null) {
      tankBody.setOnCaterpillar(this);
    }
  },
  turnRight: function() {
    if (this.checkFuel() && this.checkEngine()) {
      this.tankBody.fuelTank.consumeFuel(this.necessaryFuelToTurnCaterpillar);
      this.direction = this.turn.turnRight(this.direction);
    }
  },
  turnLeft: function() {
    if (this.checkFuel() && this.checkEngine()) {
      this.tankBody.fuelTank.consumeFuel(this.necessaryFuelToTurnCaterpillar);
      this.direction = this.turn.turnLeft(this.direction);
    }
  },
  turnBack: function() {
    if (this.checkFuel() && this.checkEngine()) {
      this.tankBody.fuelTank.consumeFuel(this.necessaryFuelToTurnCaterpillar);
      this.direction = this.turn.turnBack(this.direction);
    }
  },
  move: function(moveDistance) {
    if ((moveDistance / 100) * this.necessaryFuelToRun100m > this.tankBody.fuelTank.getAmountOfFuel()) {
      console.log("燃料不足で移動できません");
      return;
    }
    this.tankBody.fuelTank.consumeFuel(this.necessaryFuelToRun100m);
    this.positionX = this.getPositionX() + moveDistance * Direction.getByName(this.getDirection()).xVector;
    this.positionY = this.getPositionY() + moveDistance * Direction.getByName(this.getDirection()).yVector;
    console.log("戦車は位置座標（x,y）=(" + this.getPositionY() + "," + this.getPositionY() + ")に移動しました！");
  },
  checkFuel: function() {
    if (this.necessaryFuelToTurnCaterpillar > this.tankBody.fuelTank.getAmountOfFuel()) {
      console.log("燃料不足のため回転できません。")
      return false;
    } else {
      return true;
    }
  },
  checkEngine: function() {
    return this.tankBody.engine.getCondition();
  },
  getDirection: function() {
    return this.direction;
  },
  getPositionX: function() {
    return this.positionX;
  },
  getPositionY: function() {
    return this.positionY;
  },
};
