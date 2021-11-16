function Turn() {};
Turn.prototype = {
  turnRight: function(direction) {
    if (direction == 'North'){
      return 'East';
    } else if (direction == 'East'){
      return 'South';
    } else if (direction == 'South'){
      return 'West';
    } else {
      return 'North';
    }
  },
  turnLeft: function(direction) {
    if (direction == 'North'){
      return 'West';
    } else if (direction == 'East'){
      return 'North';
    } else if (direction == 'South'){
      return 'East';
    } else {
      return 'South';
    }
  },
  turnBack: function(direction) {
    if (direction == 'North'){
      return 'South';
    } else if (direction == 'East'){
      return 'West';
    } else if (direction == 'South'){
      return 'North';
    } else {
      return 'East';
    }
  }
};
