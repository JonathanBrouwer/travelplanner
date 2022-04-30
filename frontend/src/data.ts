
export enum RoutePointType {
    Route,
    SingleStation,
}

const randomColor = (() => {
  "use strict";

  const randomInt = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  };

  return () => {
    var h = randomInt(0, 360);
    var s = randomInt(42, 98);
    var l = randomInt(40, 90);
    return `hsl(${h},${s}%,${l}%)`;
  };
})();

export class RoutePoint {
    description: string
    colour: string
    type: RoutePointType

    constructor(description: string, colour: string, type: RoutePointType) {
        this.description = description;
        this.colour = colour;
        this.type = type;
    }

    static randomColour(description: string, type: RoutePointType): RoutePoint {
        return new RoutePoint(description, randomColor(), type)
    }
}

