
const API_URL = "http://localhost:8081"

export interface Point {
    lat: number,
    lng: number,
}

export interface Station extends Point {
    name: string,
}

export function onError(reason: any) {
    console.error(reason);
    return null;
}

function filterError<T>(o: T): T | null {
    if ((o as any).hasOwnProperty("error")) {
        onError((o as any)["error"]);
        return null;
    } else {
        return o;
    }
}

export async function getClosestStation(p: Point): Promise<Station | null> {
    try {
        const res = await fetch(`${API_URL}/closest_point`, {
            method: "POST",
            headers: new Headers({'content-type': 'application/json'}),
            body: JSON.stringify(p)
        });
        return filterError(await res.json());
    } catch (e) {
        return onError(e);
    }
}

export async function fuzzySearch(name: string): Promise<Station | null> {
    try {
        const res = await fetch(`${API_URL}/fuzzy_search`, {
            method: "POST",
            headers: new Headers({'content-type': 'application/json'}),
            body: JSON.stringify({name})
        });
        return filterError(await res.json());
    } catch (e) {
        return onError(e);
    }
}

export async function getRoute(station1: string, station2: string): Promise<Station | null> {
    try {
        const res = await fetch(`${API_URL}/route`, {
            method: "POST",
            headers: new Headers({'content-type': 'application/json'}),
            body: JSON.stringify({station1, station2})
        });
        return filterError(await res.json());
    } catch (e) {
        return onError(e);
    }
}
