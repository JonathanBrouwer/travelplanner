import type {Point} from "./api"

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

export class RoutePoint implements Point {
    description: string
    colour: string
    type: RoutePointType

    from: string | null
    to: string | null

    lat: number;
    lng: number;

    constructor(description: string, colour: string, type: RoutePointType, lat: number, lng: number) {
        this.description = description;
        this.colour = colour;
        this.type = type;
        this.lat = lat;
        this.lng = lng;

        this.from = null;
        this.to = null;
    }

    static randomColour(description: string, type: RoutePointType, lat: number, lng: number): RoutePoint {
        return new RoutePoint(description, randomColor(), type, lat, lng)
    }
}

