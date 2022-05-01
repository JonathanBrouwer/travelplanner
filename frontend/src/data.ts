import type {Point} from "./api"

export enum RoutePointType {
    Route,
    SingleStation,
}

export class Segment {
    parts: [number, number][]
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

    fromobj: RoutePoint | null
    toobj: RoutePoint | null

    lat: number | null;
    lng: number | null;

    segments: Segment[];

    constructor(description: string, colour: string, type: RoutePointType) {
        this.description = description;
        this.colour = colour;
        this.type = type;
        this.from = null;
        this.to = null;
        this.segments = [];
    }

    static randomColour(description: string, type: RoutePointType): RoutePoint {
        return new RoutePoint(description, randomColor(), type)
    }

    getLatTo() {
        if (this.type == RoutePointType.SingleStation) {
            return this.lat
        } else {
            return this.toobj.getLatTo()
        }
    }

    getLatFrom() {
        if (this.type == RoutePointType.SingleStation) {
            return this.lat
        } else {
            return this.fromobj.getLatFrom()
        }
    }

    getLngTo() {
        if (this.type == RoutePointType.SingleStation) {
            return this.lng
        } else {
            return this.toobj.getLngTo()
        }
    }

    getLngFrom() {
        if (this.type == RoutePointType.SingleStation) {
            return this.lng
        } else {
            return this.fromobj.getLngFrom()
        }
    }
}

