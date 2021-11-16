function Shell(name, weight, flyingDistance, necessaryFuelToShoot){
	console.log("砲弾" + name + "を作成");
	this.name = name;
	this.weight = weight;
	this.flyingDistance = flyingDistance;
	this.necessaryFuelToShoot = necessaryFuelToShoot;
	let landingPointX;
	let landingPointY;
}
